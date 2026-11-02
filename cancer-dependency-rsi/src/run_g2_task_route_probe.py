"""Dispatch the g2 task route probe under run_bounded (SPEC g2-task-route-probe-v1)."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from budget import run_bounded  # noqa: E402
from ledger import append_record  # noqa: E402

SPEC = ROOT / 'reviews/prompts/g2_task_route_probe_v1.json'
EXPECTED_SPEC_SHA = sys.argv[1]

if __name__ == '__main__':
    sha = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    if sha != EXPECTED_SPEC_SHA:
        raise SystemExit(f'spec hash mismatch {sha}')
    if (ROOT / 'reviews/g2_task_route_probe_v1.json').exists():
        raise SystemExit('immutable output already exists; never redispatch')
    job = {'name': 'g2_task_route_probe_v1', 'phase': 'phase2_lock1', 'cpu_heavy': True,
           'memory_bytes': 1073741824, 'nodes': 0, 'model_calls': 0, 'spec_sha256': sha}
    result = run_bounded(ROOT, [str(ROOT / '.venv/bin/python'), str(ROOT / 'src/g2_task_route_probe.py')], job, timeout_s=300)
    append_record(ROOT / 'ledger/experiments.jsonl', {
        'kind': 'g2_task_route_probe_metadata_only', 'spec': str(SPEC.relative_to(ROOT)), 'spec_sha256': sha,
        'returncode': result.get('returncode'), 'timed_out': result.get('timed_out'), 'wall_s': result.get('wall_s'),
        'peak_rss_bytes': result.get('peak_rss_bytes'), 'outcome_values_parsed': False, 'actual_cost_usd': 0,
        'stdout_tail': result.get('stdout_tail'), 'stderr_tail': result.get('stderr_tail')})
    print(json.dumps({k: result.get(k) for k in ('returncode', 'timed_out', 'wall_s', 'peak_rss_bytes', 'memory_killed', 'stdout_tail', 'stderr_tail')}, indent=1))
