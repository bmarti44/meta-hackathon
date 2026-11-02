#!/usr/bin/env python3
"""Weakening panels with curated BAGEL reference sets (Sanger control-genes
file categories) instead of the small hand-picked panels. Broad side from
v2 tables; Sanger side depth-scaled from table 6 + EssMatrix."""
import json
import zipfile

import pandas as pd
import pyreadr

from medium_attribution import ROOT


def main():
    ctrl = pd.read_csv(ROOT / "data/raw/sanger_figshare/control-genes_organoids.csv")
    sets = {k: sorted(ctrl.loc[ctrl.essentiality == k, "gene"].astype(str))
            for k in ("SPLICEOSOME", "RIBOSOMAL", "PROTEASOME", "RNA_POLYMERASE",
                      "DNA_REPLICATION", "HISTONES", "curated_BAGEL_essential")}
    out = {"set_sizes": {k: len(v) for k, v in sets.items()}}

    raw = pd.read_csv(ROOT / "generations/medium_attribution_v2_raw.csv", index_col=0)
    nrm = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    out["broad"] = {}
    for name, genes in sets.items():
        g = [x for x in genes if x in raw.index]
        out["broad"][name] = {
            "n": len(g),
            "D_raw_median": float(raw.loc[g, "D_org"].median()),
            "A_raw_median": float(raw.loc[g, "A_adh"].median()),
            "F_raw_median": float(raw.loc[g, "F_dome"].median()),
            "S_raw_median": float(raw.loc[g, "S_tsm"].median()),
            "D_norm_median": float(nrm.loc[g, "D_org"].median()),
            "flags_norm": nrm.loc[g, "flag"].value_counts().to_dict()}

    with zipfile.ZipFile(ROOT / "data/raw/sanger_figshare/S2_Supplementary_Tables.zip") as z:
        with z.open("supplementary_table_6_revision.csv") as f:
            t6 = pd.read_csv(f, sep=r"\s+", usecols=["sample_ID", "gene", "LFC"], dtype={"LFC": "float32"})
    org = t6.pivot_table(index="gene", columns="sample_ID", values="LFC", aggfunc="mean")
    lfc = list(pyreadr.read_r(str(ROOT / "data/quarantine/07_EssMatrix_qnorm_corrected_logFCs.RData")).values())[0]
    lfc.index = [str(g).split(" ")[0] for g in lfc.index]
    d2 = lfc[~lfc.index.duplicated()].apply(pd.to_numeric, errors="coerce")
    ess = [g for g in sets["curated_BAGEL_essential"] if g in org.index]
    depth_o = float(org.loc[ess].median(axis=0).median())
    depth_t = float(d2.loc[[g for g in ess if g in d2.index]].median(axis=0).median())
    po, pt = org.rank(axis=0, pct=True), d2.rank(axis=0, pct=True)
    out["sanger"] = {"depth_organoid": depth_o, "depth_2d": depth_t}
    for name, genes in sets.items():
        go = [g for g in genes if g in org.index]
        gt = [g for g in genes if g in d2.index]
        out["sanger"][name] = {
            "n_org": len(go), "n_2d": len(gt),
            "lfc_org_median": float(org.loc[go].median(axis=0).median()),
            "lfc_2d_median": float(d2.loc[gt].median(axis=0).median()),
            "scaled_org": float(org.loc[go].median(axis=0).median() / depth_o),
            "scaled_2d": float(d2.loc[gt].median(axis=0).median() / depth_t),
            "pct_org_median": float(po.loc[go].median(axis=0).median()),
            "pct_2d_median": float(pt.loc[gt].median(axis=0).median())}
    (ROOT / "generations/panels_curated_v1.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1)[:4200])


if __name__ == "__main__":
    main()
