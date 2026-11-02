#!/usr/bin/env python3
"""Sanger essential-depth internal control (generates sanger_essdepth_v1.json).
Reference-essential median LFC in Sanger organoids (table 6) vs 2D lines
(EssMatrix), with hand-panel splice/ribo depth-scaled ratios. Curated-set
versions live in panels_curated.py; this script exists so the essdepth
artifact has a generator in the source tree (Astra r1 #12).
"""
import json
import zipfile

import pandas as pd
import pyreadr

from medium_attribution import ROOT
from medium_attribution_v2 import RIBO, SPL


def main():
    ctrl = pd.read_csv(ROOT / "data/raw/sanger_figshare/control-genes_organoids.csv")
    ess = ctrl.loc[ctrl.essentiality == "curated_BAGEL_essential", "gene"].astype(str).tolist()
    non = ctrl.loc[ctrl.essentiality == "curated_BAGEL_non_essential", "gene"].astype(str).tolist()
    with zipfile.ZipFile(ROOT / "data/raw/sanger_figshare/S2_Supplementary_Tables.zip") as z:
        with z.open("supplementary_table_6_revision.csv") as f:
            t6 = pd.read_csv(f, sep=r"\s+", usecols=["sample_ID", "gene", "LFC"], dtype={"LFC": "float32"})
    org = t6.pivot_table(index="gene", columns="sample_ID", values="LFC", aggfunc="mean")
    lfc = list(pyreadr.read_r(str(ROOT / "data/quarantine/07_EssMatrix_qnorm_corrected_logFCs.RData")).values())[0]
    lfc.index = [str(g).split(" ")[0] for g in lfc.index]
    d2 = lfc[~lfc.index.duplicated()].apply(pd.to_numeric, errors="coerce")
    res = {}
    for nm, M in (("organoid_table6", org), ("2d_essmatrix", d2)):
        e = [g for g in ess if g in M.index]
        n = [g for g in non if g in M.index]
        r = {"n_ess_ref": len(e), "ess_median_lfc": float(M.loc[e].median(axis=0).median()),
             "non_median_lfc": float(M.loc[n].median(axis=0).median()) if n else None,
             "splice_median_lfc": float(M.loc[[g for g in SPL if g in M.index]].median(axis=0).median()),
             "ribo_median_lfc": float(M.loc[[g for g in RIBO if g in M.index]].median(axis=0).median())}
        r["splice_over_essdepth"] = r["splice_median_lfc"] / r["ess_median_lfc"]
        r["ribo_over_essdepth"] = r["ribo_median_lfc"] / r["ess_median_lfc"]
        res[nm] = r
    (ROOT / "generations/sanger_essdepth_v1.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
