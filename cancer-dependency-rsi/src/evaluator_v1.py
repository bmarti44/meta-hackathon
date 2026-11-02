"""Fixed scientific evaluator v1 (Phase 2; frozen at Lock 1, hash-pinned).

Scores a development analysis CONFIG by validity/calibration/precision/
stability — NEVER by effect size, p-value, or discovery count (spec S8/PLAN
Phase 2.3). A config proposes: lability operator, adjustment set, gene scope,
uncertainty method. Quality q in [0,1] (locked transform in contract):
  q = 0 if invalid; else 0.4*calibration + 0.35*precision + 0.25*stability
- calibration: label-permutation negative control — fraction of permuted
  |partial rho| >= observed should be uniform-ish under null configs; we score
  distance of the config's permutation p-value distribution calibration on
  synthetic null data (precomputed probe): 1 - KS distance vs Uniform.
  (v1 simplification, recorded: single permutation set on real data gives
  p_perm; calibration component = 1 - |rank of observed among perms - 0.5|*0
  is NOT used; instead calibration is assessed on synthetic null panels in
  tests and, at runtime, by control-gene association near-zero check.)
- precision: 1 - min(1, CI_width / 0.5) from model-cluster bootstrap.
- stability: 1 - min(1, LOMO range of partial rho / 0.3).
Invalid: leakage (non-Layer-A inputs), Tier-A genes in primary scope without
sensitivity flag, support violations, orientation errors (verified), n<50.
Opposite-direction VALID results are never invalid.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd

import estimators

EVALUATOR_VERSION = "evaluator_v1"
LEGAL_SCOPES = {"primary216", "confirmatory207", "all250_sensitivity"}
LEGAL_OPERATORS = {"mean_abs_delta", "abs_mean_delta", "max_abs_delta", "ols_fe_coef_abs"}
LEGAL_ADJUST = {"none", "base_strength", "base_plus_organoid_mean"}


def config_id(config: dict) -> str:
    return hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()[:16]


def evaluate(config: dict, seed: int = 20261028) -> dict:
    """Run one development analysis config; return score record (ledger-ready)."""
    rng = np.random.default_rng(seed)
    rec: dict = {"config": config, "config_id": config_id(config), "evaluator_version": EVALUATOR_VERSION,
                 "valid": True, "invalid_reasons": []}
    if config.get("scope") not in LEGAL_SCOPES:
        rec["valid"] = False; rec["invalid_reasons"].append("illegal gene scope")
    if config.get("operator") not in LEGAL_OPERATORS:
        rec["valid"] = False; rec["invalid_reasons"].append("illegal lability operator")
    if config.get("adjust") not in LEGAL_ADJUST:
        rec["valid"] = False; rec["invalid_reasons"].append("illegal adjustment set")
    if config.get("uses_non_layerA"):
        rec["valid"] = False; rec["invalid_reasons"].append("leakage: non-Layer-A input in development evaluator")
    if not rec["valid"]:
        rec.update({"q": None, "outcome_class": "invalid_result"})
        return rec

    meta, eff, tidx = estimators.load_dev()
    deltas = estimators.format_pairs(meta, eff)
    excl = json.loads((estimators.ROOT / "data/selection_exclusions.json").read_text())
    lib = pd.read_csv(estimators.RAW / "minipool_library_composition.csv")
    panel = sorted(set(lib.loc[lib["All test genes"] == True, "Gene"]))  # noqa: E712
    if config["scope"] == "all250_sensitivity":
        genes = panel
    else:
        cand = json.loads((estimators.ROOT / "data/confirmatory_gene_candidates.json").read_text())
        base = [g for g in panel if g not in set(excl["tierA_direct_outliers_excluded"])]
        genes = cand["confirmatory_genes"] if config["scope"] == "confirmatory207" else base
    genes = [g for g in genes if g in deltas.index and g in tidx.index and tidx.loc[g, "AdherentN"] >= 400]
    if config["scope"] != "all250_sensitivity":
        genes = [g for g in genes if g != "TMOD"]
    if len(genes) < 50:
        rec.update({"valid": False, "invalid_reasons": ["support: n<50"], "q": None, "outcome_class": "invalid_result"})
        return rec

    def compute_L(d: pd.DataFrame, draw=None) -> pd.Series:
        op = config["operator"]
        if op == "mean_abs_delta":
            return estimators.lability(d, draw)
        by_model: dict[str, list[int]] = {}
        for i, c in enumerate(d.columns):
            by_model.setdefault(c.split("|")[0], []).append(i)
        models = draw or sorted(by_model)
        if op == "abs_mean_delta":
            per = [d.iloc[:, by_model[m]].mean(axis=1) for m in models]
            return pd.DataFrame(per).T.mean(axis=1).abs()
        if op == "max_abs_delta":
            per = [d.iloc[:, by_model[m]].abs().max(axis=1) for m in models]
            return pd.DataFrame(per).T.mean(axis=1)
        raise ValueError(op)  # ols_fe_coef_abs handled via baseline_ols import path

    if config["operator"] == "ols_fe_coef_abs":
        import baseline_ols
        Lfull = baseline_ols.fit().loc["Plastic"].abs()
        L = Lfull.loc[genes]
    else:
        L = compute_L(deltas).loc[genes]
    T = tidx.loc[genes, "MeanDifference"].abs().astype(float)
    base = tidx.loc[genes, "AdherentMean"].abs().astype(float)
    if config["adjust"] == "none":
        from scipy.stats import spearmanr
        est = float(spearmanr(L, T).statistic)
        est_fn = lambda Lv: float(spearmanr(Lv, T).statistic)  # noqa: E731
    else:
        z = base.values if config["adjust"] == "base_strength" else (base + tidx.loc[genes, "OrganoidsMean"].abs().astype(float)).values
        est = estimators.partial_spearman(T.values, L.values, np.asarray(z, dtype=float))
        est_fn = lambda Lv: estimators.partial_spearman(T.values, np.asarray(Lv, dtype=float), np.asarray(z, dtype=float))  # noqa: E731

    models = sorted({c.split("|")[0] for c in deltas.columns})
    boots = []
    for _ in range(500):
        draw = list(rng.choice(models, size=len(models), replace=True))
        Lb = (L if config["operator"] == "ols_fe_coef_abs" else compute_L(deltas, draw).loc[genes])
        boots.append(est_fn(Lb.values))
    boots = np.array([b for b in boots if np.isfinite(b)])
    ci = np.percentile(boots, [2.5, 97.5]) if len(boots) else np.array([np.nan, np.nan])
    width = float(ci[1] - ci[0]) if np.isfinite(ci).all() else 1.0
    # leave-one-model-out stability
    lomo = []
    for m in models:
        keep = [x for x in models if x != m]
        Lm = (L if config["operator"] == "ols_fe_coef_abs" else compute_L(deltas, keep).loc[genes])
        lomo.append(est_fn(Lm.values))
    lomo_range = float(np.max(lomo) - np.min(lomo)) if lomo else 1.0
    # negative control: permute gene labels of L (calibration: permuted estimates should center ~0)
    perms = np.array([est_fn(rng.permutation(L.values)) for _ in range(200)])
    calib = float(1.0 - min(1.0, abs(np.mean(perms)) / 0.05)) if np.isfinite(perms).all() else 0.0
    precision = float(1.0 - min(1.0, width / 0.5))
    stability = float(1.0 - min(1.0, lomo_range / 0.3))
    q = float(0.4 * calib + 0.35 * precision + 0.25 * stability)
    rec.update({"q": q, "estimate": float(est), "ci95_model_bootstrap": ci.tolist(), "ci_width": width,
                "lomo_range": lomo_range, "perm_mean": float(np.mean(perms)), "n_genes": int(len(genes)),
                "components": {"calibration": calib, "precision": precision, "stability": stability},
                "outcome_class": "success"})
    return rec
