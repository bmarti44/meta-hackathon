"""Exploratory precision feasibility v2 (regenerates data/precision_feasibility_v2.json).

Corrections vs v1 (G1 review r2): lability = model-equal-weighted mean of
|within-pair deltas| (no cancellation inside ACH-003040); partial Spearman
defined EXACTLY as Pearson correlation of rank residuals; eligibility adds
AdherentN>=400 (variable reference support); TMOD excluded from primary
(unadjudicated alias TMOD1/7111; sensitivity includes it). EXPLORATORY ONLY.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent.parent
rng = np.random.default_rng(20261028)


def lability(d: pd.DataFrame, model_draw: list[str] | None = None) -> pd.Series:
    by_model: dict[str, list[int]] = {}
    for i, c in enumerate(d.columns):
        by_model.setdefault(c.split("|")[0], []).append(i)
    models = model_draw or sorted(by_model)
    per = [d.iloc[:, by_model[m]].abs().mean(axis=1) for m in models]  # mean |delta| within model
    return pd.DataFrame(per).T.mean(axis=1)  # equal weight per model (draw counts multiplicities)


def partial_spearman(y: np.ndarray, x: np.ndarray, z: np.ndarray) -> float:
    """Pearson correlation of rank residuals (exact operation, locked here)."""
    def resid(a, b):
        ra, rb = pd.Series(a).rank().values, pd.Series(b).rank().values
        X = np.column_stack([np.ones_like(rb), rb])
        beta, *_ = np.linalg.lstsq(X, ra, rcond=None)
        return ra - X @ beta
    return float(np.corrcoef(resid(y, z), resid(x, z))[0, 1])


def main() -> dict:
    d = pd.read_csv(ROOT / "data" / "paired_deltas_format.csv", index_col=0)
    tests = pd.read_csv(ROOT / "data/raw/broad_figshare/organoids_vs_2d_gene_dependency_tests_full.csv")
    tests["symbol"] = tests.Dependency.str.replace(r"\s*\(\d+\)$", "", regex=True)
    excl = json.loads((ROOT / "data/selection_exclusions.json").read_text())
    lib = pd.read_csv(ROOT / "data/raw/broad_figshare/minipool_library_composition.csv")
    panel = set(lib.loc[lib["All test genes"] == True, "Gene"])  # noqa: E712
    tidx = tests.set_index("symbol")
    base_elig = sorted(g for g in panel - set(excl["tierA_direct_outliers_excluded"]) if g in tidx.index and g in d.index)
    primary = [g for g in base_elig if tidx.loc[g, "AdherentN"] >= 400 and tidx.loc[g, "OrganoidsN"] >= 90]
    low_n = sorted(set(base_elig) - set(primary))
    out = {"status": "EXPLORATORY feasibility v2; not confirmatory", "primary_genes_n": len(primary),
           "excluded_low_reference_N": low_n, "tmod": "excluded primary (alias TMOD1/7111 unadjudicated from released guide data); sensitivity only"}
    for label, genes in [("primary", primary), ("sensitivity_plus_TMOD1_alias", primary + (["TMOD"] if "TMOD" in d.index else []))]:
        gg = [g for g in genes if (g in tidx.index or g == "TMOD")]
        L = lability(d).loc[[g for g in gg if g in d.index]]
        rows = []
        for g in L.index:
            src = "TMOD1" if g == "TMOD" else g
            if src in tidx.index:
                rows.append((g, L[g], abs(tidx.loc[src, "MeanDifference"]), abs(tidx.loc[src, "AdherentMean"])))
        df = pd.DataFrame(rows, columns=["gene", "Lval", "Tval", "base"]).set_index("gene")
        rho = float(spearmanr(df.Lval, df.Tval).statistic)
        prho = partial_spearman(df.Tval.values, df.Lval.values, df.base.values)
        models = sorted({c.split("|")[0] for c in d.columns})
        boots = []
        for _ in range(2000):
            Lb = lability(d, list(rng.choice(models, size=len(models), replace=True))).loc[df.index]
            boots.append(partial_spearman(df.Tval.values, Lb.values, df.base.values))
        ci = np.percentile([b for b in boots if np.isfinite(b)], [2.5, 97.5]).tolist()
        out[label] = {"n": int(len(df)), "raw_spearman": rho, "partial_spearman_rankresid_pearson": prho,
                      "partial_model_bootstrap_ci95": ci, "ci_width": float(ci[1] - ci[0])}
    out["caveats"] = ("Model bootstrap (6 format models) captures environmental-side uncertainty only; gene/pathway dependence and "
                      "transfer-table sampling uncertainty widen true CIs. Broad table = development/descriptive (selection source, Chronos pretraining). "
                      "External precision (148 organoids/144 donors) computed at Lock 1 from schema + donor counts, not outcomes.")
    (ROOT / "data" / "precision_feasibility_v2.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1)[:1800])
    return out


if __name__ == "__main__":
    main()
