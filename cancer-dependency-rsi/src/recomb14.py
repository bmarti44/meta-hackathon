#!/usr/bin/env python3
"""Round 14: (a) mev dependency prediction: formulation vs +expression
(SREBF program) patient-held-out. (b) proliferation expression index by
formulation class (loss-side growth check). Join: screens <-> expression
profiles via ModelConditionID.
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
PROLIF = ["MKI67", "CCNB1", "CDK1", "TOP2A", "PCNA", "MCM2", "MCM6", "CDC20", "AURKB", "PLK1"]
rng = np.random.default_rng(20261029)


def cls(f):
    if "OPAC" in f or "Organoid" in f:
        return "org_def"
    if "Tumor Stem" in f:
        return "TSM"
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
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), MCID=("ModelConditionID", "first")).reset_index())
    scr["C"] = scr.MCID.map(lambda m: cls(form.get(m, "")))
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
    scr["mev"] = GE[g].mean(axis=1).values - GE.mean(axis=1).values

    # expression by ModelConditionID (default-for-MC profiles)
    want_mc = set(scr.MCID)
    echunks = []
    META = ["SequencingID", "ModelConditionID", "ModelID", "IsDefaultEntryForMC", "IsDefaultEntryForModel"]
    for ch in pd.read_csv(DL / "OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv",
                          index_col=0, chunksize=250, low_memory=False):
        m = ch.ModelConditionID.isin(want_mc) & ch.IsDefaultEntryForMC.astype(str).str.lower().isin(["true", "yes"])
        if m.any():
            sub = ch.loc[m]
            keep = sub.drop(columns=META).astype(np.float32)
            keep.index = sub.ModelConditionID.values
            echunks.append(keep)
    EX = pd.concat(echunks)
    EX.columns = [c.split(" (")[0] for c in EX.columns]
    EX = EX[~EX.index.duplicated()]
    eg = [x for x in MEV if x in EX.columns]
    scr["mev_expr"] = scr.MCID.map(EX[eg].mean(axis=1).to_dict())
    pg = [x for x in PROLIF if x in EX.columns]
    scr["prolif_expr"] = scr.MCID.map(EX[pg].mean(axis=1).to_dict())
    rep["screens_with_expr"] = int(scr.mev_expr.notna().sum())
    rep["prolif_by_class"] = {k: round(float(v), 3) for k, v in scr.groupby("C").prolif_expr.mean().items()}
    rep["mevexpr_by_class"] = {k: round(float(v), 3) for k, v in scr.groupby("C").mev_expr.mean().items()}

    d = scr.dropna(subset=["mev_expr"]).copy()
    d["Patient"] = d.ModelID.map(patient)
    upats = np.unique(d.Patient.values)
    fmap = dict(zip(upats, rng.integers(0, 5, size=len(upats))))
    fo = d.Patient.map(fmap).values
    y = d.mev.values

    def design(dd, kind):
        cols = [np.ones(len(dd))]
        if kind in ("formulation", "both"):
            cols += [(dd.C.values == "org_def").astype(float), (dd.C.values == "TSM").astype(float)]
        if kind in ("expression", "both"):
            cols += [dd.mev_expr.values]
        return np.column_stack(cols)

    for kind in ("formulation", "expression", "both"):
        X = design(d, kind)
        pred = np.zeros_like(y)
        for f in range(5):
            tr, te = fo != f, fo == f
            pred[te] = X[te] @ ols(X[tr], y[tr])
        rep[f"R2_{kind}"] = round(float(1 - ((y - pred) ** 2).sum() / ((y - y.mean()) ** 2).sum()), 4)
    (ROOT / "generations/recomb14.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
