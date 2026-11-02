#!/usr/bin/env python3
"""Round 4: screen-level decomposition of pathway dependency scores.
Per-screen score = mean Chronos(pathway) - mean Chronos(all genes), from
ScreenGeneEffect. Model: score ~ SerumFree + Format + Library, OLS with
patient-cluster bootstrap. Pathways: mevalonate, Wnt-secretion, ribosome.
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
WNT = ["FZD5", "WLS", "PORCN", "CTNNB1", "TCF7L2", "LRP5", "LRP6"]
RIBO = ["RPL3", "RPL27", "RPS16", "RPL5", "RPS6", "RPL7", "RPS3", "RPL10", "RPS14", "RPL23"]


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
    fmt = dict(zip(mc.ModelConditionID, mc.CellFormat.str.strip().str.lower()))
    sfm = dict(zip(mc.ModelConditionID, mc.SerumFreeMedia.str.strip().str.lower()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Format"] = ok.ModelConditionID.map(fmt)
    ok["SF"] = ok.ModelConditionID.map(sfm)
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), Format=("Format", "first"), SF=("SF", "first"),
                Library=("Library", "first")).reset_index())
    scr["Patient"] = scr.ModelID.map(patient)
    scr = scr[(scr.Format != "") & (scr.SF.isin(["true", "false"]))
              & (~scr.Patient.isin(reserved))]
    rep["screens"] = int(len(scr))
    rep["format_x_serumfree"] = {f"{k[0]}|{k[1]}": int(v) for k, v in
                                 scr.groupby(["Format", "SF"]).size().items()}

    need = set(scr.ScreenID)
    chunks = []
    for ch in pd.read_csv(DL / "ScreenGeneEffect.csv", index_col=0, chunksize=250):
        hit = ch.index.intersection(need)
        if len(hit):
            chunks.append(ch.loc[hit].astype(np.float32))
    GE = pd.concat(chunks)
    GE.columns = [c.split(" (")[0] for c in GE.columns]
    scr = scr[scr.ScreenID.isin(GE.index)].set_index("ScreenID").loc[GE.index]
    glob = GE.mean(axis=1).values
    scores = {}
    for name, genes in (("mev", MEV), ("wnt", WNT), ("ribo", RIBO)):
        g = [x for x in genes if x in GE.columns]
        scores[name] = GE[g].mean(axis=1).values - glob

    # design: intercept, SF, format dummies (ref adherent), library dummies
    fmt_cats = ["dome", "spheroid", "suspension", "mixed"]
    lib_cats = sorted(set(scr.Library) - {"Avana"})
    X = [np.ones(len(scr)), (scr.SF.values == "true").astype(float)]
    names = ["intercept", "serum_free"]
    for f in fmt_cats:
        X.append((scr.Format.values == f).astype(float)); names.append(f"fmt_{f}")
    for lb in lib_cats:
        X.append((scr.Library.values == lb).astype(float)); names.append(f"lib_{lb}")
    X = np.column_stack(X)
    pats = scr.Patient.values
    upats = np.unique(pats)
    rng = np.random.default_rng(20261029)
    for name, y in scores.items():
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        boots = []
        for _ in range(500):
            pick = rng.choice(upats, size=len(upats), replace=True)
            rows = np.concatenate([np.where(pats == p)[0] for p in pick])
            b, *_ = np.linalg.lstsq(X[rows], y[rows], rcond=None)
            boots.append(b)
        boots = np.array(boots)
        rep[name] = {n: [round(float(beta[i]), 4),
                         round(float(np.percentile(boots[:, i], 2.5)), 4),
                         round(float(np.percentile(boots[:, i], 97.5)), 4)]
                     for i, n in enumerate(names)}
    (ROOT / "generations/recomb4.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1)[:3200])


if __name__ == "__main__":
    main()
