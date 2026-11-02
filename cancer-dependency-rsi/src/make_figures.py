#!/usr/bin/env python3
"""Manuscript figures + survivor-candidate table from v2 artifacts."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "manuscript" / "figures"
FIG.mkdir(exist_ok=True)


def main():
    nrm = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    raw = pd.read_csv(ROOT / "generations/medium_attribution_v2_raw.csv", index_col=0)
    hits = nrm[nrm.flag != "not_a_hit"]

    # Fig 1: attribution scatters
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    for ax, col, title in ((axes[0], "A_adh", "Adherent, organoid formulation family (no dome)"),
                           (axes[1], "F_dome", "Dome vs adherent (within organoid-medium family)")):
        m = hits.flag == "medium_attributable"
        fm = hits.flag == "format_candidate"
        ax.scatter(hits.loc[~(m | fm), "D_org"], hits.loc[~(m | fm), col], s=14, c="0.6", label="unresolved")
        ax.scatter(hits.loc[m, "D_org"], hits.loc[m, col], s=14, c="#c0392b", label="medium-consistent")
        ax.scatter(hits.loc[fm, "D_org"], hits.loc[fm, col], s=60, c="#2471a3", marker="D", label="format candidate")
        lim = 1.15
        ax.plot([-lim, lim], [-lim, lim], "k--", lw=0.8)
        ax.axhline(0, color="0.8", lw=0.6); ax.axvline(0, color="0.8", lw=0.6)
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
        ax.set_xlabel("D: dome organoid medium vs FBS 2D (Δ norm. Chronos)")
        ax.set_title(title, fontsize=10)
        for g in ("SQLE", "MSMO1", "FASN", "ALAS1", "EFTUD2", "RPL3", "ITGB1", "LSM7"):
            if g in hits.index:
                ax.annotate(g, (hits.loc[g, "D_org"], hits.loc[g, col]), fontsize=7,
                            xytext=(3, 3), textcoords="offset points",
                            bbox=dict(facecolor="white", alpha=0.8, edgecolor="none", pad=1.0))
    axes[0].set_ylabel("contrast Δ (norm. Chronos)")
    axes[0].legend(fontsize=8, loc="lower right")
    fig.tight_layout(); fig.savefig(FIG / "fig1_attribution.png", dpi=200); plt.close(fig)

    # Fig 2: weakening panels, Broad contrasts + Sanger depth-scaled ratios
    ctrl = pd.read_csv(ROOT / "data/raw/sanger_figshare/control-genes_organoids.csv")
    SPL = sorted(ctrl.loc[ctrl.essentiality == "SPLICEOSOME", "gene"].astype(str))
    RIBO = sorted(ctrl.loc[ctrl.essentiality == "RIBOSOMAL", "gene"].astype(str))
    from medium_attribution_v2 import MEV
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    x = np.arange(3); w = 0.2
    for i, col in enumerate(("D_org", "A_adh", "F_dome", "S_tsm")):
        vals = [raw.loc[[g for g in p if g in raw.index], col].median() for p in (MEV, SPL, RIBO)]
        axes[0].bar(x + (i - 1.5) * w, vals, w, label=col)
    axes[0].set_xticks(x); axes[0].set_xticklabels(["mevalonate\n(gain)", "spliceosome\n(curated, loss)", "ribosomal\n(curated, loss)"])
    axes[0].set_ylabel("median Δ raw Chronos (Broad)")
    axes[0].axhline(0, color="k", lw=0.6); axes[0].legend(fontsize=8)
    ess = json.loads((ROOT / "generations/sanger_essdepth_v1.json").read_text())
    cur = json.loads((ROOT / "generations/panels_curated_v1.json").read_text())["sanger"]
    cats = ["essential depth\n(|LFC|)", "spliceosome /\ndepth (curated)", "ribosomal /\ndepth (curated)"]
    org_v = [abs(ess["organoid_table6"]["ess_median_lfc"]), cur["SPLICEOSOME"]["scaled_org"],
             cur["RIBOSOMAL"]["scaled_org"]]
    d2_v = [abs(ess["2d_essmatrix"]["ess_median_lfc"]), cur["SPLICEOSOME"]["scaled_2d"],
            cur["RIBOSOMAL"]["scaled_2d"]]
    axes[1].bar(x - 0.15, org_v, 0.3, label="Sanger organoids")
    axes[1].bar(x + 0.15, d2_v, 0.3, label="Sanger 2D lines")
    axes[1].set_xticks(x); axes[1].set_xticklabels(cats, fontsize=8)
    axes[1].set_ylabel("median |LFC| or ratio"); axes[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(FIG / "fig2_weakening.png", dpi=200); plt.close(fig)

    # Fig 3: published catalogue fractions (from v2 json + drill numbers recomputed)
    rep = json.loads((ROOT / "generations/medium_attribution_v2.json").read_text())
    b = pd.read_csv(ROOT / "data/raw/broad_figshare/organoids_vs_2d_gene_dependency_tests_full.csv")
    b["gene"] = b.Dependency.str.split(" (", regex=False).str[0]
    j = b.set_index("gene").join(nrm[["flag"]], how="inner")
    sg = pd.read_excel(ROOT / "data/raw/sanger_supp/supplementary_table_4_revision.xlsx",
                       sheet_name="organoid_core_fitness_genes")

    def cat_flags(df):
        vc = df.flag.value_counts(normalize=True)
        return [vc.get("medium_attributable", 0), vc.get("unresolved", 0),
                vc.get("format_candidate", 0), vc.get("not_a_hit", 0)]

    cats, vals = [], []
    g = j[(j.MannWhitneyFDR < 0.05) & (j.MeanDifference < -0.25)]; cats.append(f"Broad pub. gains\n(n={len(g)})"); vals.append(cat_flags(g))
    g = j[(j.MannWhitneyFDR < 0.01) & (j.MeanDifference < -0.5)]; cats.append(f"Broad strict gains\n(n={len(g)})"); vals.append(cat_flags(g))
    g = j[(j.MannWhitneyFDR < 0.05) & (j.MeanDifference > 0.25)]; cats.append(f"Broad pub. losses\n(n={len(g)})"); vals.append(cat_flags(g))
    for label, m in (("Sanger exclusive", sg.exclusive_organoids == "Yes"),
                     ("Sanger headline-18", sg.exclusive_organoids_exclude_CommonEssentials == "Yes")):
        genes = [x for x in sg.loc[m, "gene"].astype(str) if x in nrm.index]
        cats.append(f"{label}\n(n={len(genes)})"); vals.append(cat_flags(nrm.loc[genes]))
    vals = np.array(vals)
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    bottom = np.zeros(len(cats))
    for i, (lab, c) in enumerate(zip(["medium-consistent", "unresolved", "format candidate", "not a hit (lineage-adj.)"],
                                     ["#c0392b", "#e67e22", "#2471a3", "0.75"])):
        ax.bar(cats, vals[:, i], bottom=bottom, label=lab, color=c); bottom += vals[:, i]
    ax.set_ylabel("fraction of published list"); ax.set_ylim(0, 1); ax.legend(fontsize=8)
    ax.tick_params(axis="x", labelsize=8)
    fig.tight_layout(); fig.savefig(FIG / "fig3_catalogues.png", dpi=200); plt.close(fig)

    # Survivor candidates: unresolved hits, least medium-like first; + format-leaning point estimates
    un = hits[hits.flag == "unresolved"].copy()
    fmt_lean = hits[(hits.flag != "medium_attributable") & (np.sign(hits.F_dome) == np.sign(hits.D_org))
                    & (hits.ratio_F >= 0.5)]
    s3 = json.loads((ROOT / "generations/sanger_direct_check_v3.json").read_text())
    dpct = {g: v["delta_pct"] for g, v in s3["headline18"]["per_gene"].items()}
    un["sanger_headline_dpct"] = [dpct.get(g) for g in un.index]
    un["format_leaning_point_estimate"] = un.index.isin(fmt_lean.index)
    cols = ["D_org", "D_org_q", "A_adh", "ratio_A", "ratio_A_lo", "ratio_A_hi", "F_dome", "F_dome_q",
            "ratio_F", "S_tsm", "serumfree_support", "format_leaning_point_estimate", "sanger_headline_dpct"]
    un.sort_values("ratio_A")[cols].to_csv(ROOT / "generations/survivor_candidates_v1.csv", float_format="%.4f")
    print("figures written; survivors:", len(un), "format-leaning:", len(fmt_lean))
    print(un.sort_values("ratio_A").head(12)[["D_org", "ratio_A", "F_dome", "ratio_F"]].round(3).to_string())


if __name__ == "__main__":
    main()
