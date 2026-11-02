#!/usr/bin/env python3
"""Direct analysis: paired-format dependency lability at DepMap 26Q3 scale.

Question: when do molecularly defined dependencies persist or fail across
culture formats (adherent 2D vs dome/spheroid 3D), and is per-gene format
lability a reproducible, baseline-independent signal?

Development/exploratory analysis on user-authorized Downloads data.
Reserved patients (data/sequester_patients_v1.json) excluded throughout.
"""
import csv
import json
import datetime
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"
rng = np.random.default_rng(20261029)


def main():
    reserved = set(json.load(open(ROOT / "data/sequester_patients_v1.json"))["reserved_patients"])
    models = pd.read_csv(ROOT / "data/Model.csv", usecols=["ModelID", "PatientID"])
    mpat = dict(zip(models.ModelID, models.PatientID))
    pp = {}
    for r in csv.DictReader(open(ROOT / "data/passports_model_list_20260921.csv")):
        if r.get("BROAD_ID"):
            pp[r["BROAD_ID"]] = r.get("patient_id", "")

    def patient(m):
        return mpat.get(m) or pp.get(m) or ""

    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str).fillna("")
    ex = lambda s, v: s.str.strip().str.lower() == v
    elig = seq[ex(seq.PassesQC, "true") & ex(seq.DrugTreated, "false")
               & ex(seq.IsEngineered, "false") & ex(seq.ExcludeFromCRISPRCombined, "false")
               & (seq.ModelID != "pDNA")]
    mc = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("")
    fmt = dict(zip(mc.ModelConditionID, mc.CellFormat.str.strip().str.lower()))
    screens = (elig.groupby("ScreenID")
               .agg(ModelID=("ModelID", "first"), MCID=("ModelConditionID", "first"),
                    Library=("Library", "first")).reset_index())
    screens["Format"] = screens.MCID.map(fmt)
    screens["Patient"] = screens.ModelID.map(patient)
    screens = screens[~screens.Patient.isin(reserved)]
    screens = screens[screens.Format.isin(["adherent", "dome", "spheroid"])]
    screens["Side"] = np.where(screens.Format == "adherent", "2D", "3D")

    # models with both sides under same library
    pair_keys = []
    for (model, lib), g in screens.groupby(["ModelID", "Library"]):
        if set(g.Side) == {"2D", "3D"}:
            pair_keys.append((model, lib))
    pair_models = sorted({m for m, _ in pair_keys})
    use_screens = screens.set_index(["ModelID", "Library"]).loc[pair_keys].reset_index()
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "eligible_screens_dev": int(len(screens)),
           "format_pair_models": len(pair_models),
           "format_pair_patients": int(pd.Series(pair_models).map(patient).nunique())}

    # load screen gene effects for needed screens only
    need = set(use_screens.ScreenID)
    chunks = []
    for ch in pd.read_csv(DL / "ScreenGeneEffect.csv", index_col=0, chunksize=200):
        hit = ch.index.intersection(need)
        if len(hit):
            chunks.append(ch.loc[hit].astype(np.float32))
    GE = pd.concat(chunks)
    genes = [c.split(" (")[0] for c in GE.columns]
    GE.columns = genes

    # per (model, library): delta = mean 3D - mean 2D; keep model-level (first library alphabetically if 2)
    deltas, base2d, val3d = {}, {}, {}
    meta = use_screens.set_index("ScreenID")
    for (model, lib), g in use_screens.groupby(["ModelID", "Library"]):
        s2 = [s for s in g.ScreenID if meta.loc[s, "Side"] == "2D" and s in GE.index]
        s3 = [s for s in g.ScreenID if meta.loc[s, "Side"] == "3D" and s in GE.index]
        if not s2 or not s3 or model in deltas:
            continue
        v2 = GE.loc[s2].mean(axis=0)
        v3 = GE.loc[s3].mean(axis=0)
        deltas[model] = (v3 - v2).values
        base2d[model] = v2.values
        val3d[model] = v3.values
    models_used = sorted(deltas)
    D = np.vstack([deltas[m] for m in models_used]).astype(np.float64)
    B = np.vstack([base2d[m] for m in models_used])
    V3 = np.vstack([val3d[m] for m in models_used])
    ok = np.isfinite(D).all(axis=0)
    D, B, V3 = D[:, ok], B[:, ok], V3[:, ok]
    genes_ok = [g for g, k in zip(genes, ok) if k]
    rep["models_with_deltas"] = len(models_used)
    rep["genes_complete"] = len(genes_ok)

    L = np.abs(D).mean(axis=0)          # per-gene lability
    S = D.mean(axis=0)                  # signed shift
    Bg = B.mean(axis=0)                 # baseline 2D dependency

    # split-half reproducibility of signed shift (model-level split)
    idx = rng.permutation(len(models_used))
    h = len(idx) // 2
    S1, S2 = D[idx[:h]].mean(axis=0), D[idx[h:]].mean(axis=0)
    L1, L2 = np.abs(D[idx[:h]]).mean(axis=0), np.abs(D[idx[h:]]).mean(axis=0)
    rep["split_half_signed_rho"] = float(stats.spearmanr(S1, S2).statistic)
    rep["split_half_lability_rho"] = float(stats.spearmanr(L1, L2).statistic)

    # persistence: 2D dependency (<= -0.5) -> persist (3D <= -0.5) / fail (>= -0.2)
    dep = B <= -0.5
    persist = dep & (V3 <= -0.5)
    fail = dep & (V3 >= -0.2)
    n_dep = dep.sum(axis=0)
    enough = n_dep >= 10
    fail_rate = np.where(enough, fail.sum(axis=0) / np.maximum(n_dep, 1), np.nan)
    rep["persistence_overall"] = {
        "dep_instances": int(dep.sum()),
        "persist_frac": float(persist.sum() / dep.sum()),
        "fail_frac": float(fail.sum() / dep.sum()),
        "genes_with_>=10_dep_models": int(enough.sum())}
    m = enough & np.isfinite(fail_rate)
    rep["lability_vs_failrate_rho"] = float(stats.spearmanr(L[m], fail_rate[m]).statistic)
    rep["baseline_vs_failrate_rho"] = float(stats.spearmanr(Bg[m], fail_rate[m]).statistic)
    # partial Spearman L vs fail | baseline (rank-residual)
    def rankres(y, x):
        ry, rx = stats.rankdata(y), stats.rankdata(x)
        r = np.corrcoef(rx, ry)[0, 1]
        return ry - r * rx
    rep["lability_vs_failrate_partial_rho"] = float(
        stats.spearmanr(rankres(L[m], Bg[m]), rankres(fail_rate[m], Bg[m])).statistic)

    # patient-cluster bootstrap for lability-fail rho
    pats = np.array([patient(x) for x in models_used])
    upats = np.unique(pats)
    boots = []
    for _ in range(200):
        pick = rng.choice(upats, size=len(upats), replace=True)
        rows = np.concatenate([np.where(pats == p)[0] for p in pick])
        Lb = np.abs(D[rows]).mean(axis=0)
        depb = B[rows] <= -0.5
        frb = (depb & (V3[rows] >= -0.2)).sum(axis=0) / np.maximum(depb.sum(axis=0), 1)
        mb = depb.sum(axis=0) >= 10
        boots.append(stats.spearmanr(Lb[mb], frb[mb]).statistic)
    rep["lability_fail_rho_patient_boot95"] = [float(np.percentile(boots, 2.5)),
                                               float(np.percentile(boots, 97.5))]

    # noise floor: same ModelConditionID, different Library (cross-library deltas)
    noise = []
    sby = screens.groupby(["MCID"])["ScreenID"].apply(list)
    libmap = dict(zip(screens.ScreenID, screens.Library))
    for mcid, ss in sby.items():
        ss = [s for s in ss if s in GE.index]
        libs = {libmap.get(s) for s in ss}
        if len(ss) >= 2 and len(libs) >= 2:
            noise.append(np.abs(GE.loc[ss[0]].values - GE.loc[ss[1]].values))
    if noise:
        rep["noise_floor_crosslib_meanabs"] = float(np.nanmean(np.vstack(noise)))
        rep["noise_pairs"] = len(noise)
    rep["format_meanabs_delta"] = float(np.abs(D).mean())

    # top labile genes (descriptive)
    order = np.argsort(-L)[:20]
    rep["top_labile_genes"] = [{"gene": genes_ok[i], "L": round(float(L[i]), 3),
                                "signed": round(float(S[i]), 3)} for i in order]
    out = ROOT / "generations/direct_v1.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1)[:2600])


if __name__ == "__main__":
    main()
