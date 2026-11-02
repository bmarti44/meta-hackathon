"""Retained, resumable host/codex calls. No separately metered API is used."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import time
from budget import reserve, reconcile
from ledger import sha256_file, append_record

ROOT = Path(__file__).resolve().parent.parent
# Prospective budget root (2026-10-29 remediation): config/allocations.json is
# LOCK2-pinned and restored byte-exact; user-authorized amended caps live in
# config/allocations_amended_20261029.json, exposed to the pinned budget.py
# via this shadow root (resources.json + ledger symlinked = same accounting).
BUDGET_ROOT = ROOT / 'config/.budget_root'
AMENDED = ROOT / 'config/allocations_amended_20261029.json'


def verify_budget_root():
    # Fail closed unless the shadow root resolves to the canonical identities:
    # single-source amended allocations, real resources.json, real ledger.
    expect = [(BUDGET_ROOT / 'config/allocations.json', AMENDED),
              (BUDGET_ROOT / 'config/resources.json', ROOT / 'config/resources.json'),
              (BUDGET_ROOT / 'ledger', ROOT / 'ledger')]
    for link, target in expect:
        if link.resolve() != target.resolve():
            raise RuntimeError(f'budget shadow root identity mismatch: {link} -> {link.resolve()}, expected {target.resolve()}')
    return sha256_file(AMENDED)


def call_identity(prompt_path,output,effort,phase,terminal,timeout,model='gpt-6.1-sol',web_search=None):
    return {'model':model,'effort':effort,'phase':phase,'terminal_review':terminal,'web_search':web_search,
            'timeout_s':timeout,'sandbox':'read-only','interface':'codex exec',
            'binary':os.environ.get('CDRSI_CODEX_BIN','codex'),
            'prompt_sha256':sha256_file(prompt_path),'output':str(output.resolve())}


def call(prompt_path: Path, output: Path, effort: str, phase='phase2_lock1', terminal=False, timeout=600, model='gpt-6.1-sol', web_search=None):
    prompt_path = prompt_path.resolve()
    output = output.resolve()
    receipt = output.with_suffix('.receipt.json')
    identity=call_identity(prompt_path,output,effort,phase,terminal,timeout,model,web_search)
    if receipt.exists():
        saved = json.loads(receipt.read_text())
        if saved['prompt_sha256'] != sha256_file(prompt_path):
            raise RuntimeError('immutable call ID reused with different prompt')
        if saved.get('call_identity')!=identity:
            raise RuntimeError('call identity mismatch or legacy incomplete receipt; inspect retained artifacts, never redispatch')
        digest=saved.get('response_sha256')
        if digest is not None:
            if not output.is_file() or sha256_file(output)!=digest:
                raise RuntimeError('retained model response missing or changed')
        elif saved.get('returncode')==0 or output.exists():
            raise RuntimeError('response/receipt integrity mismatch')
        return saved
    events = output.with_suffix('.events.jsonl')
    if output.exists() or events.exists():
        raise RuntimeError('interrupted/existing call: reconcile it explicitly; never redispatch automatically')
    output.parent.mkdir(parents=True, exist_ok=True)
    alloc_sha = verify_budget_root()
    allocation=json.loads((BUDGET_ROOT/'config/allocations.json').read_text())['per_phase'][phase]
    allowance=allocation.get('host_reasoning_job_timeout_s',600)
    if not 0 < timeout <= allowance:
        raise RuntimeError('model call exceeds recorded per-job host reasoning allowance')
    codex_binary = os.environ.get('CDRSI_CODEX_BIN', 'codex')
    reservation = reserve(BUDGET_ROOT, {'name': output.stem, 'phase': phase, 'model_calls': 1, 'binary': codex_binary,
                               'terminal_review': terminal, 'wall_s_max': timeout, 'model': model,
                               'effort': effort, 'prompt_path': str(prompt_path), 'prompt_sha256': sha256_file(prompt_path),
                               'allocations_sha256': alloc_sha, 'allocations_source': 'config/allocations_amended_20261029.json'})
    argv = [codex_binary, 'exec', '--skip-git-repo-check', '--ephemeral', '-m', model,
            '-c', f'model_reasoning_effort="{effort}"', '-s', 'read-only', '-C', str(ROOT.parent),
            '--json', '-o', str(output), '-']
    if web_search:
        j = argv.index('--json')
        argv[j:j] = ['-c', f'web_search="{web_search}"']
    start = time.monotonic()
    timed_out = False
    launch_error = None
    returncode = None
    with events.open('x') as out, output.with_suffix('.stderr.txt').open('x') as err:
        try:
            proc = subprocess.Popen(['/usr/bin/time', '-l', *argv], stdin=subprocess.PIPE, stdout=out, stderr=err, text=True, start_new_session=True)
            try:
                proc.communicate(prompt_path.read_text(), timeout=timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
            returncode = proc.returncode
        except OSError as exc:
            launch_error = str(exc)
            err.write(launch_error + '\n')
    usage = []
    for line in events.read_text().splitlines():
        try:
            e = json.loads(line)
        except ValueError:
            continue
        if 'usage' in e:
            usage.append(e['usage'])
    stderr = output.with_suffix('.stderr.txt').read_text()
    rss = re.search(r'(\d+)\s+maximum resident set size', stderr)
    cpu = re.search(r'([\d.]+)\s+real\s+([\d.]+)\s+user\s+([\d.]+)\s+sys', stderr)
    if returncode == 0 and (not output.exists() or not output.read_text().strip()):
        launch_error = 'process returned success without a retained model response'
        returncode = 1
    result = {'prompt_sha256': sha256_file(prompt_path), 'returncode': returncode, 'timed_out': timed_out,
              'call_identity':identity,'response_sha256':sha256_file(output) if output.is_file() else None,
              'launch_error': launch_error,
              'wall_s': time.monotonic() - start, 'cpu_s': float(cpu[2]) + float(cpu[3]) if cpu else None,
              'peak_rss_bytes': int(rss[1]) if rss else None, 'tokens': usage or None,
              'actual_cost_usd': 0.0, 'host_model_cost_usd': 'unknown', 'output': str(output),
              'model': model, 'effort': effort, 'reservation_id': reservation['record_id']}
    reconcile(BUDGET_ROOT, reservation['record_id'], {k: v for k, v in result.items() if k != 'reservation_id'})
    append_record(ROOT / 'ledger/reviews.jsonl', {'kind': 'model_call', **result})
    receipt.write_text(json.dumps(result, indent=2) + '\n')
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('prompt', type=Path); p.add_argument('output', type=Path)
    p.add_argument('--effort', choices=['high', 'xhigh'], required=True)
    p.add_argument('--phase', default='phase2_lock1'); p.add_argument('--terminal', action='store_true')
    p.add_argument('--timeout', type=int, default=600)
    p.add_argument('--model', default='gpt-6.1-sol')
    p.add_argument('--web-search', choices=['live', 'cached'], default=None)
    args = p.parse_args()
    result = call(args.prompt, args.output, args.effort, args.phase, args.terminal, args.timeout, args.model, args.web_search)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['returncode'] == 0 and not result['timed_out'] else 1)
