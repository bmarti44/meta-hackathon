"""Scoped total-local-CPU metering v2 (p004d_s006 review fixes).

Scope = launched process GROUP cumulative CPU (per-PID maxima, dead descendants retained)
PLUS controller CPU (this process's RUSAGE_SELF delta during the run, which includes the
sampler/`ps` invocation overhead of the wrapper itself). Timeout kills the whole group
(SIGKILL via killpg) and reaps it; stdout/stderr drain concurrently in threads.
Any ps failure or malformed row invalidates the measurement (raises) - never a silent zero.
Stated limits (Witness B remains SCREEN-GRADE, not total-scope proof): descendants that setpgid/setsid escape the group; sub-poll (default 50 ms)
descendants may be missed; ps time granularity ~0.01 s. New module; LOCK2 bytes untouched.
"""
from __future__ import annotations

import os
import re
import resource
import signal
import subprocess
import threading
import time

_TIME_RE = re.compile(r'(?:(\d+)-)?(?:(\d+):)?(\d+):(\d+(?:\.\d+)?)')


class MeteringError(RuntimeError):
    pass


def _parse_time(s: str) -> float:
    m = _TIME_RE.fullmatch(s.strip())
    if not m:
        raise MeteringError(f'malformed ps time field: {s!r}')
    d, h, mi, sec = (float(x) if x else 0.0 for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + sec


def _children_cpu() -> float:
    ru = resource.getrusage(resource.RUSAGE_CHILDREN)
    return ru.ru_utime + ru.ru_stime


_SAMPLER = {'cpu': 0.0}


def _run_sampler(argv):
    _c0 = _children_cpu()
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=10)
    except Exception as e:
        raise MeteringError(f'sampler launch/timeout failure: {e}') from e
    finally:
        _SAMPLER['cpu'] += max(0.0, _children_cpu() - _c0)
    return r


def _group_cpu(pgid: int) -> dict[int, float]:
    # Cheap two-step sampler: pgrep group members, then ps only those PIDs.
    r = _run_sampler(['pgrep', '-g', str(pgid)])
    if r.returncode not in (0, 1):
        raise MeteringError(f'pgrep failed rc={r.returncode}: {r.stderr[-200:]}')
    try:
        pids = [int(x) for x in r.stdout.split()]
    except ValueError as e:
        raise MeteringError(f'malformed pgrep output: {r.stdout[:120]!r}') from e
    if not pids:
        return {}
    r = _run_sampler(['ps', '-o', 'pid=,time=', '-p', ','.join(str(x) for x in pids)])
    if r.returncode != 0:
        raise MeteringError(f'ps failed rc={r.returncode}: {r.stderr[-200:]}')
    seen = {}
    for line in r.stdout.splitlines():
        parts = line.split()
        if not parts:
            continue
        if len(parts) != 2:
            raise MeteringError(f'malformed ps row: {line!r}')
        try:
            pid = int(parts[0])
        except ValueError as e:
            raise MeteringError(f'malformed ps pid: {line!r}') from e
        seen[pid] = _parse_time(parts[1])
    return seen


def _self_cpu() -> float:
    ru = resource.getrusage(resource.RUSAGE_SELF)
    return ru.ru_utime + ru.ru_stime


def run_scoped(argv, timeout_s=600, poll_s=0.1, cwd=None):
    """Run argv in a new process group; return tree+controller CPU accounting.

    Raises MeteringError on any sampling failure (job is group-killed first)."""
    start = time.monotonic()
    self0 = _self_cpu()
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, start_new_session=True, cwd=cwd)
    pgid = proc.pid
    out_buf: list[str] = []
    err_buf: list[str] = []

    def _drain(stream, buf):
        try:
            buf.append(stream.read())
        except Exception:
            pass

    peak: dict[int, float] = {}
    timed_out = False
    group_completed = False
    _SAMPLER['cpu'] = 0.0
    threads = [threading.Thread(target=_drain, args=(proc.stdout, out_buf), daemon=True),
               threading.Thread(target=_drain, args=(proc.stderr, err_buf), daemon=True)]
    try:
        for th in threads:
            th.start()
        while True:
            live = _group_cpu(pgid)
            for pid, cpu in live.items():
                if cpu > peak.get(pid, 0.0):
                    peak[pid] = cpu
            leader_done = proc.poll() is not None
            if leader_done and not live:
                group_completed = True
                break  # group completion, not merely leader exit
            if time.monotonic() - start > timeout_s:
                timed_out = True
                break
            time.sleep(poll_s)
    finally:
        if not group_completed:
            try:
                os.killpg(pgid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=10)
        for th in threads:
            th.join(timeout=5)
    # final accounting sweep may legitimately find an empty group post-reap; peaks retained
    try:
        for pid, cpu in _group_cpu(pgid).items():
            if cpu > peak.get(pid, 0.0):
                peak[pid] = cpu
    except MeteringError:
        raise
    controller = max(0.0, _self_cpu() - self0)
    sampler_cpu = _SAMPLER['cpu']  # per-ps tight windows only; never includes job descendants
    tree = float(sum(peak.values()))
    return {'returncode': proc.returncode, 'timed_out': timed_out,
            'wall_s': time.monotonic() - start,
            'tree_cpu_s': tree, 'controller_cpu_s': controller, 'sampler_cpu_s': sampler_cpu,
            'total_local_cpu_s': tree + controller + sampler_cpu,
            'per_pid_cpu_s': {str(k): v for k, v in sorted(peak.items())},
            'measurement': 'pgid cumulative maxima (group completion tracked past leader exit) + controller RUSAGE_SELF delta + sampler ps CPU via RUSAGE_CHILDREN minus leader; group-kill on timeout; any ps failure raises MeteringError',
            'stdout_tail': ''.join(out_buf)[-1000:], 'stderr_tail': ''.join(err_buf)[-1000:]}
