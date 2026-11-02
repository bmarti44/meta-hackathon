#!/usr/bin/env python3
"""Sanger-assay direct check (GOAL v4 deliverables 2-3, Herranz-Ors side).

Uses the Sanger organoid LFC matrix (qnorm corrected) and binary depletion
matrix from figshare. Within-model genome-wide percentiles for mevalonate /
spliceosome / ribosome panels vs the assay's own reference essentials, and
per-gene essential-call frequency for the published 'exclusive organoid core
fitness' lists (threshold-fragility check). Exploratory reuse of the spent
cohort assay for new gene-set questions (as in recomb21); no patient-level
held-out claim is made from this cohort.
"""
import json

import numpy as np
import pandas as pd
import pyreadr
from scipy import stats

from medium_attribution import ROOT
from medium_attribution_v2 import HEME, MEV, RIBO, SPL


def load_rdata(path):
    res = pyreadr.read_r(str(path))
    return {k: v for k, v in res.items()}


def to_matrix(obj):
    """pyreadr returns DataFrames for R matrices/data.frames with rownames as index."""
    if isinstance(obj, pd.DataFrame):
        return obj
    raise TypeError(type(obj))


def main():
    out = {}
    lfc_raw = load_rdata(ROOT / "data/quarantine/07_EssMatrix_qnorm_corrected_logFCs.RData")
    out["lfc_objects"] = list(lfc_raw.keys())
    lfc = to_matrix(list(lfc_raw.values())[0])
    # orient: genes x models or models x genes? pick the axis containing gene symbols
    def geneish(labels):
        s = set(map(str, labels))
        return len(s & set(MEV + SPL + RIBO))
    if geneish(lfc.columns) > geneish(lfc.index):
        lfc = lfc.T
    lfc.index = [str(g).split(" ")[0] for g in lfc.index]
    lfc = lfc[~lfc.index.duplicated()].apply(pd.to_numeric, errors="coerce")
    out["lfc_shape_genes_x_models"] = list(lfc.shape)

    ctrl = pd.read_csv(ROOT / "data/raw/sanger_figshare/control-genes_organoids.csv")
    out["control_file_columns"] = list(ctrl.columns)
    out["control_file_head"] = ctrl.head(3).to_dict("records").__str__()[:400]

    # within-model percentile of each gene (rank of LFC; low LFC = essential = low pct)
    pct = lfc.rank(axis=0, pct=True)
    panels = {"mevalonate": MEV, "heme": HEME, "splice_panel": SPL, "ribo_panel": RIBO}
    panel_pct = {}
    for name, genes in panels.items():
        g = [x for x in genes if x in pct.index]
        per_model = pct.loc[g].median(axis=0)
        panel_pct[name] = {"n_genes": len(g), "median_pct_across_models": float(per_model.median()),
                           "iqr": [float(per_model.quantile(0.25)), float(per_model.quantile(0.75))]}
    out["panel_percentiles"] = panel_pct

    # binary depletions: essential-call frequency per gene
    bin_raw = load_rdata(ROOT / "data/raw/sanger_figshare/07_EssMatrix_bDepletionsB2.Rdata")
    out["binary_objects"] = list(bin_raw.keys())
    b = to_matrix(list(bin_raw.values())[0])
    if geneish(b.columns) > geneish(b.index):
        b = b.T
    b.index = [str(g).split(" ")[0] for g in b.index]
    b = b[~b.index.duplicated()].apply(pd.to_numeric, errors="coerce")
    out["binary_shape"] = list(b.shape)
    out["binary_value_counts"] = pd.Series(b.values.ravel()).value_counts(dropna=True).head(5).to_dict().__str__()
    freq = b.mean(axis=1)

    sg = pd.read_excel(ROOT / "data/raw/sanger_supp/supplementary_table_4_revision.xlsx",
                       sheet_name="organoid_core_fitness_genes")
    for label, m in (("exclusive97", sg.exclusive_organoids == "Yes"),
                     ("headline18", sg.exclusive_organoids_exclude_CommonEssentials == "Yes"),
                     ("all751", pd.Series(True, index=sg.index))):
        genes = sg.loc[m, "gene"].astype(str)
        f = freq.reindex([g for g in genes if g in freq.index]).dropna()
        out[label] = {"n": int(m.sum()), "n_in_binary": int(len(f)),
                      "essential_freq_median": float(f.median()) if len(f) else None,
                      "frac_freq_lt_0.5": float((f < 0.5).mean()) if len(f) else None,
                      "frac_freq_lt_0.25": float((f < 0.25).mean()) if len(f) else None,
                      "lowest_freq_genes": f.nsmallest(10).round(3).to_dict()}
    mev_f = freq.reindex([g for g in MEV if g in freq.index]).dropna()
    out["mevalonate_freq"] = {"median": float(mev_f.median()), "genes": mev_f.round(3).to_dict()}

    (ROOT / "generations/sanger_direct_check_v1.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out, indent=1, default=str)[:4500])


if __name__ == "__main__":
    main()
