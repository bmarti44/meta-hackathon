#!/usr/bin/env python3
"""sgen010: DepMap 26Q3 metadata discriminator. Metadata only — no outcomes.

Reads data/Model.csv + data/CRISPRScreenMap.csv (user-supplied), the locked
lock_s/cohort.csv and the sgen001 identity reconciliation. Writes an
exclusive-create JSON report under generations/sgen010/.
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
OUT = ROOT / "generations/sgen010/screen_v1.json"

EXPECTED_SHA = {
    "Model.csv": "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7",
    "CRISPRScreenMap.csv": "43cc528614053d4c5a96729c2d782375227231a0cfea23de6c519b8989fa1252",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path):
    with p.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def main() -> int:
    for name, p in (("Model.csv", MODEL), ("CRISPRScreenMap.csv", SCREEN)):
        actual = sha(p)
        if actual != EXPECTED_SHA[name]:
            print(f"REFUSING: {name} sha256 {actual} != locked {EXPECTED_SHA[name]}")
            return 1

    models = rows(MODEL)
    screens = rows(SCREEN)
    cohort = rows(COHORT)
    ident = json.loads(IDENT.read_text())

    by_id = {m["ModelID"]: m for m in models}
    patients = {m["PatientID"] for m in models if m.get("PatientID")}
    screened_ids = {s["ModelID"] for s in screens}
    screened = [by_id[i] for i in screened_ids if i in by_id]
    screened_patients = {m["PatientID"] for m in screened if m.get("PatientID")}

    # --- cohort C key sets ---
    c_donor = {r["donor_ID"] for r in cohort}
    c_sample = {r["sample_ID"] for r in cohort}
    c_names = set()
    for grp in ident.get("groups", {}).values():
        for mm in grp.get("models", []):
            if mm.get("model"):
                c_names.add(mm["model"])

    # --- overlap on every candidate key (report each separately) ---
    overlap = {}
    key_models = {}
    cosmic_hit = {m["ModelID"] for m in models if m.get("COSMICID") in c_donor}
    overlap["cohort_donor_ID__vs__Model_COSMICID"] = len(cosmic_hit)
    key_models["cosmic"] = cosmic_hit

    name_hit = {
        m["ModelID"]
        for m in models
        if m.get("CellLineName") in c_names or m.get("StrippedCellLineName") in c_names
    }
    overlap["identity_model_names__vs__CellLineName"] = len(name_hit)
    key_models["name"] = name_hit

    id_cols = ["SangerModelID", "WTSIMasterCellID", "HCMIID", "ModelIDAlias", "CCLEName"]
    sample_hit = set()
    for m in models:
        for col in id_cols:
            v = (m.get(col) or "").strip()
            if v and v in c_sample:
                sample_hit.add(m["ModelID"])
    overlap["cohort_sample_ID__vs__Model_id_columns"] = len(sample_hit)
    key_models["sample"] = sample_hit

    union_hit = cosmic_hit | name_hit | sample_hit
    overlap["union_any_key_models"] = len(union_hit)
    overlap["union_any_key_screened_models"] = len(union_hit & screened_ids)
    overlap_patients = {by_id[i]["PatientID"] for i in union_hit if by_id[i].get("PatientID")}

    # --- disjoint screened pool ---
    disjoint_models = [m for m in screened if m["ModelID"] not in union_hit]
    disjoint_patients = {
        m["PatientID"]
        for m in disjoint_models
        if m.get("PatientID") and m["PatientID"] not in overlap_patients
    }
    # patient-strict disjoint models: drop models whose patient overlaps C at all
    strict_models = [
        m for m in disjoint_models if m.get("PatientID") in disjoint_patients
    ]

    def dist(field, subset):
        return dict(Counter((m.get(field) or "<missing>") for m in subset).most_common())

    report = {
        "generation": "sgen010",
        "inputs": {
            "Model.csv": {"sha256": sha(MODEL), "rows": len(models)},
            "CRISPRScreenMap.csv": {"sha256": sha(SCREEN), "rows": len(screens)},
            "cohort_C_models": len(cohort),
            "cohort_C_locked_donor_IDs": len(c_donor),
            "cohort_C_identity_names_available": len(c_names),
        },
        "model_table": {
            "models": len(models),
            "distinct_PatientID": len(patients),
            "models_missing_PatientID": sum(1 for m in models if not m.get("PatientID")),
            "GrowthPattern": dist("GrowthPattern", models),
            "ModelType": dist("ModelType", models),
        },
        "screened": {
            "screens": len(screens),
            "distinct_screened_ModelID": len(screened_ids),
            "screened_models_in_Model_table": len(screened),
            "distinct_screened_PatientID": len(screened_patients),
            "GrowthPattern": dist("GrowthPattern", screened),
            "ModelType": dist("ModelType", screened),
        },
        "cohort_C_overlap_by_key": overlap,
        "overlap_models_listed": sorted(union_hit),
        "disjoint_screened_pool": {
            "models": len(disjoint_models),
            "patients": len(disjoint_patients),
            "patient_strict_models": len(strict_models),
            "GrowthPattern_patient_strict": dist("GrowthPattern", strict_models),
            "ModelType_patient_strict": dist("ModelType", strict_models),
        },
    }
    ok = len(strict_models) >= 100 and len(disjoint_patients) >= 100
    report["verdict"] = "POOL_IDENTIFIED" if ok else "POOL_TOO_SMALL"
    report["decision_rule"] = ">=100 patient-strict disjoint screened models AND >=100 disjoint patients"

    OUT.parent.mkdir(parents=True, exist_ok=True)
        # exclusive create: never overwrite a prior report version
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({k: report[k] for k in ("verdict", "cohort_C_overlap_by_key", "disjoint_screened_pool")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
