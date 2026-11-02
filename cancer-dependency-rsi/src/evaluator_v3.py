"""UNAPPROVED pre-Lock1 safety draft. Not admissible for policy optimization.

Retired v2 is retained byte-for-byte; all v2 scores are invalidated for policy use.

Changes vs v1 (sol-high G2 review, 54/100):
- OLS coefficient operator REMOVED from scored space (anchor only, baseline_ols).
- Degenerate/constant/nonfinite inputs and rank residuals are INVALID.
- Calibration = Freedman-Lane synthetic-null coverage of the config's own
  model-bootstrap CI for true 0 (not permuted-mean proximity).
- Canonical config: only {scope, operator, adjust} allowed; unknown keys
  rejected; config_id hashes only canonical scientific fields.
- Gene scopes from frozen data/gene_scopes.json (exact membership).
- base_plus_organoid_mean = SIMULTANEOUS two-covariate rank adjustment.
- Bootstrap failure rate recorded; >10% failed replicates => invalid.
Quality q in [0,1]: 0.4*calibration + 0.35*precision + 0.25*stability for valid
configs; never effect size, p-value, or discovery count. Opposite-direction
valid results are never invalid.
"""
from __future__ import annotations

import hashlib
import json

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

import estimators

EVALUATOR_VERSION = "evaluator_v3_draft"
ALLOWED_KEYS = {"scope", "operator", "adjust"}
LEGAL_SCOPES = {"primary216", "confirmatory207", "panel242_reference_filtered", "tmod1_alias208"}
LEGAL_OPERATORS = {"mean_abs_delta", "abs_mean_delta", "max_abs_delta"}
LEGAL_ADJUST = {"none", "base_strength", "base_plus_organoid_mean"}
N_BOOT, N_NULL, N_NULL_BOOT = 300, 25, 60
MAX_BOOT_FAIL_FRAC = 0.10


def canonical(config: dict) -> dict:
    return {k: config[k] for k in sorted(ALLOWED_KEYS) if k in config}


def config_id(config: dict) -> str:
    return hashlib.sha256(json.dumps(canonical(config), sort_keys=True).encode()).hexdigest()[:16]


def _invalid(rec: dict, reason: str) -> dict:
    rec.update({"valid": False, "invalid_reasons": rec["invalid_reasons"] + [reason],
                "q": None, "outcome_class": "invalid_result"})
    return rec


def evaluate(config: dict, seed: int = 20261028) -> dict:
    rng = np.random.default_rng(seed)
    rec: dict = {"config": canonical(config), "config_id": config_id(config),
                 "evaluator_version": EVALUATOR_VERSION, "valid": True, "invalid_reasons": [],
                 "admissible_for_policy": False, "calibration_status": "legacy_unvalidated"}
    unknown = set(config) - ALLOWED_KEYS - {"uses_non_layerA"}
    if unknown:
        return _invalid(rec, f"unknown config keys rejected: {sorted(unknown)}")
    if config.get("uses_non_layerA"):
        return _invalid(rec, "leakage: non-Layer-A input in development evaluator")
    if config.get("scope") not in LEGAL_SCOPES:
        return _invalid(rec, "illegal gene scope")
    if config.get("operator") not in LEGAL_OPERATORS:
        return _invalid(rec, "illegal lability operator")
    if config.get("adjust") not in LEGAL_ADJUST:
        return _invalid(rec, "illegal adjustment set")

    meta, eff, tidx = estimators.load_dev()
    deltas = estimators.format_pairs(meta, eff)
    scopes = json.loads((estimators.ROOT / "data/gene_scopes.json").read_text())
    alias = scopes.get("alias_map", {})
    genes = scopes[config["scope"]]
    if len(set(genes)) != len(genes) or deltas.index.has_duplicates or tidx.index.has_duplicates:
        return _invalid(rec, "duplicate frozen or source gene membership")
    missing = [g for g in genes if g not in deltas.index or alias.get(g, g) not in tidx.index]
    if missing:
        return _invalid(rec, f"missing frozen scope members: {missing}")
    if len(genes) < 50:
        return _invalid(rec, "support: n<50 after frozen scope join")

    by_model: dict[str, list[int]] = {}
    for i, c in enumerate(deltas.columns):
        by_model.setdefault(c.split("|")[0], []).append(i)
    models = sorted(by_model)

    def compute_L(draw: list[str] | None) -> pd.Series:
        ms = draw or models
        if config["operator"] == "mean_abs_delta":
            per = [deltas.iloc[:, by_model[m]].abs().mean(axis=1) for m in ms]
        elif config["operator"] == "abs_mean_delta":
            return pd.DataFrame([deltas.iloc[:, by_model[m]].mean(axis=1) for m in ms]).T.mean(axis=1).abs()
        else:  # max_abs_delta
            per = [deltas.iloc[:, by_model[m]].abs().max(axis=1) for m in ms]
        return pd.DataFrame(per).T.mean(axis=1)

    def ref(g: str, col: str) -> float:
        return float(tidx.loc[alias.get(g, g), col])

    T = np.array([abs(ref(g, "MeanDifference")) for g in genes])
    base = np.array([abs(ref(g, "AdherentMean")) for g in genes])
    if config["adjust"] == "none":
        Z = None
    elif config["adjust"] == "base_strength":
        Z = base.reshape(-1, 1)
    else:
        org = np.array([abs(ref(g, "OrganoidsMean")) for g in genes])
        Z = np.column_stack([base, org])

    def est_fn(Lv: np.ndarray, Tv: np.ndarray) -> float:
        if not np.isfinite(Lv).all() or not np.isfinite(Tv).all() or (Z is not None and not np.isfinite(Z).all()):
            raise ValueError("nonfinite original estimator inputs")
        if Z is None:
            if np.std(Lv) < 1e-12 or np.std(Tv) < 1e-12:
                raise ValueError("degenerate input")
            return float(spearmanr(Lv, Tv).statistic)
        return estimators.partial_spearman(Tv, Lv, Z)

    try:
        L = compute_L(None).loc[genes]
        if not np.isfinite(L.values).all() or np.std(L.values) < 1e-12:
            return _invalid(rec, "degenerate lability (constant/nonfinite)")
        est = est_fn(L.values, T)
    except ValueError as e:
        return _invalid(rec, f"degenerate estimator: {e}")
    if not np.isfinite(est):
        return _invalid(rec, "nonfinite estimate")

    def boot_ci(Tv: np.ndarray, n_boot: int, rng_: np.random.Generator) -> tuple[np.ndarray, float]:
        boots, fails = [], 0
        for _ in range(n_boot):
            draw = list(rng_.choice(models, size=len(models), replace=True))
            try:
                value = est_fn(compute_L(draw).loc[genes].values, Tv)
                if not np.isfinite(value):
                    raise ValueError("nonfinite bootstrap statistic")
                boots.append(value)
            except ValueError:
                fails += 1
        boots = np.array([b for b in boots if np.isfinite(b)])
        if len(boots) < 20:
            return np.array([np.nan, np.nan]), 1.0
        return np.percentile(boots, [2.5, 97.5]), fails / n_boot

    ci, fail_frac = boot_ci(T, N_BOOT, rng)
    if fail_frac > MAX_BOOT_FAIL_FRAC or not np.isfinite(ci).all():
        return _invalid(rec, f"bootstrap failure rate {fail_frac:.2f} or nonfinite CI")
    width = float(ci[1] - ci[0])
    if width <= 0:
        return _invalid(rec, "zero-width CI (artificial sharpness)")

    lomo = []
    for m in models:
        try:
            lomo.append(est_fn(compute_L([x for x in models if x != m]).loc[genes].values, T))
        except ValueError:
            return _invalid(rec, f"degenerate under leave-one-model-out {m}")
    lomo_range = float(np.max(lomo) - np.min(lomo))

    # Freedman-Lane synthetic-null coverage calibration:
    # rank-residualize T on Z, permute residuals, reconstruct null T (true partial rho = 0).
    if Z is None:
        def null_T(rng_: np.random.Generator) -> np.ndarray:
            return rng_.permutation(T)
    else:
        rT = estimators._rank_resid(T, Z)
        fit = pd.Series(T).rank().values.astype(float) - rT
        def null_T(rng_: np.random.Generator) -> np.ndarray:
            return fit + rng_.permutation(rT)
    covered = 0
    for _ in range(N_NULL):
        ci_n, ff = boot_ci(null_T(rng), N_NULL_BOOT, rng)
        if ff <= MAX_BOOT_FAIL_FRAC and np.isfinite(ci_n).all() and ci_n[0] <= 0.0 <= ci_n[1]:
            covered += 1
    coverage = covered / N_NULL
    # Pre-Lock1 safety fix only. This legacy permutation diagnostic is not a
    # justified biological coverage target. No policy run is admissible until
    # the xhigh design consultation and G2-approved replacement are frozen.
    rec.update({"estimate": float(est), "null_coverage": coverage, "ci_width": width,
                "n_genes": len(genes), "lomo_range": lomo_range})
    if coverage < 0.90:
        return _invalid(rec, "uncertainty inadequacy: legacy null coverage <0.90; G2 redesign required")
    calib = float(max(0.0, 1.0 - abs(coverage - 0.95) / 0.25))
    precision = float(1.0 - min(1.0, width / 0.5))
    stability = float(1.0 - min(1.0, lomo_range / 0.3))
    q = float(0.4 * calib + 0.35 * precision + 0.25 * stability)
    rec.update({"q": q, "estimate": float(est), "ci95_model_bootstrap": ci.tolist(), "ci_width": width,
                "boot_fail_frac": fail_frac, "lomo_range": lomo_range, "null_coverage": coverage,
                "n_genes": int(len(genes)), "genes_sha256": hashlib.sha256(",".join(genes).encode()).hexdigest(),
                "components": {"calibration": calib, "precision": precision, "stability": stability},
                "outcome_class": "success"})
    return rec
