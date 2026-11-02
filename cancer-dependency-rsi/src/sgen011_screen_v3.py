#!/usr/bin/env python3
"""sgen011-C: metadata-only identifiability discriminator (SPEC locked).

Provenance audit for screening-environment fields + attainable-precision
computations for framings A and B. No dependency outcomes in any input.
"""
import csv
import hashlib
import json
import math
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "Model.csv": (ROOT / "data/Model.csv",
                  "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7"),
    "CRISPRScreenMap.csv": (ROOT / "data/CRISPRScreenMap.csv",
                            "43cc528614053d4c5a96729c2d782375227231a0cfea23de6c519b8989fa1252"),
}
POOL = ROOT / "generations/sgen010/established_pool_v4.json"
POOL_SHA256 = "0c1080f8a4330e9be93b1fa0e0821fdf557a7985403b0ffa9d0129a0614bb26b"
SCREEN7 = ROOT / "generations/sgen010/screen_v7.json"
SCREEN7_SHA256 = "d6e6eb69a9f239ea61671397a16031a8c78be9330f049f17437ce3698832766e"


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
OUT = ROOT / "generations/sgen011/screen_v3.json"
LOCK_S_RHO = 0.146

# fields that could plausibly denote environment; classification fixed in SPEC:
# onboarding annotations do NOT establish screened-in environment.
ENV_CANDIDATES = ["GrowthPattern", "OnboardedMedia", "FormulationID",
                  "SerumFreeMedia", "PlateCoating", "ModelDerivationMaterial"]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path):
    with p.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def min_detectable_rho(n: int, alpha: float = 0.05) -> float:
    """80% power, two-sided, Fisher-z for Spearman/Pearson-type correlation."""
    if n <= 3:
        return float("inf")
    from statistics import NormalDist
    z = NormalDist().inv_cdf(1 - alpha / 2) + NormalDist().inv_cdf(0.80)
    return math.tanh(z / math.sqrt(n - 3))


def main() -> int:
    for name, (p, want) in FILES.items():
        if sha(p) != want:
            print(f"REFUSING: {name} hash mismatch")
            return 1
    if sha(POOL) != POOL_SHA256 or sha(SCREEN7) != SCREEN7_SHA256:
        print("REFUSING: derived-input (pool/screen_v7) hash mismatch vs pinned values")
        return 1
    models = rows(FILES["Model.csv"][0])
    screens = rows(FILES["CRISPRScreenMap.csv"][0])
    pool = json.loads(POOL.read_text())
    by_id = {m["ModelID"]: m for m in models}
    est = [by_id[i] for i in pool["established_model_ids"]]

    # reconstruct patient components from pinned assignments (DM PatientID <-> SIDP)
    assign = pool["assignments_screened"]
    dsu = DSU()
    for m in est:
        node = ("DM", m.get("PatientID") or "")
        dsu.find(node)
        pat = assign[m["ModelID"]].get("patient")
        if pat:
            dsu.union(node, ("SIDP", pat))

    def components(subset):
        return len({dsu.find(("DM", m.get("PatientID") or "")) for m in subset})

    n_components = components(est)
    n_sidp = len({assign[m["ModelID"]]["patient"] for m in est
                  if assign[m["ModelID"]].get("patient")})
    v7 = json.loads(SCREEN7.read_text())
    assert n_components == v7["classification"]["established"]["linked_patient_components"], \
        (n_components, "reconstruction != v7")
    assert n_sidp == v7["classification"]["established"]["confirmed_SIDP_patients"]

    # (1) provenance audit
    screen_fields = list(screens[0].keys()) if screens else []
    field_pop = {}
    for col in ENV_CANDIDATES:
        pop = sum(1 for m in est if (m.get(col) or "").strip())
        field_pop[col] = {"populated_established": pop, "rate": round(pop / len(est), 4),
                          "distinct": len({m.get(col) for m in est if m.get(col)})}
    provenance = {
        "CRISPRScreenMap_fields": screen_fields,
        "screen_level_environment_field_present": False,
        "note": ("Screen map carries identifiers only; no per-screen format/medium. "
                 "Model.csv environment-adjacent fields are onboarding annotations "
                 "(OnboardedMedia/GrowthPattern/FormulationID), which per locked SPEC "
                 "and xhigh ruling do not establish the screened-in environment."),
        "field_population": field_pop,
        "verdict": "FAIL",
    }

    # (2) precision A (pooled + largest lineages, components approximated by
    # DepMap PatientID counts within established pool as metadata proxy)
    def patient_n(subset):
        return len({m.get("PatientID") for m in subset if m.get("PatientID")})

    cell_lines = [m for m in est if m.get("ModelType") == "Cell Line"]
    n_comp_A = components(cell_lines)
    precA = {"population": "established CELL LINES only (amendment v2)",
             "models": len(cell_lines), "linked_patient_components": n_comp_A,
             "pooled_min_detectable_rho": round(min_detectable_rho(n_comp_A), 4),
             "interpretation": "optimistic Fisher-z bound only; NOT feasibility (SPEC amendment v2)"}
    lin = Counter(m.get("OncotreeLineage") for m in cell_lines)
    precA["largest5_lineages"] = {}
    for name_, _ in lin.most_common(5):
        sub = [m for m in cell_lines if m.get("OncotreeLineage") == name_]
        n = components(sub)
        precA["largest5_lineages"][name_] = {
            "linked_patient_components": n,
            "min_detectable_rho_alpha05": round(min_detectable_rho(n), 4),
            "min_detectable_rho_FWER5": round(min_detectable_rho(n, 0.01), 4)}
    precA["pass"] = precA["pooled_min_detectable_rho"] <= LOCK_S_RHO

    # (3) precision B: established organoids
    org = [m for m in est if m.get("ModelType") == "Organoid"]
    nB = components(org)
    precB = {"established_organoid_models": len(org), "patients": nB,
             "min_detectable_rho": round(min_detectable_rho(nB), 4),
             "pass": min_detectable_rho(nB) <= LOCK_S_RHO,
             "n_required_for_rho_0.146": int(math.ceil(
                 (2.8016 / math.atanh(LOCK_S_RHO)) ** 2 + 3))}

    a_pass = provenance["verdict"] == "PASS" and precA["pass"]
    # B prerequisites as executable gates (SPEC amendment v2): precision alone never passes B
    b_gates = {"precision": bool(precB["pass"]),
               "authoritative_crosswalk_for_unresolved_organoids": False,
               "renewed_component_level_C_exclusion": False}
    b_pass = all(b_gates.values())
    precB["prerequisite_gates"] = b_gates
    verdict = ("B_PREFERRED" if a_pass and b_pass else
               "A_ONLY" if a_pass else "B_ONLY" if b_pass else "NEITHER_PASSES")

    report = {
        "generation": "sgen011-C", "version": 3,
        "inputs": {**{k: {"sha256": v[1]} for k, v in FILES.items()},
                   "established_pool_v4.json": {"sha256": POOL_SHA256},
                   "screen_v7.json": {"sha256": SCREEN7_SHA256}},
        "population": {"established_models": len(est),
                       "confirmed_SIDP_v7": n_sidp,
                       "linked_patient_components_v7": n_components},
        "provenance_A": provenance,
        "precision_A": precA,
        "precision_B": precB,
        "A_pass": a_pass, "B_pass": b_pass,
        "verdict": verdict,
        "decision_rule": "SPEC: A needs provenance+precision; B needs precision AND crosswalk AND renewed C-exclusion; both->B; neither->reject outcome generation",
        "consequence": ("Outcome generation rejected on current metadata. Next capital: "
                        "(i) authoritative identity crosswalk for the 97 unresolved screened "
                        "organoids (B needs ~%d organoid patients for rho=0.146 at 80%% power); "
                        "(ii) screening-environment provenance source for A."
                        % precB["n_required_for_rho_0.146"]) if verdict == "NEITHER_PASSES" else "proceed to locked outcome design for surviving framing",
    }
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({"verdict": verdict, "A_pass": a_pass, "B_pass": b_pass,
                      "provenance_A": provenance["verdict"],
                      "precision_A_pooled": precA["pooled_min_detectable_rho"],
                      "precision_B": precB}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
