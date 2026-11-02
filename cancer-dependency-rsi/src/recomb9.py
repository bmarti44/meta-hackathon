#!/usr/bin/env python3
"""Round 9: nutrient-pathway generalization screen by medium class."""
import csv
import json
import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"
PATHWAYS = {
    "purine_synth": ["PPAT", "GART", "PFAS", "PAICS", "ADSL", "ATIC", "IMPDH1", "IMPDH2", "GMPS", "PRPS1", "PRPS2"],
    "pyrimidine_synth": ["CAD", "DHODH", "UMPS", "CTPS1", "CTPS2", "TYMS", "DTYMK", "RRM1", "RRM2"],
    "serine_onecarbon": ["PHGDH", "PSAT1", "PSPH", "SHMT1", "SHMT2", "MTHFD1", "MTHFD2", "ALDH1L2", "AMT", "GLDC"],
    "glutamine": ["GLS", "GLS2", "GLUD1", "GLUL", "SLC1A5", "SLC38A2", "GOT1", "GOT2", "GPT2", "ASNS"],
    "fa_synth": ["ACACA", "ACACB", "FASN", "SCD", "ACLY", "ACSS2", "ELOVL6", "SLC25A1"],
    "fa_oxidation": ["CPT1A", "CPT2", "ACADM", "ACADVL", "HADHA", "ECHS1", "ACAA2"],
    "heme": ["ALAS1", "ALAD", "HMBS", "UROS", "UROD", "CPOX", "PPOX", "FECH"],
    "nad_salvage": ["NAMPT", "NMNAT1", "NMNAT2", "NMNAT3", "NAPRT", "QPRT", "NADSYN1"],
    "oxphos_c1": ["NDUFA1", "NDUFB8", "NDUFS1", "NDUFS3", "NDUFV1", "NDUFA9", "NDUFS7"],
    "oxphos_c4": ["COX5B", "COX6C", "COX7B", "COX4I1", "SCO1", "SURF1"],
    "glycolysis": ["HK1", "HK2", "GPI", "PFKL", "PFKM", "ALDOA", "GAPDH", "PGK1", "ENO1", "PKM", "LDHA"],
    "iron": ["TFRC", "SLC11A2", "STEAP3", "FTH1", "FTL", "IREB2", "ACO1"],
    "cholesterol_uptake": ["LDLR", "PCSK9", "MYLIP", "LRP1", "SCARB1"],
    "aa_transport": ["SLC7A5", "SLC3A2", "SLC7A11", "SLC1A4", "SLC38A1"],
    "folate": ["DHFR", "TYMS", "MTHFD1", "SLC19A1", "FPGS", "GGH"],
    "redox_gsh": ["GCLC", "GCLM", "GSS", "GPX4", "TXNRD1", "GSR", "SLC7A11", "NFE2L2"],
    "pentose_phosphate": ["G6PD", "PGLS", "PGD", "TKT", "TALDO1", "RPIA"],
    "urea_arg": ["ASS1", "ASL", "ARG1", "OTC", "CPS1"],
}


def cls(f):
    if "OPAC" in f or "Organoid" in f:
        return "org_def"
    if "Tumor Stem" in f:
        return "TSM"
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
    glob = GE.mean(axis=1).values
    classes = scr.C.values
    pats = scr.ModelID.map(patient).values
    rng = np.random.default_rng(20261029)
    table = {}
    for name, genes in PATHWAYS.items():
        g = [x for x in genes if x in GE.columns]
        y = GE[g].mean(axis=1).values - glob
        row = {"n_genes": len(g)}
        means = {k: float(y[classes == k].mean()) for k in ("FBS", "TSM", "org_def")}
        boots = []
        for _ in range(300):
            est = {}
            for k in ("FBS", "org_def"):
                rows = np.where(classes == k)[0]
                up = np.unique(pats[rows])
                pick = rng.choice(up, size=len(up), replace=True)
                rr = np.concatenate([rows[pats[rows] == q] for q in pick])
                est[k] = y[rr].mean()
            boots.append(est["org_def"] - est["FBS"])
        row["means"] = {k: round(v, 3) for k, v in means.items()}
        row["org_minus_FBS"] = [round(means["org_def"] - means["FBS"], 3),
                                round(float(np.percentile(boots, 2.5)), 3),
                                round(float(np.percentile(boots, 97.5)), 3)]
        table[name] = row
    rep["pathways"] = dict(sorted(table.items(), key=lambda kv: kv[1]["org_minus_FBS"][0]))
    (ROOT / "generations/recomb9.json").write_text(json.dumps(rep, indent=1))
    for k, v in rep["pathways"].items():
        print(f"{k:22s} d={v['org_minus_FBS'][0]:+.3f} [{v['org_minus_FBS'][1]:+.3f},{v['org_minus_FBS'][2]:+.3f}]  FBS={v['means']['FBS']:+.2f} TSM={v['means']['TSM']:+.2f} ORG={v['means']['org_def']:+.2f} (n={v['n_genes']})")


if __name__ == "__main__":
    main()
