#!/usr/bin/env python3
"""Medium attribution of organoid-specific dependencies (GOAL v4 lead question).

For every gene: organoid-dome vs lineage-matched 2D-FBS shift (D_org), and how much
of it reappears (a) in organoid-medium models grown adherent (A_adh, same medium,
no dome) and (b) in CNS models in serum-free TSM vs CNS in FBS (S_tsm, unrelated
lineage/format). Library bias removed per gene from 32 FBS models screened in both
Avana and Humagne-CD. Dev patients only (reserved patients excluded).
Two scales: raw Chronos and per-screen dynamic-range normalized
(common-essential median -> -1, nonessential median -> 0).
"""
import csv
import json
import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"
ORG_LINEAGES = ["Bowel", "Esophagus/Stomach", "Pancreas", "Breast", "Ovary/Fallopian Tube",
                "Uterus", "Biliary Tract", "Prostate"]


def load_screens():
    reserved = set(json.load(open(ROOT / "data/sequester_patients_v1.json"))["reserved_patients"])
    mod = pd.read_csv(ROOT / "data/Model.csv", dtype=str).set_index("ModelID")
    pp = {r["BROAD_ID"]: r.get("patient_id", "") for r in
          csv.DictReader(open(ROOT / "data/passports_model_list_20260921.csv")) if r.get("BROAD_ID")}
    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str).fillna("")
    mc = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("").set_index("ModelConditionID")
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")
             & ~ex(seq.DrugTreated, "true") & ~ex(seq.IsEngineered, "true")].copy()
    ok["Fmt"] = ok.ModelConditionID.map(mc.CellFormat).str.strip().str.lower()
    ok["Form"] = ok.ModelConditionID.map(mc.FormulationID).str.strip()
    scr = ok.groupby("ScreenID").agg(ModelID=("ModelID", "first"), Lib=("Library", "first"),
                                     Fmt=("Fmt", "first"), Form=("Form", "first"))
    scr["cls"] = np.select([scr.Form.str.contains("OPAC|Organoid"), scr.Form.str.contains("Tumor Stem"),
                            scr.Form.str.contains("FBS")], ["org", "TSM", "FBS"], "other")
    scr["lin"] = scr.ModelID.map(mod.OncotreeLineage)
    scr["patient"] = scr.ModelID.map(lambda m: mod.PatientID.get(m) or pp.get(m) or "")
    scr["reserved"] = scr.patient.isin(reserved)
    return scr[scr.cls != "other"]


def load_effects(screens):
    chunks = []
    for ch in pd.read_csv(DL / "ScreenGeneEffect.csv", index_col=0, chunksize=300):
        hit = ch.index.intersection(screens)
        if len(hit):
            chunks.append(ch.loc[hit].astype(np.float32))
    ge = pd.concat(chunks)
    ge.columns = [c.split(" (")[0] for c in ge.columns]
    return ge


def library_offset(ge, scr):
    """Per-gene Humagne-CD minus Avana, from FBS models screened in both."""
    f = scr[scr.cls == "FBS"]
    both = f.groupby("ModelID").Lib.agg(set)
    both = both[both.map(lambda s: {"Avana", "Humagne-CD"} <= s)].index
    h = ge.loc[f[(f.Lib == "Humagne-CD") & f.ModelID.isin(both)].index].groupby(scr.ModelID).mean()
    a = ge.loc[f[(f.Lib == "Avana") & f.ModelID.isin(both)].index].groupby(scr.ModelID).mean()
    return (h - a.loc[h.index]).mean(), len(both)


def normalize(ge, ess, non):
    """Per screen: common essentials median -> -1, nonessentials median -> 0."""
    e = ge[ess].median(axis=1)
    n = ge[non].median(axis=1)
    return ge.sub(n, axis=0).div((n - e), axis=0)


def contrast(Y, groups, lineage):
    """OLS per gene: y ~ lineage dummies + group indicator. Returns beta, se, n1, n0."""
    lin = pd.get_dummies(lineage, drop_first=True, dtype=float)
    X = np.column_stack([np.ones(len(Y)), groups.astype(float), lin.values])
    XtX_inv = np.linalg.pinv(X.T @ X)
    B = XtX_inv @ X.T @ Y.values
    resid = Y.values - X @ B
    dof = len(Y) - np.linalg.matrix_rank(X)
    s2 = (resid ** 2).sum(axis=0) / dof
    se = np.sqrt(s2 * XtX_inv[1, 1])
    return pd.Series(B[1], Y.columns), pd.Series(se, Y.columns), int(groups.sum()), int((~groups).sum())


def bh(p):
    p = np.asarray(p)
    o = np.argsort(p)
    q = p[o] * len(p) / np.arange(1, len(p) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    out = np.empty_like(q)
    out[o] = np.minimum(q, 1)
    return out


def main():
    from scipy import stats
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    scr = load_screens()
    ge = load_effects(set(scr.index))
    ge = ge.loc[:, ge.notna().mean() > 0.99]
    scr = scr.loc[ge.index]
    off, n_pairs = library_offset(ge, scr)
    off = off.fillna(0)
    rep["library_offset_models"] = n_pairs
    ge = ge.fillna(ge.mean())
    ge.loc[scr.Lib == "Avana"] = ge.loc[scr.Lib == "Avana"] + off
    scr = scr[scr.Lib.isin(["Avana", "Humagne-CD"]) & ~scr.reserved]
    ge = ge.loc[scr.index]

    fbs_adh = scr[(scr.cls == "FBS") & (scr.Fmt == "adherent")]
    med = ge.loc[fbs_adh.index].median()
    frac = (ge.loc[fbs_adh.index] < -0.5).mean()
    ess = list(frac[frac > 0.9].index)
    non = list(med[(med.abs() < 0.05) & (ge.loc[fbs_adh.index].std() < 0.15)].index)
    rep["n_common_essential"], rep["n_nonessential"] = len(ess), len(non)

    for scale in ("raw", "norm"):
        Y = ge if scale == "raw" else normalize(ge, ess, non)
        Ym = Y.groupby(scr.ModelID).mean()
        meta = scr.groupby("ModelID").agg(cls=("cls", "first"), Fmt=("Fmt", "first"), lin=("lin", "first"))
        res = {}
        # D_org: organoid medium + dome vs 2D FBS adherent, organoid lineages
        sel = meta[meta.lin.isin(ORG_LINEAGES) & (((meta.cls == "org") & (meta.Fmt == "dome"))
                                                  | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
        res["D_org"] = contrast(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
        # A_adh: organoid medium + adherent vs 2D FBS adherent
        sel = meta[meta.lin.isin(ORG_LINEAGES) & (((meta.cls == "org") & (meta.Fmt == "adherent"))
                                                  | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
        res["A_adh"] = contrast(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
        # F_dome: dome vs adherent within organoid medium (format at fixed medium)
        sel = meta[meta.lin.isin(ORG_LINEAGES) & (meta.cls == "org")]
        res["F_dome"] = contrast(Ym.loc[sel.index], (sel.Fmt == "dome").values, sel.lin)
        # S_tsm: CNS serum-free TSM vs CNS FBS (adherent + spheroid TSM)
        sel = meta[(meta.lin == "CNS/Brain") & meta.cls.isin(["TSM", "FBS"])]
        res["S_tsm"] = contrast(Ym.loc[sel.index], (sel.cls == "TSM").values, sel.lin)

        tab = pd.DataFrame({k: v[0] for k, v in res.items()})
        for k, v in res.items():
            tab[k + "_se"] = v[1]
        p = 2 * stats.norm.sf((tab.D_org / tab.D_org_se).abs())
        tab["D_org_q"] = bh(p)
        tab.to_csv(ROOT / f"generations/medium_attribution_v1_{scale}.csv", float_format="%.4f")
        rep[scale] = {"n": {k: [v[2], v[3]] for k, v in res.items()}}

        hits = tab[(tab.D_org_q < 0.01) & (tab.D_org < -0.25)]
        losses = tab[(tab.D_org_q < 0.01) & (tab.D_org > 0.25)]
        out = {}
        for name, h in (("gains", hits), ("losses", losses)):
            # share of each hit's organoid shift reproduced without the dome / in unrelated serum-free lineage
            slope = lambda col: float(np.polyfit(h.D_org, h[col], 1)[0]) if len(h) > 2 else None
            out[name] = {"n": int(len(h)),
                         "slope_A_adh_on_D": slope("A_adh"),
                         "slope_S_tsm_on_D": slope("S_tsm"),
                         "slope_F_dome_on_D": slope("F_dome"),
                         "median_ratio_A_adh": float((h.A_adh / h.D_org).median()) if len(h) else None,
                         "median_ratio_S_tsm": float((h.S_tsm / h.D_org).median()) if len(h) else None,
                         "top": h.sort_values("D_org").head(40)[["D_org", "A_adh", "F_dome", "S_tsm"]]
                                 .round(3).reset_index().values.tolist() if name == "gains"
                         else h.sort_values("D_org", ascending=False).head(40)[["D_org", "A_adh", "F_dome", "S_tsm"]]
                                 .round(3).reset_index().values.tolist()}
        rep[scale]["hits"] = out
    (ROOT / "generations/medium_attribution_v1.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({k: (v if k not in ("raw", "norm") else {kk: vv for kk, vv in v.items() if kk != "hits"}
                          | {"hits": {h: {x: y for x, y in d.items() if x != "top"} for h, d in v["hits"].items()}})
                      for k, v in rep.items()}, indent=1))


if __name__ == "__main__":
    main()
