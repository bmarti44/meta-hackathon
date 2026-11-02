import json
import numpy as np
import pytest

import budget, estimators, history_index, lineage, memo, status_rules
import evaluator_v3 as evaluator_v2


def test_degenerate_inputs_raise():
    with pytest.raises(ValueError):
        estimators.partial_spearman(np.ones(50), np.arange(50.0), np.arange(50.0))
    with pytest.raises(ValueError):
        estimators.partial_spearman(np.arange(50.0), np.full(50, np.nan), np.arange(50.0))


def test_evaluator_v2_canonical_and_guards():
    base = {"scope": "primary216", "operator": "mean_abs_delta", "adjust": "base_strength"}
    assert evaluator_v2.config_id(base) == evaluator_v2.config_id(dict(base))
    bad = evaluator_v2.evaluate({**base, "note": "x"})
    assert not bad["valid"] and "unknown" in bad["invalid_reasons"][0]
    ols = evaluator_v2.evaluate({"scope": "primary216", "operator": "ols_fe_coef_abs", "adjust": "base_strength"})
    assert not ols["valid"]  # OLS removed from scored space (anchor only)


def test_evaluator_v2_primary_reproduces_estimate():
    r = evaluator_v2.evaluate({"scope": "primary216", "operator": "mean_abs_delta", "adjust": "base_strength"})
    assert r["n_genes"] == 216 and abs(r["estimate"] - 0.0552525147) < 1e-9 and r["ci_width"] > 0
    # The legacy uncertainty diagnostic fails. Do not preserve the old false-valid test.
    assert not r["valid"] and "uncertainty inadequacy" in r["invalid_reasons"][0]


def test_gene_scope_membership_exact():
    s = json.loads(open("data/gene_scopes.json").read())
    assert s["counts"] == {"primary216": 216, "confirmatory207": 207, "panel242_reference_filtered": 242, "tmod1_alias208": 208}
    assert "TMOD" not in s["primary216"] and "TMOD" in s["tmod1_alias208"]
    assert "SQLE" not in s["primary216"]  # Tier-A excluded
    assert set(s["confirmatory207"]) <= set(s["primary216"])


def test_status_rules_total_function():
    empty = status_rules.direction_status([], [])
    assert empty["depth"] == "unexplored" and empty["promise"] == "unknown" and empty["recoverability"] == "na"
    conflict = [
        {"attempt_id": "a", "valid": False, "q": None, "outcome_class": "implementation_failure", "config_id": "c1", "seq": 1,
         "repair_citation": {"node_id": "a", "fix_class": "bug_fix"}},
        {"attempt_id": "b", "valid": False, "q": None, "outcome_class": "conceptual_failure", "config_id": "c2", "seq": 2},
        {"attempt_id": "c", "valid": False, "q": None, "outcome_class": "conceptual_failure", "config_id": "c3", "seq": 3},
    ]
    assert status_rules.direction_status(conflict, [0.5])["recoverability"] == "dead"  # precedence dead > recoverable
    ties = status_rules.direction_status([{"attempt_id": "x", "valid": True, "q": 0.5, "outcome_class": "success", "seq": 1}], [0.5, 0.5, 0.5])
    assert ties["promise"] == "unknown"  # IQR == 0


def test_history_index_bounded_at_scale():
    entries = [{"attempt_id": f"a{i:06d}", "direction_id": f"d{i % 300}"} for i in range(100_000)]
    h = history_index.HistoryIndex(entries)
    page = h.header_page(0)
    assert len(page["partitions"]) <= history_index.PAGE_MAX_ENTRIES
    assert all(len(h.partition_page(p["partition_id"])) <= 50 for p in page["partitions"][:5])
    assert h.lookup("a099999")["direction_id"] == "d99"
    assert h.locate("a000001")


def test_memo_arm_isolation_and_order_invariance():
    def run(order):
        m = memo.MemoStore()
        out = {}
        for arm in order:
            e, _ = m.get_or_create("summary", arm, "proto-v1", {"s": 1}, lambda a=arm: {"by": a})
            out[arm] = e["payload"]
        return out, m
    o1, m1 = run(["A", "B"]); o2, m2 = run(["B", "A"])
    assert o1 == o2 == {"A": {"by": "A"}, "B": {"by": "B"}}
    assert m1.arm_charges("A") == m2.arm_charges("A") == 1.0
    # cross-arm lookup is a miss by construction
    assert m1.get("summary", "B", "proto-v1", {"s": 2}) is None


def test_budget_outstanding_and_unbounded(tmp_path):
    import json as js
    (tmp_path / "config").mkdir(); (tmp_path / "ledger").mkdir()
    (tmp_path / "config/resources.json").write_text(js.dumps({"additional_api_spend_cap_usd": 1.0, "exploratory_timeout_s": 5, "research_memory_ceiling_bytes": 8589934592}))
    r1 = budget.reserve(tmp_path, {"n": "a"}, est_cost_usd=0.6)
    with pytest.raises(RuntimeError):
        budget.reserve(tmp_path, {"n": "b"}, est_cost_usd=0.6)  # concurrent counts
    budget.reconcile(tmp_path, r1["record_id"], {"actual_cost_usd": 0.5})
    budget.reserve(tmp_path, {"n": "c"}, est_cost_usd=0.5)  # reconciled frees the difference
    with pytest.raises(RuntimeError):
        budget.reserve(tmp_path, {"n": "d"}, est_cost_usd=float("inf"))


def test_lineage_cycle_and_version_mismatch():
    ex = {"a": {"attempt_id": "a", "parents": ["b"], "study_id": "S", "evaluator_version": "v2"},
          "b": {"attempt_id": "b", "parents": [], "study_id": "S", "evaluator_version": "v1"}}
    errs = lineage.validate_node({"attempt_id": "b", "origin": "refinement", "parents": ["a"], "study_id": "S", "evaluator_version": "v2"}, ex)
    assert any("cycle" in e for e in errs)
    errs2 = lineage.validate_node({"attempt_id": "c", "origin": "refinement", "parents": ["b"], "study_id": "S", "evaluator_version": "v2"}, ex)
    assert any("evaluator-version mismatch" in e for e in errs2)
