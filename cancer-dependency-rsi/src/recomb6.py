#!/usr/bin/env python3
"""Round 6: genome-wide formulation-conditional dependency atlas.
Per-screen centered Chronos (gene - screen mean), averaged by medium class
(FBS / TSM_B27 / organoid_defined / other). Effect = organoid_defined - FBS.
Patient-bootstrap CI for top genes. Dev patients only.
"""
import csv
import json
import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"


def cls(f):
    if "OPAC" in f or "Organoid" in f:
        return "organoid_defined"
    if "Tumor Stem" in f:
        return "TSM_B27"
    if "FBS" in f:
        return "FBS"
    return "other"


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
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), Formulation=("Formulation", "first")).reset_index())
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
    C = GE.values - np.nanmean(GE.values, axis=1, keepdims=True)
    classes = scr.Class.values
    means = {k: np.nanmean(C[classes == k], axis=0) for k in ("FBS", "TSM_B27", "organoid_defined")}
    eff = pd.Series(means["organoid_defined"] - means["FBS"], index=GE.columns)
    eff_tsm = pd.Series(means["TSM_B27"] - means["FBS"], index=GE.columns)
    rep["n_screens"] = {k: int((classes == k).sum()) for k in means}
    rep["eff_corr_org_vs_tsm"] = round(float(np.corrcoef(
        eff.values[np.isfinite(eff.values) & np.isfinite(eff_tsm.values)],
        eff_tsm.values[np.isfinite(eff.values) & np.isfinite(eff_tsm.values)])[0, 1]), 4)
    top_gain = eff.nsmallest(30)
    top_loss = eff.nlargest(30)
    # patient bootstrap on union of top genes
    genes = list(top_gain.index) + list(top_loss.index)
    gidx = [GE.columns.get_loc(g) for g in genes]
    pats = scr.ModelID.map(patient).values
    rng = np.random.default_rng(20261029)
    boots = {g: [] for g in genes}
    class_rows = {k: np.where(classes == k)[0] for k in ("FBS", "organoid_defined")}
    for _ in range(300):
        est = {}
        for k, rows in class_rows.items():
            up = np.unique(pats[rows])
            pick = rng.choice(up, size=len(up), replace=True)
            rr = np.concatenate([rows[pats[rows] == q] for q in pick])
            est[k] = np.nanmean(C[rr][:, gidx], axis=0)
        d = est["organoid_defined"] - est["FBS"]
        for j, g in enumerate(genes):
            boots[g].append(d[j])
    def pack(s):
        return {g: [round(float(s[g]), 3), round(float(np.percentile(boots[g], 2.5)), 3),
                    round(float(np.percentile(boots[g], 97.5)), 3)] for g in s.index}
    rep["top_gain_dependency_in_defined"] = pack(top_gain)
    rep["top_loss_dependency_in_defined"] = pack(top_loss)
    rep["tsm_effects_top"] = {g: round(float(eff_tsm[g]), 3) for g in genes}
    atlas = pd.DataFrame({"eff_defined_minus_FBS": eff, "eff_TSM_minus_FBS": eff_tsm})
    atlas.to_csv(ROOT / "generations/formulation_atlas_v1.csv")
    (ROOT / "generations/recomb6.json").write_text(json.dumps(rep, indent=1))
    print("eff corr org vs TSM:", rep["eff_corr_org_vs_tsm"], "| screens:", rep["n_screens"])
    print("GAIN:", list(rep["top_gain_dependency_in_defined"].items())[:12])
    print("LOSS:", list(rep["top_loss_dependency_in_defined"].items())[:12])


if __name__ == "__main__":
    main()
