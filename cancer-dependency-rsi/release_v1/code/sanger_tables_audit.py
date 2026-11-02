#!/usr/bin/env python3
"""Deliverable-2 hardening within Sanger's own calls.
Table 5: BAGEL binary depletion per organoid -> per-gene frequency for the
exclusive/headline lists (threshold fragility in their own assay).
Table 7: their per-tissue differential-dependency analysis -> join Broad v2 flags.
"""
import io
import json
import zipfile

import pandas as pd

from medium_attribution import ROOT


def main():
    out = {}
    zpath = ROOT / "data/raw/sanger_figshare/S2_Supplementary_Tables.zip"
    z = zipfile.ZipFile(zpath)
    with z.open("supplementary_table_5_revision.csv") as f:
        t5 = pd.read_csv(f, sep=r"\s+", usecols=["sample_ID", "gene", "is_depleted"],
                         dtype={"is_depleted": "float32"})
    # 178 model-library profiles over 162 models: collapse within model first
    per_model = t5.groupby(["sample_ID", "gene"]).is_depleted.mean().reset_index()
    freq = per_model.groupby("gene").is_depleted.mean()
    n_models = t5.sample_ID.nunique()
    out["table5_n_models"] = int(n_models)

    sg = pd.read_excel(ROOT / "data/raw/sanger_supp/supplementary_table_4_revision.xlsx",
                       sheet_name="organoid_core_fitness_genes")
    v2 = pd.read_csv(ROOT / "generations/medium_attribution_v2_norm.csv", index_col=0)
    for label, m in (("exclusive97", sg.exclusive_organoids == "Yes"),
                     ("headline18", sg.exclusive_organoids_exclude_CommonEssentials == "Yes"),
                     ("all751", pd.Series(True, index=sg.index))):
        genes = [g for g in sg.loc[m, "gene"].astype(str) if g in freq.index]
        f = freq[genes]
        out[label] = {"n": len(genes), "freq_median": float(f.median()),
                      "frac_lt_0.25": float((f < 0.25).mean()), "frac_lt_0.5": float((f < 0.5).mean()),
                      "frac_ge_0.9": float((f >= 0.9).mean()),
                      "per_gene": f.round(3).to_dict() if label == "headline18" else f.nsmallest(12).round(3).to_dict()}

    # table 7: discover columns, then significant-gene audit per sheet
    wb_bytes = z.read("supplementary_table_7_revision.xlsx")
    keys = pd.read_excel(io.BytesIO(wb_bytes), sheet_name="keys_and_definitions", header=None)
    out["table7_keys"] = keys.head(30).astype(str).values.tolist()
    xls = pd.ExcelFile(io.BytesIO(wb_bytes))
    out["table7"] = {}
    for sheet in xls.sheet_names:
        if sheet == "keys_and_definitions":
            continue
        df = pd.read_excel(io.BytesIO(wb_bytes), sheet_name=sheet)
        out["table7"][sheet] = {"shape": list(df.shape), "columns": [str(c) for c in df.columns][:16]}
    (ROOT / "generations/sanger_tables_audit_v1.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if k != "table7_keys"}, indent=1, default=str)[:3500])
    print("T7 KEYS:", out["table7_keys"][:12])


if __name__ == "__main__":
    main()
