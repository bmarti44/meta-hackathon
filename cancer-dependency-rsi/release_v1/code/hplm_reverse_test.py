#!/usr/bin/env python3
"""HPLM reverse test (Rossiter et al. 2021, PMC8172426 supplements).

Both HPLM and RPMI arms contain dialyzed serum (lipoproteins retained), so
nutrient-formulation change alone should NOT create sterol dependency if our
attribution (serum/lipid absence, not formulation per se) is right.
Delta = HPLM - RPMI gene score (negative = more essential in HPLM).
"""
import json

import numpy as np
import pandas as pd
from scipy import stats

from medium_attribution import ROOT
from medium_attribution_v2 import HEME, MEV

H = ROOT / "data/raw/hplm_rossiter2021"
FASYN = ["FASN", "ACLY", "ACACA", "SCD", "ACSS2"]


def main():
    out = {}
    gw = pd.read_excel(H / "NIHMS1674248-supplement-2.xlsx", sheet_name="GW-Gene Score_2",
                       skiprows=5, usecols="A:D")
    gw.columns = ["gene", "rpmi", "hplm", "zdiff"]
    gw = gw.dropna(subset=["gene"]).set_index("gene")
    gw = gw.apply(pd.to_numeric, errors="coerce").dropna()
    gw["delta"] = gw.hplm - gw.rpmi
    gw["delta_pct"] = gw.delta.rank(pct=True)
    out["gw_n"] = int(len(gw))

    v2 = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    j = gw.join(v2[["D_org", "A_adh", "flag"]], how="inner")
    out["joined_n"] = int(len(j))
    out["corr_delta_Dorg"] = float(j.delta.corr(j.D_org))
    out["corr_delta_Aadh"] = float(j.delta.corr(j.A_adh))
    out["corr_zdiff_Dorg"] = float(j.zdiff.corr(j.D_org))

    ctrl = pd.read_csv(ROOT / "data/raw/sanger_figshare/control-genes_organoids.csv")
    panels = {"mevalonate": MEV, "heme": HEME, "fa_synthesis": FASYN,
              "ribosomal_curated": sorted(ctrl.loc[ctrl.essentiality == "RIBOSOMAL", "gene"].astype(str)),
              "spliceosome_curated": sorted(ctrl.loc[ctrl.essentiality == "SPLICEOSOME", "gene"].astype(str))}
    out["panels"] = {}
    rng = np.random.default_rng(7)
    allv = gw.delta.values
    for name, genes in panels.items():
        g = [x for x in genes if x in gw.index]
        med = float(gw.loc[g, "delta"].median())
        null = [np.median(rng.choice(allv, len(g), replace=False)) for _ in range(2000)]
        z = (med - np.mean(null)) / np.std(null)
        out["panels"][name] = {"n": len(g), "delta_median": med, "null_z": float(z),
                               "median_Dorg_broad": float(j.loc[[x for x in g if x in j.index], "D_org"].median())}
    for g in ("SQLE", "MSMO1", "HMGCR", "LDLR", "UMPS", "FASN", "ALAS1"):
        if g in gw.index:
            out.setdefault("named", {})[g] = {"rpmi": float(gw.loc[g, "rpmi"]), "hplm": float(gw.loc[g, "hplm"]),
                                              "delta": float(gw.loc[g, "delta"]), "zdiff": float(gw.loc[g, "zdiff"])}

    def enrich(sel, flagmask):
        a = int((sel & flagmask).sum()); b = int((sel & ~flagmask).sum())
        c = int((~sel & flagmask).sum()); d = int((~sel & ~flagmask).sum())
        orr, p = stats.fisher_exact([[a, b], [c, d]])
        prev = (a / max(a + b, 1)) / (c / max(c + d, 1)) if c else None
        return {"n_sel": int(sel.sum()), "n_flagged_in_sel": a, "odds_ratio": float(orr),
                "prevalence_ratio": float(prev) if prev else None, "fisher_p": float(p)}
    med_all = j.flag == "medium_attributable"
    med_gain = med_all & (j.D_org < 0)
    med_loss = med_all & (j.D_org > 0)
    for label, sel in (("relatively_more_essential_in_HPLM_Zlt-3", j.zdiff < -3),
                       ("relatively_more_essential_in_RPMI_Zgt3", j.zdiff > 3)):
        out[label] = {"all_medium": enrich(sel, med_all), "medium_gains_only": enrich(sel, med_gain),
                      "medium_losses_only": enrich(sel, med_loss),
                      "medium_genes": j[sel & med_all].index.tolist()[:25]}

    # focused paired screens: 4 lines
    raw = pd.read_excel(H / "NIHMS1674248-supplement-4.xlsx", sheet_name="Paired-Gene Score_1",
                        skiprows=4, header=None)
    lines = ["K562", "NOMO1", "MOLM13", "SUDHL4"]
    focused = {}
    genes_col = raw.iloc[:, 0].astype(str)
    for i, ln in enumerate(lines):
        r = pd.to_numeric(raw.iloc[:, 1 + 3 * i], errors="coerce")
        h = pd.to_numeric(raw.iloc[:, 2 + 3 * i], errors="coerce")
        focused[ln] = pd.Series((h - r).values, index=genes_col.values)
    foc = pd.DataFrame(focused).groupby(level=0).mean()
    out["focused"] = {}
    for name, genes in panels.items():
        g = [x for x in genes if x in foc.index]
        if g:
            out["focused"][name] = {"n": len(g),
                                    "median_delta_by_line": foc.loc[g].median().round(3).to_dict(),
                                    "median_delta_overall": float(foc.loc[g].median().median())}
    (ROOT / "generations/hplm_reverse_test_v1.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1)[:4200])


if __name__ == "__main__":
    main()
