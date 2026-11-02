#!/usr/bin/env python3
"""Harmonized Lock-S estimand replicated in Broad 26Q3 organoids.

Frozen pieces reused verbatim: 207 genes, L_g, AdherentMean reference
ordering, base_strength (lock_s/covariates.csv); estimator = Pearson
correlation of OLS rank residuals (partial Spearman, no reranking).
D_g: per organoid model, within-207 average ranks of Chronos;
|rank - reference_rank|/(G-1); averaged within patient, patients equal.
Panels: dev (non-reserved patients) | heldout (sequestered patients).
"""
import csv
import json
import sys
import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
DL = Path.home() / "Downloads"


def ranks_avg(x):
    return stats.rankdata(x, method="average")


def partial_spearman(y, x, z):
    ry, rx, rz = ranks_avg(y), ranks_avg(x), ranks_avg(z)
    Z = np.column_stack([np.ones_like(rz), rz])
    ey = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
    ex = rx - Z @ np.linalg.lstsq(Z, rx, rcond=None)[0]
    return float(np.corrcoef(ex, ey)[0, 1])


def compute_D(org, genes, ref_rank, pats):
    """org: models x genes Chronos (207 cols in genes order). Returns D_g."""
    G = len(genes)
    Dmat = np.empty_like(org, dtype=np.float64)
    for i in range(org.shape[0]):
        Dmat[i] = np.abs(ranks_avg(org[i]) - ref_rank) / (G - 1)
    # average within patient, then patients equally
    by = {}
    for i, p in enumerate(pats):
        by.setdefault(p, []).append(i)
    patient_means = np.vstack([Dmat[idx].mean(axis=0) for idx in by.values()])
    return patient_means.mean(axis=0), patient_means, list(by.keys())


def main():
    panel = sys.argv[1] if len(sys.argv) > 1 else "dev"
    cov = pd.read_csv(ROOT / "lock_s/covariates.csv")
    cov = cov[cov.in_207.astype(str).str.lower().isin(["true", "1"])].reset_index(drop=True)
    genes = list(cov.gene_broad)
    L = cov.L.values.astype(float)
    base = cov.base_strength.values.astype(float)
    ref_rank = ranks_avg(cov.AdherentMean.values.astype(float))

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
    ex = lambda s, v: s.str.strip().str.lower() == v
    ok = seq[ex(seq.PassesQC, "true") & (seq.ModelID != "pDNA")
             & ex(seq.ExcludeFromCRISPRCombined, "false")]
    ok = ok[~ex(ok.DrugTreated, "true") & ~ex(ok.IsEngineered, "true")].copy()
    ok["Format"] = ok.ModelConditionID.map(fmt)
    org_models = sorted(ok[ok.Format.isin(["dome", "spheroid"])].ModelID.unique())
    keep = [m for m in org_models
            if (patient(m) in reserved) == (panel == "heldout") and patient(m)]

    chunks = []
    for ch in pd.read_csv(DL / "CRISPRGeneEffect.csv", index_col=0, chunksize=250):
        hit = ch.index.intersection(keep)
        if len(hit):
            sub = ch.loc[hit]
            sub.columns = [c.split(" (")[0] for c in sub.columns]
            chunks.append(sub[genes].astype(np.float64))
    GE = pd.concat(chunks).loc[keep]
    assert list(GE.columns) == genes
    pats = [patient(m) for m in GE.index]
    D, pmeans, upats = compute_D(GE.values, genes, ref_rank, pats)
    rho = partial_spearman(D, L, base)
    raw = float(stats.spearmanr(D, L).statistic)

    rng = np.random.default_rng(20261029)
    boots = []
    for _ in range(5000):
        pick = rng.integers(0, len(upats), size=len(upats))
        boots.append(partial_spearman(pmeans[pick].mean(axis=0), L, base))
    out = {"panel": panel, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "n_models": int(GE.shape[0]), "n_patients": len(upats), "n_genes": len(genes),
           "rho_partial_frozen_estimator": rho, "rho_raw_spearman": raw,
           "patient_boot95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
           "locks_reference": "Sanger Lock-S: rho=-0.1458 [-0.175,-0.114] BOUND",
           "kill_criterion": "held-out 95% CI inside (-0.20,+0.20) terminates material-association claim"}
    tag = "dev" if panel == "dev" else "heldout"
    (ROOT / f"generations/harmonized_{tag}.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
