#!/usr/bin/env python3
"""sgen013: outcome-blind feasibility of one-sample lability transport.

METADATA/COVERAGE ONLY. Counts presence of source paired-format observations
(atlas/v4, development source) per patient component x candidate endpoint
(gene). Predictor VALUES are never inspected for selection: endpoint choice is
by eligible component count, tie by ascending gene symbol (SPEC rule). No
CRISPR outcome file is read. Gene.csv is never read.
"""
import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parent.parent
PINS = {
    "data/Model.csv": "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7",
    "generations/sgen010/established_pool_v4.json": "0c1080f8a4330e9be93b1fa0e0821fdf557a7985403b0ffa9d0129a0614bb26b",
    "generations/sgen010/screen_v7.json": "d6e6eb69a9f239ea61671397a16031a8c78be9330f049f17437ce3698832766e",
}
OUT = ROOT / "generations/sgen013/screen_v1.json"
ZSUM = NormalDist().inv_cdf(0.975) + NormalDist().inv_cdf(0.80)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


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


def mdr_one_sample(n, p_cov):
    df = n - 3 - p_cov
    if df <= 0:
        return float("inf")
    return math.tanh(ZSUM / math.sqrt(df))


def main() -> int:
    for rel, want in PINS.items():
        if sha(ROOT / rel) != want:
            print(f"REFUSING: pin mismatch {rel}")
            return 1
    # atlas inputs pinned transitively via sgen002-verified manifest
    man = json.loads((ROOT / "atlas/v4/manifest.json").read_text())
    atlas_pins = {}
    for rel, digest in {**man.get("inputs", {}), **man.get("code", {})}.items():
        p = ROOT / rel
        if p.exists():
            assert sha(p) == digest, f"atlas manifest hash mismatch: {rel}"
            atlas_pins[rel] = digest

    models = rows("data/Model.csv")
    pool = json.loads((ROOT / "generations/sgen010/established_pool_v4.json").read_text())
    v7 = json.loads((ROOT / "generations/sgen010/screen_v7.json").read_text())
    paired = rows("atlas/v4/paired_observations.csv")
    genes_tbl = rows("atlas/v4/genes.csv")

    by_id = {m["ModelID"]: m for m in models}
    assign = pool["assignments_screened"]
    est = [by_id[i] for i in pool["established_model_ids"]]

    dsu = DSU()
    for m in est:
        node = ("DM", m.get("PatientID") or "")
        dsu.find(node)
        pat = assign[m["ModelID"]].get("patient")
        if pat:
            dsu.union(node, ("SIDP", pat))
    comp_of = {m["ModelID"]: dsu.find(("DM", m.get("PatientID") or "")) for m in est}
    assert len(set(comp_of.values())) == \
        v7["classification"]["established"]["linked_patient_components"]

    # SPEC population: 729 establishable models from sgen012 v4 retained set
    s12_audit = json.loads((ROOT / "generations/sgen012/screen_v4_audit.json").read_text())
    retained_models = set(s12_audit["exclusion_membership"]["established_models"])
    retained_comps = {comp_of[m] for m in retained_models}
    assert len(retained_models) == 729 and len(retained_comps) == 724

    # one model per component: ascending canonical ModelID (SPEC unit rule)
    comp_model = {}
    for mid in sorted(retained_models):
        comp_model.setdefault(comp_of[mid], mid)
    selected_models = set(comp_model.values())

    # coverage ONLY: presence of paired-format observation per (model, gene).
    # L exists where an observed paired row exists on a format/medium axis with
    # both scores present (B = reference-condition score presence is the same row).
    cov = defaultdict(set)          # gene -> set(components with L+B via selected model)
    cov_any_model = defaultdict(set)  # gene -> components via ANY retained model (diagnostic)
    bundles = defaultdict(set)      # gene -> set((screen_a, screen_b)) among selected
    axis_cov = Counter()
    for r in paired:
        mid = r.get("model_id")
        if mid not in retained_models:
            continue
        if not (r.get("score_a") and r.get("score_b") and r.get("delta_a_minus_b")):
            continue
        g, c = r["gene"], comp_of[mid]
        cov_any_model[g].add(c)
        if mid in selected_models:
            cov[g].add(c)
            bundles[g].add((r.get("screen_a"), r.get("screen_b")))
            axis_cov[r.get("axis")] += 1

    ranked = sorted(cov.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    panel = {g["gene"]: g for g in genes_tbl}
    report = {
        "generation": "sgen013", "version": 1,
        "inputs": {**{k: {"sha256": v} for k, v in PINS.items()},
                   "atlas/v4 (manifest-verified)": atlas_pins},
        "population": {"retained_models": len(retained_models),
                       "retained_components": len(retained_comps),
                       "selected_one_model_per_component": len(selected_models)},
        "coverage": {
            "genes_with_any_paired_coverage_selected_models": len(cov),
            "genes_with_any_paired_coverage_any_retained_model": len(cov_any_model),
            "top10_by_components": [{"gene": g, "components": len(cs)}
                                    for g, cs in ranked[:10]],
            "axis_rows_selected": dict(axis_cov),
        },
        "identity_gate": {
            "component_level_LB_mapping_exists": bool(cov),
            "source": "atlas/v4 paired_observations (development paired screens; per model x gene deltas)",
            "donor_id_in_atlas": "unresolved (atlas field); component identity via sgen010 pinned assignments on ModelID",
            "gene_level_copying": False,
            "lock_s_reuse": "Lock-S is spent; panel-level result is context only, not component evidence",
        },
    }

    if not ranked:
        report.update({"verdict": "FAIL", "failed_requirement": "no candidate endpoint with component-level L/B coverage",
                       "resource_needed": "independently measured paired-format L/B on matched components"})
        return _finish(report)

    gene, comps = ranked[0]
    n = len(comps)
    lineages = {by_id[comp_model[c]].get("OncotreeLineage") for c in comps}
    lineages.discard(None); lineages.discard("")
    p_cov = 1 + max(0, len(lineages) - 1)  # rank(B) + lineage indicators
    mdr = mdr_one_sample(n, p_cov)
    n_bundles = len(bundles[gene])
    mdr_bundle = mdr_one_sample(min(n, n_bundles), p_cov)
    precision_pass = mdr <= 0.146 and mdr_bundle <= 0.146

    # policy feasibility (SPEC): assay availability = selected components have an
    # eligible established screen (by construction of the retained population);
    # direction must be justifiable outcome-blind from source definitions.
    direction = {
        "proposed": "prioritize components with larger |L| (greater paired-format lability) for confirmation",
        "outcome_blind_rationale": ("Lock-S source definition: genes with greater measured paired-format "
                                    "lability showed greater external rank displacement; confirmation "
                                    "priority targets the components where dependency is least "
                                    "environment-stable. Registered here WITHOUT CRISPR outcome inspection."),
        "status": "registered_candidate_not_validated",
    }
    K = math.ceil(0.10 * n)
    policy_pass = bool(n and K >= 1)

    report.update({
        "selected_endpoint": gene,
        "selected_components": n,
        "distinct_source_bundles": n_bundles,
        "lineages_in_cohort": len(lineages),
        "p_covariates": p_cov,
        "mdr": round(mdr, 4) if mdr != float("inf") else None,
        "mdr_bundle_capped": round(mdr_bundle, 4) if mdr_bundle != float("inf") else None,
        "precision_pass": precision_pass,
        "panel_row_for_endpoint": {k: panel.get(gene, {}).get(k) for k in
                                   ("panel_member", "confirmatory_eligible",
                                    "development_primary_eligible", "atlas_status")},
        "policy": {"K_slots": K, "budget_normalized_units": K, **direction,
                   "feasibility_pass": policy_pass},
    })
    ok = precision_pass and policy_pass and report["identity_gate"]["component_level_LB_mapping_exists"]
    report["verdict"] = "PASS" if ok else "FAIL"
    if not ok:
        failed = []
        if not precision_pass:
            failed.append(f"precision (MDR {report['mdr']} / bundle-capped {report['mdr_bundle_capped']} vs 0.146 at n={n})")
        if not policy_pass:
            failed.append("policy feasibility")
        report["failed_requirement"] = "; ".join(failed)
        report["resource_needed"] = ("more independent components with measured paired-format L/B "
                                     "for a single endpoint, or an endpoint with broader paired coverage")
    return _finish(report)


def _finish(report) -> int:
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({k: report.get(k) for k in
                      ("verdict", "coverage", "selected_endpoint", "selected_components",
                       "mdr", "mdr_bundle_capped", "precision_pass", "failed_requirement")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
