"""Phase-1 identifiability audit v2 — fully regenerates every reported number.

Corrections vs v1 (sol-high G1 review): contrast-specific DISTINCT model
counts (medium 4, format 6; ACH-003040 contributes 2 pairs each); sign-flip
rates reported for test genes AND 750 controls with NO heterogeneity claim
(sign flips at control rates prove little — magnitudes are the evidence);
direction check vs published OLS coefficients computed here, not pasted.
Descriptive audit only — no adaptive search, no claims.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "broad_figshare"


def paired_deltas(meta, eff, contrast):
    rows = {}
    if contrast == "medium":  # OPAC - RPMI/FBS within model+format (treatment BUNDLE: full medium change)
        groups, key, a, b = meta.groupby(["DepMap ID", "Growth Format"]), "Culture medium", "OPAC", "RPMI/FBS"
    else:  # Dome - Plastic within model+medium (BUNDLE: geometry + Matrigel matrix exposure)
        groups, key, a, b = meta.groupby(["DepMap ID", "Culture medium"]), "Growth Format", "Dome", "Plastic"
    for gkey, g in groups:
        ga, gb = g[g[key] == a], g[g[key] == b]
        if len(ga) == 1 and len(gb) == 1:
            rows[f"{gkey[0]}|{gkey[1]}"] = eff.loc[ga.cell_line_name.iloc[0]] - eff.loc[gb.cell_line_name.iloc[0]]
    return pd.DataFrame(rows)


def _stats(x: pd.DataFrame) -> dict:
    return {
        "both_signs_frac": float(((x > 0).any(axis=1) & (x < 0).any(axis=1)).mean()),
        "note": "sign-flip rate is DESCRIPTIVE ONLY (controls flip at similar rates; not evidence of biological heterogeneity)",
        "median_abs_delta": float(x.abs().median().median()),
        "mean_abs_mean_delta": float(x.mean(axis=1).abs().mean()),
        "frac_genes_abs_mean_delta_gt_0.5": float((x.mean(axis=1).abs() > 0.5).mean()),
    }


def main() -> dict:
    meta = pd.read_csv(RAW / "minipool_screen_metadata.csv")
    eff = pd.read_csv(RAW / "minipool_chronos_gene_effects.csv").set_index("ScreenID")
    lib = pd.read_csv(RAW / "minipool_library_composition.csv")
    test = set(lib.loc[lib["All test genes"] == True, "Gene"])  # noqa: E712
    out: dict = {"audit_version": 2, "n_screens": int(len(meta)), "n_models_total": int(meta["DepMap ID"].nunique()),
                 "models": sorted(meta["DepMap ID"].unique()), "n_test_genes": len(test),
                 "treatment_bundles": {"medium": "OPAC (serum-free defined) vs RPMI/FBS — full medium-composition bundle, NOT isolated serum",
                                        "format": "Matrigel dome vs plastic — geometry + matrix-exposure bundle, NOT isolated geometry"}}
    coef = pd.read_csv(RAW / "minipool_regression_coefficients.csv", index_col=0)
    pub = {"format": -coef.loc["C(Growth_Format)[T.Plastic]"], "medium": coef.loc["C(Serum_status)[T.Serum-free]"]}
    for contrast in ("medium", "format"):
        d = paired_deltas(meta, eff, contrast)
        d.to_csv(ROOT / "data" / f"paired_deltas_{contrast}.csv")
        distinct = sorted({c.split("|")[0] for c in d.columns})
        entry = {"n_pairs": int(d.shape[1]), "pair_keys": list(d.columns),
                 "n_distinct_models": len(distinct), "distinct_models": distinct,
                 "donors": "UNRESOLVED (crosswalk open; do not equate models with independent donors)",
                 "double_counted_model": "ACH-003040 contributes 2 pairs; equal-pair weighting overweights it — Lock 1 must define model-level weighting",
                 "test250": _stats(d.loc[d.index.intersection(test)]),
                 "controls750": _stats(d.loc[~d.index.isin(test)])}
        ours = d.mean(axis=1)
        j = pd.DataFrame({"ours": ours, "pub": pub[contrast]}).dropna()
        jt = j.loc[j.index.intersection(test)]
        entry["direction_check_vs_published_OLS"] = {
            "test250_pearson": float(jt.ours.corr(jt.pub)), "test250_spearman": float(jt.ours.corr(jt.pub, method="spearman")),
            "test250_sign_agreement": float((np.sign(jt.ours) == np.sign(jt.pub)).mean()),
            "all1000_pearson": float(j.ours.corr(j.pub)),
            "note": "format sign flipped (ours Dome-Plastic vs published Plastic indicator). C5 precursor only."}
        out[contrast] = entry
    out["retracted_v1_claim"] = ("v1 'heterogeneity dominates / averages near-uninterpretable' RETRACTED: control genes flip signs at "
                                  "equal rates. Evidence must come from magnitudes vs controls/technical variation.")
    (ROOT / "data" / "identifiability_audit.json").write_text(json.dumps(out, indent=2))
    print(json.dumps({k: out[k] for k in ("medium", "format")}, indent=1)[:2200])
    return out


if __name__ == "__main__":
    main()
