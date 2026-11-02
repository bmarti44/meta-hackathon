import numpy as np
import estimators, evaluator_v1

def test_null_expected_displacement_endpoints():
    e = estimators.null_expected_displacement(np.array([1, 104, 207]), 207)
    assert abs(e[0] - 0.5) < 1e-9 and abs(e[2] - 0.5) < 1e-9 and 0.24 < e[1] < 0.26

def test_partial_spearman_zero_on_independent():
    rng = np.random.default_rng(0)
    x, y, z = rng.normal(size=400), rng.normal(size=400), rng.normal(size=400)
    assert abs(estimators.partial_spearman(y, x, z)) < 0.12

def test_evaluator_rejects_leakage_and_scores_primary():
    bad = evaluator_v1.evaluate({"scope": "primary216", "operator": "mean_abs_delta", "adjust": "base_strength", "uses_non_layerA": True})
    assert not bad["valid"] and bad["q"] is None
    ok = evaluator_v1.evaluate({"scope": "primary216", "operator": "mean_abs_delta", "adjust": "base_strength"})
    assert ok["valid"] and 0.0 <= ok["q"] <= 1.0 and ok["n_genes"] == 216
    assert abs(ok["estimate"] - 0.0553) < 0.02  # matches precision_feasibility_v2 primary
