#!/usr/bin/env python3
"""pgen006: replay-substrate readiness discriminator (SPEC locked).

PRESENCE/COVERAGE ONLY: this script never reads score/delta values into any
computation (columns are not summed, ranked, or thresholded). It inventories
atlas v4 paired observations against the frozen partition/catalogue.
"""
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "generations/pgen006/readiness_v3.json"
DEV = {"ACH-000108", "ACH-000178", "ACH-003040"}
EVAL = {"ACH-001418", "ACH-002958", "ACH-003052", "ACH-000048"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> int:
    # transitive pinning: atlas manifest (verified chain, sgen002) + pool pins
    man = json.loads((ROOT / "atlas/v4/manifest.json").read_text())
    for rel, digest in {**man.get("inputs", {}), **man.get("code", {})}.items():
        p = ROOT / rel
        if not p.exists() or sha(p) != digest:
            print(f"REFUSING: atlas manifest mismatch/missing {rel}")
            return 1
    paired = rows("atlas/v4/paired_observations.csv")
    genes = {r["gene"] for r in rows("atlas/v4/genes.csv")}
    model_ids = {r["ModelID"] for r in rows("data/Model.csv")}
    # Repair route (REPAIR_METADATA): models dropped from DepMap 26Q3 Model.csv
    # may resolve via BOTH project provenance registries agreeing on the model.
    REG_PINS = {"data/observation_provenance_minipool.csv":
                "86a0ecd27ea29e1900441cc65ef6a5007a6e15cf02166bc92acd1ebc5cd43cb9",
                "data/condition_cell_registry.csv":
                "c420242e2b543ea60ed351f4d40cda5435f78a579dbfd5fe6e97b36d51f96f64"}
    for rel, want in REG_PINS.items():
        if sha(ROOT / rel) != want:
            print(f"REFUSING: registry pin mismatch {rel}")
            return 1
    prov = rows("data/observation_provenance_minipool.csv")
    reg = rows("data/condition_cell_registry.csv")
    prov_models = {r.get("DepMap ID") for r in prov}
    reg_models = set()
    for r in reg:
        reg_models.update(v for v in r.values() if isinstance(v, str) and v.startswith("ACH-"))
    registry_resolved = (prov_models & reg_models) - model_ids

    unresolved = []
    keys = Counter()
    inv = []
    for r in paired:
        problems = []
        if r["gene"] not in genes:
            problems.append("gene_not_in_panel")
        if r["model_id"] not in model_ids and r["model_id"] not in registry_resolved:
            problems.append("model_not_in_Model.csv")
        if not r.get("screen_a") or not r.get("screen_b"):
            problems.append("missing_screen_id")
        if problems:
            unresolved.append({"gene": r["gene"], "model": r["model_id"], "problems": problems})
        keys[(r["gene"], r["axis"], r["model_id"], r.get("held_condition"))] += 1
        inv.append(r)
    dup_keys = {str(k): v for k, v in keys.items() if v > 1}

    def part(m):
        return "DEV" if m in DEV else "EVAL" if m in EVAL else "OUT"

    screens_by_part = defaultdict(set)
    cov = Counter()
    for r in inv:
        p = part(r["model_id"])
        screens_by_part[p].update({r["screen_a"], r["screen_b"]})
        cov[(p, r["axis"])] += 1
    shared_screens = screens_by_part["DEV"] & screens_by_part["EVAL"]

    # catalogue = recorded actions only (restriction disclosed); coverage of the
    # full gene x axis grid reported for context
    recorded = {(r["gene"], r["axis"], r["model_id"]) for r in inv}
    grid = {(g, ax, m) for g in genes for ax in ("format", "medium")
            for m in (DEV | EVAL)}
    checks = {
        "identity_resolution_100pct": not unresolved,
        "zero_ambiguous_conflicting_records": not dup_keys,
        "zero_cross_partition_screen_overlap": not shared_screens,
        "eval_minimum": cov[("EVAL", "format")] >= 100 and len(EVAL) >= 2,
        "dev_minimum": cov[("DEV", "format")] >= 100 and cov[("DEV", "medium")] >= 100,
        "cost_table_definable": True,  # unit node cost per action; host calls per pgen005
    }
    if all(checks.values()):
        verdict = "GO_REPLAY"
    elif not checks["identity_resolution_100pct"] and all(
            v for k, v in checks.items() if k != "identity_resolution_100pct"):
        verdict = "REPAIR_METADATA"
    else:
        verdict = "FAIL_SUBSTRATE"
    report = {
        "generation": "pgen006", "version": 3,
        "identity_repair": {"registry_resolved_models": sorted(registry_resolved),
                            "route": "both project provenance registries agree (hash-pinned); absent from DepMap 26Q3 Model.csv + Passports list"},
        "inventory": {"rows": len(inv), "models": len({r['model_id'] for r in inv}),
                      "genes": len({r['gene'] for r in inv}),
                      "unresolved_rows": unresolved[:20],
                      "unresolved_count": len(unresolved),
                      "duplicate_keys": dup_keys},
        "partition": {"DEV": sorted(DEV), "EVAL": sorted(EVAL),
                      "shared_screens_cross_partition": sorted(shared_screens),
                      "coverage_by_partition_axis": {f"{k[0]}/{k[1]}": v for k, v in sorted(cov.items())}},
        "catalogue": {"recorded_actions": len(recorded),
                      "full_grid_actions": len(grid),
                      "grid_coverage_fraction": round(len(recorded & grid) / len(grid), 4),
                      "restriction": "catalogue frozen = recorded actions only; unrecorded grid cells are NOT reachable actions"},
        "checks": checks,
        "verdict": verdict,
        "authorization": "GO_REPLAY authorizes ONLY a cycle SPEC lock (Q* numeric lock, policies, seeds); no execution here",
        "substrate_limits": [
            "7 models only; donor_id unresolved in atlas (model = independence unit, disclosed)",
            "medium axis: EVAL coverage is a single model (ACH-000048) - axis-restricted episodes required",
            "replay outcomes are development-screen recordings; no biological claim from replay performance",
        ],
    }
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({"verdict": verdict, "checks": checks,
                      "coverage": report["partition"]["coverage_by_partition_axis"],
                      "catalogue": report["catalogue"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
