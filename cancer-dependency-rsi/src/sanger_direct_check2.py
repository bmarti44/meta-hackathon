#!/usr/bin/env python3
"""Sanger direct check v2: organoid vs 2D columns split within the combined
Sanger EssMatrix (930 screens). Organoid ACH columns identified via
passports synonyms (HCM-SANG -> BROAD_ID) x organoid covariates sample_IDs.
Supersedes sanger_direct_check_v1 (which pooled all screens).
"""
import json

import pandas as pd
import pyreadr

from medium_attribution import ROOT
from medium_attribution_v2 import HEME, MEV, RIBO, SPL


def load(path):
    m = list(pyreadr.read_r(str(path)).values())[0]
    m.index = [str(g).split(" ")[0] for g in m.index]
    return m[~m.index.duplicated()].apply(pd.to_numeric, errors="coerce")


def main():
    out = {}
    pp = pd.read_csv(ROOT / "data/passports_model_list_20260921.csv", dtype=str).fillna("")
    hcm2ach = {}
    for _, r in pp.iterrows():
        for tok in str(r.synonyms).replace(";", "|").split("|"):
            tok = tok.strip()
            if tok.startswith("HCM-SANG") and r.BROAD_ID:
                hcm2ach[tok] = r.BROAD_ID
    cov = pd.read_csv(ROOT / "data/raw/sanger_figshare/data_covariates_ALL-organoids.csv", dtype=str)
    org_ach = sorted({hcm2ach[s] for s in cov.sample_ID if s in hcm2ach})
    out["n_covariate_samples"] = int(cov.sample_ID.nunique())
    out["n_mapped_to_ach"] = len(org_ach)

    lfc = load(ROOT / "data/quarantine/07_EssMatrix_qnorm_corrected_logFCs.RData")
    org_cols = [c for c in org_ach if c in lfc.columns]
    d2_cols = [c for c in lfc.columns if c not in set(org_cols)]
    out["n_organoid_cols"] = len(org_cols)
    out["n_2d_cols"] = len(d2_cols)

    pct = lfc.rank(axis=0, pct=True)
    panels = {"mevalonate": MEV, "heme": HEME, "splice_panel": SPL, "ribo_panel": RIBO}
    out["panels"] = {}
    for name, genes in panels.items():
        g = [x for x in genes if x in pct.index]
        o = pct.loc[g, org_cols].median(axis=0)
        t = pct.loc[g, d2_cols].median(axis=0)
        out["panels"][name] = {"n_genes": len(g),
                               "pct_organoid_median": float(o.median()),
                               "pct_2d_median": float(t.median()),
                               "lfc_organoid_median": float(lfc.loc[g, org_cols].median(axis=0).median()),
                               "lfc_2d_median": float(lfc.loc[g, d2_cols].median(axis=0).median())}

    b = load(ROOT / "data/raw/sanger_figshare/07_EssMatrix_bDepletionsB2.Rdata")
    fo = b[org_cols].mean(axis=1)
    ft = b[[c for c in d2_cols if c in b.columns]].mean(axis=1)
    sg = pd.read_excel(ROOT / "data/raw/sanger_supp/supplementary_table_4_revision.xlsx",
                       sheet_name="organoid_core_fitness_genes")
    for label, m in (("exclusive97", sg.exclusive_organoids == "Yes"),
                     ("headline18", sg.exclusive_organoids_exclude_CommonEssentials == "Yes")):
        genes = [g for g in sg.loc[m, "gene"].astype(str) if g in fo.index]
        d = pd.DataFrame({"freq_org": fo[genes], "freq_2d": ft[genes]})
        out[label] = {"n": len(genes), "freq_org_median": float(d.freq_org.median()),
                      "freq_2d_median": float(d.freq_2d.median()),
                      "frac_org_freq_lt_0.5": float((d.freq_org < 0.5).mean()),
                      "per_gene": d.round(3).to_dict("index") if label == "headline18" else
                      d.nsmallest(8, "freq_org").round(3).to_dict("index")}
    mev = pd.DataFrame({"freq_org": fo[[g for g in MEV if g in fo.index]],
                        "freq_2d": ft[[g for g in MEV if g in ft.index]]})
    out["mevalonate_freq"] = mev.round(3).to_dict("index")

    (ROOT / "generations/sanger_direct_check_v2.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "mevalonate_freq"}, indent=1)[:4000])
    print("MEV freq org vs 2D (median):", float(mev.freq_org.median()), float(mev.freq_2d.median()))


if __name__ == "__main__":
    main()
