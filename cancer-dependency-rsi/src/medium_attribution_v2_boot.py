#!/usr/bin/env python3
"""Joint bootstrap for medium attribution (Astra r1 #2, r2 H1).

Each replicate draws ONE model multiset used for BOTH library calibration
(weighted offset over dual-library models) and the analysis contrasts, so
calibration-analysis covariance from shared models is preserved.
Preprocessing mirrors medium_attribution_v2.main exactly (dev-only,
completeness filter, offset on unimputed data, imputation with fixed
pre-offset column means); ess/non reference sets are the main estimator's
(corrected-data) sets, frozen across replicates (documented simplification).
An identity replicate (each model once, point offset) must reproduce the
point-estimate flags on the hit set; the result is recorded in the JSON.
Norm scale, dev patients.
"""
import json

import numpy as np
import pandas as pd

from medium_attribution import ROOT, bh, library_offset, load_effects, load_screens, normalize
from medium_attribution_v2 import ORG_LINEAGES, contrast2, flag_hits

B = 150
SEED = 11


def weighted_offset(diffs_v, w):
    """Missingness-aware weighted mean of per-model library differences:
    nansum(w*d) / sum(w*isfinite(d)) per gene; zero where no valid pair.
    Matches pandas skipna mean in library_offset at w=1 (Astra r3)."""
    finite = np.isfinite(diffs_v)
    num = np.nansum(diffs_v * w[:, None], axis=0)
    den = (finite * w[:, None]).sum(axis=0)
    return np.where(den > 0, num / np.maximum(den, 1e-300), 0.0)


def build_tab(Ym, meta):
    orglin = meta.lin.isin(ORG_LINEAGES)
    res = {}
    sel = meta[orglin & (((meta.cls == "org") & (meta.Fmt == "dome"))
                         | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
    res["D_org"] = contrast2(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
    sel = meta[orglin & (((meta.cls == "org") & (meta.Fmt == "adherent"))
                         | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
    res["A_adh"] = contrast2(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
    sel = meta[orglin & (meta.cls == "org")]
    res["F_dome"] = contrast2(Ym.loc[sel.index], (sel.Fmt == "dome").values, sel.lin)
    sel = meta[(meta.lin == "CNS/Brain") & meta.cls.isin(["TSM", "FBS"])]
    res["S_tsm"] = contrast2(Ym.loc[sel.index], (sel.cls == "TSM").values, sel.lin)
    tab = pd.DataFrame({k: v[0] for k, v in res.items()})
    for k, v in res.items():
        tab[k + "_se"], tab[k + "_p"] = v[1], v[2]
        tab[k + "_q"] = bh(v[2].fillna(1).values)
        tab[k + "_se_hc3"] = v[5]
    return flag_hits(tab)


def main():
    rng = np.random.default_rng(SEED)
    scr = load_screens()
    ge = load_effects(set(scr.index))
    scr = scr[scr.Lib.isin(["Avana", "Humagne-CD"]) & ~scr.reserved]
    ge = ge.loc[scr.index].astype("float64")
    ge = ge.loc[:, ge.notna().mean() > 0.99]
    scr = scr.loc[ge.index]

    # point-estimate route, identical to medium_attribution_v2.main
    off_point, n_dual = library_offset(ge, scr)
    col_means = ge.mean()
    ge_point = ge.fillna(col_means)
    ge_point.loc[scr.Lib == "Avana"] = ge_point.loc[scr.Lib == "Avana"] + off_point.fillna(0)
    fbs_adh = scr[(scr.cls == "FBS") & (scr.Fmt == "adherent")]
    med = ge_point.loc[fbs_adh.index].median()
    frac = (ge_point.loc[fbs_adh.index] < -0.5).mean()
    ess = list(frac[frac > 0.9].index)
    non = list(med[(med.abs() < 0.05) & (ge_point.loc[fbs_adh.index].std() < 0.15)].index)
    rep_main = json.loads((ROOT / "generations/medium_attribution_v2.json").read_text())
    assert len(ess) == rep_main["n_common_essential"] and len(non) == rep_main["n_nonessential"], \
        (len(ess), len(non))

    # per-dual-model offset ingredients from UNIMPUTED ge (as in library_offset)
    f = scr[scr.cls == "FBS"]
    both = f.groupby("ModelID").Lib.agg(set)
    both = both[both.map(lambda s: {"Avana", "Humagne-CD"} <= s)].index.tolist()
    mh = ge.loc[f[(f.Lib == "Humagne-CD") & f.ModelID.isin(both)].index].groupby(scr.ModelID).mean().loc[both]
    ma = ge.loc[f[(f.Lib == "Avana") & f.ModelID.isin(both)].index].groupby(scr.ModelID).mean().loc[both]
    diffs = (mh - ma)
    avana_rows = (scr.Lib.values == "Avana")

    point = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    hits = point[point.flag != "not_a_hit"].index.tolist()
    meta_all = scr.groupby("ModelID").agg(cls=("cls", "first"), Fmt=("Fmt", "first"), lin=("lin", "first"))
    models = meta_all.index.values
    pos = {m: i for i, m in enumerate(models)}
    dual_pos = np.array([pos[m] for m in both])
    gev = ge.values
    col_means_v = col_means.values

    def run(draw_idx, off_v):
        g2 = gev.copy()
        nan_mask = np.isnan(g2)
        if nan_mask.any():
            g2[nan_mask] = np.broadcast_to(col_means_v, g2.shape)[nan_mask]
        g2[avana_rows] += np.nan_to_num(off_v)
        Y = normalize(pd.DataFrame(g2, index=ge.index, columns=ge.columns), ess, non)
        Ym_full = Y.groupby(scr.ModelID).mean()
        draw_models = models[draw_idx]
        Ym = Ym_full.loc[draw_models]
        Ym.index = range(len(draw_idx))
        meta = meta_all.loc[draw_models].reset_index(drop=True)
        return build_tab(Ym, meta).loc[hits]

    # identity replicate through the ACTUAL weighted-offset path (all-one
    # weights over dual models): must reproduce point flags on the hit set
    w_ident = np.zeros(len(models)); w_ident[dual_pos] = 1.0
    ident = run(np.arange(len(models)), weighted_offset(diffs.values, w_ident[dual_pos]))
    identity_ok = bool((ident.flag.values == point.loc[hits, "flag"].values).all())
    identity_detail = {"matches": identity_ok,
                       "n_mismatch": int((ident.flag.values != point.loc[hits, "flag"].values).sum())}
    print("identity check:", identity_detail, flush=True)

    slopes, fracs = [], []
    flag_counts = pd.Series(0.0, index=hits)
    diffs_v = diffs.values
    for b in range(B):
        draw_idx = rng.integers(0, len(models), len(models))
        counts = np.bincount(draw_idx, minlength=len(models))
        w = counts[dual_pos].astype(float)
        if w.sum() == 0:
            continue
        off_b = weighted_offset(diffs_v, w)
        h = run(draw_idx, off_b)
        slopes.append(float(np.polyfit(h.D_org, h.A_adh, 1)[0]))
        fracs.append(float((h.flag == "medium_attributable").mean()))
        flag_counts += (h.flag == "medium_attributable").astype(float)
        if (b + 1) % 25 == 0:
            print(f"rep {b+1}/{B} slope={slopes[-1]:.3f} frac={fracs[-1]:.3f}", flush=True)

    freq = (flag_counts / len(slopes)).rename("boot_medium_freq")
    freq.to_csv(ROOT / "generations/medium_attribution_v2_boot_freq.csv", float_format="%.4f")
    out = {"B": len(slopes), "seed": SEED, "n_dual_calibration_models": len(both),
           "identity_check": identity_detail,
           "ess_non_frozen_from_point_estimate": [len(ess), len(non)],
           "n_hits_fixed_from_point_estimate": len(hits),
           "slope_A_on_D": {"median": float(np.median(slopes)),
                            "ci95": [float(np.quantile(slopes, 0.025)), float(np.quantile(slopes, 0.975))]},
           "frac_medium_of_hits": {"median": float(np.median(fracs)),
                                   "ci95": [float(np.quantile(fracs, 0.025)), float(np.quantile(fracs, 0.975))]},
           "frac_hits_boot_freq_ge_0.9": float((freq >= 0.9).mean()),
           "frac_hits_boot_freq_ge_0.5": float((freq >= 0.5).mean())}
    (ROOT / "generations/medium_attribution_v2_boot.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
