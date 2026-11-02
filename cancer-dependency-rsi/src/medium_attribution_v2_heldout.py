#!/usr/bin/env python3
"""One-shot held-out confirmation of medium_attribution_v2 (reserved patients).
Contrasts use reserved-patient organoid-medium models vs DISJOINT reserved-patient
FBS-adherent baseline; library offset, gene filter, imputation and ess/non sets
all derived from development screens only (Astra r1 #5).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from medium_attribution import ROOT, library_offset, load_effects, load_screens, normalize
from medium_attribution_v2 import ORG_LINEAGES, contrast2


def main():
    scr = load_screens()
    ge = load_effects(set(scr.index))
    scr = scr[scr.Lib.isin(["Avana", "Humagne-CD"])]
    ge = ge.loc[scr.index]
    ge = ge.astype("float64")
    # Astra r1 #5: calibration/filtering/imputation from DEVELOPMENT screens only
    dev = scr[~scr.reserved]
    ged = ge.loc[dev.index]
    ged = ged.loc[:, ged.notna().mean() > 0.99]
    ge = ge[ged.columns]
    off, _ = library_offset(ged, dev.loc[ged.index])
    ge = ge.fillna(ged.mean())
    ge.loc[scr.Lib == "Avana"] = ge.loc[scr.Lib == "Avana"] + off.fillna(0)
    ge = ge.loc[scr.index]
    fbs_adh = scr[(scr.cls == "FBS") & (scr.Fmt == "adherent") & ~scr.reserved]
    med = ge.loc[fbs_adh.index].median()
    frac = (ge.loc[fbs_adh.index] < -0.5).mean()
    ess = list(frac[frac > 0.9].index)
    non = list(med[(med.abs() < 0.05) & (ge.loc[fbs_adh.index].std() < 0.15)].index)

    out = {}
    for scale in ("raw", "norm"):
        Y = ge if scale == "raw" else normalize(ge, ess, non)
        Ym = Y.groupby(scr.ModelID).mean()
        meta = scr.groupby("ModelID").agg(cls=("cls", "first"), Fmt=("Fmt", "first"),
                                           lin=("lin", "first"), reserved=("reserved", "first"))
        orglin = meta.lin.isin(ORG_LINEAGES)
        res = {}
        sel = meta[orglin & (((meta.cls == "org") & (meta.Fmt == "dome") & meta.reserved)
                             | ((meta.cls == "FBS") & (meta.Fmt == "adherent") & meta.reserved))]
        res["D_heldout"] = contrast2(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
        sel = meta[orglin & (((meta.cls == "org") & (meta.Fmt == "adherent") & meta.reserved)
                             | ((meta.cls == "FBS") & (meta.Fmt == "adherent") & meta.reserved))]
        res["A_heldout"] = contrast2(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
        tab = pd.DataFrame({k: v[0] for k, v in res.items()})
        for k, v in res.items():
            tab[k + "_se"] = v[1]
        tab.to_csv(ROOT / f"generations/medium_attribution_v2_heldout_{scale}.csv", float_format="%.6g")

        dev = pd.read_csv(ROOT / f"generations/medium_attribution_v2_{scale}.csv", index_col=0)
        j = dev.join(tab, how="inner")
        s = {"n": {k: [v[3], v[4]] for k, v in res.items()},
             "corr_D_dev_heldout_all": float(j.D_org.corr(j.D_heldout))}
        for flag in ("medium_attributable", "unresolved"):
            h = j[j.flag == flag]
            s[flag] = {"n": int(len(h)), "corr_D": float(h.D_org.corr(h.D_heldout)) if len(h) > 2 else None,
                       "slope_Dheld_on_Ddev": float(np.polyfit(h.D_org, h.D_heldout, 1)[0]) if len(h) > 2 else None,
                       "same_sign_frac": float((np.sign(h.D_heldout) == np.sign(h.D_org)).mean()) if len(h) else None,
                       "slope_Aheld_on_Ddev": float(np.polyfit(h.D_org, h.A_heldout, 1)[0]) if len(h) > 2 else None}
        out[scale] = s
    (ROOT / "generations/medium_attribution_v2_heldout.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
