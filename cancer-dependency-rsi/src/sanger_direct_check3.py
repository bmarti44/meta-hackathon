#!/usr/bin/env python3
"""Sanger direct check v3 (correct matrices).

Organoid LFC: Herranz-Ors supplementary table 6 (long format, 162 samples,
streamed from the figshare zip). 2D reference: Sanger EssMatrix qnorm LFC
(930 cell lines). Within-model genome-wide percentiles (processing-robust)
for panels and for the published exclusive/headline gene lists.
Exploratory reuse of the spent cohort (recomb21 precedent); no held-out claim.
"""
import json
import zipfile

import pandas as pd
import pyreadr

from medium_attribution import ROOT
from medium_attribution_v2 import HEME, MEV, RIBO, SPL


def main():
    out = {}
    zpath = ROOT / "data/raw/sanger_figshare/S2_Supplementary_Tables.zip"
    with zipfile.ZipFile(zpath) as z:
        with z.open("supplementary_table_6_revision.csv") as f:
            t6 = pd.read_csv(f, sep=r"\s+", usecols=["sample_ID", "gene", "LFC"], dtype={"LFC": "float32"})
    org = t6.pivot_table(index="gene", columns="sample_ID", values="LFC", aggfunc="mean")
    out["organoid_shape"] = list(org.shape)

    lfc = list(pyreadr.read_r(str(ROOT / "data/quarantine/07_EssMatrix_qnorm_corrected_logFCs.RData")).values())[0]
    lfc.index = [str(g).split(" ")[0] for g in lfc.index]
    d2 = lfc[~lfc.index.duplicated()].apply(pd.to_numeric, errors="coerce")
    out["2d_shape"] = list(d2.shape)

    po = org.rank(axis=0, pct=True)
    pt = d2.rank(axis=0, pct=True)
    panels = {"mevalonate": MEV, "heme": HEME, "splice_panel": SPL, "ribo_panel": RIBO}
    out["panels"] = {}
    for name, genes in panels.items():
        go = [g for g in genes if g in po.index]
        gt = [g for g in genes if g in pt.index]
        out["panels"][name] = {
            "n_org": len(go), "n_2d": len(gt),
            "pct_organoid_median": float(po.loc[go].median(axis=0).median()),
            "pct_2d_median": float(pt.loc[gt].median(axis=0).median()),
            "lfc_organoid_median": float(org.loc[go].median(axis=0).median()),
            "lfc_2d_median": float(d2.loc[gt].median(axis=0).median())}

    med_o = po.median(axis=1)
    med_t = pt.median(axis=1)
    sg = pd.read_excel(ROOT / "data/raw/sanger_supp/supplementary_table_4_revision.xlsx",
                       sheet_name="organoid_core_fitness_genes")
    v2 = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    for label, m in (("exclusive97", sg.exclusive_organoids == "Yes"),
                     ("headline18", sg.exclusive_organoids_exclude_CommonEssentials == "Yes")):
        genes = [g for g in sg.loc[m, "gene"].astype(str) if g in med_o.index and g in med_t.index]
        d = pd.DataFrame({"pct_org": med_o[genes], "pct_2d": med_t[genes]})
        d["delta_pct"] = d.pct_org - d.pct_2d
        d["broad_D"] = v2.D_org.reindex(genes)
        d["broad_flag"] = v2.flag.reindex(genes)
        out[label] = {"n": len(genes), "delta_pct_median": float(d.delta_pct.median()),
                      "frac_stronger_in_organoids": float((d.delta_pct < -0.05).mean()),
                      "frac_weaker_in_organoids": float((d.delta_pct > 0.05).mean()),
                      "per_gene": d.round(3).to_dict("index") if label == "headline18" else
                      d.sort_values("delta_pct").head(10).round(3).to_dict("index") | {"_weakest_": d.sort_values("delta_pct").tail(10).round(3).to_dict("index")}}

    (ROOT / "generations/sanger_direct_check_v3.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: (v if k not in ("headline18",) else {kk: vv for kk, vv in v.items() if kk != "per_gene"})
                      for k, v in out.items()}, indent=1)[:3000])


if __name__ == "__main__":
    main()
