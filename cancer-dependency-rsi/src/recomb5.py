#!/usr/bin/env python3
"""Round 5: mevalonate score by exact medium formulation (screen level)."""
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
    form = dict(zip(mc.ModelConditionID, mc.FormulationID.str.strip()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Format"] = ok.ModelConditionID.map(fmt)
    ok["Formulation"] = ok.ModelConditionID.map(form)
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), Format=("Format", "first"),
                Formulation=("Formulation", "first")).reset_index())
    scr = scr[(scr.Formulation != "") & (~scr.ModelID.map(patient).isin(reserved))]
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
    for name, genes in (("mev", MEV), ("wnt", WNT)):
        g = [x for x in genes if x in GE.columns]
        scr[name] = GE[g].mean(axis=1).values - glob
    pats = scr.ModelID.map(patient).values
    rng = np.random.default_rng(20261029)
    table = {}
    for (formulation, format_), grp in scr.groupby(["Formulation", "Format"]):
        if len(grp) < 8:
            continue
        row = {"n_screens": int(len(grp)), "n_models": int(grp.ModelID.nunique())}
        for name in ("mev", "wnt"):
            y = grp[name].values
            p = grp.ModelID.map(patient).values
            up = np.unique(p)
            boots = []
            for _ in range(300):
                pick = rng.choice(up, size=len(up), replace=True)
                rows = np.concatenate([np.where(p == q)[0] for q in pick])
                boots.append(y[rows].mean())
            row[name] = [round(float(y.mean()), 4), round(float(np.percentile(boots, 2.5)), 4),
                         round(float(np.percentile(boots, 97.5)), 4)]
        table[f"{formulation} [{format_}]"] = row
    rep["by_formulation"] = dict(sorted(table.items(), key=lambda kv: kv[1]["mev"][0]))
    (ROOT / "generations/recomb5.json").write_text(json.dumps(rep, indent=1))
    for k, v in rep["by_formulation"].items():
        print(f"{v['mev'][0]:+.3f} [{v['mev'][1]:+.3f},{v['mev'][2]:+.3f}] n={v['n_screens']:3d} wnt={v['wnt'][0]:+.3f}  {k}")


if __name__ == "__main__":
    main()
