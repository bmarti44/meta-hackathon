#!/usr/bin/env python3
"""sgen010 v4: established-pool discriminator (responds to sol-high review v1).

Fixes vs v3: identity-resolved vs unresolved classification (unresolved models
are NOT counted as disjoint); patient counting in both DepMap PatientID and
Passports SIDP spaces with connected-component patient-strict exclusion; all
input hashes pinned/enforced; Witness-A map pinned by canonical sha256;
DepmapModelType reported; clinical columns dropped unused (this generation
makes no dependency-outcome access; Model.csv clinical fields are parsed by
the CSV reader and discarded); outputs computed fully before any write.
"""
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "Model.csv": (ROOT / "data/Model.csv",
                  "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7"),
    "CRISPRScreenMap.csv": (ROOT / "data/CRISPRScreenMap.csv",
                            "43cc528614053d4c5a96729c2d782375227231a0cfea23de6c519b8989fa1252"),
    "passports_model_list_20260921.csv": (
        ROOT / "data/passports_model_list_20260921.csv",
        "419f65d1d6534454194f1a744550fab632cd1d7411f6b13411a885735aa37006"),
    "lock_s/cohort.csv": (ROOT / "lock_s/cohort.csv",
                          "11b1d9a7df6e7700e91129e366e55d99844a4cd96ad6a350fe850bcdc2ab168e"),
}
MAP_SHA256 = "4ddd01592c2d8221eff73d4eded6a051bcac676e1c13fcbd5bc4db91a3ae1f61"  # canonical Witness-A map
OUT = ROOT / "generations/sgen010/screen_v4.json"
POOL_OUT = ROOT / "generations/sgen010/established_pool_v1.json"
DROP_COLS = {"PatientTreatmentResponse", "PatientTreatmentDetails",
             "PatientTreatmentType", "PatientTreatmentStatus"}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path, drop=()):
    with p.open(newline="", encoding="utf-8-sig") as f:
        out = list(csv.DictReader(f))
    for r in out:  # discard clinical columns immediately; never used
        for c in drop:
            r.pop(c, None)
    return out


def norm(s) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(s or "").upper())


def norm_num(v: str) -> str:
    v = (v or "").strip()
    try:
        return str(int(float(v)))
    except (ValueError, OverflowError):
        return v


class DSU:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def main() -> int:
    for name, (p, want) in FILES.items():
        if sha(p) != want:
            print(f"REFUSING: {name} hash mismatch vs pinned value")
            return 1

    models = rows(FILES["Model.csv"][0], drop=DROP_COLS)
    screens = rows(FILES["CRISPRScreenMap.csv"][0])
    cohort = rows(FILES["lock_s/cohort.csv"][0])
    pp = rows(FILES["passports_model_list_20260921.csv"][0])

    # --- Witness A reproduction, pinned at identity level ---
    name2pats = {}
    for r in pp:
        for cand in [r.get("model_name")] + re.split(r"[|;]", str(r.get("synonyms") or "")):
            k = norm(cand)
            if k:
                name2pats.setdefault(k, set()).add(str(r["patient_id"]))
    c_res, n_unres, n_multi = {}, 0, 0
    for r in cohort:
        pats = name2pats.get(norm(r["sample_ID"]), set())
        if len(pats) == 1:
            c_res[r["sample_ID"]] = next(iter(pats))
        elif len(pats) == 0:
            n_unres += 1
        else:
            n_multi += 1
    canon = json.dumps(dict(sorted(c_res.items())), sort_keys=True,
                       separators=(",", ":")).encode()
    if hashlib.sha256(canon).hexdigest() != MAP_SHA256 or n_unres or n_multi:
        print("REFUSING: Witness-A map does not match pinned canonical sha256")
        return 1
    c_patients = set(c_res.values())  # 142 SIDP

    # --- resolve every DepMap model to Passports patient(s) ---
    sidm2pat = {r["model_id"]: str(r["patient_id"]) for r in pp if r.get("model_id")}
    broad2pat = {r["BROAD_ID"]: str(r["patient_id"]) for r in pp if r.get("BROAD_ID")}
    cosmic2pat = {norm_num(r["COSMIC_ID"]): str(r["patient_id"]) for r in pp if r.get("COSMIC_ID")}
    hcmi2pat = {r["HCMI"].strip(): str(r["patient_id"]) for r in pp if r.get("HCMI")}

    def resolve(m):
        pats, routes = set(), []
        if m["ModelID"] in broad2pat:
            pats.add(broad2pat[m["ModelID"]]); routes.append("BROAD_ID")
        if (m.get("SangerModelID") or "") in sidm2pat:
            pats.add(sidm2pat[m["SangerModelID"]]); routes.append("SIDM")
        if m.get("COSMICID") and norm_num(m["COSMICID"]) in cosmic2pat:
            pats.add(cosmic2pat[norm_num(m["COSMICID"])]); routes.append("COSMIC")
        if (m.get("HCMIID") or "") in hcmi2pat:
            pats.add(hcmi2pat[m["HCMIID"]]); routes.append("HCMI")
        np_ = name2pats.get(norm(m.get("CellLineName")), set()) | \
            name2pats.get(norm(m.get("StrippedCellLineName")), set())
        if np_:
            pats |= np_; routes.append("NAME")
        return pats, routes

    by_id = {m["ModelID"]: m for m in models}
    screened_ids = []
    seen = set()
    for s in screens:
        if s["ModelID"] in by_id and s["ModelID"] not in seen:
            seen.add(s["ModelID"]); screened_ids.append(s["ModelID"])
    screened = [by_id[i] for i in screened_ids]

    resolution = {}
    for m in screened:
        pats, routes = resolve(m)
        resolution[m["ModelID"]] = {"patients_SIDP": sorted(pats), "routes": routes}

    # --- connected components over DepMap PatientID <-> SIDP (screened only) ---
    dsu = DSU()
    for m in screened:
        node = ("DM", m.get("PatientID") or "")
        dsu.find(node)
        for p in resolution[m["ModelID"]]["patients_SIDP"]:
            dsu.union(node, ("SIDP", p))
    c_components = {dsu.find(("SIDP", p)) for p in c_patients}

    established, unresolved, c_overlap = [], [], []
    for m in screened:
        pats = resolution[m["ModelID"]]["patients_SIDP"]
        if not pats:
            unresolved.append(m)
        elif dsu.find(("DM", m.get("PatientID") or "")) in c_components or \
                any(p in c_patients for p in pats):
            c_overlap.append(m)
        else:
            established.append(m)

    def dist(field, subset):
        return dict(Counter((m.get(field) or "<missing>") for m in subset).most_common())

    def summ(subset):
        sidps = {p for m in subset for p in resolution[m["ModelID"]]["patients_SIDP"]}
        comps = {dsu.find(("DM", m.get("PatientID") or "")) for m in subset}
        return {"models": len(subset),
                "DepMap_PatientIDs": len({m.get("PatientID") for m in subset if m.get("PatientID")}),
                "Passports_SIDP_patients": len(sidps),
                "linked_patient_components": len(comps)}

    est_org = [m for m in established if m.get("ModelType") == "Organoid"]
    unres_org = [m for m in unresolved if m.get("ModelType") == "Organoid"]
    est = summ(established)

    report = {
        "generation": "sgen010", "version": 4,
        "inputs": {k: {"sha256": v[1]} for k, v in FILES.items()},
        "witness_A": {"map_canonical_sha256": MAP_SHA256, "verified": True,
                      "models_resolved": len(c_res), "C_patients_SIDP": len(c_patients)},
        "note_dependency_outcomes": "No dependency-outcome access. Model.csv clinical "
                                    "columns are parsed by the CSV reader and dropped unused.",
        "model_table": {"models": len(models),
                        "GrowthPattern": dist("GrowthPattern", models),
                        "ModelType": dist("ModelType", models),
                        "DepmapModelType": dist("DepmapModelType", models)},
        "screened_total": {"models": len(screened),
                           "DepmapModelType": dist("DepmapModelType", screened)},
        "classification": {
            "established_disjoint": est,
            "c_overlap": summ(c_overlap),
            "identity_unresolved": summ(unresolved),
            "resolution_routes": dict(Counter(
                r for v in resolution.values() for r in v["routes"]).most_common()),
        },
        "organoid_subset": {
            "established": summ(est_org),
            "identity_unresolved": summ(unres_org),
            "residual": "Most screened DepMap organoids have no Passports linkage in "
                        "these metadata; their donor disjointness from C is NOT established here.",
        },
        "patient_space_note": "DepMap PatientID and Passports SIDP partitions differ; "
                              "both spaces and linked components are reported. SIDP space "
                              "is the exclusion space for C.",
        "decision_rule": "SPEC: >=100 established disjoint models AND >=100 patients "
                         "(SIDP space, patient-strict via linked components)",
    }
    ok = est["models"] >= 100 and est["Passports_SIDP_patients"] >= 100
    report["verdict"] = "POOL_IDENTIFIED" if ok else "POOL_TOO_SMALL"
    report["verdict_scope"] = "established (identity-resolved) pool only; unresolved excluded"

    pool = {"generation": "sgen010", "version": 1,
            "established_model_ids": sorted(m["ModelID"] for m in established),
            "unresolved_model_ids": sorted(m["ModelID"] for m in unresolved),
            "c_overlap_model_ids": sorted(m["ModelID"] for m in c_overlap),
            "resolution": {k: resolution[k] for k in sorted(resolution)}}

    # compute-then-write: both artifacts only after full computation succeeds
    with OUT.open("x") as f:
        json.dump(report, f, indent=2); f.write("\n")
    with POOL_OUT.open("x") as f:
        json.dump(pool, f, indent=2); f.write("\n")

    print(json.dumps({"verdict": report["verdict"],
                      "established": est,
                      "c_overlap_models": len(c_overlap),
                      "unresolved_models": len(unresolved),
                      "organoid_established": len(est_org),
                      "organoid_unresolved": len(unres_org),
                      "routes": report["classification"]["resolution_routes"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
