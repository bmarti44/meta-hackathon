#!/usr/bin/env python3
"""Build itsthemedium.com static site data from v2r2 artifacts."""
import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
(SITE / "data").mkdir(parents=True, exist_ok=True)
(SITE / "assets").mkdir(parents=True, exist_ok=True)

FLAG = {"medium_attributable": 1, "unresolved": 2, "format_candidate": 3, "not_a_hit": 0}


def r3(x):
    return None if pd.isna(x) else round(float(x), 3)


def main():
    t = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    raw = pd.read_csv(ROOT / "generations/medium_attribution_v2_raw.csv", index_col=0)
    boot = pd.read_csv(ROOT / "generations/medium_attribution_v2_boot_freq.csv", index_col=0).iloc[:, 0]
    rep = json.loads((ROOT / "generations/medium_attribution_v2.json").read_text())
    held = json.loads((ROOT / "generations/medium_attribution_v2_heldout.json").read_text())
    bootj = json.loads((ROOT / "generations/medium_attribution_v2_boot.json").read_text())
    loo = json.loads((ROOT / "generations/medium_attribution_v2_loo.json").read_text())

    # published-list tags
    tags = {}
    b = pd.read_csv(ROOT / "data/raw/broad_figshare/organoids_vs_2d_gene_dependency_tests_full.csv")
    b["gene"] = b.Dependency.str.split(" (", regex=False).str[0]
    for _, row in b.iterrows():
        tg = []
        if row.MannWhitneyFDR < 0.05 and row.MeanDifference < -0.25:
            tg.append("broad_gain")
        if row.MannWhitneyFDR < 0.05 and row.MeanDifference > 0.25:
            tg.append("broad_loss")
        if row.MannWhitneyFDR < 0.01 and row.MeanDifference < -0.5:
            tg.append("broad_strict")
        if tg:
            tags[row.gene] = tg
    sg = pd.read_excel(ROOT / "data/raw/sanger_supp/supplementary_table_4_revision.xlsx",
                       sheet_name="organoid_core_fitness_genes")
    for label, m in (("sanger18", sg.exclusive_organoids_exclude_CommonEssentials == "Yes"),
                     ("sanger97", sg.exclusive_organoids == "Yes")):
        for g in sg.loc[m, "gene"].astype(str):
            tags.setdefault(g, []).append(label)
    surv = pd.read_csv(ROOT / "generations/survivor_candidates_v1.csv", index_col=0)

    genes = []
    for g, row in t.iterrows():
        genes.append({
            "g": g, "D": r3(row.D_org), "A": r3(row.A_adh), "F": r3(row.F_dome), "S": r3(row.S_tsm),
            "f": FLAG.get(row.flag, 0), "ff": FLAG.get(row.flag_fdr, 0),
            "rA": r3(row.ratio_A), "rAlo": r3(row.ratio_A_lo), "rAhi": r3(row.ratio_A_hi),
            "rF": r3(row.ratio_F), "Dq": float(row.D_org_q), "Ap": float(row.A_adh_p), "Fp": float(row.F_dome_p),
            "Draw": r3(raw.loc[g, "D_org"]) if g in raw.index else None,
            "bf": (round(float(boot[g]), 3) if g in boot.index else None),
            "tags": tags.get(g, []),
        })
    (SITE / "data/genes.json").write_text(json.dumps(genes, separators=(",", ":")))

    hits = t[t.flag != "not_a_hit"]
    pub = rep["published_hits"]
    stats = {
        "n_genes": int(len(t)), "n_hits": int(len(hits)),
        "n_gains": int((hits.D_org < 0).sum()), "n_losses": int((hits.D_org > 0).sum()),
        "n_medium": int((hits.flag == "medium_attributable").sum()),
        "frac_medium_gains": rep["norm"]["gains"]["frac_medium_of_hits"],
        "frac_medium_losses": rep["norm"]["losses"]["frac_medium_of_hits"],
        "hc3_gains": rep["norm"]["hc3_sensitivity"]["gains"]["frac_medium_of_hits"],
        "hc3_losses": rep["norm"]["hc3_sensitivity"]["losses"]["frac_medium_of_hits"],
        "slope_gains": rep["norm"]["gains"]["slope_A_on_D"], "slope_losses": rep["norm"]["losses"]["slope_A_on_D"],
        "boot_slope_ci": bootj["slope_A_on_D"]["ci95"], "boot_slope_med": bootj["slope_A_on_D"]["median"],
        "boot_freq_ge_half": bootj["frac_hits_boot_freq_ge_0.5"],
        "heldout_slope": held["norm"]["medium_attributable"]["slope_Dheld_on_Ddev"],
        "heldout_corr": held["norm"]["medium_attributable"]["corr_D"],
        "loo_min_retention": loo["summary"]["flag_retention_min"],
        "loo_slope_range": [loo["summary"]["slope_min"], loo["summary"]["slope_max"]],
        "broad_gain_flags": pub["broad_published[FDR<0.05 & diff<-0.25]"]["flags"],
        "broad_strict_flags": pub["broad_published[FDR<0.01 & diff<-0.5]"]["flags"],
        "sanger": {k: pub["sanger_organoid_core_fitness"].get(k)
                   for k in ("n_listed", "n_in_broad_table", "flags", "n_also_our_hit")},
        "format_genes": t[t.flag == "format_candidate"].index.tolist(),
        "survivors_top": [{"g": g, "D": r3(surv.loc[g, "D_org"]), "rA": r3(surv.loc[g, "ratio_A"]),
                           "rF": r3(surv.loc[g, "ratio_F"])} for g in surv.index[:15]],
        "top_medium_gains": [{"g": g, "D": r3(t.loc[g, "D_org"]), "rA": r3(t.loc[g, "ratio_A"])}
                             for g in hits[(hits.D_org < 0) & (hits.flag == "medium_attributable")].sort_values("D_org").index[:12]],
        "generated": rep["timestamp"], "revision": rep.get("revision", ""),
    }
    (SITE / "data/stats.json").write_text(json.dumps(stats, indent=1))

    for src, dst in (("manuscript/figures/fig1_attribution.png", "assets/fig1.png"),
                     ("manuscript/figures/fig2_weakening.png", "assets/fig2.png"),
                     ("manuscript/figures/fig3_catalogues.png", "assets/fig3.png"),
                     ("release_v1/manuscript_v2.pdf", "assets/manuscript_v2.pdf"),
                     ("generations/medium_attribution_v2_norm.csv", "assets/medium_attribution_v2_norm.csv"),
                     ("generations/medium_attribution_v2_raw.csv", "assets/medium_attribution_v2_raw.csv"),
                     ("generations/survivor_candidates_v1.csv", "assets/survivor_candidates_v1.csv"),
                     ("manuscript/wetlab_proposal_v1.md", "assets/wetlab_proposal_v1.md")):
        shutil.copy(ROOT / src, SITE / dst)
    print("genes:", len(genes), "hits:", stats["n_hits"], "site data bytes:",
          (SITE / "data/genes.json").stat().st_size)


if __name__ == "__main__":
    main()
