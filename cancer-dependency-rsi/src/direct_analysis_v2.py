#!/usr/bin/env python3
"""Direct analysis v2: does paired-format lability predict organoid failure?

A1 (primary): minipool paired-format lability L_g (atlas v4) vs organoid
   displacement in DepMap 26Q3 Broad Chronos (110 3D models vs 2D panel),
   baseline-adjusted, patient bootstrap. Independent measurement system
   from spent Lock-S cohort C (Sanger) - development-side replication.
A2: medium-axis lability genome-wide (170 multi-media models): split-half
   reproducibility; correlation with format lability on shared genes.
A3: expression moderation: organoid-vs-2D expression shift vs displacement.

Reserved patients excluded from 26Q3 panels. Exploratory/development.
"""
import csv
import json
import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"
rng = np.random.default_rng(20261029)


def spearman(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    return float(stats.spearmanr(a[m], b[m]).statistic), int(m.sum())


def partial_spearman(a, b, c):
    def rr(y, x):
        ry, rx = stats.rankdata(y), stats.rankdata(x)
        return ry - np.corrcoef(rx, ry)[0, 1] * rx
    m = np.isfinite(a) & np.isfinite(b) & np.isfinite(c)
    return float(stats.spearmanr(rr(a[m], c[m]), rr(b[m], c[m])).statistic)


def load_rows(path, want_ids, chunksize=250):
    chunks = []
    for ch in pd.read_csv(path, index_col=0, chunksize=chunksize):
        hit = ch.index.intersection(want_ids)
        if len(hit):
            chunks.append(ch.loc[hit].astype(np.float32))
    out = pd.concat(chunks)
    out.columns = [c.split(" (")[0] for c in out.columns]
    return out


def main():
    reserved = set(json.load(open(ROOT / "data/sequester_patients_v1.json"))["reserved_patients"])
    models = pd.read_csv(ROOT / "data/Model.csv", usecols=["ModelID", "PatientID"])
    mpat = dict(zip(models.ModelID, models.PatientID))
    pp = {}
    for r in csv.DictReader(open(ROOT / "data/passports_model_list_20260921.csv")):
        if r.get("BROAD_ID"):
            pp[r["BROAD_ID"]] = r.get("patient_id", "")
    patient = lambda m: mpat.get(m) or pp.get(m) or ""

    # ---- panels from screen metadata
    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str).fillna("")
    mc = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("")
    fmt = dict(zip(mc.ModelConditionID, mc.CellFormat.str.strip().str.lower()))
    med = dict(zip(mc.ModelConditionID, mc.FormulationID.str.strip()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA")
             & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Format"] = ok.ModelConditionID.map(fmt)
    ok["Medium"] = ok.ModelConditionID.map(med)
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), Format=("Format", "first"),
                Medium=("Medium", "first"), Library=("Library", "first")).reset_index())
    scr["Patient"] = scr.ModelID.map(patient)
    scr = scr[~scr.Patient.isin(reserved)]
    org_models = sorted(scr[scr.Format.isin(["dome", "spheroid"])].ModelID.unique())
    twod_models = sorted(scr[scr.Format == "adherent"].ModelID.unique())
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "organoid_models_dev": len(org_models), "twod_models_dev": len(twod_models)}

    # ---- A1: atlas format lability
    atlas = pd.read_csv(ROOT / "atlas/v4/paired_observations.csv")
    fa = atlas[atlas.axis == "format"]
    L = fa.groupby("gene")["delta_a_minus_b"].apply(lambda s: np.abs(s).mean())
    S = fa.groupby("gene")["delta_a_minus_b"].mean()
    ma = atlas[atlas.axis == "medium"]
    Lmed_atlas = ma.groupby("gene")["delta_a_minus_b"].apply(lambda s: np.abs(s).mean())
    rep["atlas_format_models"] = int(fa.model_id.nunique())
    rep["atlas_genes"] = int(L.shape[0])

    # organoid displacement from CRISPRGeneEffect (model-level Chronos)
    GE = load_rows(DL / "CRISPRGeneEffect.csv", set(org_models) | set(twod_models))
    org = GE.loc[[m for m in org_models if m in GE.index]]
    two = GE.loc[[m for m in twod_models if m in GE.index]]
    rep["organoid_models_in_GE"] = int(len(org))
    rep["twod_models_in_GE"] = int(len(two))
    disp = org.mean(axis=0) - two.mean(axis=0)     # + = dependency weaker in organoids
    base = two.mean(axis=0)
    genes = L.index.intersection(disp.index)
    rep["A1_genes"] = int(len(genes))
    rep["A1_L_vs_disp_rho"], _ = spearman(L[genes].values, disp[genes].values)
    rep["A1_signed_vs_disp_rho"], _ = spearman(S[genes].values, disp[genes].values)
    rep["A1_L_vs_disp_partial_base"] = partial_spearman(
        L[genes].values, disp[genes].values, base[genes].values)
    rep["A1_medlab_vs_disp_rho"], _ = spearman(
        Lmed_atlas.reindex(genes).values, disp[genes].values)
    # split-half displacement reproducibility (patient halves)
    opats = pd.Series(org.index).map(patient).values
    up = np.unique(opats)
    rng.shuffle(up)
    h1 = org[[patient(m) in set(up[: len(up) // 2]) for m in org.index]]
    h2 = org[[patient(m) in set(up[len(up) // 2:]) for m in org.index]]
    rep["A1_disp_splithalf_rho"], _ = spearman(
        (h1.mean(axis=0) - two.mean(axis=0))[genes].values,
        (h2.mean(axis=0) - two.mean(axis=0))[genes].values)
    # patient bootstrap CI for A1 rho
    boots = []
    orgv, twomean = org.values.astype(np.float64), two.mean(axis=0).values
    gidx = [GE.columns.get_loc(g) for g in genes]
    Lv = L[genes].values
    for _ in range(300):
        pick = rng.choice(up, size=len(up), replace=True)
        rows = np.concatenate([np.where(opats == p)[0] for p in pick])
        d = orgv[rows][:, gidx].mean(axis=0) - twomean[gidx]
        boots.append(stats.spearmanr(Lv, d).statistic)
    rep["A1_rho_patient_boot95"] = [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]
    # null: permuted gene labels
    nulls = [stats.spearmanr(rng.permutation(Lv), disp[genes].values).statistic for _ in range(200)]
    rep["A1_null_rho_95"] = [float(np.percentile(nulls, 2.5)), float(np.percentile(nulls, 97.5))]

    # ---- A2: medium-axis lability genome-wide (ScreenGeneEffect)
    ad = scr[scr.Format == "adherent"]
    multi = ad.groupby("ModelID").Medium.nunique()
    mm_models = sorted(multi[multi >= 2].index)
    ad = ad[ad.ModelID.isin(mm_models)]
    SGE = load_rows(DL / "ScreenGeneEffect.csv", set(ad.ScreenID))
    meta = ad.set_index("ScreenID")
    deltas = []
    used = []
    for model, g in ad.groupby("ModelID"):
        meds = sorted(g.Medium.unique())[:2]
        s1 = [s for s in g.ScreenID if meta.loc[s, "Medium"] == meds[0] and s in SGE.index]
        s2 = [s for s in g.ScreenID if meta.loc[s, "Medium"] == meds[1] and s in SGE.index]
        if s1 and s2:
            deltas.append((SGE.loc[s1].mean(axis=0) - SGE.loc[s2].mean(axis=0)).values)
            used.append(model)
    Dm = np.vstack(deltas).astype(np.float64)
    okc = np.isfinite(Dm).all(axis=0)
    Dm = Dm[:, okc]
    gmed = [g for g, k in zip(SGE.columns, okc) if k]
    Lm = pd.Series(np.abs(Dm).mean(axis=0), index=gmed)
    Sm = pd.Series(Dm.mean(axis=0), index=gmed)
    idx = rng.permutation(len(used))
    hh = len(idx) // 2
    rep["A2_models"] = len(used)
    rep["A2_splithalf_L_rho"], _ = spearman(np.abs(Dm[idx[:hh]]).mean(axis=0),
                                             np.abs(Dm[idx[hh:]]).mean(axis=0))
    rep["A2_splithalf_signed_rho"], _ = spearman(Dm[idx[:hh]].mean(axis=0), Dm[idx[hh:]].mean(axis=0))
    shared = L.index.intersection(Lm.index)
    rep["A2_formatL_vs_mediumL_rho"], rep["A2_shared_genes"] = spearman(
        L[shared].values, Lm[shared].values)
    rep["A2_mediumL_vs_disp_rho"], _ = spearman(Lm.reindex(genes).values, disp[genes].values)

    (ROOT / "generations/direct_v2_partial.json").write_text(json.dumps(rep, indent=1))

    # ---- A3: expression moderation (file carries ModelID + default flags)
    want_models = set(org.index) | set(two.index)
    chunks = []
    meta_cols = ["SequencingID", "ModelConditionID", "ModelID",
                 "IsDefaultEntryForMC", "IsDefaultEntryForModel"]
    for ch in pd.read_csv(DL / "OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv",
                          index_col=0, chunksize=250, low_memory=False):
        m = ch.ModelID.isin(want_models) & ch.IsDefaultEntryForModel.astype(str).str.lower().isin(["true", "yes"])
        if m.any():
            sub = ch.loc[m]
            keep = sub.drop(columns=meta_cols).astype(np.float32)
            keep.index = sub.ModelID.values
            chunks.append(keep)
    EX = pd.concat(chunks)
    EX.columns = [c.split(" (")[0] for c in EX.columns]
    EX = EX[~EX.index.duplicated()]
    eo = EX.loc[[m for m in org.index if m in EX.index]]
    et = EX.loc[[m for m in two.index if m in EX.index]]
    edisp = eo.mean(axis=0) - et.mean(axis=0)
    rep["A3_expr_models"] = [int(len(eo)), int(len(et))]
    rep["A3_exprshift_vs_disp_rho"], _ = spearman(edisp[genes].values, disp[genes].values)
    rep["A3_L_vs_disp_partial_expr"] = partial_spearman(
        L[genes].values, disp[genes].values, edisp[genes].values)
    rep["A3_L_vs_absexprshift_rho"], _ = spearman(L[genes].values, np.abs(edisp[genes].values))
    (ROOT / "generations/direct_v2_partial.json").write_text(json.dumps(rep, indent=1))

    # ---- A4: lineage-matched displacement (composition-controlled A1)
    lin = pd.read_csv(ROOT / "data/Model.csv", usecols=["ModelID", "OncotreeLineage"]).fillna("")
    lmap = dict(zip(lin.ModelID, lin.OncotreeLineage.astype(str)))
    disps, used_lin = [], []
    for lineage in sorted(set(lmap.values())):
        o = [m for m in org.index if lmap.get(m) == lineage]
        t = [m for m in two.index if lmap.get(m) == lineage]
        if len(o) >= 5 and len(t) >= 10:
            disps.append(org.loc[o].mean(axis=0) - two.loc[t].mean(axis=0))
            used_lin.append((lineage, len(o), len(t)))
    if disps:
        ldisp = pd.concat(disps, axis=1).mean(axis=1)
        rep["A4_lineages"] = used_lin
        rep["A4_L_vs_ldisp_rho"], _ = spearman(L[genes].values, ldisp[genes].values)
        rep["A4_signed_vs_ldisp_rho"], _ = spearman(S[genes].values, ldisp[genes].values)
        rep["A4_L_vs_ldisp_partial_base"] = partial_spearman(
            L[genes].values, ldisp[genes].values, base[genes].values)
        rep["A4_exprshift_vs_ldisp_rho"], _ = spearman(edisp[genes].values, ldisp[genes].values)
        rep["A4_disp_vs_ldisp_rho"], _ = spearman(disp[genes].values, ldisp[genes].values)

    out = ROOT / "generations/direct_v2.json"
    out.write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
