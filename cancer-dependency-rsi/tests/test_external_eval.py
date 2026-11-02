"""Guard and fixture tests for the Lock2 external evaluation (synthetic LFC only; no C values)."""
import csv
import io
import json
import shutil
import sys
import threading
import zipfile
from pathlib import Path

import numpy as np
import pytest
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import budget  # noqa: E402
import external_eval as ee  # noqa: E402
from ledger import sha256_file  # noqa: E402

FILES = sorted(ee.REQUIRED - {'data/raw/sanger_figshare/S2_Supplementary_Tables.zip'})


def make_root(tmp_path, seed=1):
    for rel in FILES:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, tmp_path / rel)
    (tmp_path / 'ledger').mkdir(exist_ok=True)
    cov = list(csv.DictReader(open(ROOT / 'lock_s/covariates.csv')))
    coh = list(csv.DictReader(open(ROOT / 'lock_s/cohort.csv')))
    rng = np.random.default_rng(seed)
    buf = io.StringIO()
    buf.write('sample_ID gene ensembl_id HGNC_ID library LFC\n')
    for c in coh:
        for lib in [c['library_primary']] + ([c['library_alternate']] if c['library_alternate'] else []):
            for r in cov:
                buf.write(f"{c['sample_ID']} {r['gene_sanger']} ENSG0 HGNC:0 {lib} {rng.normal():.6f}\n")
            buf.write(f"{c['sample_ID']} NOTPANEL ENSG0 HGNC:0 {lib} 0.1\n")
    z = tmp_path / 'data/raw/sanger_figshare/S2_Supplementary_Tables.zip'
    z.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(z, 'w') as zf:
        zf.writestr(ee.T6, buf.getvalue())
    return tmp_path


def commit(root):
    (root / 'lock_s/LOCK2_COMMIT.json').write_text(json.dumps(
        {'state': 'COMMITTED', 'commit_id': 'fixture', 'files': {f: sha256_file(root / f) for f in sorted(ee.REQUIRED)}}))


def reserve(root, monkeypatch, nonce='n0nce', pid=None):
    import hashlib, os
    monkeypatch.setenv(ee.NONCE_ENV, nonce)
    return budget.reserve(root, {'name': ee.JOB_NAME, 'phase': 'phase6_7', 'cpu_heavy': True, 'memory_bytes': 1 << 30,
                                 'argv': ['python', str(root / 'src/external_eval.py')], 'wall_s_max': 600,
                                 'launch_nonce_sha256': hashlib.sha256(b'n0nce').hexdigest(),
                                 'launcher_pid': os.getppid() if pid is None else pid})


def test_refuses_without_commit(tmp_path):
    root = make_root(tmp_path)
    with pytest.raises(ee.LockError, match='not committed'):
        ee.main(root)
    assert not (root / 'data/exposure_log.jsonl').exists()


def test_refuses_on_hash_mismatch(tmp_path):
    root = make_root(tmp_path)
    commit(root)
    with open(root / 'lock_s/covariates.csv', 'a') as fh:
        fh.write('\n')
    with pytest.raises(ee.LockError, match='hash mismatch'):
        ee.main(root)
    assert not (root / 'data/exposure_log.jsonl').exists()


def test_refuses_incomplete_commit(tmp_path):
    root = make_root(tmp_path)
    (root / 'lock_s/LOCK2_COMMIT.json').write_text(json.dumps({'state': 'COMMITTED', 'files': {'src/external_eval.py': 'x'}}))
    with pytest.raises(ee.LockError, match='lacks required'):
        ee.main(root)


def test_refuses_direct_invocation_without_bounded_reservation(tmp_path):
    root = make_root(tmp_path)
    commit(root)
    with pytest.raises(ee.LockError, match='run_external_eval'):
        ee.main(root)
    assert not (root / 'lock_s/results').exists() and not (root / 'data/exposure_log.jsonl').exists()


def test_refuses_stale_or_unbound_reservations(tmp_path, monkeypatch):
    root = make_root(tmp_path)
    commit(root)
    reserve(root, monkeypatch)
    monkeypatch.delenv(ee.NONCE_ENV)                      # direct invocation: no nonce
    with pytest.raises(ee.LockError, match='nonce'):
        ee.main(root)
    monkeypatch.setenv(ee.NONCE_ENV, 'wrong')             # wrong nonce
    with pytest.raises(ee.LockError, match='matching live'):
        ee.main(root)
    root2 = make_root(tmp_path / 'b'); commit(root2)
    reserve(root2, monkeypatch, pid=-1)                    # not supervised child of launcher
    with pytest.raises(ee.LockError, match='supervised child'):
        ee.main(root2)
    root3 = make_root(tmp_path / 'c'); commit(root3)
    reserve(root3, monkeypatch)
    monkeypatch.setattr(ee, 'MAX_RESERVATION_AGE_S', -10)  # simulate stale reservation
    with pytest.raises(ee.LockError, match='stale'):
        ee.main(root3)
    for r in (root, root2, root3):
        assert not (r / 'lock_s/results').exists() and not (r / 'data/exposure_log.jsonl').exists()


def test_launcher_runs_supervised_child_and_refuses_rerun(tmp_path, monkeypatch):
    import run_external_eval as rl
    root = make_root(tmp_path)
    (root / '.venv/bin').mkdir(parents=True)
    py = root / '.venv/bin/python'
    py.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n'); py.chmod(0o755)
    commit(root)
    r = rl.launch(root, timeout_s=300)
    assert r['returncode'] == 0, r['stderr_tail']
    assert (root / 'lock_s/results/external_v1.json').exists()
    assert ee.NONCE_ENV not in __import__('os').environ
    r2 = rl.launch(root, timeout_s=60)
    assert r2['returncode'] == 3 and 'single execution' in r2['stderr_tail']


def _fixture_launcher_root(tmp_path):
    root = make_root(tmp_path)
    (root / '.venv/bin').mkdir(parents=True)
    py = root / '.venv/bin/python'
    py.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n'); py.chmod(0o755)
    commit(root)
    return root


def _wait_started(root, proc, limit=60):
    import time
    marker = root / 'lock_s/results/external_v1.started.json'
    t0 = time.time()
    while not marker.exists():
        assert proc.poll() is None, proc.stderr.read() if proc.stderr else ''
        assert time.time() - t0 < limit
        time.sleep(0.05)
    time.sleep(0.2)
    return json.loads(marker.read_text())['pid']


def _gone(pid, limit=15):
    import os, time
    t0 = time.time()
    while time.time() - t0 < limit:
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return True
        time.sleep(0.1)
    return False


@pytest.mark.parametrize('sig', ['SIGINT', 'SIGTERM', 'SIGKILL'])
def test_launcher_interruption_stops_child(tmp_path, sig):
    import signal, subprocess
    root = _fixture_launcher_root(tmp_path)
    proc = subprocess.Popen([str(root / '.venv/bin/python'), str(root / 'src/run_external_eval.py')],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    child = _wait_started(root, proc)
    proc.send_signal(getattr(signal, sig))
    proc.wait(timeout=30)
    assert _gone(child), f'child {child} survived launcher {sig}'
    assert not (root / 'lock_s/results/external_v1.json').exists()
    if sig != 'SIGKILL':
        recs = [json.loads(l) for l in open(root / 'ledger/resources.jsonl')]
        assert any(r.get('kind') == 'reconcile' and r.get('interrupted') for r in recs)


def test_fixture_end_to_end_logs_exposure_and_single_execution(tmp_path, monkeypatch):
    monkeypatch.setattr(ee, 'STAB_REPS', 40)
    root = make_root(tmp_path)
    commit(root)
    reserve(root, monkeypatch)
    assert ee.main(root) == 0
    res = json.loads((root / 'lock_s/results/external_v1.json').read_text())
    p = res['primary']
    assert p['n_models_analyzed'] == 148 and p['n_donors_analyzed'] == 144 and p['model_exclusions'] == []
    assert p['interval_valid'] and res['decision'] in ('BOUND', 'INCONCLUSIVE')  # random null data
    fam = res['secondary_holm_family']
    assert set(fam) == {'S1_null_calibrated', 'S2_tmod1_alias208', 'S3_v1_1_dual_library', 'S4_unadjusted'}
    assert all('model_exclusions' in v and 'n_models_analyzed' in v for v in fam.values())
    assert 'leave_one_model_out' in res['stability_not_decision']
    log = [json.loads(l) for l in open(root / 'data/exposure_log.jsonl')]
    assert log[-1]['operation'] == 'LOCK2_external_outcome_decode' and log[-1]['outcome_values_decoded']
    with pytest.raises(ee.LockError, match='single execution'):
        ee.main(root)


def test_crash_after_start_refuses_silent_rerun(tmp_path, monkeypatch):
    root = make_root(tmp_path)
    commit(root)
    reserve(root, monkeypatch)
    def boom(*a, **k):
        raise KeyboardInterrupt('simulated crash')
    monkeypatch.setattr(ee, 'stream_lfc', boom)
    with pytest.raises(KeyboardInterrupt):
        ee.main(root)
    assert (root / 'lock_s/results/external_v1.started.json').exists()
    assert not (root / 'lock_s/results/external_v1.json').exists()
    with pytest.raises(ee.LockError, match='adjudication'):
        ee.main(root)


def test_atomic_start_concurrency(tmp_path):
    target = tmp_path / 'r' / 'started.json'
    wins, errs = [], []
    def go(i):
        try:
            ee.acquire_start(target, {'i': i}); wins.append(i)
        except ee.LockError:
            errs.append(i)
    ts = [threading.Thread(target=go, args=(i,)) for i in range(16)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert len(wins) == 1 and len(errs) == 15


def test_commit_bytes_never_overwrites(tmp_path):
    p = tmp_path / 'x.json'
    ee.commit_bytes(p, b'one')
    with pytest.raises(FileExistsError):
        ee.commit_bytes(p, b'two')
    assert p.read_bytes() == b'one' and list(tmp_path.iterdir()) == [p]


def test_nonfinite_model_exclusion_rule():
    coh = [{'sample_ID': f's{i}', 'donor_ID': f'd{i}', 'library_primary': 'minLib', 'library_alternate': ''} for i in range(3)]
    lfc = {(f's{i}', 'minLib', g): 1.0 for i in range(3) for g in 'abc'}
    lfc[('s1', 'minLib', 'b')] = float('nan')
    del lfc[('s2', 'minLib', 'c')]
    S, sids, dids, excl = ee.build_matrix(lfc, coh, list('abc'))
    assert sids == ['s0'] and [e['sample_ID'] for e in excl] == ['s1', 's2']


def test_invalid_analyses_are_structured_not_raised():
    rng = np.random.default_rng(0)
    G, M = 30, 20
    S = rng.normal(size=(G, M)); ref = rng.normal(size=G); L = rng.normal(size=G)
    sids = [f's{i}' for i in range(M)]; dids = [f'd{i}' for i in range(M)]
    r, pt = ee.analysis(S, ref, L, L.copy(), sids, dids, [], M)          # L == base -> degenerate residuals
    assert r['decision'] == 'INCONCLUSIVE' and r['bootstrap_p_two_sided_rho0'] is None and pt is None
    S2 = S.copy(); S2[:, 0] = 1.0                                       # constant sample ordering
    r2, _ = ee.analysis(S2, ref, L, rng.normal(size=G), sids, dids, [], M)
    assert r2['decision'] == 'INCONCLUSIVE' and r2['bootstrap_p_two_sided_rho0'] is None
    r3, _ = ee.analysis(S, ref, L, rng.normal(size=G), sids[:1], dids[:1], [{'x': 1}] * 5, M)
    assert r3['decision'] == 'INCONCLUSIVE' and 'exceed' in r3['invalid_reasons'][0]


def test_family_invalid_members_never_reject():
    sec = {'S1': {'point_valid': True, 'interval_valid': True, 'bootstrap_p_two_sided_rho0': 0.001},
           'S2': {'point_valid': True, 'interval_valid': False, 'bootstrap_p_two_sided_rho0': 0.0004},
           'S3': {'point_valid': False, 'interval_valid': False, 'bootstrap_p_two_sided_rho0': None},
           'S4': {'point_valid': True, 'interval_valid': True, 'bootstrap_p_two_sided_rho0': 0.2}}
    out = ee.finalize_family(sec)
    assert out['S2']['holm_reject_rho0_at_0.05'] is False and out['S2']['holm_adjusted_p'] is None
    assert out['S3']['holm_reject_rho0_at_0.05'] is False
    assert out['S1']['holm_adjusted_p'] == pytest.approx(0.004) and out['S1']['holm_reject_rho0_at_0.05']


def test_holm_and_boot_p_failures_count_against_rejection():
    assert ee.holm({'a': 0.01, 'b': 0.04, 'c': 0.03, 'd': 0.5}) == {'a': 0.04, 'c': 0.09, 'b': 0.09, 'd': 0.5}
    assert ee.boot_p(np.ones(99)) == pytest.approx(0.02)
    v = np.r_[np.ones(4600), np.full(400, np.nan)]
    assert ee.boot_p(v, 5000) == pytest.approx(2 * 401 / 5001)
    assert ee.boot_p(np.array([np.nan])) is None


def test_unadjusted_equals_spearman():
    import donor_kernel as dk
    rng = np.random.default_rng(3)
    y, x = rng.normal(size=50), rng.normal(size=50)
    assert dk.rank_correlations(y, x, np.zeros(50))[0] == pytest.approx(spearmanr(y, x).statistic, abs=1e-12)


def test_cli_evaluate_external_refuses_before_lock2():
    import subprocess
    if (ROOT / 'lock_s/LOCK2_COMMIT.json').exists():
        pytest.skip('Lock2 committed in real root')
    r = subprocess.run([sys.executable, str(ROOT / 'src/cli.py'), 'evaluate-external'], capture_output=True, text=True)
    assert r.returncode == 3 and 'not committed' in r.stderr
