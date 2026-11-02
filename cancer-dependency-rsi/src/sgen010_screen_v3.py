#!/usr/bin/env python3
"""sgen010 v3: full patient-level disjointness via reproduced Witness-A bridge.

Reproduces pgen003 Witness A locally (normalized model_name+synonyms join of
cohort sample_IDs on passports_model_list_20260921.csv). Refuses to proceed
unless it reproduces pgen003's published counts (148 resolved, 0 multi, 142
patients). Then excludes every DepMap model tied to a C patient through any
Passports model of that patient. Metadata only.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL = ROOT / "data/Model.csv"
SCREEN = ROOT / "data/CRISPRScreenMap.csv"
COHORT = ROOT / "lock_s/cohort.csv"
PASSPORTS = ROOT / "data/passports_model_list_20260921.csv"
PGEN003 = ROOT / "generations/pgen003/probe_results_v1.json"
OUT = ROOT / "generations/sgen010/screen_v3.json"
MAP_OUT = ROOT / "generations/sgen010/cohort_C_patient_map_v1.json"

EXPECTED_SHA = {
    "Model.csv": "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7",
    "CRISPRScreenMap.csv": "43cc528614053d4c5a96729c2d782375227231a0cfea23de6c519b8989fa1252",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path):
    with p.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def norm(s) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(s or "").upper())


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
    pp = rows(PASSPORTS)
    wa_ref = json.loads(PGEN003.read_text())["witness_A"]

    # --- reproduce Witness A exactly (pgen003_probe.py logic) ---
    key = {}
    for r in pp:
        for cand in [r.get("model_name")] + re.split(r"[|;]", str(r.get("synonyms") or "")):
            k = norm(cand)
            if k:
                key.setdefault(k, set()).add(str(r["patient_id"]))
    c_res, c_unres, c_multi = {}, [], []
    for r in cohort:
        s = r["sample_ID"]
        pats = key.get(norm(s), set())
        if len(pats) == 1:
            c_res[s] = next(iter(pats))
        elif len(pats) == 0:
            c_unres.append(s)
        else:
            c_multi.append(s)
    reproduced = {
        "resolved": len(c_res),
        "unresolved": len(c_unres),
        "multi_patient": len(c_multi),
        "unique_c_patients_passports": len(set(c_res.values())),
    }
    expected = {
        "resolved": wa_ref["resolved"],
        "unresolved": len(wa_ref["unresolved"]),
        "multi_patient": len(wa_ref["multi_patient"]),
        "unique_c_patients_passports": wa_ref["unique_c_patients_passports"],
    }
    if reproduced != expected:
        print(f"REFUSING: Witness-A reproduction mismatch {reproduced} != pgen003 {expected}")
        return 1

    with MAP_OUT.open("x") as f:
        json.dump(
            {"source": "pgen003 Witness A reproduced by sgen010 v3",
             "counts": reproduced, "sample_ID_to_SIDP": dict(sorted(c_res.items()))},
            f, indent=2)
        f.write("\n")

    c_patients = set(c_res.values())
    c_pp = [r for r in pp if str(r.get("patient_id")) in c_patients]
    c_sidm = {r["model_id"] for r in c_pp if r.get("model_id")}
    c_broad = {r["BROAD_ID"] for r in c_pp if r.get("BROAD_ID")}
    c_cosmic = {norm_num(r["COSMIC_ID"]) for r in c_pp if r.get("COSMIC_ID")}
    c_names = {norm(r["model_name"]) for r in c_pp if r.get("model_name")}
    for r in c_pp:  # synonyms of C-patient models are also C names
        for cand in re.split(r"[|;]", str(r.get("synonyms") or "")):
            if norm(cand):
                c_names.add(norm(cand))
    c_hcmi = {r["HCMI"].strip() for r in c_pp if r.get("HCMI")}

    by_id = {m["ModelID"]: m for m in models}
    screened_ids = {s["ModelID"] for s in screens}
    screened = [by_id[i] for i in screened_ids if i in by_id]

    def hit(pred):
        return {m["ModelID"] for m in models if pred(m)}

    keys = {
        "ModelID_in_C_patient_BROAD_IDs": hit(lambda m: m["ModelID"] in c_broad),
        "SangerModelID_in_C_patient_SIDMs": hit(lambda m: (m.get("SangerModelID") or "") in c_sidm),
        "COSMICID_norm_in_C_patient_COSMIC": hit(
            lambda m: bool(m.get("COSMICID")) and norm_num(m["COSMICID"]) in c_cosmic),
        "name_norm_in_C_patient_names": hit(
            lambda m: norm(m.get("CellLineName")) in c_names
            or norm(m.get("StrippedCellLineName")) in c_names),
        "HCMIID_in_C_patient_HCMI": hit(lambda m: (m.get("HCMIID") or "") in c_hcmi),
    }
    union_hit = set().union(*keys.values())
    overlap_patients = {by_id[i]["PatientID"] for i in union_hit if by_id[i].get("PatientID")}

    disjoint = [m for m in screened if m["ModelID"] not in union_hit]
    disjoint_patients = {
        m["PatientID"] for m in disjoint
        if m.get("PatientID") and m["PatientID"] not in overlap_patients
    }
    strict = [m for m in disjoint if m.get("PatientID") in disjoint_patients]
    organoid = [m for m in strict if m.get("ModelType") == "Organoid"]

    def dist(field, subset):
        return dict(Counter((m.get(field) or "<missing>") for m in subset).most_common())

    report = {
        "generation": "sgen010",
        "version": 3,
        "inputs": {
            "Model.csv": {"sha256": sha(MODEL), "rows": len(models)},
            "CRISPRScreenMap.csv": {"sha256": sha(SCREEN), "rows": len(screens)},
            "passports_model_list_20260921.csv": {"sha256": sha(PASSPORTS), "rows": len(pp)},
        },
        "witness_A_reproduction": {"reproduced": reproduced, "pgen003_expected": expected,
                                   "match": reproduced == expected,
                                   "map_artifact": "generations/sgen010/cohort_C_patient_map_v1.json"},
        "bridge_coverage": {
            "cohort_models_mapped": len(c_res), "cohort_models_total": len(cohort),
            "C_patients_SIDP": len(c_patients),
            "C_patient_passports_models_total": len(c_pp),
            "C_patient_BROAD_IDs": len(c_broad), "C_patient_SIDMs": len(c_sidm),
        },
        "cohort_C_overlap_by_key": {k: len(v) for k, v in keys.items()},
        "union_overlap_models": len(union_hit),
        "union_overlap_screened_models": len(union_hit & screened_ids),
        "overlap_models_listed": sorted(union_hit),
        "disjoint_screened_pool": {
            "models": len(disjoint), "patients": len(disjoint_patients),
            "patient_strict_models": len(strict),
            "organoid_patient_strict_models": len(organoid),
            "organoid_patient_strict_patients": len({m["PatientID"] for m in organoid if m.get("PatientID")}),
            "GrowthPattern_patient_strict": dist("GrowthPattern", strict),
            "ModelType_patient_strict": dist("ModelType", strict),
        },
        "key_connectivity": {
            "bridge_full_coverage": len(c_res) == len(cohort),
            "disjointness_basis": "patient-level via Passports SIDP, all 148 C models / 142 patients bridged (Witness A reproduced)",
        },
        "decision_rule": "SPEC: >=100 patient-strict disjoint screened models AND >=100 disjoint patients",
    }
    ok = len(strict) >= 100 and len(disjoint_patients) >= 100
    report["verdict"] = "POOL_IDENTIFIED" if ok else "POOL_TOO_SMALL"

    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({"verdict": report["verdict"], "bridge_coverage": report["bridge_coverage"],
                      "cohort_C_overlap_by_key": report["cohort_C_overlap_by_key"],
                      "union_overlap_screened_models": report["union_overlap_screened_models"],
                      "disjoint_screened_pool": report["disjoint_screened_pool"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
