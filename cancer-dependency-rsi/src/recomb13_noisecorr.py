#!/usr/bin/env python3
"""Round 13: noise-corrected lability.
noise_g = per-gene mean |delta| across same-model, same-library,
different-screen adherent pairs (genome-wide screens). Test: frozen-style
partial Spearman of D (Broad dev organoids, absolute-rank displacement on
minipool 1000-gene panel) vs L1000 controlling base |AdherentMean|-analog
(2D mean) AND noise_g. Dev panel only; single pre-declared retest.
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


def partial_multi(y, x, Z):
    ry, rx = stats.rankdata(y), stats.rankdata(x)
    Zm = np.column_stack([np.ones(len(y))] + [stats.rankdata(z) for z in Z])
    ey = ry - Zm @ np.linalg.lstsq(Zm, ry, rcond=None)[0]
    ex = rx - Zm @ np.linalg.lstsq(Zm, rx, rcond=None)[0]
    return float(np.corrcoef(ex, ey)[0, 1])


def main():
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    reserved = set(json.load(open(ROOT / "data/sequester_patients_v1.json"))["reserved_patients"])
    models = pd.read_csv(ROOT / "data/Model.csv", usecols=["ModelID", "PatientID"])
    mpat = dict(zip(models.ModelID, models.PatientID))
    pp = {}
    for r in csv.DictReader(open(ROOT / "data/passports_model_list_20260921.csv")):
        if r.get("BROAD_ID"):
            pp[r["BROAD_ID"]] = r.get("patient_id", "")
    patient = lambda m: mpat.get(m) or pp.get(m) or ""

    # L1000 (equal-weight, from recomb1 logic)
    sm = pd.read_csv(ROOT / "data/minipool/minipool_screen_metadata.csv")
    ge = pd.read_csv(ROOT / "data/minipool/minipool_chronos_gene_effects.csv", index_col=0)
    sm = sm[sm.cell_line_name.isin(ge.index)].set_index("cell_line_name")
    per_model = {}
    for (model, med, serum), g in sm.groupby(["DepMap ID", "Culture medium", "Serum status"]):
        dome = [s for s in g.index if g.loc[s, "Growth Format"] == "Dome"]
        plas = [s for s in g.index if g.loc[s, "Growth Format"] != "Dome"]
        if dome and plas:
            per_model.setdefault(model, []).append(
                (ge.loc[dome].mean(axis=0) - ge.loc[plas].mean(axis=0)).values)
    genes1000 = list(ge.columns)
    Dm = np.vstack([np.mean(v, axis=0) for v in per_model.values()])
    L1000 = pd.Series(np.abs(Dm).mean(axis=0), index=genes1000)

    # noise_g from same-model same-library screen pairs (adherent)
    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str).fillna("")
    mc = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("")
    fmt = dict(zip(mc.ModelConditionID, mc.CellFormat.str.strip().str.lower()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Format"] = ok.ModelConditionID.map(fmt)
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), Format=("Format", "first"),
                Library=("Library", "first")).reset_index())
    scr = scr[(scr.Format == "adherent") & (~scr.ModelID.map(patient).isin(reserved))]
    multi = scr.groupby(["ModelID", "Library"]).size()
    keep_keys = [k for k, v in multi.items() if v >= 2]
    scr_k = scr.set_index(["ModelID", "Library"]).loc[keep_keys].reset_index()
    need = set(scr_k.ScreenID)
    # also need organoid + adherent models for D
    org_m = sorted({m for m in ok[ok.Format.isin(["dome", "spheroid"])].ModelID if patient(m) not in reserved})
    chunks = []
    for ch in pd.read_csv(DL / "ScreenGeneEffect.csv", index_col=0, chunksize=250):
        hit = ch.index.intersection(need)
        if len(hit):
            chunks.append(ch.loc[hit].astype(np.float32))
    SGE = pd.concat(chunks)
    SGE.columns = [c.split(" (")[0] for c in SGE.columns]
    SGE = SGE.loc[:, ~SGE.columns.duplicated()]
    deltas = []
    for (model, lib), g in scr_k.groupby(["ModelID", "Library"]):
        ss = [s for s in g.ScreenID if s in SGE.index]
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                deltas.append(np.abs(SGE.loc[ss[i]].values - SGE.loc[ss[j]].values))
    noise = pd.Series(np.nanmean(np.vstack(deltas), axis=0), index=SGE.columns)
    rep["noise_pairs"] = len(deltas)

    # D on 1000-gene panel (dev organoids, frozen-style absolute rank vs 2D reference)
    chunks = []
    two_m = sorted(set(scr.ModelID))
    for ch in pd.read_csv(DL / "CRISPRGeneEffect.csv", index_col=0, chunksize=250):
        hit = ch.index.intersection(set(org_m) | set(two_m))
        if len(hit):
            sub = ch.loc[hit]
            sub.columns = [c.split(" (")[0] for c in sub.columns]
            chunks.append(sub.astype(np.float64))
    GE = pd.concat(chunks)
    GE = GE.loc[:, ~GE.columns.duplicated()]
    genes = [g for g in genes1000 if g in GE.columns and g in noise.index]
    org = GE.loc[[m for m in org_m if m in GE.index], genes]
    two = GE.loc[[m for m in two_m if m in GE.index], genes]
    base = two.mean(axis=0)
    ref_rank = base.rank().values
    ranks = org.rank(axis=1).values
    Dmat = np.abs(ranks - ref_rank) / (len(genes) - 1)
    pats = [patient(m) for m in org.index]
    by = {}
    for i, p in enumerate(pats):
        by.setdefault(p, []).append(i)
    pmeans = np.vstack([np.nanmean(Dmat[v], axis=0) for v in by.values()])
    D = np.nanmean(pmeans, axis=0)
    Lv, Bv, Nv = L1000[genes].values, np.abs(base.values), noise[genes].values
    m = np.isfinite(D) & np.isfinite(Lv) & np.isfinite(Bv) & np.isfinite(Nv)
    rep["genes"] = int(m.sum())
    rep["rho_partial_base_only"] = round(partial_multi(D[m], Lv[m], [Bv[m]]), 4)
    rep["rho_partial_base_plus_noise"] = round(partial_multi(D[m], Lv[m], [Bv[m], Nv[m]]), 4)
    rep["rho_L_vs_noise"] = round(float(stats.spearmanr(Lv[m], Nv[m]).statistic), 4)
    rep["rho_noise_vs_D_partial_base"] = round(partial_multi(D[m], Nv[m], [Bv[m]]), 4)
    up = list(by.keys())
    boots = []
    for _ in range(1000):
        pick = rng.integers(0, len(up), size=len(up))
        Db = np.nanmean(pmeans[pick], axis=0)
        boots.append(partial_multi(Db[m], Lv[m], [Bv[m], Nv[m]]))
    rep["boot95_base_plus_noise"] = [round(float(np.percentile(boots, 2.5)), 4),
                                     round(float(np.percentile(boots, 97.5)), 4)]
    (ROOT / "generations/recomb13_noisecorr.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
