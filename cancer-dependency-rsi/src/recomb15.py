#!/usr/bin/env python3
"""Round 15: (a) proliferation mediation of spliceosome/ribosome loss;
(b) Wnt score in Wnt-conditioned-medium formulation vs OPAC;
(c) per-pathway formulation R2 map (patient-held-out)."""
import csv
import json
import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"
SPL = ["EFTUD2", "SF3A3", "SRSF7", "RBM39", "U2SURP", "THOC2", "PRPF8", "SNRPA1"]
RIBO = ["RPL3", "RPL27", "RPS16", "RPL5", "RPS6", "RPL7", "RPS3", "RPL10", "RPS14", "RPL23", "RPS23", "RPS19"]
WNT = ["FZD5", "WLS", "PORCN", "CTNNB1", "TCF7L2", "LRP5", "LRP6", "LGR4"]
PROLIF = ["MKI67", "CCNB1", "CDK1", "TOP2A", "PCNA", "MCM2", "MCM6", "CDC20", "AURKB", "PLK1"]
rng = np.random.default_rng(20261029)


def cls(f):
    if "Pancreas Organoid" in f:
        return "panc_wntCM"
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
    scr = ok.groupby("ScreenID").agg(ModelID=("ModelID", "first"), MCID=("ModelConditionID", "first")).reset_index()
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
    glob = GE.mean(axis=1).values
    for name, genes in (("splice", SPL), ("ribo", RIBO), ("wnt", WNT)):
        g = [x for x in genes if x in GE.columns]
        scr[name] = GE[g].mean(axis=1).values - glob
    # expression proliferation by MCID
    want_mc = set(scr.MCID)
    META = ["SequencingID", "ModelConditionID", "ModelID", "IsDefaultEntryForMC", "IsDefaultEntryForModel"]
    ech = []
    for ch in pd.read_csv(DL / "OmicsExpressionTPMLogp1HumanProteinCodingGenes.csv",
                          index_col=0, chunksize=250, low_memory=False):
        m = ch.ModelConditionID.isin(want_mc) & ch.IsDefaultEntryForMC.astype(str).str.lower().isin(["true", "yes"])
        if m.any():
            sub = ch.loc[m]
            keep = sub.drop(columns=META).astype(np.float32)
            keep.index = sub.ModelConditionID.values
            ech.append(keep)
    EX = pd.concat(ech)
    EX.columns = [c.split(" (")[0] for c in EX.columns]
    EX = EX[~EX.index.duplicated()]
    scr["prolif"] = scr.MCID.map(EX[[g for g in PROLIF if g in EX.columns]].mean(axis=1).to_dict())
    d = scr.reset_index()
    rep["wnt_by_class"] = {k: [round(float(v), 3), int((d.C == k).sum())]
                           for k, v in d.groupby("C").wnt.mean().items()}

    dd = d.dropna(subset=["prolif"]).copy()
    pats = dd.ModelID.map(patient).values
    up = np.unique(pats)
    for name in ("splice", "ribo"):
        y = dd[name].values
        for adj in (False, True):
            cols = [np.ones(len(dd)), (dd.C.values == "org_def").astype(float),
                    (dd.C.values == "TSM").astype(float), (dd.C.values == "panc_wntCM").astype(float)]
            if adj:
                cols.append(dd.prolif.values)
            X = np.column_stack(cols)
            b = ols(X, y)
            boots = []
            for _ in range(300):
                pick = rng.choice(up, size=len(up), replace=True)
                rows = np.concatenate([np.where(pats == q)[0] for q in pick])
                boots.append(ols(X[rows], y[rows])[1])
            rep[f"{name}_{'prolif_adj' if adj else 'raw'}_orgdef"] = [
                round(float(b[1]), 4), round(float(np.percentile(boots, 2.5)), 4),
                round(float(np.percentile(boots, 97.5)), 4)]
    rep["prolif_by_class"] = {k: round(float(v), 3) for k, v in dd.groupby("C").prolif.mean().items()}
    rep["n_screens_expr"] = int(len(dd))
    (ROOT / "generations/recomb15.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
