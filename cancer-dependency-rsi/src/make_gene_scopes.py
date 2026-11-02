"""Regenerate frozen gene-scope lists (data/gene_scopes.json). Deterministic.

Scopes (names describe actual populations):
- primary216: 250 panel - 26 Tier-A - TMOD - 7 AdherentN<400 (all joined).
- confirmatory207: primary216 present in Sanger Table 6 (schema-verified list).
- panel242_reference_filtered: all 250 joined to Broad table with AdherentN>=400
  and OrganoidsN>=90 (TMOD absent from table; no Tier-A exclusion). Sensitivity.
- tmod1_alias208: confirmatory207 + TMOD (Broad side) mapped to TMOD1 (7111)
  for reference-table values. Sensitivity only; alias unadjudicated from
  released guide data (guides named TMOD, no Entrez in released metadata).
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "broad_figshare"


def main() -> dict:
    lib = pd.read_csv(RAW / "minipool_library_composition.csv")
    panel = sorted(set(lib.loc[lib["All test genes"] == True, "Gene"]))  # noqa: E712
    excl = json.loads((ROOT / "data/selection_exclusions.json").read_text())
    tier_a = set(excl["tierA_direct_outliers_excluded"])
    tests = pd.read_csv(RAW / "organoids_vs_2d_gene_dependency_tests_full.csv")
    tests["symbol"] = tests.Dependency.str.replace(r"\s*\(\d+\)$", "", regex=True)
    tidx = tests.set_index("symbol")
    schema = json.loads((ROOT / "data/sanger_table6_schema.json").read_text())
    t6_missing = set(schema["panel250_missing"])

    def ref_ok(g: str) -> bool:
        return g in tidx.index and tidx.loc[g, "AdherentN"] >= 400 and tidx.loc[g, "OrganoidsN"] >= 90

    primary = sorted(g for g in panel if g not in tier_a and g != "TMOD" and ref_ok(g))
    confirmatory = sorted(g for g in primary if g not in t6_missing)
    panel242 = sorted(g for g in panel if ref_ok(g))
    out = {
        "primary216": primary,
        "confirmatory207": confirmatory,
        "panel242_reference_filtered": panel242,
        "tmod1_alias208": sorted(confirmatory + ["TMOD"]),
        "alias_map": {"TMOD": "TMOD1"},
        "counts": {"primary216": len(primary), "confirmatory207": len(confirmatory),
                   "panel242_reference_filtered": len(panel242), "tmod1_alias208": len(confirmatory) + 1},
        "excluded_low_reference_N_from_primary": sorted(g for g in panel if g not in tier_a and g != "TMOD" and g in tidx.index and not ref_ok(g)),
        "tierA_excluded_n": len(tier_a),
    }
    (ROOT / "data/gene_scopes.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out["counts"], indent=1))
    return out


if __name__ == "__main__":
    main()
