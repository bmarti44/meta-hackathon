import json
import sys
import budget


def test_real_memory_watchdog_kills_allocating_process_group(tmp_path):
    (tmp_path/'config').mkdir();(tmp_path/'ledger').mkdir()
    (tmp_path/'config/resources.json').write_text(json.dumps({'additional_api_spend_cap_usd':0,
        'research_memory_ceiling_bytes':64*1024**2,'max_cpu_heavy_jobs':2,'exploratory_timeout_s':10}))
    program='import time\na=[]\nwhile True:\n a.append(bytearray(4*1024*1024))\n time.sleep(0.05)\n'
    r=budget.run_bounded(tmp_path,[sys.executable,'-c',program],{'cpu_heavy':True,'memory_bytes':64*1024**2},timeout_s=10)
    assert r['memory_killed'] and not r['timed_out'] and r['returncode']!=0
    assert 48*1024**2 < r['peak_rss_bytes'] < 64*1024**2
    assert not r['memory_observer_error']


def test_memory_observer_failure_prevents_dispatch(tmp_path,monkeypatch):
    (tmp_path/'config').mkdir();(tmp_path/'ledger').mkdir()
    (tmp_path/'config/resources.json').write_text(json.dumps({'additional_api_spend_cap_usd':0,
        'research_memory_ceiling_bytes':64*1024**2,'exploratory_timeout_s':10}))
    def fail():raise RuntimeError('RSS observer unavailable')
    monkeypatch.setattr(budget,'_rss_snapshot',fail)
    r=budget.run_bounded(tmp_path,['must-not-run'],{'cpu_heavy':True},timeout_s=10)
    assert 'observer unavailable' in r['launch_error'] and r['returncode'] is None
