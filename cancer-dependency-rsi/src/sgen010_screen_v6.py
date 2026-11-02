#!/usr/bin/env python3
"""sgen010 v6: tiered identity resolution (responds to sol-high re-review v2, 84).

Strong ID routes (BROAD_ID/SIDM/HCMI/COSMIC, semicolon-tokenized) confirm a
patient only when unanimous; conflicts quarantine. NAME is candidate evidence
only: never an identity edge, but any candidate C hit excludes conservatively.
Patient-component graph spans ALL Model.csv rows (confirmed assignments);
C-component membership is checked before unresolved. SPEC diagnostics restored.
Outputs serialized to temp files and renamed as a pair with rollback.
No dependency-outcome access; Model.csv clinical columns dropped unused.
"""
import csv
import hashlib
import json
import os
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
MAP_SHA256 = "4ddd01592c2d8221eff73d4eded6a051bcac676e1c13fcbd5bc4db91a3ae1f61"
OUT = ROOT / "generations/sgen010/screen_v6.json"
POOL_OUT = ROOT / "generations/sgen010/established_pool_v3.json"
DROP_COLS = {"PatientTreatmentResponse", "PatientTreatmentDetails",
             "PatientTreatmentType", "PatientTreatmentStatus"}
STRONG_ROUTES = ("BROAD_ID", "SIDM", "HCMI", "COSMIC")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path, drop=()):
    with p.open(newline="", encoding="utf-8-sig") as f:
        out = list(csv.DictReader(f))
    for r in out:
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


def tokens(v) -> set:
    """Split a possibly semicolon-multivalued identifier cell."""
    if not v:
        return set()
    return {t.strip() for t in str(v).split(";") if t.strip()}


def assign(strong: dict, name_candidates: set) -> dict:
    """Tiered assignment. strong: route -> set(SIDP). NAME never confirms."""
    strong_pats = set()
    for pats in strong.values():
        strong_pats |= set(pats)
    base = {"strong_routes": {r: sorted(p) for r, p in sorted(strong.items()) if p},
            "strong_patients": sorted(strong_pats),
            "name_candidates": sorted(name_candidates)}
    if len(strong_pats) == 1:
        return {**base, "status": "confirmed", "patient": next(iter(strong_pats))}
    if len(strong_pats) > 1:
        return {**base, "status": "conflict", "patient": None}
    if name_candidates:
        return {**base, "status": "name_only", "patient": None}
    return {**base, "status": "unresolved", "patient": None}


def c_candidate_hit(assignment: dict, c_patients: set) -> bool:
    evidence = set(assignment["strong_patients"]) | set(assignment["name_candidates"])
    return bool(evidence & c_patients)


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


def write_pair(pairs) -> None:
    """Serialize all outputs to unique temp files, then rename; rollback on failure."""
    import uuid
    tag = uuid.uuid4().hex[:12]
    tmps, done = [], []
    try:
        for path, obj in pairs:
            if path.exists():
                raise FileExistsError(f"refusing to overwrite {path}")
            tmp = path.with_name(path.name + f".tmp-{tag}")
            with tmp.open("x") as f:
                json.dump(obj, f, indent=2)
                f.write("\n")
            tmps.append((tmp, path))
        for tmp, path in tmps:
            os.rename(tmp, path)
            done.append(path)
    except Exception:
        for p in done:
            p.unlink(missing_ok=True)
        for tmp, _ in tmps:
            tmp.unlink(missing_ok=True)
        raise


def main() -> int:
    for name, (p, want) in FILES.items():
        if sha(p) != want:
            print(f"REFUSING: {name} hash mismatch vs pinned value")
            return 1

    models = rows(FILES["Model.csv"][0], drop=DROP_COLS)
    screens = rows(FILES["CRISPRScreenMap.csv"][0])
    cohort = rows(FILES["lock_s/cohort.csv"][0])
    pp = rows(FILES["passports_model_list_20260921.csv"][0])

    # --- Witness A (pinned canonical map) ---
    name2pats = {}
    for r in pp:
        for cand in [r.get("model_name")] + re.split(r"[|;]", str(r.get("synonyms") or "")):
            k = norm(cand)
            if k:
                name2pats.setdefault(k, set()).add(str(r["patient_id"]))
    c_res, bad = {}, 0
    for r in cohort:
        pats = name2pats.get(norm(r["sample_ID"]), set())
        if len(pats) == 1:
            c_res[r["sample_ID"]] = next(iter(pats))
        else:
            bad += 1
    canon = json.dumps(dict(sorted(c_res.items())), sort_keys=True,
                       separators=(",", ":")).encode()
    if bad or hashlib.sha256(canon).hexdigest() != MAP_SHA256:
        print("REFUSING: Witness-A map mismatch vs pinned canonical sha256")
        return 1
    c_patients = set(c_res.values())

    # --- strong-route indexes (tokenized, patient sets per key) ---
    idx = {r: {} for r in STRONG_ROUTES}
    for r in pp:
        pat = str(r["patient_id"])
        for route, cell in (("BROAD_ID", r.get("BROAD_ID")), ("SIDM", r.get("model_id")),
                            ("HCMI", r.get("HCMI")), ("COSMIC", r.get("COSMIC_ID"))):
            for t in tokens(cell):
                key = norm_num(t) if route == "COSMIC" else t
                idx[route].setdefault(key, set()).add(pat)

    def strong_for(m):
        out = {}
        checks = (("BROAD_ID", {m["ModelID"]}),
                  ("SIDM", tokens(m.get("SangerModelID"))),
                  ("HCMI", tokens(m.get("HCMIID"))),
                  ("COSMIC", {norm_num(t) for t in tokens(m.get("COSMICID"))}))
        for route, keys in checks:
            pats = set()
            for k in keys:
                pats |= idx[route].get(k, set())
            if pats:
                out[route] = pats
        return out

    def assignment(m):
        nc = name2pats.get(norm(m.get("CellLineName")), set()) | \
            name2pats.get(norm(m.get("StrippedCellLineName")), set())
        return assign(strong_for(m), nc)

    # --- assign ALL models; graph over confirmed only ---
    all_assign = {m["ModelID"]: assignment(m) for m in models}
    by_id = {m["ModelID"]: m for m in models}
    dsu = DSU()
    for m in models:
        node = ("DM", m.get("PatientID") or "")
        dsu.find(node)
        a = all_assign[m["ModelID"]]
        if a["status"] == "confirmed":
            dsu.union(node, ("SIDP", a["patient"]))
    c_components = {dsu.find(("SIDP", p)) for p in c_patients}
    # every SIDP confirmed-linked into a C component is also C-candidate evidence
    c_evidence_patients = set(c_patients)
    for m in models:
        a = all_assign[m["ModelID"]]
        if a["status"] == "confirmed" and \
                dsu.find(("SIDP", a["patient"])) in c_components:
            c_evidence_patients.add(a["patient"])
    # component-level candidate C evidence (any member, any route incl. NAME)
    comp_c_candidate = set()
    for m in models:
        if c_candidate_hit(all_assign[m["ModelID"]], c_evidence_patients):
            comp_c_candidate.add(dsu.find(("DM", m.get("PatientID") or "")))

    screened_ids, seen = [], set()
    for s in screens:
        if s["ModelID"] in by_id and s["ModelID"] not in seen:
            seen.add(s["ModelID"]); screened_ids.append(s["ModelID"])
    screened = [by_id[i] for i in screened_ids]

    buckets = {"established": [], "c_overlap": [], "conflict": [],
               "name_only": [], "unresolved": []}
    for m in screened:
        a = all_assign[m["ModelID"]]
        comp = dsu.find(("DM", m.get("PatientID") or ""))
        if comp in c_components or comp in comp_c_candidate or \
                c_candidate_hit(a, c_evidence_patients):
            buckets["c_overlap"].append(m)
        elif a["status"] == "confirmed":
            buckets["established"].append(m)
        else:
            buckets[a["status"]].append(m)

    def dist(field, subset):
        return dict(Counter((m.get(field) or "<missing>") for m in subset).most_common())

    def summ(subset):
        sidps = {all_assign[m["ModelID"]]["patient"] for m in subset
                 if all_assign[m["ModelID"]]["patient"]}
        comps = {dsu.find(("DM", m.get("PatientID") or "")) for m in subset}
        return {"models": len(subset),
                "DepMap_PatientIDs": len({m.get("PatientID") for m in subset if m.get("PatientID")}),
                "confirmed_SIDP_patients": len(sidps),
                "linked_patient_components": len(comps)}

    # per-key C-overlap diagnostics (candidate evidence, screened models)
    per_key = {}
    for route in STRONG_ROUTES + ("NAME",):
        n = 0
        for m in screened:
            a = all_assign[m["ModelID"]]
            ev = set(a["name_candidates"]) if route == "NAME" else \
                set(a["strong_routes"].get(route, []))
            if ev & c_evidence_patients:
                n += 1
        per_key[route] = n

    est = summ(buckets["established"])
    est_org = [m for m in buckets["established"] if m.get("ModelType") == "Organoid"]
    not_est_org = [m for b in ("c_overlap", "conflict", "name_only", "unresolved")
                   for m in buckets[b] if m.get("ModelType") == "Organoid"]

    report = {
        "generation": "sgen010", "version": 6,
        "inputs": {k: {"sha256": v[1]} for k, v in FILES.items()},
        "witness_A": {"map_canonical_sha256": MAP_SHA256, "verified": True,
                      "models_resolved": len(c_res), "C_patients_SIDP": len(c_patients)},
        "note_dependency_outcomes": "No dependency-outcome access. Model.csv clinical "
                                    "columns parsed by the CSV reader are dropped unused; "
                                    "Passports clinical fields unused.",
        "diagnostics": {
            "Model_rows": len(models),
            "whole_table_distinct_PatientID": len({m.get("PatientID") for m in models if m.get("PatientID")}),
            "screen_rows": len(screens),
            "distinct_screened_ModelID": len(screened_ids),
            "screened_distinct_PatientID": len({m.get("PatientID") for m in screened if m.get("PatientID")}),
            "c_overlap_by_key_candidate_evidence": per_key,
        },
        "model_table": {"GrowthPattern": dist("GrowthPattern", models),
                        "ModelType": dist("ModelType", models),
                        "DepmapModelType": dist("DepmapModelType", models)},
        "screened": {"DepmapModelType": dist("DepmapModelType", screened),
                     "ModelType": dist("ModelType", screened)},
        "classification": {k: summ(v) for k, v in buckets.items()},
        "identity_tiers": "confirmed = unanimous strong ID routes; conflict quarantined; "
                          "NAME = candidate evidence only (never established, always "
                          "conservative for C-exclusion); graph over ALL Model.csv rows, "
                          "confirmed assignments only",
        "organoid_subset": {"established": summ(est_org),
                            "not_established": summ(not_est_org),
                            "residual": "Most screened DepMap organoids lack confirmed "
                                        "Passports linkage; disjointness NOT established for them."},
        "decision_rule": "SPEC: >=100 established models AND >=100 confirmed SIDP patients",
    }
    ok = est["models"] >= 100 and est["confirmed_SIDP_patients"] >= 100
    report["verdict"] = "POOL_IDENTIFIED" if ok else "POOL_TOO_SMALL"
    report["verdict_scope"] = "established (confirmed-identity) pool only"

    pool = {"generation": "sgen010", "version": 3,
            **{f"{k}_model_ids": sorted(m["ModelID"] for m in v)
               for k, v in buckets.items()},
            "assignments_screened": {k: all_assign[k] for k in sorted(screened_ids)}}

    write_pair([(OUT, report), (POOL_OUT, pool)])
    print(json.dumps({"verdict": report["verdict"], "established": est,
                      "buckets": {k: len(v) for k, v in buckets.items()},
                      "organoid_established": len(est_org),
                      "organoid_not_established": len(not_est_org),
                      "per_key_c_overlap": per_key}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
