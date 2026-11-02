"""Regression tests for independently reproduced G2-r2 defects, not biological evidence."""
import json
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp
from pathlib import Path
import threading
import numpy as np
import pytest
import budget
import estimators
import evaluator_v3 as evaluator_v2
import lineage
import status_rules


def root_config(root):
    (root / 'config').mkdir(); (root / 'ledger').mkdir()
    (root / 'config/resources.json').write_text(json.dumps({'additional_api_spend_cap_usd': 1,
        'exploratory_timeout_s': 5, 'research_memory_ceiling_bytes': 1000, 'max_cpu_heavy_jobs': 2}))
    return root


def try_reserve(args):
    path, barrier = args
    barrier.wait(timeout=10)
    try:
        budget.reserve(Path(path), {'name': 'concurrent'}, 0.6)
        return 'ok'
    except RuntimeError:
        return 'cap'


def test_atomic_reservation_threads(tmp_path):
    root_config(tmp_path)
    barrier = threading.Barrier(2)
    with ThreadPoolExecutor(2) as pool:
        outcomes = list(pool.map(try_reserve, [(str(tmp_path), barrier)] * 2))
    assert sorted(outcomes) == ['cap', 'ok']


def test_atomic_reservation_processes(tmp_path):
    root_config(tmp_path)
    ctx = mp.get_context('spawn')
    # Manager sockets may be forbidden by the host; use process-shared semaphore barrier.
    barrier = ctx.Barrier(2)
    queue = ctx.Queue()
    procs = [ctx.Process(target=process_worker, args=(str(tmp_path), barrier, queue)) for _ in range(2)]
    for p in procs: p.start()
    for p in procs:
        p.join(timeout=20)
        assert p.exitcode == 0
    assert sorted(queue.get(timeout=2) for _ in procs) == ['cap', 'ok']


def process_worker(path, barrier, queue):
    queue.put(try_reserve((path, barrier)))


def test_reconciliation_identity_validation_and_interruption(tmp_path):
    root_config(tmp_path)
    r = budget.reserve(tmp_path, {'name': 'interrupted'}, 0.6)
    with pytest.raises(RuntimeError, match='spend cap'):
        budget.reserve(tmp_path, {'name': 'retry'}, 0.6)
    with pytest.raises(RuntimeError, match='nonnegative'):
        budget.reconcile(tmp_path, r['record_id'], {'actual_cost_usd': -1})
    with pytest.raises(RuntimeError, match='identity'):
        budget.reconcile(tmp_path, r['record_id'], {'kind': 'reserve'})
    with pytest.raises(RuntimeError, match='unknown reservation'):
        budget.reconcile(tmp_path, 'absent', {})
    budget.reconcile(tmp_path, r['record_id'], {'actual_cost_usd': 0.4, 'wall_s': 1})
    with pytest.raises(RuntimeError, match='already reconciled'):
        budget.reconcile(tmp_path, r['record_id'], {'actual_cost_usd': 0})
    budget.reserve(tmp_path, {'name': 'after'}, 0.6)


def test_phase_total_slots_and_terminal_reserve(tmp_path):
    root_config(tmp_path)
    alloc = {'total': {'wall_h': 1, 'evaluated_nodes_max': 2, 'model_calls_max': 3},
        'terminal_review_reserve': {'sol_xhigh_calls_reserved': 1},
        'per_phase': {'p': {'wall_h': 1, 'nodes': 2, 'model_calls': 3},
                      'phase6_7': {'wall_h': 1, 'model_calls': 2}}}
    (tmp_path / 'config/allocations.json').write_text(json.dumps(alloc))
    r = budget.reserve(tmp_path, {'phase': 'p', 'model_calls': 2, 'nodes': 2, 'cpu_heavy': True, 'memory_bytes': 600})
    with pytest.raises(RuntimeError, match='memory'):
        budget.reserve(tmp_path, {'phase': 'p', 'memory_bytes': 600})
    with pytest.raises(RuntimeError, match='total nodes'):
        budget.reserve(tmp_path, {'phase': 'p', 'nodes': 1})
    with pytest.raises(RuntimeError, match='total model_calls'):
        budget.reserve(tmp_path, {'phase': 'p', 'model_calls': 1})
    budget.reconcile(tmp_path, r['record_id'], {'wall_s': 1})
    budget.reserve(tmp_path, {'phase': 'phase6_7', 'model_calls': 1, 'terminal_review': True})


def test_nonfinite_rejected_before_ranking():
    x = np.arange(60., dtype=float)
    for value in (np.inf, -np.inf, np.nan):
        bad = x.copy(); bad[3] = value
        with pytest.raises(ValueError, match='nonfinite'):
            estimators.partial_spearman(bad, np.sin(x), x)
        with pytest.raises(ValueError, match='nonfinite'):
            estimators.partial_spearman(x, np.sin(x), bad)


def test_exact_membership_and_nonfinite_original_target(monkeypatch):
    meta, eff, idx = estimators.load_dev()
    original_pairs = estimators.format_pairs(meta, eff)
    gene = json.loads((estimators.ROOT / 'data/gene_scopes.json').read_text())['primary216'][0]
    config = {'scope': 'primary216', 'operator': 'mean_abs_delta', 'adjust': 'base_strength'}
    monkeypatch.setattr(estimators, 'format_pairs', lambda *args: original_pairs.drop(index=gene))
    r = evaluator_v2.evaluate(config)
    assert not r['valid'] and 'missing frozen' in r['invalid_reasons'][0]
    monkeypatch.setattr(estimators, 'format_pairs', lambda *args: original_pairs)
    for column in ('MeanDifference', 'AdherentMean'):
        bad_idx = idx.copy(); bad_idx.loc[gene, column] = np.inf
        monkeypatch.setattr(estimators, 'load_dev', lambda: (meta, eff, bad_idx))
        r = evaluator_v2.evaluate(config)
        assert not r['valid'] and 'nonfinite' in r['invalid_reasons'][0]


def test_failure_dominance_and_success_recovery():
    attempts = [{'attempt_id': 'a', 'outcome_class': 'implementation_failure', 'seq': 1,
        'repair_citation': {'node_id': 'a', 'fix_class': 'bug_fix'}},
        {'attempt_id': 'b', 'outcome_class': 'invalid_result', 'seq': 2},
        {'attempt_id': 'c', 'outcome_class': 'success', 'valid': True, 'q': 0.5, 'seq': 3}]
    assert status_rules.direction_status(attempts, [])['recoverability'] == 'na'
    failures = [{'attempt_id': str(i), 'config_id': str(i), 'outcome_class': 'conceptual_failure', 'seq': i} for i in range(2)]
    assert status_rules.direction_status(failures, [])['recoverability'] == 'dead'
    assert status_rules.direction_status(failures + attempts[-1:], [])['recoverability'] == 'na'


def test_schema_parent_objects_reach_dag_validator():
    base = {'study_id': 'S', 'evaluator_version': 'v2'}
    existing = {'a': {'attempt_id': 'a', 'parents': [], **base}}
    node = {'attempt_id': 'b', 'origin': 'refinement', 'parents': [{'attempt_id': 'a', 'contribution': 'refine original'}], **base}
    assert lineage.validate_node(node, existing) == []
    existing['b'] = node
    assert lineage.ancestry('b', existing) == {'a', 'b'}
    node['parents'].append(dict(node['parents'][0]))
    assert 'duplicate' in lineage.validate_node(node, existing)[0]


def test_cpu_slots_and_wall_limits(tmp_path):
    root_config(tmp_path)
    a = budget.reserve(tmp_path, {'cpu_heavy': True, 'memory_bytes': 100})
    budget.reserve(tmp_path, {'cpu_heavy': True, 'memory_bytes': 100})
    with pytest.raises(RuntimeError, match='CPU-job'):
        budget.reserve(tmp_path, {'cpu_heavy': True, 'memory_bytes': 100})
    budget.reconcile(tmp_path, a['record_id'], {'wall_s': 0})
    budget.reserve(tmp_path, {'cpu_heavy': True, 'memory_bytes': 100})


def test_phase_wall_reservations_count_before_dispatch(tmp_path):
    root_config(tmp_path)
    (tmp_path / 'config/allocations.json').write_text(json.dumps({
        'total': {'wall_h': 1, 'evaluated_nodes_max': 2, 'model_calls_max': 3},
        'terminal_review_reserve': {'sol_xhigh_calls_reserved': 1},
        'per_phase': {'p': {'wall_h': 10/3600, 'nodes': 2, 'model_calls': 3}}}))
    budget.reserve(tmp_path, {'phase': 'p', 'wall_s_max': 6})
    with pytest.raises(RuntimeError, match='phase wall'):
        budget.reserve(tmp_path, {'phase': 'p', 'wall_s_max': 6})


def test_memory_cap_launch_failure_reconciles_without_dispatch(tmp_path, monkeypatch):
    import subprocess
    from ledger import read_records
    root_config(tmp_path)
    def fail(*args, **kwargs):
        raise subprocess.SubprocessError('memory limit unavailable')
    monkeypatch.setattr(subprocess, 'Popen', fail)
    r = budget.run_bounded(tmp_path, ['unused'], {'cpu_heavy': True, 'memory_bytes': 100})
    assert r['returncode'] is None and 'memory limit' in r['launch_error']
    assert [r['kind'] for r in read_records(tmp_path / 'ledger/resources.jsonl')] == ['reserve', 'reconcile']


def test_model_resume_does_not_repeat_failed_or_successful_calls(tmp_path, monkeypatch):
    import model_call
    from ledger import sha256_file
    prompt = tmp_path / 'prompt.txt'; prompt.write_text('retained prompt')
    output = tmp_path / 'answer.md'
    receipt = output.with_suffix('.receipt.json')
    def unexpected(*args, **kwargs):
        raise AssertionError('resume must not redispatch')
    monkeypatch.setattr(model_call.subprocess, 'Popen', unexpected)
    for code in (0, 1):
        if code==0:output.write_text('retained response')
        elif output.exists():output.unlink()
        identity=model_call.call_identity(prompt,output,'xhigh','phase2_lock1',False,600)
        receipt.write_text(json.dumps({'prompt_sha256':sha256_file(prompt),'returncode':code,
            'call_identity':identity,'response_sha256':sha256_file(output) if output.exists() else None}))
        assert model_call.call(prompt, output, 'xhigh')['returncode'] == code
        with pytest.raises(RuntimeError,match='identity'):
            model_call.call(prompt,output,'high')
    prompt.write_text('changed prompt')
    with pytest.raises(RuntimeError, match='different prompt'):
        model_call.call(prompt, output, 'xhigh')


def test_scientific_timeout_cannot_borrow_host_reasoning_allowance(tmp_path):
    root_config(tmp_path)
    (tmp_path/'config/allocations.json').write_text(json.dumps({
        'total':{'wall_h':20,'evaluated_nodes_max':10,'model_calls_max':10},
        'terminal_review_reserve':{'sol_xhigh_calls_reserved':1},
        'per_phase':{'p':{'wall_h':20,'model_calls':10,'host_reasoning_job_timeout_s':1200}}}))
    with pytest.raises(RuntimeError,match='scientific job'):
        budget.reserve(tmp_path,{'phase':'p','cpu_heavy':True,'memory_bytes':100,'wall_s_max':1200})


def test_model_resume_response_hash_must_match(tmp_path,monkeypatch):
    import model_call
    from ledger import sha256_file
    prompt=tmp_path/'prompt';prompt.write_text('p');output=tmp_path/'answer.md';output.write_text('original')
    identity=model_call.call_identity(prompt,output,'high','phase2_lock1',False,600)
    output.with_suffix('.receipt.json').write_text(json.dumps({'prompt_sha256':sha256_file(prompt),
        'returncode':0,'call_identity':identity,'response_sha256':sha256_file(output)}))
    output.write_text('tampered')
    with pytest.raises(RuntimeError,match='response missing or changed'):
        model_call.call(prompt,output,'high')
