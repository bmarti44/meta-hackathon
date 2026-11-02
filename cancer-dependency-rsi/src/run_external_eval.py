"""Bounded launcher for the Lock2 external evaluation (the only supported execution path)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from budget import run_bounded  # noqa: E402
import external_eval  # noqa: E402

JOB = {'name': external_eval.JOB_NAME, 'phase': 'phase6_7', 'cpu_heavy': True, 'memory_bytes': 2147483648,
       'nodes': 0, 'model_calls': 0}


def launch(root: Path = ROOT, timeout_s: int = 600) -> dict:
    import hashlib
    import os
    import secrets
    external_eval.verify_lock(root)  # fail before reserving if Lock2 is absent/mismatched
    nonce = secrets.token_hex(32)
    job = {**JOB, 'launch_nonce_sha256': hashlib.sha256(nonce.encode()).hexdigest(), 'launcher_pid': os.getpid()}
    argv = [str(root / '.venv/bin/python'), str(root / 'src/external_eval.py')]
    import signal

    def _as_interrupt(signum, frame):
        raise KeyboardInterrupt(f'launcher received signal {signum}')
    previous = {sig: signal.signal(sig, _as_interrupt) for sig in (signal.SIGTERM, signal.SIGHUP)}
    os.environ[external_eval.NONCE_ENV] = nonce  # inherited only by the supervised child
    try:
        # run_bounded kills/reaps the child process group on any interruption; the child also
        # self-terminates if this launcher disappears (start_parent_watchdog).
        return run_bounded(root, argv, job, timeout_s=timeout_s)
    finally:
        os.environ.pop(external_eval.NONCE_ENV, None)
        for sig, h in previous.items():
            signal.signal(sig, h)


if __name__ == '__main__':
    try:
        r = launch()
    except external_eval.LockError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(3)
    print(json.dumps({k: r.get(k) for k in ('returncode', 'timed_out', 'wall_s', 'peak_rss_bytes', 'memory_killed', 'stdout_tail', 'stderr_tail')}, indent=1))
    sys.exit(0 if r.get('returncode') == 0 else 1)
