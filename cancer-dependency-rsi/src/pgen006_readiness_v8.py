#!/usr/bin/env python3
"""pgen006 v8: engineering-pilot metadata readiness screen (amended SPEC).

Framing (xhigh adjudication 2026-10-29): ENGINEERING_PILOT_SEPARATE; a pass
is METADATA_SCREEN_PASS (not GO_REPLAY, no C13 credit). Presence/coverage
only - score/delta values are never used. ACH-003052 (donor unresolved) is
quarantined from the catalogue. Pilot catalogue restricted to format axis
for evaluation; medium axis reported as development-only material.
"""
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "generations/pgen006/readiness_v8.json"
PINS = {
    "atlas/v4/manifest.json": "e4206db12133a6904b162f66c4f88a170525caf9fd0d83b5fd9872c536676dcf",
    "atlas/v4/paired_observations.csv": "00f7fa86f7c8c74d287b7fc940f6140727c77f1b7ed58ccd85f0e13fe8144801",
    "atlas/v4/genes.csv": "72c01a4b98ec0385367441025b1c6b75780a7bed262e5271e593780d3ec38b80",
    "data/Model.csv": "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7",
    "data/observation_provenance_minipool.csv": "86a0ecd27ea29e1900441cc65ef6a5007a6e15cf02166bc92acd1ebc5cd43cb9",
    "data/condition_cell_registry.csv": "c420242e2b543ea60ed351f4d40cda5435f78a579dbfd5fe6e97b36d51f96f64",
}
DEV = {"ACH-000108", "ACH-000178", "ACH-003040"}
EVAL = {"ACH-001418", "ACH-002958", "ACH-003052", "ACH-000048"}
QUARANTINE = {"ACH-003052"}  # donor unresolved: excluded from catalogue (xhigh)
EXPECTED_ROWS = 3000


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> int:
    for rel, want in PINS.items():
        if sha(ROOT / rel) != want:
            print(f"REFUSING: pin mismatch {rel}")
            return 1
    man = json.loads((ROOT / "atlas/v4/manifest.json").read_text())
    _entries = {**man.get("inputs", {}), **man.get("code", {})}
    if not _entries:
        print("REFUSING: atlas manifest has no entries")
        return 1
    for rel, digest in _entries.items():
        p = ROOT / rel
        if not p.exists() or sha(p) != digest:
            print(f"REFUSING: atlas manifest mismatch {rel}")
            return 1

    paired = rows("atlas/v4/paired_observations.csv")
    genes = {r["gene"] for r in rows("atlas/v4/genes.csv")}
    model_tbl = {r["ModelID"]: r for r in rows("data/Model.csv")}
    prov = rows("data/observation_provenance_minipool.csv")
    registry = rows("data/condition_cell_registry.csv")
    prov_models = {r.get("DepMap ID") for r in prov}
    reg_models = {r.get("DepMap ID") for r in registry}
    registry_resolved = (prov_models & reg_models) - set(model_tbl)
    # per-screen provenance: sequence -> (model, medium, format); condition cells
    # provenance is per-SEQUENCE (replicate suffix _RepA/_RepB); paired rows
    # reference the SCREEN (base id). Join on base id; all replicates of a
    # screen must agree on model/medium/format or the screen is unresolved.
    from collections import defaultdict as _dd
    _grp = _dd(list)
    for r in prov:
        _grp[r["sequence_ID"].rsplit("_Rep", 1)[0]].append(r)
    seq_prov = {}
    for base, rs in _grp.items():
        sig = {(x.get("DepMap ID"), x.get("Culture medium"), x.get("Growth Format")) for x in rs}
        seq_prov[base] = rs[0] if len(sig) == 1 else None
    reg_cells = {(r.get("DepMap ID"), r.get("Culture medium"), r.get("Growth Format")): r.get("disposition")
                 for r in registry}

    def part(m):
        return "DEV" if m in DEV else "EVAL" if m in EVAL else "OUT"

    unresolved, keys, actions = [], Counter(), {}
    screens_by_part = defaultdict(set)
    cov = Counter()
    prov_mismatch = []
    for r in paired:
        problems = []
        mid = r["model_id"]
        if r["gene"] not in genes:
            problems.append("gene_not_in_panel")
        if mid not in model_tbl and mid not in registry_resolved:
            problems.append("model_unresolved")
        for s_col, c_col in (("screen_a", "condition_a"), ("screen_b", "condition_b")):
            sid = r.get(s_col)
            pr = seq_prov.get(sid)
            if not sid or sid not in seq_prov:
                problems.append(f"screen_not_in_provenance:{s_col}")
            elif seq_prov[sid] is None:
                problems.append(f"screen_replicates_disagree:{s_col}")
            elif pr.get("DepMap ID") != mid:
                problems.append(f"screen_model_mismatch:{s_col}")
            else:
                cell = reg_cells.get((mid, pr.get("Culture medium"), pr.get("Growth Format")))
                if cell != "in released matrix":
                    problems.append(f"condition_cell_not_recorded:{s_col}")
        # orientation validation against provenance (screen_a must BE the
        # condition_a screen; held dimension constant and equal to held_condition)
        for s_col, c_col in (("screen_a", "condition_a"), ("screen_b", "condition_b")):
            pr = seq_prov.get(r.get(s_col) or "")
            if pr is not None:
                dim = ("Growth Format" if r["axis"] == "format" else "Culture medium")
                if pr.get(dim) != r.get(c_col):
                    problems.append(f"screen_orientation_mismatch:{s_col}")
        pa, pb = seq_prov.get(r.get("screen_a") or ""), seq_prov.get(r.get("screen_b") or "")
        if pa is not None and pb is not None:
            held_dim = ("Culture medium" if r["axis"] == "format" else "Growth Format")
            if not (pa.get(held_dim) == pb.get(held_dim) == r.get("held_condition")):
                problems.append("held_condition_provenance_mismatch")
        # declared-contrast validation (frozen vocabularies from atlas design)
        if r["axis"] == "format":
            if not (r.get("condition_a") == "Dome" and r.get("condition_b") == "Plastic"
                    and r.get("held_condition") in ("OPAC", "RPMI/FBS")):
                problems.append("contrast_mismatch_format")
        elif r["axis"] == "medium":
            if not (r.get("condition_a") == "OPAC" and r.get("condition_b") == "RPMI/FBS"
                    and r.get("held_condition") in ("Dome", "Plastic")):
                problems.append("contrast_mismatch_medium")
        else:
            problems.append("axis_not_permitted")
        if r.get("screen_a") == r.get("screen_b"):
            problems.append("screens_not_distinct")
        if problems:
            unresolved.append({"gene": r["gene"], "model": mid, "problems": problems})
            if len(prov_mismatch) < 10 and any("provenance" in p or "screen" in p for p in problems):
                prov_mismatch.append(problems)
        # action identity INCLUDES held_condition (v1 review fix)
        key = (r["gene"], r["axis"], mid, r.get("held_condition"))
        keys[key] += 1
        actions[key] = r
        p_ = part(mid)
        screens_by_part[p_].update({r["screen_a"], r["screen_b"]})
        cov[(p_, r["axis"])] += 1
    dup_keys = {str(k): v for k, v in keys.items() if v > 1}
    out_rows = sum(1 for r in paired if part(r["model_id"]) == "OUT")

    # patient components (Model.csv PatientID); quarantined model excluded
    patient_of = {m: ((model_tbl[m].get("PatientID") or "").strip() or None
                      if m in model_tbl else None) for m in DEV | EVAL}
    dev_patients = {patient_of[m] for m in DEV}
    eval_patients = {patient_of[m] for m in EVAL - QUARANTINE}
    patient_overlap = (dev_patients & eval_patients) - {None, ""}
    patient_complete = all(patient_of[m] for m in (DEV | EVAL) - QUARANTINE)

    catalogue = {k: r for k, r in actions.items() if k[2] not in QUARANTINE}
    cat_cov = Counter((part(k[2]), k[1]) for k in catalogue)
    eval_format_models = {k[2] for k in catalogue if part(k[2]) == "EVAL" and k[1] == "format"}

    checks = {
        "frozen_inventory_exact_3000_rows": len(paired) == EXPECTED_ROWS,
        "identity_resolution_100pct": not unresolved,
        "zero_ambiguous_conflicting_records": not dup_keys,
        "zero_out_of_partition_rows": out_rows == 0,
        "zero_cross_partition_screen_overlap": not (screens_by_part["DEV"] & screens_by_part["EVAL"]),
        "zero_patient_overlap_dev_eval": not patient_overlap,
        "patient_identity_complete_nonquarantined": patient_complete,
        "eval_format_minimum": cat_cov[("EVAL", "format")] >= 100 and len(eval_format_models) >= 2,
        "dev_minimum": cat_cov[("DEV", "format")] >= 100,
        "cost_table_present": True,
    }
    # structural only if minimums fail even counting ALL rows (incl unresolved)
    full_cov = Counter((part(r["model_id"]), r["axis"]) for r in paired)
    inventory_complete_unambiguous = (checks["frozen_inventory_exact_3000_rows"]
                                      and checks["zero_ambiguous_conflicting_records"]
                                      and checks["zero_out_of_partition_rows"]
                                      and checks["identity_resolution_100pct"])
    structural_fail = (inventory_complete_unambiguous
                       and (full_cov[("EVAL", "format")] < 100 or full_cov[("DEV", "format")] < 100))
    if all(checks.values()):
        verdict = "METADATA_SCREEN_PASS"
    elif structural_fail:
        verdict = "FAIL_SUBSTRATE"
    else:
        verdict = "REPAIR_METADATA"

    report = {
        "generation": "pgen006", "version": 8,
        "framing": "ENGINEERING_PILOT_SEPARATE (xhigh 2026-10-29); no C13 credit",
        "inputs": {k: {"sha256": v} for k, v in PINS.items()},
        "inventory": {"rows": len(paired), "expected_rows": EXPECTED_ROWS,
                      "unresolved_count": len(unresolved), "unresolved_sample": unresolved[:10],
                      "duplicate_action_keys": dup_keys, "out_of_partition_rows": out_rows},
        "identity_repair": {"registry_resolved_models": sorted(registry_resolved),
                            "criterion_amendment": "recording identity via dual registries; donor identity for ACH-003052 remains unresolved (quarantined)"},
        "partition": {"DEV": sorted(DEV), "EVAL": sorted(EVAL), "QUARANTINE": sorted(QUARANTINE),
                      "patient_overlap": sorted(x for x in patient_overlap if x),
                      "patient_of": {k: patient_of[k] for k in sorted(patient_of)},
                      "coverage_rows": {f"{k[0]}/{k[1]}": v for k, v in sorted(cov.items())},
                      "catalogue_actions_by_partition_axis": {f"{k[0]}/{k[1]}": v for k, v in sorted(cat_cov.items())}},
        "catalogue": {"actions_incl_held_condition": len(actions),
                      "actions_after_quarantine": len(catalogue),
                      "pilot_axis": "format (evaluation); medium = development-only material (1 EVAL model)"},
        "cost_table": {"per_action": {"evaluated_nodes": 1, "evaluator_calls": 0},
                       "host_call_attribution": {
                           "shared_equally": "substrate/E0 production + evaluator construction calls (charged equally to every arm)",
                           "arm_attributed": "policy-generation, policy-specific review, and unstick calls (charged to the arm that caused them; learning overhead NOT shared)",
                           "unresolved": "conservative learned-arm attribution per pgen005",
                           "basis": "amended estimated-cost schedule (estimator v8); metered $0 reported alongside"},
                       "matching": "exact evaluated-node equality across arms at cycle lock",
                       "witness_status": "attribution rules frozen here; Q*/policies/evaluator remain cycle-lock witnesses (open)"},
        "checks": checks,
        "verdict": verdict,
        "authorization": ("METADATA_SCREEN_PASS authorizes ONLY drafting a cycle SPEC for xhigh/lead lock "
                          "(Q* justification, policies, evaluator, matching). It is not GO_REPLAY and "
                          "authorizes no execution and no biological claim."),
        "source_history_note": "v2 source was overwritten during v3 patching and reconstructed (disclosed); v1/v3 sources reproduce their reports",
    }
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({"verdict": verdict, "checks": checks,
                      "catalogue_actions": len(catalogue),
                      "cat_cov": {f"{k[0]}/{k[1]}": v for k, v in sorted(cat_cov.items())}}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
