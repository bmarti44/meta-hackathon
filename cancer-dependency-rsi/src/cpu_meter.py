"""Client-side CPU measurement for FUTURE prospective code (sgen002+).

src/budget.py bytes are pinned by LOCK2_COMMIT (3459abdd...) and must not change;
this module exists so new generations can record honest CPU without touching locked code.
Measurement = RUSAGE_CHILDREN delta over a waited child: client-side waited-children CPU
only. It never measures hosted model inference.
"""
from __future__ import annotations

import resource
import subprocess
import time


def _cpu():
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    return ru.ru_utime + ru.ru_stime


def run_measured(argv, timeout_s=600):
    """Run argv to completion; return dict with returncode, wall_s, cpu_s, stdout/stderr tails."""
    start, c0 = time.monotonic(), _cpu()
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout_s)
        return {'returncode': p.returncode, 'timed_out': False, 'wall_s': time.monotonic() - start,
                'cpu_s': max(0.0, _cpu() - c0),
                'cpu_measurement': 'RUSAGE_CHILDREN delta (client-side waited children only; not hosted inference)',
                'stdout_tail': p.stdout[-2000:], 'stderr_tail': p.stderr[-2000:]}
    except subprocess.TimeoutExpired as e:
        return {'returncode': None, 'timed_out': True, 'wall_s': time.monotonic() - start,
                'cpu_s': max(0.0, _cpu() - c0),
                'cpu_measurement': 'RUSAGE_CHILDREN delta (client-side waited children only; not hosted inference)',
                'stdout_tail': (e.stdout or b'')[-2000:] if isinstance(e.stdout, bytes) else (e.stdout or '')[-2000:],
                'stderr_tail': (e.stderr or b'')[-2000:] if isinstance(e.stderr, bytes) else (e.stderr or '')[-2000:]}
