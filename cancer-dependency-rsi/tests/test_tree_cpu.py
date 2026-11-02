import os
import subprocess
import sys
import time

import pytest

import tree_cpu

BURN = 'import time\nt=time.process_time()\nwhile time.process_time()-t<%s: pass'


def test_single_within_25pct():
    r = tree_cpu.run_scoped([sys.executable, '-c', BURN % 1.2])
    assert r['returncode'] == 0
    assert abs(r['total_local_cpu_s'] - 1.2) <= 0.25 * 1.2
    assert r['controller_cpu_s'] >= 0


def test_concurrent_contamination_excluded():
    unrelated = subprocess.Popen([sys.executable, '-c', BURN % 2.0], start_new_session=True)
    try:
        r = tree_cpu.run_scoped([sys.executable, '-c', 'import time; time.sleep(0.6)'])
    finally:
        unrelated.wait(timeout=30)
    assert r['total_local_cpu_s'] < 0.6  # unrelated 2 CPU-s burn not counted


def test_failed_cpu_job_charged():
    r = tree_cpu.run_scoped([sys.executable, '-c', (BURN % 0.5) + '\nraise SystemExit(3)'])
    assert r['returncode'] == 3
    assert r['tree_cpu_s'] >= 0.3


def test_timeout_kills_group():
    code = ("import os,time\npid=os.fork()\n"
            "if pid==0:\n time.sleep(30); os._exit(0)\n"
            "time.sleep(30)")
    t0 = time.monotonic()
    r = tree_cpu.run_scoped([sys.executable, '-c', code], timeout_s=1)
    assert r['timed_out'] is True
    assert time.monotonic() - t0 < 8  # group killed, no 30s hang on pipes/children


def test_fork_workers_majority():
    code = ("import os,time\npids=[]\n"
            "for _ in range(2):\n"
            " pid=os.fork()\n"
            " if pid==0:\n"
            "  t=time.process_time()\n"
            "  while time.process_time()-t<0.5: pass\n"
            "  os._exit(0)\n"
            " pids.append(pid)\n"
            "[os.waitpid(p,0) for p in pids]")
    r = tree_cpu.run_scoped([sys.executable, '-c', code])
    assert r['returncode'] == 0
    assert 0.75 <= r['tree_cpu_s'] <= 1.25
    assert r['timed_out'] is False
    assert 0.75 <= r['total_local_cpu_s'] <= 1.35  # combined incl sampler/controller, no double count
    assert len(r['per_pid_cpu_s']) >= 3



def test_leader_exit_descendant_tracked():
    code = ("import os,time\npid=os.fork()\n"
            "if pid==0:\n"
            " t=time.process_time()\n"
            " while time.process_time()-t<0.7: pass\n"
            " os._exit(0)\n"
            "print('leader exits immediately')")
    r = tree_cpu.run_scoped([sys.executable, '-c', code], timeout_s=10)
    assert 0.45 <= r['tree_cpu_s'] <= 1.05 and r['total_local_cpu_s'] <= 1.2 and r['timed_out'] is False and r['returncode'] == 0
