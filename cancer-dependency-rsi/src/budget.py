"""Atomic reserve-before-dispatch accounting; outstanding jobs retain their maxima."""
from __future__ import annotations
from contextlib import contextmanager
import fcntl
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import time
import tempfile
from ledger import append_record, read_records


def load_config(root: Path) -> dict:
    return json.loads((root / 'config/resources.json').read_text())


@contextmanager
def transaction(root: Path):
    (root / 'ledger').mkdir(parents=True, exist_ok=True)
    with (root / 'ledger/resources.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            yield read_records(root / 'ledger/resources.jsonl')
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def _number(value, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise RuntimeError(f'budget: {field} must be finite and nonnegative')
    return float(value)


def reserve(root: Path, job: dict, est_cost_usd: float = 0.0) -> dict:
    cost = _number(est_cost_usd, 'billable maximum')
    cfg = load_config(root)
    path = root / 'config/allocations.json'
    alloc = json.loads(path.read_text()) if path.exists() else None
    job = dict(job)
    job.setdefault('wall_s_max', cfg.get('exploratory_timeout_s', 600))
    job.setdefault('nodes', 0)
    job.setdefault('model_calls', 0)
    job.setdefault('cpu_heavy', False)
    job.setdefault('memory_bytes', cfg.get('research_memory_ceiling_bytes', 8589934592) if job['cpu_heavy'] else 0)
    for key in ('wall_s_max', 'nodes', 'model_calls', 'memory_bytes'):
        _number(job[key], key)
    for key in ('nodes', 'model_calls'):
        if int(job[key]) != job[key]:
            raise RuntimeError(f'budget: {key} must be integral')
    if alloc:
        if job.get('phase') not in alloc['per_phase']:
            raise RuntimeError('budget: job requires a named campaign phase')
        if job.get('terminal_review') and (job['phase'] != 'phase6_7' or job['model_calls'] != 1):
            raise RuntimeError('budget: terminal reserve is only for one phase6_7 terminal review')
    if job['cpu_heavy']:
        limit=cfg.get('exploratory_timeout_s',600)
        if alloc:
            limit=alloc['per_phase'][job['phase']].get('scientific_job_allowances',{}).get(job.get('name'),limit)
        if job['wall_s_max']>limit:
            raise RuntimeError('budget: scientific job exceeds default or explicitly recorded scientific allowance')
    with transaction(root) as records:
        reservations = [r for r in records if r.get('kind') == 'reserve']
        reconciled = {r['reservation_id']: r for r in records if r.get('kind') == 'reconcile'}
        active = [r for r in reservations if r['record_id'] not in reconciled]
        spent = sum(r.get('actual_cost_usd', 0) for r in reconciled.values())
        outstanding = sum(r['est_cost_usd'] for r in active)
        if spent + outstanding + cost > cfg.get('additional_api_spend_cap_usd', 0):
            raise RuntimeError('budget: spend cap would be exceeded')
        if sum(bool(r['job'].get('cpu_heavy')) for r in active) + bool(job['cpu_heavy']) > cfg.get('max_cpu_heavy_jobs', 2):
            raise RuntimeError('budget: CPU-job concurrency exceeded')
        if sum(r['job'].get('memory_bytes', 0) for r in active) + job['memory_bytes'] > cfg.get('research_memory_ceiling_bytes', 8589934592):
            raise RuntimeError('budget: aggregate research memory exceeded')
        if alloc:
            def used(rows, key):
                if key == 'wall_s_max':
                    return sum(reconciled.get(r['record_id'], {}).get('wall_s', r['job'].get(key, 0)) for r in rows)
                return sum(r['job'].get(key, 0) for r in rows)
            total = alloc['total']
            caps = {'nodes': total['evaluated_nodes_max'], 'model_calls': total['model_calls_max'], 'wall_s_max': total['wall_h'] * 3600}
            terminal_used = sum(r['job'].get('model_calls', 0) for r in reservations if r['job'].get('terminal_review'))
            if not job.get('terminal_review'):
                caps['model_calls'] -= max(0, alloc['terminal_review_reserve']['sol_xhigh_calls_reserved'] - terminal_used)
            phase_rows = [r for r in reservations if r['job'].get('phase') == job['phase']]
            phase = alloc['per_phase'][job['phase']]
            for key, cap in caps.items():
                if used(reservations, key) + job[key] > cap:
                    raise RuntimeError(f'budget: total {key} cap exceeded')
            phase_caps = {'nodes': phase.get('nodes', phase.get('fresh_nodes_max', phase.get('rollouts_max', total['evaluated_nodes_max']))),
                          'model_calls': phase['model_calls'], 'wall_s_max': phase['wall_h'] * 3600}
            if job['phase'] == 'phase4_per_cycle':
                cycle = job.get('cycle')
                if not isinstance(cycle, int) or not 1 <= cycle <= phase['cycles_max']:
                    raise RuntimeError('budget: valid cycle number required')
                phase_rows = [r for r in phase_rows if r['job'].get('cycle') == cycle]
            for key, cap in phase_caps.items():
                if used(phase_rows, key) + job[key] > cap:
                    raise RuntimeError(f'budget: phase {key} cap exceeded')
        return append_record(root / 'ledger/resources.jsonl', {'kind': 'reserve', 'job': job, 'est_cost_usd': cost, 'state': 'reserved'})


def reconcile(root: Path, reservation_id: str, actual: dict) -> dict:
    if set(actual) & {'kind', 'reservation_id', 'record_id', 'state', 'job', 'ts_utc'}:
        raise RuntimeError('budget: reconciliation cannot override accounting identity')
    actual = dict(actual)
    actual.setdefault('actual_cost_usd', 0.0)
    for key in ('actual_cost_usd', 'wall_s', 'cpu_s', 'peak_rss_bytes'):
        if key in actual and actual[key] is not None:
            _number(actual[key], key)
    with transaction(root) as records:
        reserved = [r for r in records if r.get('kind') == 'reserve' and r['record_id'] == reservation_id]
        if len(reserved) != 1:
            raise RuntimeError('budget: unknown reservation')
        if any(r.get('kind') == 'reconcile' and r.get('reservation_id') == reservation_id for r in records):
            raise RuntimeError('budget: already reconciled')
        # Preserve and charge actual overruns, rather than refusing to record them.
        actual['budget_overrun'] = actual['actual_cost_usd'] > reserved[0]['est_cost_usd'] or actual.get('wall_s', 0) > reserved[0]['job']['wall_s_max'] + 1
        return append_record(root / 'ledger/resources.jsonl', {**actual, 'kind': 'reconcile', 'reservation_id': reservation_id, 'state': 'reconciled'})


def _rss_snapshot() -> dict[int, int]:
    """Sample summed resident bytes per process group, including descendants.

    This is an observed RSS watchdog, not an OS allocation barrier. Jobs are
    trusted local research code; the kill threshold reserves headroom below
    their allocated memory. A failed observer terminates the job (fail closed).
    """
    raw = subprocess.check_output(['/bin/ps', '-axo', 'pgid=,rss='], text=True, timeout=2)
    groups = {}
    for line in raw.splitlines():
        fields = line.split()
        if len(fields) != 2:
            raise RuntimeError('malformed RSS observer output')
        group, kib = map(int, fields)
        groups[group] = groups.get(group, 0) + kib * 1024
    if groups.get(os.getpgrp(), 0) <= 0:
        raise RuntimeError('RSS observer cannot see its own process group')
    return groups


def _kill_group(pid: int):
    try:
        os.killpg(pid, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_bounded(root: Path, argv: list[str], job: dict, timeout_s: int | None = None) -> dict:
    cfg = load_config(root)
    timeout_s = timeout_s or int(cfg['exploratory_timeout_s'])
    monitor = cfg.get('memory_monitor', {})
    interval = float(monitor.get('interval_s', 0.05))
    fraction = float(monitor.get('kill_fraction', 0.75))
    if interval <= 0 or interval > 0.1 or not 0 < fraction <= 0.75:
        raise RuntimeError('invalid memory monitor config (cannot relax reserve headroom)')
    reservation = reserve(root, {**job, 'argv': argv, 'wall_s_max': timeout_s})
    mem_bytes = reservation['job']['memory_bytes']
    started = time.monotonic()
    timed_out, memory_killed, observer_error = False, False, None
    peak, proc = 0, None
    with tempfile.TemporaryFile() as out_file, tempfile.TemporaryFile() as err_file:
        try:
            if job.get('cpu_heavy'):
                _rss_snapshot()  # require working observer before dispatch
            proc = subprocess.Popen(argv, stdout=out_file, stderr=err_file, text=True, start_new_session=True)
        except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
            result = {'returncode': None, 'timed_out': False, 'launch_error': str(exc),
                      'wall_s': time.monotonic() - started, 'actual_cost_usd': 0.0}
            reconcile(root, reservation['record_id'], result)
            return result
        interrupted = None
        try:
            while proc.poll() is None:
                if job.get('cpu_heavy'):
                    try:
                        rss = _rss_snapshot().get(proc.pid, 0)
                        peak = max(peak, rss)
                        if rss > mem_bytes * fraction:
                            memory_killed = True
                            _kill_group(proc.pid)
                            break
                    except (OSError, subprocess.SubprocessError, ValueError, RuntimeError) as exc:
                        observer_error = str(exc)
                        _kill_group(proc.pid)
                        break
                remaining = timeout_s - (time.monotonic() - started)
                if remaining <= 0:
                    timed_out = True
                    _kill_group(proc.pid)
                    break
                try:
                    proc.wait(timeout=min(interval, remaining))
                except subprocess.TimeoutExpired:
                    pass
        except BaseException as exc:  # KeyboardInterrupt/SystemExit/signal-derived: never leave an unsupervised job
            interrupted = f'{type(exc).__name__}: {exc}'
            _kill_group(proc.pid)
            try:
                proc.wait(timeout=10)
            except Exception:  # noqa: BLE001
                pass
            reconcile(root, reservation['record_id'], {'returncode': proc.returncode, 'timed_out': False,
                      'interrupted': interrupted, 'wall_s': time.monotonic() - started, 'actual_cost_usd': 0.0,
                      'peak_rss_bytes': peak or None})
            raise
        proc.wait()
        # Always remove a job's surviving descendants, including after a
        # successful leader exit. A research job must not leave work running.
        _kill_group(proc.pid)
        out_file.seek(0, os.SEEK_END); length=out_file.tell(); out_file.seek(max(0,length-2000))
        out=out_file.read().decode(errors='replace')
        err_file.seek(0, os.SEEK_END); length=err_file.tell(); err_file.seek(max(0,length-2000))
        err=err_file.read().decode(errors='replace')
    result = {'returncode': proc.returncode, 'timed_out': timed_out,
              'memory_killed': memory_killed, 'memory_observer_error': observer_error,
              'peak_rss_bytes': peak or None, 'rss_sample_interval_s': interval,
              'rss_kill_threshold_bytes': int(mem_bytes*fraction) if job.get('cpu_heavy') else None,
              'memory_enforcement': 'sampled_process_group_RSS_with_25percent_headroom' if job.get('cpu_heavy') else 'utility_no_research_RSS_reservation',
              'wall_s': time.monotonic()-started,'stdout_tail':out,'stderr_tail':err,'actual_cost_usd':0.0}
    reconcile(root,reservation['record_id'],result)
    return result
