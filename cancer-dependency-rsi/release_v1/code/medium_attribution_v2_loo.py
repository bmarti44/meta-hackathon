#!/usr/bin/env python3
"""Leave-one-out robustness for the adherent organoid-medium contrast (n=9).
Refits A_adh dropping each adherent model in turn; reports slope A-on-D over
dev hits, median ratio, and how many medium-attributable flags survive
(recomputed with the LOO A). Norm scale (primary). Offset uncertainty is handled by the joint bootstrap (medium_attribution_v2_boot.py). (Was: LOO over the 27
dual-library models for the library offset's effect on D of hit genes.
"""
import json

import numpy as np
import pandas as pd

from medium_attribution import ROOT, library_offset, load_effects, load_screens, normalize
from medium_attribution import bh
from medium_attribution_v2 import ORG_LINEAGES, contrast2, flag_hits


def main():
    scr = load_screens()
    ge = load_effects(set(scr.index))
    scr = scr[scr.Lib.isin(["Avana", "Humagne-CD"]) & ~scr.reserved]
    ge = ge.loc[scr.index]
    ge = ge.astype("float64")
    ge = ge.loc[:, ge.notna().mean() > 0.99]
    scr = scr.loc[ge.index]
    off, _ = library_offset(ge, scr)
    ge = ge.fillna(ge.mean())
    base_avana = ge.loc[scr.Lib == "Avana"].copy()
    ge.loc[scr.Lib == "Avana"] = base_avana + off.fillna(0)
    scr = scr[scr.Lib.isin(["Avana", "Humagne-CD"]) & ~scr.reserved]
    ge = ge.loc[scr.index]
    ge = ge.astype("float64")
    fbs_adh = scr[(scr.cls == "FBS") & (scr.Fmt == "adherent")]
    med = ge.loc[fbs_adh.index].median()
    frac = (ge.loc[fbs_adh.index] < -0.5).mean()
    ess = list(frac[frac > 0.9].index)
    non = list(med[(med.abs() < 0.05) & (ge.loc[fbs_adh.index].std() < 0.15)].index)
    Y = normalize(ge, ess, non)
    Ym = Y.groupby(scr.ModelID).mean()
    meta = scr.groupby("ModelID").agg(cls=("cls", "first"), Fmt=("Fmt", "first"), lin=("lin", "first"))
    orglin = meta.lin.isin(ORG_LINEAGES)

    dev = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    hits = dev[dev.flag != "not_a_hit"]
    adh_models = meta[orglin & (meta.cls == "org") & (meta.Fmt == "adherent")].index.tolist()
    out = {"n_adherent_models": len(adh_models), "models": adh_models, "loo": {}}

    sel_all = meta[orglin & (((meta.cls == "org") & (meta.Fmt == "adherent"))
                             | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
    selF_all = meta[orglin & (meta.cls == "org")]
    base_cols = [c for c in hits.columns if c not in
                 ("flag", "flag_fdr", "ratio_A", "ratio_A_se", "ratio_A_lo", "ratio_A_hi",
                  "ratio_F", "ratio_F_se", "ratio_F_lo", "ratio_F_hi", "serumfree_support")]
    for drop in adh_models:
        sel = sel_all.drop(index=drop)
        beta, se, p, n1, n0, se_hc3 = contrast2(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
        selF = selF_all.drop(index=drop)
        bF, seF, pF, _n1, _n0, seF_hc3 = contrast2(Ym.loc[selF.index], (selF.Fmt == "dome").values, selF.lin)
        h = hits[base_cols].copy()
        h["A_adh"], h["A_adh_se"], h["A_adh_p"] = beta[h.index], se[h.index], p[h.index]
        h["A_adh_q"] = pd.Series(bh(p.fillna(1).values), p.index)[h.index]
        h["A_adh_se_hc3"] = se_hc3[h.index]
        h["F_dome"], h["F_dome_se"], h["F_dome_p"] = bF[h.index], seF[h.index], pF[h.index]
        h["F_dome_q"] = pd.Series(bh(pF.fillna(1).values), pF.index)[h.index]
        h["F_dome_se_hc3"] = seF_hc3[h.index]
        h = flag_hits(h)
        med_hits = hits[hits.flag == "medium_attributable"].index
        ratio = h.A_adh / h.D_org
        out["loo"][drop] = {
            "slope_Aloo_on_D_hits": float(np.polyfit(h.D_org, h.A_adh, 1)[0]),
            "median_ratio_hits": float(ratio.median()),
            "frac_medium_flags_retained": float((h.loc[med_hits, "flag"] == "medium_attributable").mean()),
            "n_medium_of_all_hits": int((h.flag == "medium_attributable").sum()),
        }
    slopes = [v["slope_Aloo_on_D_hits"] for v in out["loo"].values()]
    rets = [v["frac_medium_flags_retained"] for v in out["loo"].values()]
    out["summary"] = {"slope_min": min(slopes), "slope_max": max(slopes),
                      "flag_retention_min": min(rets), "flag_retention_median": float(np.median(rets))}
    (ROOT / "generations/medium_attribution_v2_loo.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
