#!/usr/bin/env python3
"""Round 3: mevalonate/sterol dependency gain - medium or format?
C1: minipool serum-free(OPAC) vs serum(RPMI/FBS) deltas, same format.
C2: 26Q3 same-model media pairs split by SerumFreeMedia: pathway delta.
C3: pathway expression shift organoid vs 2D; SREBF targets coherence.
C4: Wnt-pathway displacement snapshot.
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
WNT = ["FZD1", "FZD2", "FZD5", "FZD7", "LRP5", "LRP6", "CTNNB1", "APC", "AXIN1",
       "RSPO1", "RSPO2", "RSPO3", "LGR5", "PORCN", "WLS", "TCF7L2"]


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
    # C1 minipool: within (model, format): serum-free - serum delta
    sm = pd.read_csv(ROOT / "data/minipool/minipool_screen_metadata.csv")
    ge = pd.read_csv(ROOT / "data/minipool/minipool_chronos_gene_effects.csv", index_col=0)
    sm = sm[sm.cell_line_name.isin(ge.index)].set_index("cell_line_name")
    deltas = []
    for (model, fmt_), g in sm.groupby(["DepMap ID", "Growth Format"]):
        sf = [s for s in g.index if g.loc[s, "Serum status"] == "Serum-free"]
        se = [s for s in g.index if g.loc[s, "Serum status"] == "Serum"]
        if sf and se:
            deltas.append((ge.loc[sf].mean(axis=0) - ge.loc[se].mean(axis=0)))
    if deltas:
        Dser = pd.concat(deltas, axis=1)
        mev_in = [g for g in MEV if g in Dser.index]
        rep["C1_pairs"] = int(Dser.shape[1])
        rep["C1_mev_mean_delta_serumfree_minus_serum"] = round(float(Dser.loc[mev_in].values.mean()), 4)
        rep["C1_allgene_mean_abs_delta"] = round(float(np.abs(Dser.values).mean()), 4)
        # rank of mev mean delta among all genes' mean deltas
        md = Dser.mean(axis=1)
        rep["C1_mev_genes"] = {g: round(float(md[g]), 3) for g in mev_in}
        rep["C1_mev_mean_rank_pct"] = round(float((md < md[mev_in].mean()).mean()), 4)

    # C2 26Q3 media pairs by serum-free status
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
    med = dict(zip(mc.ModelConditionID, mc.FormulationID.str.strip()))
    sfm = dict(zip(mc.ModelConditionID, mc.SerumFreeMedia.str.strip()))
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA") & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Format"] = ok.ModelConditionID.map(fmt)
    ok["Medium"] = ok.ModelConditionID.map(med)
    ok["SF"] = ok.ModelConditionID.map(sfm)
    scr = (ok.groupby("ScreenID")
           .agg(ModelID=("ModelID", "first"), Format=("Format", "first"), Medium=("Medium", "first"),
                SF=("SF", "first"), Library=("Library", "first")).reset_index())
    scr = scr[(scr.Format == "adherent") & (~scr.ModelID.map(patient).isin(reserved))]
    rep["C2_serumfree_values"] = {str(k): int(v) for k, v in scr.SF.value_counts().items()}
    pair_rows = []
    for model, g in scr.groupby("ModelID"):
        sf_screens = g[g.SF.str.lower().isin(["true", "yes"])].ScreenID.tolist()
        se_screens = g[g.SF.str.lower().isin(["false", "no"])].ScreenID.tolist()
        if sf_screens and se_screens:
            pair_rows.append((model, sf_screens, se_screens))
    rep["C2_serumpair_models"] = len(pair_rows)
    if pair_rows:
        need = {s for _, a, b in pair_rows for s in a + b}
        SGE = load_rows(DL / "ScreenGeneEffect.csv", need)
        ds = []
        for model, a, b in pair_rows:
            a = [s for s in a if s in SGE.index]
            b = [s for s in b if s in SGE.index]
            if a and b:
                ds.append(SGE.loc[a].mean(axis=0) - SGE.loc[b].mean(axis=0))
        Dm = pd.concat(ds, axis=1)
        mev_in = [g for g in MEV if g in Dm.index]
        rep["C2_pairs_used"] = int(Dm.shape[1])
        rep["C2_mev_mean_delta"] = round(float(Dm.loc[mev_in].values.mean()), 4)
        md = Dm.mean(axis=1)
        rep["C2_mev_mean_rank_pct"] = round(float((md < md[mev_in].mean()).mean()), 4)
        rep["C2_mev_genes"] = {g: round(float(md[g]), 3) for g in mev_in}

    # C3/C4 via recomb2-style panels: reuse GE quick loads
    org_m = sorted(set(ok[ok.Format.isin(["dome", "spheroid"])].ModelID))
    org_m = [m for m in org_m if patient(m) not in reserved]
    two_m = sorted(set(scr.ModelID))
    GE = load_rows(DL / "CRISPRGeneEffect.csv", set(org_m) | set(two_m))
    org = GE.loc[[m for m in org_m if m in GE.index]]
    two = GE.loc[[m for m in two_m if m in GE.index]]
    disp = org.mean(axis=0) - two.mean(axis=0)
    mev_in = [g for g in MEV if g in GE.columns]
    rep["C3_mev_disp_mean"] = round(float(disp[mev_in].mean()), 4)
    rep["C3_mev_disp_rank_pct"] = round(float((disp < disp[mev_in].mean()).mean()), 4)
    # per-organoid-model mev score (mean disp contribution)
    mev_score = org[mev_in].mean(axis=1) - two[mev_in].mean(axis=0).mean()
    rep["C3_mev_score_frac_negative"] = round(float((mev_score < 0).mean()), 3)
    wnt_in = [g for g in WNT if g in GE.columns]
    rep["C4_wnt_disp"] = {g: round(float(disp[g]), 3) for g in wnt_in}
    (ROOT / "generations/recomb3.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps(rep, indent=1)[:2800])


if __name__ == "__main__":
    main()
