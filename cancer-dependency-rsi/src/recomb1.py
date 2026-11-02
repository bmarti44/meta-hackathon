#!/usr/bin/env python3
"""Recombination round 1:
R1: L1000 (equal-weight minipool format lability, 1000 genes) vs Broad
    organoid displacement (frozen-style absolute-rank estimand, dev panel).
R2: genome-wide displacement driver hunt: baseline, expression level/shift,
    copy-number shift, selectivity (tau), common-essential status.
Development/exploratory. Reserved patients excluded.
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


def sp(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    return round(float(stats.spearmanr(a[m], b[m]).statistic), 4), int(m.sum())


def partial(y, x, z):
    def rr(a, b):
        ra, rb = stats.rankdata(a), stats.rankdata(b)
        return ra - np.corrcoef(rb, ra)[0, 1] * rb
    m = np.isfinite(y) & np.isfinite(x) & np.isfinite(z)
    return round(float(stats.spearmanr(rr(y[m], z[m]), rr(x[m], z[m])).statistic), 4)


def load_rows(path, want, meta_drop=None, chunk=250):
    out = []
    for ch in pd.read_csv(path, index_col=0, chunksize=chunk, low_memory=False):
        hit = ch.index.intersection(want)
        if len(hit):
            sub = ch.loc[hit]
            if meta_drop:
                sub = sub.drop(columns=[c for c in meta_drop if c in sub.columns])
            out.append(sub.astype(np.float32))
    df = pd.concat(out)
    df.columns = [c.split(" (")[0] for c in df.columns]
    return df


def main():
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    reserved = set(json.load(open(ROOT / "data/sequester_patients_v1.json"))["reserved_patients"])
    models = pd.read_csv(ROOT / "data/Model.csv", usecols=["ModelID", "PatientID", "OncotreeLineage"]).fillna("")
    mpat = dict(zip(models.ModelID, models.PatientID))
    pp = {}
    for r in csv.DictReader(open(ROOT / "data/passports_model_list_20260921.csv")):
        if r.get("BROAD_ID"):
            pp[r["BROAD_ID"]] = r.get("patient_id", "")
    patient = lambda m: mpat.get(m) or pp.get(m) or ""

    # ---- L1000 from minipool (equal-weight per model)
    sm = pd.read_csv(ROOT / "data/minipool/minipool_screen_metadata.csv")
    ge = pd.read_csv(ROOT / "data/minipool/minipool_chronos_gene_effects.csv", index_col=0)
    sm = sm[sm.cell_line_name.isin(ge.index)]
    per_model = {}
    for (model, med, serum), g in sm.groupby(["DepMap ID", "Culture medium", "Serum status"]):
        dome = [s for s in g.cell_line_name if g.set_index("cell_line_name").loc[s, "Growth Format"] == "Dome"]
        plas = [s for s in g.cell_line_name if g.set_index("cell_line_name").loc[s, "Growth Format"] != "Dome"]
        if dome and plas:
            d = (ge.loc[dome].mean(axis=0) - ge.loc[plas].mean(axis=0)).values
            per_model.setdefault(model, []).append(d)
    genes1000 = list(ge.columns)
    Dm = np.vstack([np.mean(v, axis=0) for v in per_model.values()])  # per-model signed delta
    L1000 = pd.Series(np.abs(Dm).mean(axis=0), index=genes1000)
    S1000 = pd.Series(Dm.mean(axis=0), index=genes1000)
    rep["L1000_models"] = len(per_model)
    # split-half reliability across the 6 models (3v3, all combos avg via bootstrap)
    rhos = []
    idx = np.arange(len(per_model))
    for _ in range(100):
        rng.shuffle(idx)
        a = np.abs(Dm[idx[:3]]).mean(axis=0)
        b = np.abs(Dm[idx[3:]]).mean(axis=0)
        rhos.append(stats.spearmanr(a, b).statistic)
    rep["L1000_splithalf_rho"] = round(float(np.median(rhos)), 4)

    # ---- Broad panels (dev only)
    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str).fillna("")
    mc = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("")
    fmt = dict(zip(mc.ModelConditionID, mc.CellFormat.str.strip().str.lower()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Format"] = ok.ModelConditionID.map(fmt)
    org_m = sorted({m for m in ok[ok.Format.isin(["dome", "spheroid"])].ModelID if patient(m) not in reserved})
    two_m = sorted({m for m in ok[ok.Format == "adherent"].ModelID if patient(m) not in reserved})
    GE = load_rows(DL / "CRISPRGeneEffect.csv", set(org_m) | set(two_m))
    org = GE.loc[[m for m in org_m if m in GE.index]]
    two = GE.loc[[m for m in two_m if m in GE.index]]
    rep["panels"] = [int(len(org)), int(len(two))]

    # displacement: signed mean shift + absolute-rank (frozen style, genome-wide panel)
    disp_signed = org.mean(axis=0) - two.mean(axis=0)
    base = two.mean(axis=0)
    G = GE.shape[1]
    ref_rank = pd.Series(base.values).rank().values
    pats = [patient(m) for m in org.index]
    ranks = org.rank(axis=1).values  # NaN-safe (NaN stays NaN)
    Dmat = np.abs(ranks - ref_rank) / (G - 1)
    by = {}
    for i, p in enumerate(pats):
        by.setdefault(p, []).append(i)
    disp_abs = pd.Series(
        np.nanmean(np.vstack([np.nanmean(Dmat[v], axis=0) for v in by.values()]), axis=0),
        index=GE.columns)
    rep["disp_splithalf_genomewide"] = sp(
        (org.iloc[::2].mean(axis=0) - two.mean(axis=0)).values,
        (org.iloc[1::2].mean(axis=0) - two.mean(axis=0)).values)[0]

    g1k = [g for g in genes1000 if g in GE.columns]
    rep["R1_L1000_vs_dispabs"], rep["R1_n"] = sp(L1000[g1k].values, disp_abs[g1k].values)
    rep["R1_L1000_partial_base"] = partial(disp_abs[g1k].values, L1000[g1k].values, np.abs(base[g1k].values))
    rep["R1_signed1000_vs_dispsigned"] = sp(S1000[g1k].values, disp_signed[g1k].values)[0]

    # ---- R2 driver hunt (genome-wide, signed displacement endpoint)
    feats = {"baseline_2D": base, "abs_baseline": base.abs()}
    # selectivity tau-like: sd across 2D models / range proxy
    feats["chronos_sd_2D"] = two.std(axis=0)
    feats["frac_dep_2D"] = (two <= -0.5).mean(axis=0)
    gene_csv = pd.read_csv(ROOT / "data/Gene.csv")
    if "IsCommonEssential" in gene_csv.columns:
        ce = dict(zip(gene_csv.Symbol, gene_csv.IsCommonEssential.astype(str).str.lower().isin(["true", "yes"]).astype(float)))
        feats["common_essential"] = pd.Series(ce).reindex(GE.columns)
    # expression
    want = set(org.index) | set(two.index)
    chunks = []
    for ch in pd.read_csv(DL / "OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv",
                          index_col=0, chunksize=250, low_memory=False):
        msk = ch.ModelID.isin(want) & ch.IsDefaultEntryForModel.astype(str).str.lower().isin(["true", "yes"])
        if msk.any():
            sub = ch.loc[msk]
            keep = sub.drop(columns=["SequencingID", "ModelConditionID", "ModelID",
                                     "IsDefaultEntryForMC", "IsDefaultEntryForModel"]).astype(np.float32)
            keep.index = sub.ModelID.values
            chunks.append(keep)
    EX = pd.concat(chunks)
    EX.columns = [c.split(" (")[0] for c in EX.columns]
    EX = EX[~EX.index.duplicated()]
    eo = EX.loc[[m for m in org.index if m in EX.index]]
    et = EX.loc[[m for m in two.index if m in EX.index]]
    common = [g for g in GE.columns if g in EX.columns]
    feats["expr_level_org"] = eo[common].mean(axis=0).reindex(GE.columns)
    feats["expr_shift"] = (eo[common].mean(axis=0) - et[common].mean(axis=0)).reindex(GE.columns)
    feats["abs_expr_shift"] = feats["expr_shift"].abs()
    # copy number shift
    CN = load_rows(DL / "OmicsCNGeneWGS.csv", want,
                   meta_drop=["SequencingID", "ModelConditionID", "ModelID",
                              "IsDefaultEntryForMC", "IsDefaultEntryForModel"]) \
        if False else None
    # CN file format check happens in load below (index may be ModelID directly)
    try:
        cn_chunks = []
        for ch in pd.read_csv(DL / "OmicsCNGeneWGS.csv", index_col=0, chunksize=250, low_memory=False):
            if "ModelID" in ch.columns:
                msk = ch.ModelID.isin(want)
                if msk.any():
                    sub = ch.loc[msk]
                    keep = sub.drop(columns=[c for c in sub.columns if not (" (" in c)]).astype(np.float32)
                    keep.index = sub.ModelID.values
                    cn_chunks.append(keep)
            else:
                hit = ch.index.intersection(want)
                if len(hit):
                    cn_chunks.append(ch.loc[hit].astype(np.float32))
        CN = pd.concat(cn_chunks)
        CN.columns = [c.split(" (")[0] for c in CN.columns]
        CN = CN[~CN.index.duplicated()]
        co = CN.loc[[m for m in org.index if m in CN.index]]
        ct = CN.loc[[m for m in two.index if m in CN.index]]
        cg = [g for g in GE.columns if g in CN.columns]
        feats["cn_shift"] = (co[cg].mean(axis=0) - ct[cg].mean(axis=0)).reindex(GE.columns)
        rep["cn_models"] = [int(len(co)), int(len(ct))]
    except Exception as e:
        rep["cn_error"] = str(e)[:160]

    drivers = {}
    for name, f in feats.items():
        drivers[name] = {"vs_disp_signed": sp(f.values, disp_signed.values)[0],
                         "vs_disp_abs": sp(f.values, disp_abs.values)[0]}
    rep["R2_drivers"] = drivers
    # multivariable rank regression (signed disp ~ ranked features)
    finite = np.isfinite(disp_signed.values)
    F = pd.DataFrame({k: stats.rankdata(v.fillna(v.median()).values[finite]) for k, v in feats.items()})
    y = stats.rankdata(disp_signed.values[finite])
    X = np.column_stack([np.ones(len(y))] + [F[c].values for c in F.columns])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ beta
    rep["R2_multivar_rank_R2"] = round(float(1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()), 4)
    rep["R2_betas"] = {c: round(float(b), 2) for c, b in zip(F.columns, beta[1:])}
    (ROOT / "generations/recomb1.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
