#!/usr/bin/env python3
"""sgen010 v2: metadata discriminator with Cell Model Passports bridge.

v1 keys did not connect (float-formatted COSMICIDs, only 5 identity names,
HCM-BROD vs HCM-SANG). v2 bridges cohort C -> Passports (HCMI / COSMIC_ID /
model_name) -> patient_id (SIDP), then excludes every DepMap model whose
Passports patient is a C patient, plus direct SIDM/BROAD_ID matches.
Metadata only — no outcomes anywhere in these inputs.
"""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "data/Model.csv"
SCREEN = ROOT / "data/CRISPRScreenMap.csv"
COHORT = ROOT / "lock_s/cohort.csv"
IDENT = ROOT / "generations/sgen001/identity_reconciliation_v1.json"
PASSPORTS = ROOT / "data/passports_model_list_20260921.csv"
OUT = ROOT / "generations/sgen010/screen_v2.json"

EXPECTED_SHA = {
    "Model.csv": "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7",
    "CRISPRScreenMap.csv": "43cc528614053d4c5a96729c2d782375227231a0cfea23de6c519b8989fa1252",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path):
    with p.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def norm_num(v: str) -> str:
    v = (v or "").strip()
    try:
        return str(int(float(v)))
    except (ValueError, OverflowError):
        return v


def main() -> int:
    for name, p in (("Model.csv", MODEL), ("CRISPRScreenMap.csv", SCREEN)):
        if sha(p) != EXPECTED_SHA[name]:
            print(f"REFUSING: {name} hash mismatch vs locked value")
            return 1

    models = rows(MODEL)
    screens = rows(SCREEN)
    cohort = rows(COHORT)
    ident = json.loads(IDENT.read_text())
    pp = rows(PASSPORTS)

    by_id = {m["ModelID"]: m for m in models}
    screened_ids = {s["ModelID"] for s in screens}
    screened = [by_id[i] for i in screened_ids if i in by_id]

    # ---------- bridge cohort C into Passports ----------
    pp_by_hcmi = {}
    pp_by_cosmic = {}
    pp_by_name = {}
    for r in pp:
        if r.get("HCMI"):
            pp_by_hcmi.setdefault(r["HCMI"].strip(), []).append(r)
        if r.get("COSMIC_ID"):
            pp_by_cosmic.setdefault(norm_num(r["COSMIC_ID"]), []).append(r)
        if r.get("model_name"):
            pp_by_name.setdefault(r["model_name"].strip(), []).append(r)

    ident_names = {
        mm["model"]
        for g in ident.get("groups", {}).values()
        for mm in g.get("models", [])
        if mm.get("model")
    }
    ident_sidp = set(ident.get("groups", {}).keys())

    cover = {"by_HCMI_sample_ID": 0, "by_COSMIC_donor_ID": 0, "by_identity_name": 0}
    c_pp_rows = {}  # cohort sample_ID -> passports row (first hit, route recorded)
    routes = {}
    for r in cohort:
        sid = r["sample_ID"]
        hit, route = None, None
        if sid in pp_by_hcmi:
            hit, route = pp_by_hcmi[sid][0], "by_HCMI_sample_ID"
        elif norm_num(r["donor_ID"]) in pp_by_cosmic:
            hit, route = pp_by_cosmic[norm_num(r["donor_ID"])][0], "by_COSMIC_donor_ID"
        if hit is not None:
            c_pp_rows[sid] = hit
            routes[sid] = route
            cover[route] += 1
    name_hits = [pp_by_name[n][0] for n in ident_names if n in pp_by_name]
    cover["by_identity_name"] = len(name_hits)

    c_patients_sidp = {r["patient_id"] for r in c_pp_rows.values() if r.get("patient_id")}
    c_patients_sidp |= {r["patient_id"] for r in name_hits if r.get("patient_id")}
    c_patients_sidp |= ident_sidp
    c_sidm = {r["model_id"] for r in c_pp_rows.values() if r.get("model_id")}
    c_sidm |= {r["model_id"] for r in name_hits if r.get("model_id")}
    c_broad = {r["BROAD_ID"] for r in c_pp_rows.values() if r.get("BROAD_ID")}

    # every Passports model belonging to a C patient (patient-level exclusion)
    c_patient_pp = [r for r in pp if r.get("patient_id") in c_patients_sidp]
    c_patient_sidm = {r["model_id"] for r in c_patient_pp if r.get("model_id")}
    c_patient_broad = {r["BROAD_ID"] for r in c_patient_pp if r.get("BROAD_ID")}
    c_patient_cosmic = {norm_num(r["COSMIC_ID"]) for r in c_patient_pp if r.get("COSMIC_ID")}
    c_patient_names = {r["model_name"].strip() for r in c_patient_pp if r.get("model_name")}

    # ---------- overlap of DepMap Model.csv with C (per key, then union) ----------
    def hit_models(pred):
        return {m["ModelID"] for m in models if pred(m)}

    keys = {
        "ModelID_in_C_BROAD_IDs": hit_models(lambda m: m["ModelID"] in c_patient_broad),
        "SangerModelID_in_C_patient_SIDMs": hit_models(
            lambda m: (m.get("SangerModelID") or "") in c_patient_sidm
        ),
        "COSMICID_norm_in_C_patient_COSMIC": hit_models(
            lambda m: norm_num(m.get("COSMICID", "")) in c_patient_cosmic
            and bool(m.get("COSMICID"))
        ),
        "CellLineName_in_C_patient_names": hit_models(
            lambda m: (m.get("CellLineName") or "") in c_patient_names
            or (m.get("StrippedCellLineName") or "") in c_patient_names
        ),
        "HCMIID_in_cohort_sample_IDs": hit_models(
            lambda m: (m.get("HCMIID") or "") in {r["sample_ID"] for r in cohort}
        ),
    }
    union_hit = set().union(*keys.values()) if keys else set()
    overlap_patients = {
        by_id[i]["PatientID"] for i in union_hit if by_id[i].get("PatientID")
    }

    disjoint = [m for m in screened if m["ModelID"] not in union_hit]
    disjoint_patients = {
        m["PatientID"]
        for m in disjoint
        if m.get("PatientID") and m["PatientID"] not in overlap_patients
    }
    strict = [m for m in disjoint if m.get("PatientID") in disjoint_patients]
    organoid_strict = [m for m in strict if m.get("ModelType") == "Organoid"]

    def dist(field, subset):
        return dict(Counter((m.get(field) or "<missing>") for m in subset).most_common())

    coverage_full = len(c_pp_rows) == len(cohort)
    report = {
        "generation": "sgen010",
        "version": 2,
        "supersedes_note": "v1 keys did not connect; v1 retained, verdict not used",
        "inputs": {
            "Model.csv": {"sha256": sha(MODEL), "rows": len(models)},
            "CRISPRScreenMap.csv": {"sha256": sha(SCREEN), "rows": len(screens)},
            "passports_model_list_20260921.csv": {"sha256": sha(PASSPORTS), "rows": len(pp)},
            "cohort_C_models": len(cohort),
        },
        "bridge_coverage": {
            **cover,
            "cohort_models_mapped_to_passports": len(c_pp_rows),
            "cohort_models_unmapped": len(cohort) - len(c_pp_rows),
            "unmapped_sample_IDs": sorted(
                r["sample_ID"] for r in cohort if r["sample_ID"] not in c_pp_rows
            )[:20],
            "C_patients_SIDP_identified": len(c_patients_sidp),
            "expected_C_patients": 142,
            "C_patient_passports_models_total": len(c_patient_pp),
            "C_direct_BROAD_IDs": len(c_broad),
        },
        "model_table": {
            "models": len(models),
            "distinct_PatientID": len({m["PatientID"] for m in models if m.get("PatientID")}),
            "GrowthPattern": dist("GrowthPattern", models),
            "ModelType": dist("ModelType", models),
        },
        "screened": {
            "screens": len(screens),
            "distinct_screened_ModelID": len(screened_ids),
            "screened_models_in_Model_table": len(screened),
            "ModelType": dist("ModelType", screened),
        },
        "cohort_C_overlap_by_key": {k: len(v) for k, v in keys.items()},
        "union_overlap_models": len(union_hit),
        "union_overlap_screened_models": len(union_hit & screened_ids),
        "overlap_models_listed": sorted(union_hit),
        "disjoint_screened_pool": {
            "models": len(disjoint),
            "patients": len(disjoint_patients),
            "patient_strict_models": len(strict),
            "organoid_patient_strict_models": len(organoid_strict),
            "organoid_patient_strict_patients": len(
                {m["PatientID"] for m in organoid_strict if m.get("PatientID")}
            ),
            "GrowthPattern_patient_strict": dist("GrowthPattern", strict),
            "ModelType_patient_strict": dist("ModelType", strict),
        },
        "key_connectivity": {
            "bridge_full_coverage": coverage_full,
            "disjointness_basis": (
                "patient-level via Passports SIDP for all 148 C models"
                if coverage_full
                else "PARTIAL: disjointness proven only for bridged subset; unmapped C models listed"
            ),
        },
    }
    ok = len(strict) >= 100 and len(disjoint_patients) >= 100
    report["verdict"] = "POOL_IDENTIFIED" if ok else "POOL_TOO_SMALL"
    report["verdict_qualified"] = (
        report["verdict"] if coverage_full else report["verdict"] + "_BRIDGE_PARTIAL"
    )
    report["decision_rule"] = "SPEC: >=100 patient-strict disjoint screened models AND >=100 disjoint patients"

    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({
        "verdict_qualified": report["verdict_qualified"],
        "bridge_coverage": report["bridge_coverage"],
        "cohort_C_overlap_by_key": report["cohort_C_overlap_by_key"],
        "union_overlap_screened_models": report["union_overlap_screened_models"],
        "disjoint_screened_pool": report["disjoint_screened_pool"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
