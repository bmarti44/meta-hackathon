#!/usr/bin/env python3
"""Medium attribution v2 (GOAL v4 deliverables 1-3, Broad side).

Changes vs v1: Ampulla lineage included; per-contrast p/q for all contrasts;
uncertainty-aware per-gene flags (medium_attributable / format_candidate /
unresolved) with delta-method CIs on the adherent-reproduction ratio;
Humagne-CD-only sensitivity for D_org; core-essential weakening decomposition
(global dynamic-range compression vs gene-specific residual, with screen Days
as the only recorded duration -- CPD is recorded for 1/1241 screens);
join to published hit lists (Broad organoids-vs-2D figshare table, Sanger
supp. table 4 organoid core fitness genes). Dev patients only.
"""
import datetime
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from medium_attribution import ROOT, bh, library_offset, load_effects, load_screens, normalize

ORG_LINEAGES = ["Bowel", "Esophagus/Stomach", "Pancreas", "Breast", "Ovary/Fallopian Tube",
                "Uterus", "Biliary Tract", "Prostate", "Ampulla of Vater"]
MEV = ["HMGCS1", "HMGCR", "MVK", "PMVK", "MVD", "IDI1", "IDI2", "FDPS", "FDFT1", "SQLE",
       "LSS", "CYP51A1", "MSMO1", "NSDHL", "HSD17B7", "EBP", "SC5D", "DHCR7", "DHCR24", "ACAT2"]
RIBO = ["RPL3", "RPL27", "RPS16", "RPL5", "RPS6", "RPL7", "RPS3", "RPL10", "RPS14", "RPL23", "RPS23", "RPS19"]
SPL = ["EFTUD2", "SF3A3", "SRSF7", "RBM39", "U2SURP", "THOC2", "PRPF8", "SNRPA1"]
HEME = ["ALAS1", "ALAD", "HMBS", "UROS", "UROD", "CPOX", "PPOX", "FECH"]


def contrast2(Y, groups, lineage, extra=None):
    """OLS per gene: y ~ 1 + group + lineage dummies (+ extra covars). beta, se, p, ns."""
    lin = pd.get_dummies(lineage, drop_first=True, dtype=float)
    cols = [np.ones(len(Y)), groups.astype(float), lin.values]
    if extra is not None:
        cols.append(np.asarray(extra, dtype=float).reshape(len(Y), -1))
    X = np.column_stack(cols)
    XtX_inv = np.linalg.pinv(X.T @ X)
    B = XtX_inv @ X.T @ Y.values
    resid = Y.values - X @ B
    dof = max(len(Y) - np.linalg.matrix_rank(X), 1)
    s2 = (resid ** 2).sum(axis=0) / dof
    se = np.sqrt(np.maximum(s2 * XtX_inv[1, 1], 0))
    beta = pd.Series(B[1], Y.columns)
    se = pd.Series(se, Y.columns)
    p = pd.Series(2 * stats.t.sf(np.abs(beta / se.replace(0, np.nan)), dof), Y.columns)
    # HC3 robust SE for the group coefficient:
    # Var = sum_i [(X'X)^-1 X']_{1,i}^2 * e_i^2 / (1 - h_i)^2
    XtXi_X = XtX_inv @ X.T
    h = np.einsum("ij,ji->i", X, XtXi_X)
    var_hc3 = (XtXi_X[1][:, None] ** 2 * (resid / (1 - h)[:, None]) ** 2).sum(axis=0)
    se_hc3 = pd.Series(np.sqrt(np.maximum(var_hc3, 0)), Y.columns)
    return beta, se, p, int(groups.sum()), int((~groups).sum()), se_hc3


def flag_hits(tab):
    """Classify D_org hits. Ratio CI by delta method (contrasts share the FBS
    baseline, so independence overstates the ratio SE slightly: conservative)."""
    t = tab.copy()
    t["ratio_A"] = t.A_adh / t.D_org
    var = (t.A_adh_se / t.D_org) ** 2 + (t.A_adh * t.D_org_se / t.D_org ** 2) ** 2
    t["ratio_A_se"] = np.sqrt(var)
    t["ratio_A_lo"] = t.ratio_A - 1.645 * t.ratio_A_se
    t["ratio_A_hi"] = t.ratio_A + 1.645 * t.ratio_A_se
    t["ratio_F"] = t.F_dome / t.D_org
    varF = (t.F_dome_se / t.D_org) ** 2 + (t.F_dome * t.D_org_se / t.D_org ** 2) ** 2
    t["ratio_F_se"] = np.sqrt(varF)
    t["ratio_F_lo"] = t.ratio_F - 1.645 * t.ratio_F_se
    t["ratio_F_hi"] = t.ratio_F + 1.645 * t.ratio_F_se
    hit = (t.D_org_q < 0.01) & (t.D_org.abs() >= 0.25)
    same_A = np.sign(t.A_adh) == np.sign(t.D_org)
    same_F = np.sign(t.F_dome) == np.sign(t.D_org)
    # primary rule (Astra r1 #6): symmetric nominal-p evidence for medium and format
    medium = hit & same_A & (t.ratio_A >= 0.5) & (t.A_adh_p < 0.05) & (t.ratio_A_lo > 0) \
        & ~(same_F & (t.F_dome_p < 0.05) & (t.ratio_F >= 0.5) & (t.ratio_F_lo > 0))
    fmt = hit & ~medium & same_F & (t.F_dome_p < 0.05) & (t.ratio_F >= 0.5) \
        & (t.ratio_F_lo > 0) & (t.ratio_A < 0.25)
    t["flag"] = np.where(~hit, "not_a_hit", np.where(medium, "medium_attributable",
                             np.where(fmt, "format_candidate", "unresolved")))
    # strict-FDR variant (pre-review rule): format evidence at genome-wide q<0.05
    medium_f = hit & same_A & (t.ratio_A >= 0.5) & (t.A_adh_p < 0.05) & (t.ratio_A_lo > 0) \
        & ~(same_F & (t.F_dome_q < 0.05) & (t.ratio_F >= 0.5))
    fmt_f = hit & ~medium_f & same_F & (t.F_dome_q < 0.05) & (t.ratio_F >= 0.5) & (t.ratio_A < 0.25)
    t["flag_fdr"] = np.where(~hit, "not_a_hit", np.where(medium_f, "medium_attributable",
                                 np.where(fmt_f, "format_candidate", "unresolved")))
    t["serumfree_support"] = np.sign(t.S_tsm) == np.sign(t.D_org)
    return t


def main():
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "revision": "v2r2 (Astra r1 fixes: dev-only calibration/preprocessing, symmetric format rule + flag_fdr, HC3, screen-level Humagne, common-support, %.6g export)"}
    scr = load_screens()
    ge = load_effects(set(scr.index))
    # Astra r1 #5: exclude reserved patients BEFORE calibration/filtering/imputation
    scr = scr[scr.Lib.isin(["Avana", "Humagne-CD"]) & ~scr.reserved]
    ge = ge.loc[scr.index]
    ge = ge.astype("float64")
    ge = ge.loc[:, ge.notna().mean() > 0.99]
    scr = scr.loc[ge.index]
    off, n_pairs = library_offset(ge, scr)
    rep["library_offset_models"] = n_pairs
    ge = ge.fillna(ge.mean())
    ge.loc[scr.Lib == "Avana"] = ge.loc[scr.Lib == "Avana"] + off.fillna(0)
    ge = ge.loc[scr.index]

    seq = pd.read_csv(ROOT / "data/ScreenSequenceMap.csv", dtype=str)
    seq["Days"] = pd.to_numeric(seq.Days, errors="coerce")
    days = seq[seq.ScreenID.isin(scr.index)].groupby("ScreenID").Days.max()
    scr["Days"] = scr.index.map(days)
    rep["days_by_group"] = scr.groupby(["cls", "Fmt"]).Days.agg(["median", "min", "max"]).round(1).to_dict("index").__str__()

    fbs_adh = scr[(scr.cls == "FBS") & (scr.Fmt == "adherent")]
    med = ge.loc[fbs_adh.index].median()
    frac = (ge.loc[fbs_adh.index] < -0.5).mean()
    ess = list(frac[frac > 0.9].index)
    non = list(med[(med.abs() < 0.05) & (ge.loc[fbs_adh.index].std() < 0.15)].index)
    rep["n_common_essential"], rep["n_nonessential"] = len(ess), len(non)

    # ---- deliverable 3 (Broad side): essential-depth / weakening decomposition
    grp = scr.assign(g=np.select(
        [(scr.cls == "FBS") & (scr.Fmt == "adherent"), (scr.cls == "org") & (scr.Fmt == "dome"),
         (scr.cls == "org") & (scr.Fmt == "adherent"), scr.cls == "TSM"],
        ["FBS_adh", "org_dome", "org_adh", "TSM"], "other"))
    d3 = {}
    depth = ge[ess].median(axis=1)
    for name, idx in grp.groupby("g").groups.items():
        if name == "other":
            continue
        d3[name] = {"n_screens": int(len(idx)), "ess_median_chronos": float(depth[idx].median()),
                    "days_median": float(scr.loc[idx, "Days"].median())}
    r = d3["org_dome"]["ess_median_chronos"] / d3["FBS_adh"]["ess_median_chronos"]
    d3["compression_ratio_dome_over_FBS"] = float(r)
    d3["implied_doubling_time_ratio_if_chronos_proportional_to_doublings"] = float(
        (d3["org_dome"]["days_median"] / d3["FBS_adh"]["days_median"]) / r)
    rep["essential_depth"] = d3

    tabs = {}
    for scale in ("raw", "norm"):
        Y = ge if scale == "raw" else normalize(ge, ess, non)
        Ym = Y.groupby(scr.ModelID).mean()
        meta = scr.groupby("ModelID").agg(cls=("cls", "first"), Fmt=("Fmt", "first"),
                                           lin=("lin", "first"), Lib=("Lib", "first"),
                                           Days=("Days", "mean"))
        orglin = meta.lin.isin(ORG_LINEAGES)
        res = {}
        sel = meta[orglin & (((meta.cls == "org") & (meta.Fmt == "dome"))
                             | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
        res["D_org"] = contrast2(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
        # Astra r1 #4: Humagne-only sensitivity filtered at SCREEN level, then aggregated
        scr_h = scr[scr.Lib == "Humagne-CD"]
        Yh = (ge if scale == "raw" else normalize(ge, ess, non)).loc[scr_h.index]
        Ymh = Yh.groupby(scr_h.ModelID).mean()
        mh = scr_h.groupby("ModelID").agg(cls=("cls", "first"), Fmt=("Fmt", "first"), lin=("lin", "first"))
        selh = mh[mh.lin.isin(ORG_LINEAGES) & (((mh.cls == "org") & (mh.Fmt == "dome"))
                                               | ((mh.cls == "FBS") & (mh.Fmt == "adherent")))]
        res["D_org_humagne_only"] = contrast2(Ymh.loc[selh.index], (selh.cls == "org").values, selh.lin)
        sel = meta[orglin & (((meta.cls == "org") & (meta.Fmt == "adherent"))
                             | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
        res["A_adh"] = contrast2(Ym.loc[sel.index], (sel.cls == "org").values, sel.lin)
        sel = meta[orglin & (meta.cls == "org")]
        res["F_dome"] = contrast2(Ym.loc[sel.index], (sel.Fmt == "dome").values, sel.lin)
        sel = meta[(meta.lin == "CNS/Brain") & meta.cls.isin(["TSM", "FBS"])]
        res["S_tsm"] = contrast2(Ym.loc[sel.index], (sel.cls == "TSM").values, sel.lin)

        tab = pd.DataFrame({k: v[0] for k, v in res.items()})
        for k, v in res.items():
            tab[k + "_se"], tab[k + "_p"] = v[1], v[2]
            tab[k + "_q"] = bh(v[2].fillna(1).values)
            tab[k + "_se_hc3"] = v[5]
        tab = flag_hits(tab)
        tab.to_csv(ROOT / f"generations/medium_attribution_v2_{scale}.csv", float_format="%.6g")
        tabs[scale] = tab
        s = {"n": {k: [v[3], v[4]] for k, v in res.items()}}
        for direction, h in (("gains", tab[(tab.flag != "not_a_hit") & (tab.D_org < 0)]),
                             ("losses", tab[(tab.flag != "not_a_hit") & (tab.D_org > 0)])):
            s[direction] = {
                "n_hits": int(len(h)),
                "flags": h.flag.value_counts().to_dict(),
                "frac_medium_of_hits": float((h.flag == "medium_attributable").mean()) if len(h) else None,
                "slope_A_on_D": float(np.polyfit(h.D_org, h.A_adh, 1)[0]) if len(h) > 2 else None,
                "slope_S_on_D": float(np.polyfit(h.D_org, h.S_tsm, 1)[0]) if len(h) > 2 else None,
                "slope_F_on_D": float(np.polyfit(h.D_org, h.F_dome, 1)[0]) if len(h) > 2 else None,
                "median_ratio_A": float(h.ratio_A.median()) if len(h) else None,
                "serumfree_support_frac": float(h.serumfree_support.mean()) if len(h) else None,
            }
        s["humagne_only_corr_D"] = float(tab.D_org.corr(tab.D_org_humagne_only))
        s["humagne_only_slope_D"] = float(np.polyfit(tab.D_org, tab.D_org_humagne_only, 1)[0])
        s["flags_fdr_variant"] = tab[tab.flag_fdr != "not_a_hit"].flag_fdr.value_counts().to_dict()
        # Astra r1 #2: HC3-robust flag sensitivity (normal-approx p from HC3 SEs)
        th = tab.copy()
        for k in ("D_org", "A_adh", "F_dome", "S_tsm"):
            th[k + "_se"] = th[k + "_se_hc3"]
            th[k + "_p"] = 2 * stats.norm.sf((th[k] / th[k + "_se"].replace(0, np.nan)).abs())
            th[k + "_q"] = bh(th[k + "_p"].fillna(1).values)
        th = flag_hits(th.drop(columns=["flag", "flag_fdr", "ratio_A", "ratio_A_se", "ratio_A_lo",
                                        "ratio_A_hi", "ratio_F", "ratio_F_se", "ratio_F_lo",
                                        "ratio_F_hi", "serumfree_support"], errors="ignore"))
        s["hc3_sensitivity"] = {}
        for direction, h in (("gains", th[(th.flag != "not_a_hit") & (th.D_org < 0)]),
                             ("losses", th[(th.flag != "not_a_hit") & (th.D_org > 0)])):
            s["hc3_sensitivity"][direction] = {
                "n_hits": int(len(h)), "flags": h.flag.value_counts().to_dict(),
                "frac_medium_of_hits": float((h.flag == "medium_attributable").mean()) if len(h) else None}
        # Astra r1 #1: common-support sensitivity - only lineages with adherent org-medium models
        cs_lin = sorted(meta[(meta.cls == "org") & (meta.Fmt == "adherent")].lin.unique())
        cs = {}
        selD = meta[meta.lin.isin(cs_lin) & (((meta.cls == "org") & (meta.Fmt == "dome"))
                                             | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
        selA = meta[meta.lin.isin(cs_lin) & (((meta.cls == "org") & (meta.Fmt == "adherent"))
                                             | ((meta.cls == "FBS") & (meta.Fmt == "adherent")))]
        bD = contrast2(Ym.loc[selD.index], (selD.cls == "org").values, selD.lin)
        bA = contrast2(Ym.loc[selA.index], (selA.cls == "org").values, selA.lin)
        qD = pd.Series(bh(bD[2].fillna(1).values), bD[0].index)
        hits_cs = bD[0][(qD < 0.01) & (bD[0].abs() >= 0.25)]
        ratio_cs = bA[0][hits_cs.index] / hits_cs
        cs = {"lineages": cs_lin, "n_dome": int((selD.cls == "org").sum()), "n_adh": int((selA.cls == "org").sum()),
              "n_hits": int(len(hits_cs)),
              "slope_A_on_D": float(np.polyfit(hits_cs, bA[0][hits_cs.index], 1)[0]) if len(hits_cs) > 2 else None,
              "median_ratio_A": float(ratio_cs.median()) if len(hits_cs) else None,
              "frac_ratio_ge_half_same_sign": float(((ratio_cs >= 0.5)).mean()) if len(hits_cs) else None}
        s["common_support"] = cs
        rep[scale] = s

    # weakening decomposition on the raw table: observed vs pure-scaling prediction
    raw = tabs["raw"]
    base = ge.loc[fbs_adh.index].groupby(scr.loc[fbs_adh.index, "ModelID"]).mean().mean()
    dec = {}
    for name, genes in (("common_essentials", ess), ("splice_panel", SPL), ("ribo_panel", RIBO)):
        g = [x for x in genes if x in raw.index]
        pred = base[g] * (r - 1)  # weakening expected if every gene scales by compression ratio
        dec[name] = {"n": len(g), "observed_D_median": float(raw.loc[g, "D_org"].median()),
                     "scaling_predicted_D_median": float(pred.median()),
                     "norm_scale_D_median": float(tabs["norm"].loc[g, "D_org"].median()),
                     "frac_observed_exceeds_scaling": float((raw.loc[g, "D_org"] > pred).mean())}
    rep["weakening_decomposition"] = dec
    (ROOT / "generations/medium_attribution_v2.json").write_text(json.dumps(rep, indent=1, default=str))

    # ---- deliverable 2: published hit lists
    pub = {}
    b = pd.read_csv(ROOT / "data/raw/broad_figshare/organoids_vs_2d_gene_dependency_tests_full.csv")
    b["gene"] = b.Dependency.str.split(" (", regex=False).str[0]
    b = b.set_index("gene")
    j = b.join(tabs["norm"][["D_org", "flag"]], how="inner")
    for label, m in (("FDR<0.05 & diff<-0.25", (j.MannWhitneyFDR < 0.05) & (j.MeanDifference < -0.25)),
                     ("FDR<0.01 & diff<-0.5", (j.MannWhitneyFDR < 0.01) & (j.MeanDifference < -0.5)),
                     ("FDR<0.05 & diff<-0.25 & !DropEssential",
                      (j.MannWhitneyFDR < 0.05) & (j.MeanDifference < -0.25) & ~j.DropEssential)):
        h = j[m]
        pub[f"broad_published[{label}]"] = {
            "n": int(len(h)), "flags": h.flag.value_counts().to_dict(),
            "frac_medium": float((h.flag == "medium_attributable").mean()) if len(h) else None,
            "frac_medium_or_unresolved": float(h.flag.isin(["medium_attributable", "unresolved"]).mean()) if len(h) else None,
            "top_by_published_diff": h.sort_values("MeanDifference").head(25).index.tolist()}
    try:
        sg = pd.read_excel(ROOT / "data/raw/sanger_supp/supplementary_table_4_revision.xlsx",
                           sheet_name="organoid_core_fitness_genes")
        gcol = [c for c in sg.columns if "gene" in str(c).lower() or "symbol" in str(c).lower()]
        genes = sorted(set(sg[gcol[0]].dropna().astype(str))) if gcol else []
        ing = [g for g in genes if g in tabs["norm"].index]
        h = tabs["norm"].loc[ing]
        pub["sanger_organoid_core_fitness"] = {
            "n_listed": len(genes), "n_in_broad_table": len(ing), "gene_col": gcol,
            "columns": [str(c) for c in sg.columns][:12],
            "flags": h.flag.value_counts().to_dict(),
            "n_also_our_hit": int((h.flag != "not_a_hit").sum()),
            "median_D_org": float(h.D_org.median()) if len(h) else None,
            "medium_attributable_genes": h[h.flag == "medium_attributable"].index.tolist()}
    except Exception as e:  # recorded, not hidden
        pub["sanger_organoid_core_fitness"] = {"error": repr(e)}
    rep["published_hits"] = pub

    for name, genes in (("mevalonate", MEV), ("heme", HEME)):
        g = [x for x in genes if x in tabs["norm"].index]
        h = tabs["norm"].loc[g]
        rep[f"panel_{name}"] = {"n": len(g), "flags": h.flag.value_counts().to_dict(),
                                "median_D": float(h.D_org.median()), "median_ratio_A": float(h.ratio_A.median())}

    (ROOT / "generations/medium_attribution_v2.json").write_text(json.dumps(rep, indent=1, default=str))
    print(json.dumps(rep, indent=1, default=str)[:6000])


if __name__ == "__main__":
    main()
