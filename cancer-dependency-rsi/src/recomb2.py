#!/usr/bin/env python3
"""Recombination round 2: displacement anatomy.
B1: per-organoid-model overall shift vs growth (CPD), days, library.
B2: top signed-displacement genes genome-wide + HGNC group counts.
B3: lineage consistency of signed displacement.
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


def load_rows(path, want, chunk=250):
    out = []
    for ch in pd.read_csv(path, index_col=0, chunksize=chunk):
        hit = ch.index.intersection(want)
        if len(hit):
            out.append(ch.loc[hit].astype(np.float32))
    df = pd.concat(out)
    df.columns = [c.split(" (")[0] for c in df.columns]
    return df


def main():
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    reserved = set(json.load(open(ROOT / "data/sequester_patients_v1.json"))["reserved_patients"])
    models = pd.read_csv(ROOT / "data/Model.csv",
                          usecols=["ModelID", "PatientID", "OncotreeLineage"]).fillna("")
    mpat = dict(zip(models.ModelID, models.PatientID))
    lmap = dict(zip(models.ModelID, models.OncotreeLineage.astype(str)))
    pp = {}
    for r in csv.DictReader(open(ROOT / "data/passports_model_list_20260921.csv")):
        if r.get("BROAD_ID"):
            pp[r["BROAD_ID"]] = r.get("patient_id", "")
    patient = lambda m: mpat.get(m) or pp.get(m) or ""

    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str).fillna("")
    mc = pd.read_csv(ROOT / "data/ModelCondition.csv", dtype=str).fillna("")
    fmt = dict(zip(mc.ModelConditionID, mc.CellFormat.str.strip().str.lower()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Format"] = ok.ModelConditionID.map(fmt)
    ok["CPDn"] = pd.to_numeric(ok.CPD, errors="coerce")
    ok["Daysn"] = pd.to_numeric(ok.Days, errors="coerce")
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), Format=("Format", "first"),
                Library=("Library", "first"), CPD=("CPDn", "median"),
                Days=("Daysn", "median")).reset_index())
    scr["Patient"] = scr.ModelID.map(patient)
    scr = scr[~scr.Patient.isin(reserved)]
    org_scr = scr[scr.Format.isin(["dome", "spheroid"])]
    two_m = sorted(set(scr[scr.Format == "adherent"].ModelID))
    org_m = sorted(set(org_scr.ModelID))

    GE = load_rows(DL / "CRISPRGeneEffect.csv", set(org_m) | set(two_m))
    org = GE.loc[[m for m in org_m if m in GE.index]]
    two = GE.loc[[m for m in two_m if m in GE.index]]
    base = two.mean(axis=0)
    disp_signed = org.mean(axis=0) - base

    # B1: per-model overall shift vs growth
    shift = (org - base.values).mean(axis=1)
    growth = org_scr.groupby("ModelID").agg(CPD=("CPD", "median"), Days=("Days", "median"),
                                             Library=("Library", "first"))
    j = pd.DataFrame({"shift": shift}).join(growth).dropna(subset=["shift"])
    rep["B1_n"] = int(len(j))
    for col in ("CPD", "Days"):
        s = j.dropna(subset=[col])
        rep[f"B1_shift_vs_{col}_rho"] = round(float(stats.spearmanr(s[col], s["shift"]).statistic), 4)
        rep[f"B1_{col}_n"] = int(len(s))
    rep["B1_shift_by_library"] = {k: round(float(v), 4) for k, v in j.groupby("Library")["shift"].mean().items()}
    rep["B1_shift_mean_sd"] = [round(float(j["shift"].mean()), 4), round(float(j["shift"].std()), 4)]
    # essential-gene depletion depth per model (proxy: mean of most-negative 500 genes in 2D base)
    ess = base.nsmallest(500).index
    depth = org[ess].mean(axis=1) - base[ess].mean()
    jj = j.join(depth.rename("ess_depth")).dropna(subset=["CPD"])
    rep["B1_essdepth_vs_CPD_rho"] = round(float(stats.spearmanr(jj.CPD, jj.ess_depth).statistic), 4)
    rep["B1_shift_vs_essdepth_rho"] = round(float(stats.spearmanr(jj["shift"], jj.ess_depth).statistic), 4)

    # B2: extremes + HGNC groups
    ds = disp_signed.dropna().sort_values()
    rep["B2_top_loss_in_3D"] = {g: round(float(v), 3) for g, v in ds.tail(15).items()}   # + = weaker in 3D
    rep["B2_top_gain_in_3D"] = {g: round(float(v), 3) for g, v in ds.head(15).items()}   # - = stronger in 3D
    hgnc = pd.read_csv(ROOT / "data/Gene.csv", usecols=["symbol", "gene_group"], dtype=str, low_memory=False).fillna("")
    gmap = dict(zip(hgnc.symbol, hgnc.gene_group))
    for label, genes_ in (("loss", ds.tail(200).index), ("gain", ds.head(200).index)):
        from collections import Counter
        c = Counter()
        for g in genes_:
            for grp in str(gmap.get(g, "")).split("|"):
                if grp.strip():
                    c[grp.strip()] += 1
        rep[f"B2_groups_{label}_top200"] = c.most_common(8)

    # B3: lineage consistency
    cors = []
    lins = {}
    for lineage in sorted(set(lmap.values())):
        o = [m for m in org.index if lmap.get(m) == lineage]
        t = [m for m in two.index if lmap.get(m) == lineage]
        if len(o) >= 5 and len(t) >= 10:
            lins[lineage] = (org.loc[o].mean(axis=0) - two.loc[t].mean(axis=0))
    names = list(lins)
    for i in range(len(names)):
        for k in range(i + 1, len(names)):
            a, b = lins[names[i]], lins[names[k]]
            m = np.isfinite(a.values) & np.isfinite(b.values)
            cors.append(stats.spearmanr(a.values[m], b.values[m]).statistic)
    rep["B3_lineages"] = names
    rep["B3_pairwise_disp_rho_median"] = round(float(np.median(cors)), 4) if cors else None
    rep["B3_pairwise_disp_rho_range"] = [round(float(np.min(cors)), 3), round(float(np.max(cors)), 3)] if cors else None

    (ROOT / "generations/recomb2.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1)[:3000])


if __name__ == "__main__":
    main()
