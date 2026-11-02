"""C5 baseline: exact reproduction of S1 minipool environmental OLS.

Author design (DepMap-NextGen-Public @5c6f1e0ab23b, src/generate.py
gene_effect_linear_regression, called from run_linear_regression_analysis):
per-gene Gaussian GLM (~OLS) on the 18 screen-collapsed Chronos effects with
covariates Serum status + Growth Format + DepMap ID (model fixed effects)
+ Growth_Format:Serum_status interaction. Our full-rank reparameterization
(model dummies, no intercept) reproduces the three published environmental
coefficients to numerical precision on all 1000 genes.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "broad_figshare"
TERMS = {"Plastic": "C(Growth_Format)[T.Plastic]", "SerumFree": "C(Serum_status)[T.Serum-free]",
         "Interaction": "C(Growth_Format)[T.Plastic]:C(Serum_status)[T.Serum-free]"}


def fit() -> pd.DataFrame:
    meta = pd.read_csv(RAW / "minipool_screen_metadata.csv")
    eff = pd.read_csv(RAW / "minipool_chronos_gene_effects.csv").set_index("ScreenID").loc[meta.cell_line_name]
    plastic = (meta["Growth Format"] == "Plastic").astype(float).values
    sf = (meta["Serum status"] == "Serum-free").astype(float).values
    models = sorted(meta["DepMap ID"].unique())
    dummies = np.column_stack([(meta["DepMap ID"] == m).astype(float).values for m in models])
    X = np.column_stack([dummies, plastic, sf, plastic * sf])
    beta, *_ = np.linalg.lstsq(X, eff.values, rcond=None)
    return pd.DataFrame(beta, index=models + list(TERMS), columns=eff.columns)


def main() -> dict:
    ours = fit()
    pub = pd.read_csv(RAW / "minipool_regression_coefficients.csv", index_col=0)
    out = {"status": "C5 baseline reproduction: authors' minipool OLS (model fixed effects) reproduced from released Chronos matrix",
           "author_code": "broadinstitute/DepMap-NextGen-Public @5c6f1e0ab23b src/generate.py:gene_effect_linear_regression", "terms": {}}
    for ours_term, pub_term in TERMS.items():
        a, b = ours.loc[ours_term].astype(float), pub.loc[pub_term].astype(float)
        j = pd.DataFrame({"a": a, "b": b}).dropna()
        out["terms"][pub_term] = {"pearson": float(j.a.corr(j.b)), "max_abs_diff": float((j.a - j.b).abs().max()),
                                  "median_abs_diff": float((j.a - j.b).abs().median()), "n_genes": int(len(j))}
    (ROOT / "data" / "baseline_reproduction_ols.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
