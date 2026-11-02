#!/usr/bin/env python3
"""Round 7: (a) ribosome/spliceosome loss - growth artifact or real?
Adjust per-screen pathway scores for essential-depth (depletion strength)
and Days; does formulation class survive? (b) prediction benchmark:
patient-held-out R2 for mev score from formulation vs +SREBF expression.
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
MEV = ["HMGCS1", "HMGCR", "MVK", "PMVK", "MVD", "IDI1", "IDI2", "FDPS", "FDFT1",
       "SQLE", "LSS", "CYP51A1", "MSMO1", "NSDHL", "HSD17B7", "EBP", "SC5D",
       "DHCR7", "DHCR24", "ACAT2", "SREBF2", "INSIG1", "LDLR"]
RIBO = ["RPL3", "RPL27", "RPS16", "RPL5", "RPS6", "RPL7", "RPS3", "RPL10", "RPS14", "RPL23", "RPS23", "RPS19"]
SPL = ["EFTUD2", "SF3A3", "SRSF7", "RBM39", "U2SURP", "THOC2", "PRPF8", "SNRPA1"]


def cls(f):
    if "OPAC" in f or "Organoid" in f:
        return "organoid_defined"
    if "Tumor Stem" in f:
        return "TSM_B27"
    if "FBS" in f:
        return "FBS"
    return "other"


def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b


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

    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str).fillna("")
    mc = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("")
    form = dict(zip(mc.ModelConditionID, mc.FormulationID.str.strip()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Formulation"] = ok.ModelConditionID.map(form)
    ok["Daysn"] = pd.to_numeric(ok.Days, errors="coerce")
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), Formulation=("Formulation", "first"),
                Days=("Daysn", "median")).reset_index())
    scr["Class"] = scr.Formulation.map(cls)
    scr = scr[(scr.Class != "other") & (~scr.ModelID.map(patient).isin(reserved))]
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
    glob = GE.mean(axis=1).values
    ess500 = GE.mean(axis=0).nsmallest(500).index
    depth = GE[ess500].mean(axis=1).values - glob
    scores = {}
    for name, genes in (("mev", MEV), ("ribo", RIBO), ("splice", SPL)):
        g = [x for x in genes if x in GE.columns]
        scores[name] = GE[g].mean(axis=1).values - glob
    pats = scr.ModelID.map(patient).values
    upats = np.unique(pats)
    rng = np.random.default_rng(20261029)

    def design(adjust):
        cols = [np.ones(len(scr)),
                (scr.Class.values == "organoid_defined").astype(float),
                (scr.Class.values == "TSM_B27").astype(float)]
        names = ["int", "org_def", "tsm"]
        if adjust:
            cols += [depth, np.nan_to_num(scr.Days.values, nan=np.nanmedian(scr.Days.values))]
            names += ["ess_depth", "days"]
        return np.column_stack(cols), names

    for name, y in scores.items():
        for adj in (False, True):
            X, names = design(adj)
            b = ols(X, y)
            boots = []
            for _ in range(300):
                pick = rng.choice(upats, size=len(upats), replace=True)
                rows = np.concatenate([np.where(pats == q)[0] for q in pick])
                boots.append(ols(X[rows], y[rows]))
            boots = np.array(boots)
            rep[f"{name}_{'adj' if adj else 'raw'}"] = {
                n: [round(float(b[i]), 4), round(float(np.percentile(boots[:, i], 2.5)), 4),
                    round(float(np.percentile(boots[:, i], 97.5)), 4)] for i, n in enumerate(names)}
    rep["depth_by_class"] = {k: round(float(depth[scr.Class.values == k].mean()), 3)
                             for k in ("FBS", "TSM_B27", "organoid_defined")}
    rep["days_by_class"] = {k: round(float(np.nanmedian(scr.Days.values[scr.Class.values == k])), 1)
                            for k in ("FBS", "TSM_B27", "organoid_defined")}

    # (b) prediction benchmark: patient-held-out (group 5-fold by patient)
    y = scores["mev"]
    Xc = np.column_stack([np.ones(len(scr)),
                          (scr.Class.values == "organoid_defined").astype(float),
                          (scr.Class.values == "TSM_B27").astype(float)])
    folds = rng.integers(0, 5, size=len(upats))
    fmap = dict(zip(upats, folds))
    fo = np.array([fmap[p] for p in pats])
    pred = np.zeros_like(y)
    for f in range(5):
        tr, te = fo != f, fo == f
        pred[te] = Xc[te] @ ols(Xc[tr], y[tr])
    rep["bench_mev_formulation_only_R2"] = round(
        float(1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()), 4)
    pred0 = np.array([y[fo != f].mean() for f in fo])
    rep["bench_mev_mean_R2"] = round(
        float(1 - ((y - pred0) ** 2).sum() / ((y - y.mean()) ** 2).sum()), 4)
    (ROOT / "generations/recomb7.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1)[:2400])


if __name__ == "__main__":
    main()
