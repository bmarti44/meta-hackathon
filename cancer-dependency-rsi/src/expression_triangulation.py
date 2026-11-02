#!/usr/bin/env python3
"""Expression triangulation: does the transcriptome mirror medium attribution?
Omics TPM (logp1) profiles mapped to model conditions via OmicsProfiles.
Contrasts mirror medium_attribution_v2 (dev patients, organoid lineages).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from medium_attribution import ROOT, load_screens
from medium_attribution_v2 import HEME, MEV, ORG_LINEAGES, contrast2

DL = Path.home() / "Downloads"
FASYN = ["FASN", "ACLY", "ACACA", "SCD", "ACSS2", "MLYCD"]


def main():
    out = {}
    prof = pd.read_csv(DL / "OmicsProfiles.csv", dtype=str).fillna("")
    out["omics_profiles_columns"] = list(prof.columns)
    ex_head = pd.read_csv(DL / "OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv", nrows=2, index_col=0)
    out["expression_index_example"] = str(ex_head.index[0])
    out["expression_col_example"] = str(ex_head.columns[0])

    scr = load_screens()
    scr = scr[scr.Lib.isin(["Avana", "Humagne-CD"]) & ~scr.reserved]
    mod_meta = scr.groupby("ModelID").agg(cls=("cls", "first"), Fmt=("Fmt", "first"), lin=("lin", "first"))
    mcid = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("").set_index("ModelConditionID")

    ex = pd.read_csv(DL / "OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv", index_col=0)
    embedded = {c: ex.pop(c) for c in list(ex.columns) if c in
                ("SequencingID", "ModelConditionID", "ModelID", "IsDefaultEntryForMC", "IsDefaultEntryForModel")}
    ex = ex.apply(pd.to_numeric, errors="coerce").astype(np.float32)
    ex.columns = [str(c).split(" (")[0] for c in ex.columns]
    ex = ex.loc[:, ~ex.columns.duplicated()]
    if "ModelID" in embedded:
        mcid_map = embedded.get("ModelConditionID")
        meta_emb = pd.DataFrame({"ModelID": embedded["ModelID"].values}, index=ex.index)
        if mcid_map is not None:
            mcids = pd.Series(mcid_map.values, index=ex.index)
            meta_emb["Fmt"] = [str(mcid.CellFormat.get(m, "")).strip().lower() for m in mcids]
            form = pd.Series([str(mcid.FormulationID.get(m, "")) for m in mcids], index=ex.index)
            meta_emb["cls"] = np.select([form.str.contains("OPAC|Organoid"), form.str.contains("Tumor Stem"),
                                         form.str.contains("FBS")], ["org", "TSM", "FBS"], "other")
            prof = prof.iloc[0:0]  # skip profile mapping below
            meta = meta_emb
            out["mapping"] = "embedded_condition_columns"

    # map expression rows to (ModelID, cls, Fmt): row may be ProfileID or ModelID
    pid_col = [c for c in prof.columns if "Profile" in c]
    mid_col = [c for c in prof.columns if c in ("ModelID", "ModelId")]
    mcid_col = [c for c in prof.columns if "ModelCondition" in c]
    if "mapping" not in out:
        meta = None
    else:
        pid_col = []
    if pid_col and mid_col and len(set(ex.index) & set(prof[pid_col[0]])) > 100:
        p = prof.set_index(pid_col[0])
        meta = pd.DataFrame({"ModelID": ex.index.map(p[mid_col[0]])})
        if mcid_col:
            mc = ex.index.map(p[mcid_col[0]])
            meta["Fmt"] = [str(mcid.CellFormat.get(m, "")).strip().lower() for m in mc]
            form = [str(mcid.FormulationID.get(m, "")) for m in mc]
            meta["cls"] = np.select([pd.Series(form).str.contains("OPAC|Organoid"),
                                     pd.Series(form).str.contains("Tumor Stem"),
                                     pd.Series(form).str.contains("FBS")], ["org", "TSM", "FBS"], "other")
    if meta is None or meta.ModelID.isna().mean() > 0.5:
        meta = pd.DataFrame({"ModelID": ex.index})
        meta["cls"] = meta.ModelID.map(mod_meta.cls)
        meta["Fmt"] = meta.ModelID.map(mod_meta.Fmt)
        out["mapping"] = "model_level_fallback"
    elif out.get("mapping") != "embedded_condition_columns":
        out["mapping"] = "profile_to_condition"
    meta["lin"] = meta.ModelID.map(mod_meta.lin)
    keep = meta.ModelID.isin(mod_meta.index) & meta.lin.isin(ORG_LINEAGES) & meta.cls.isin(["org", "FBS"])
    meta = meta[keep]
    ex = ex.loc[meta.index]
    # one expression vector per (ModelID, cls, Fmt)
    grp = meta.groupby([meta.ModelID, meta.cls, meta.Fmt]).ngroup()
    exm = ex.groupby(grp.values).mean()
    mm = meta.groupby([meta.ModelID, meta.cls, meta.Fmt]).first().reset_index()
    mm.index = exm.index
    out["n_expression_units"] = mm.groupby(["cls", "Fmt"]).size().to_dict().__str__()

    def contrast(mask_a, mask_b, label):
        sel = mm[mask_a | mask_b]
        b, se, p, n1, n0, _hc3 = contrast2(exm.loc[sel.index], mask_a[sel.index].values, sel.lin)
        out[label + "_n"] = [n1, n0]
        return b

    is_dome = (mm.cls == "org") & (mm.Fmt == "dome")
    is_adh_org = (mm.cls == "org") & (mm.Fmt == "adherent")
    is_fbs = (mm.cls == "FBS") & (mm.Fmt == "adherent")
    E = contrast(is_dome, is_fbs, "E_dome")
    Ea = contrast(is_adh_org, is_fbs, "E_adh") if is_adh_org.sum() >= 3 else None

    v2 = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    j = v2.join(E.rename("E_expr"), how="inner")
    if Ea is not None:
        j = j.join(Ea.rename("Ea_expr"), how="left")
    res = {"corr_all": float(j.D_org.corr(j.E_expr))}
    for flag in ("medium_attributable", "unresolved"):
        h = j[j.flag == flag]
        res[flag] = {"n": int(len(h)), "corr_D_E": float(h.D_org.corr(h.E_expr)) if len(h) > 2 else None,
                     "median_E_gains": float(h[h.D_org < 0].E_expr.median()) if (h.D_org < 0).any() else None,
                     "median_E_losses": float(h[h.D_org > 0].E_expr.median()) if (h.D_org > 0).any() else None}
    for name, genes in (("mevalonate", MEV), ("heme", HEME), ("fa_synthesis", FASYN)):
        g = [x for x in genes if x in j.index]
        res[name] = {"n": len(g), "median_E": float(j.loc[g, "E_expr"].median()),
                     "median_D": float(j.loc[g, "D_org"].median())}
    for g in ("LDLR", "SREBF2", "SQLE", "HMGCR", "INSIG1"):
        if g in j.index:
            res[g] = {"E": float(j.loc[g, "E_expr"]), "D": float(j.loc[g, "D_org"])}
    score_genes = [g for g in MEV + ["LDLR"] if g in exm.columns]
    z = (exm[score_genes] - exm[score_genes].mean()) / exm[score_genes].std()
    mm["mev_expr_score"] = z.mean(axis=1).values
    res["mev_expr_score_by_condition"] = mm.groupby([mm.cls, mm.Fmt]).mev_expr_score.median().round(3).to_dict().__str__()
    out["results"] = res
    (ROOT / "generations/expression_triangulation_v1.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out, indent=1, default=str)[:3500])


if __name__ == "__main__":
    main()
