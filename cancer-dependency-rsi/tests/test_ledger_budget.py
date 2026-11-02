import json
from pathlib import Path

import pytest

import budget
import ledger


def _root(tmp_path: Path) -> Path:
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "resources.json").write_text(json.dumps({
        "research_memory_ceiling_bytes": 8589934592,
        "exploratory_timeout_s": 5,
        "additional_api_spend_cap_usd": 0.0,
    }))
    (tmp_path / "ledger").mkdir()
    return tmp_path


def test_ledger_append_only_and_hash_stable(tmp_path):
    p = tmp_path / "l.jsonl"
    ledger.append_record(p, {"kind": "x"})
    ledger.append_record(p, {"kind": "y"})
    recs = ledger.read_records(p)
    assert [r["kind"] for r in recs] == ["x", "y"]
    assert ledger.context_hash({"b": 1, "a": 2}) == ledger.context_hash({"a": 2, "b": 1})


def test_budget_zero_cap_blocks_paid_reservation(tmp_path):
    root = _root(tmp_path)
    with pytest.raises(RuntimeError):
        budget.reserve(root, {"name": "paid"}, est_cost_usd=0.01)


def test_run_bounded_enforces_timeout(tmp_path):
    root = _root(tmp_path)
    res = budget.run_bounded(root, ["sleep", "30"], {"name": "slow"}, timeout_s=1)
    assert res["timed_out"] is True
    kinds = [r["kind"] for r in ledger.read_records(root / "ledger" / "resources.jsonl")]
    assert kinds == ["reserve", "reconcile"]


def test_cpu_meter_records_client_cpu():
    # budget.py bytes are LOCK2-pinned; CPU measurement lives in cpu_meter for new code.
    import cpu_meter
    r = cpu_meter.run_measured([__import__('sys').executable, '-c', 'x=sum(i*i for i in range(2_000_000)); print(x)'], timeout_s=30)
    assert r['returncode'] == 0
    assert r['cpu_s'] is not None and r['cpu_s'] > 0
    assert 'RUSAGE_CHILDREN' in r['cpu_measurement'] and 'not hosted inference' in r['cpu_measurement']
    assert r['cpu_s'] <= r['wall_s'] * 4 + 1
