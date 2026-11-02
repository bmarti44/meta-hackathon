#!/usr/bin/env python3
"""Round 10: policy substrate at screen scale (engineering thread, real n).

World: per-screen mevalonate scores (centered) for ~900 screens with
formulation class + lineage metadata. Task per episode: estimate the mev
score of held-out TARGET screens (patient-disjoint) by revealing up to
B=30 query screens from the pool. Predictor (fixed): shrinkage blend of
queried same-class mean, same-lineage mean, global mean.
Policies: incumbent (0 queries: train class means), random, fixed
(class-stratified round-robin), adaptive (greedy: query the screen whose
class has fewest reveals so far, ties by largest |score| uncertainty proxy
= class variance estimate). Exact query accounting; MAE primary.
"""
import csv
import json
import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"
MEV = ["HMGCS1", "HMGCR", "MVK", "PMVK", "MVD", "IDI1", "IDI2", "FDPS", "FDFT1",
       "SQLE", "LSS", "CYP51A1", "MSMO1", "NSDHL", "HSD17B7", "EBP", "SC5D",
       "DHCR7", "DHCR24", "ACAT2", "SREBF2", "INSIG1", "LDLR"]
B = 30
rng = np.random.default_rng(20261029)


def cls(f):
    if "OPAC" in f or "Organoid" in f:
        return "org_def"
    if "Tumor Stem" in f:
        return "TSM"
    if "FBS" in f:
        return "FBS"
    return "other"


def main():
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(), "budget": B}
    reserved = set(json.load(open(ROOT / "data/sequester_patients_v1.json"))["reserved_patients"])
    models = pd.read_csv(ROOT / "data/Model.csv",
                          usecols=["ModelID", "PatientID", "OncotreeLineage"]).fillna("")
    mpat = dict(zip(models.ModelID, models.PatientID))
    mlin = dict(zip(models.ModelID, models.OncotreeLineage.astype(str)))
    pp = {}
    for r in csv.DictReader(open(ROOT / "data/passports_model_list_20260921.csv")):
        if r.get("BROAD_ID"):
            pp[r["BROAD_ID"]] = r.get("patient_id", "")
    patient = lambda m: mpat.get(m) or pp.get(m) or ""
    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str).fillna("")
    mc = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("")
    form = dict(zip(mc.ModelConditionID, mc.FormulationID.str.strip()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["C"] = ok.ModelConditionID.map(lambda m: cls(form.get(m, "")))
    scr = ok.groupby("ScreenID").agg(ModelID=("ModelID", "first"), C=("C", "first")).reset_index()
    scr = scr[(scr.C != "other") & (~scr.ModelID.map(patient).isin(reserved))]
    need = set(scr.ScreenID)
    chunks = []
    for ch in pd.read_csv(DL / "ScreenGeneEffect.csv", index_col=0, chunksize=250):
        hit = ch.index.intersection(need)
        if len(hit):
            chunks.append(ch.loc[hit].astype(np.float32))
    GE = pd.concat(chunks)
    GE.columns = [c.split(" (")[0] for c in GE.columns]
    GE = GE.loc[:, ~GE.columns.duplicated()]
    scr = scr[scr.ScreenID.isin(GE.index)].set_index("ScreenID").loc[GE.index]
    g = [x for x in MEV if x in GE.columns]
    y = (GE[g].mean(axis=1) - GE.mean(axis=1)).values
    scr["y"] = y
    scr["Patient"] = scr.ModelID.map(patient)
    scr["Lineage"] = scr.ModelID.map(lambda m: mlin.get(m, ""))
    scr = scr.reset_index()

    upats = np.unique(scr.Patient.values)
    fold_of = dict(zip(upats, rng.integers(0, 5, size=len(upats))))
    scr["fold"] = scr.Patient.map(fold_of)

    def predict(target, revealed, train):
        # shrinkage: class mean from revealed+train-class prior
        c = target.C
        prior = train[train.C == c].y.mean()
        if not revealed:
            return prior
        R = scr.loc[revealed]
        same = R[R.C == c].y
        lin = R[(R.Lineage == target.Lineage) & (R.C == c)].y
        est = prior
        if len(same):
            est = (same.sum() + 5 * prior) / (len(same) + 5)
        if len(lin) >= 3:
            est = 0.5 * est + 0.5 * lin.mean()
        return est

    results = {}
    for policy in ("incumbent", "random", "fixed", "adaptive"):
        errs, queries = [], 0
        for f in range(5):
            test = scr[scr.fold == f]
            train = scr[scr.fold != f]
            pool = list(train.index)
            revealed = []
            if policy == "incumbent":
                pass
            elif policy == "random":
                revealed = list(rng.choice(pool, size=min(B, len(pool)), replace=False))
            elif policy == "fixed":
                byc = {c: sorted(train[train.C == c].index) for c in ("FBS", "TSM", "org_def")}
                order = []
                while len(order) < B and any(byc.values()):
                    for c in ("org_def", "TSM", "FBS"):
                        if byc[c] and len(order) < B:
                            order.append(byc[c].pop(0))
                revealed = order
            else:  # adaptive: greedy coverage of least-revealed class, seed by class variance
                counts = {"FBS": 0, "TSM": 0, "org_def": 0}
                avail = list(pool)
                for _ in range(min(B, len(pool))):
                    cmin = min(counts, key=lambda k: counts[k])
                    cand = [i for i in avail if scr.loc[i, "C"] == cmin] or avail
                    pick = cand[0]
                    revealed.append(pick)
                    avail.remove(pick)
                    counts[scr.loc[pick, "C"]] += 1
            queries += len(revealed)
            for _, t in test.iterrows():
                errs.append(abs(predict(t, revealed, train) - t.y))
        results[policy] = {"MAE": round(float(np.mean(errs)), 4), "queries_total": int(queries),
                           "n_targets": len(errs)}
    rep["results"] = results
    rep["world"] = {"screens": int(len(scr)), "patients": int(len(upats))}
    base = results["incumbent"]["MAE"]
    rep["gain_vs_incumbent"] = {k: round(base - v["MAE"], 4) for k, v in results.items()}
    (ROOT / "generations/recomb10_policy.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
