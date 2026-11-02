#!/usr/bin/env python3
"""sgen013 v3: outcome-blind feasibility of one-sample lability transport.

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
    "atlas/v4/paired_observations.csv": "00f7fa86f7c8c74d287b7fc940f6140727c77f1b7ed58ccd85f0e13fe8144801",
    "atlas/v4/genes.csv": "72c01a4b98ec0385367441025b1c6b75780a7bed262e5271e593780d3ec38b80",
    "atlas/v4/manifest.json": "e4206db12133a6904b162f66c4f88a170525caf9fd0d83b5fd9872c536676dcf",
    "generations/sgen012/screen_v4_audit.json": "0f27bf1554dad57e15fe0fdb01ab376137d21939edbd1f1a4bb39ca611d14cb4",
    "data/Model.csv": "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7",
    "generations/sgen010/established_pool_v4.json": "0c1080f8a4330e9be93b1fa0e0821fdf557a7985403b0ffa9d0129a0614bb26b",
    "generations/sgen010/screen_v7.json": "d6e6eb69a9f239ea61671397a16031a8c78be9330f049f17437ce3698832766e",
}
OUT = ROOT / "generations/sgen013/screen_v3.json"
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
        if not p.exists():
            print(f"REFUSING: manifest-listed input missing: {rel}")
            return 1
        if sha(p) != digest:
            print(f"REFUSING: atlas manifest hash mismatch: {rel}")
            return 1
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
    # Registered source definitions (fixed here, before counting):
    # L = signed delta_a_minus_b on the FORMAT axis (Dome - Plastic, medium held);
    # B = score_b (Plastic reference condition). Medium axis is diagnostic only.
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
        if r.get("axis") != "format":
            continue  # primary contrast is the format axis only
        cov_any_model[g].add(c)
        if mid in selected_models:
            cov[g].add(c)
            bundles[g].add((r.get("screen_a"), r.get("screen_b")))
            axis_cov[r.get("axis")] += 1

    panel = {g["gene"]: g for g in genes_tbl}

    def qualified(g):
        row = panel.get(g)
        if row is None:
            return False, "not_in_panel_table"
        reasons = (row.get("development_exclusion_reasons") or "") + ";" + \
                  (row.get("confirmatory_exclusion_reasons") or "")
        if "Tier-A_outcome_informed_selection_exclusion" in reasons:
            return False, "Tier-A outcome-informed selection exclusion (adjudicated: disqualifying - endpoint choice must not inherit outcome-informed selection history)"
        if not (row.get("external_gene_sanger") or "").strip():
            return False, "no adjudicated external identity (external_gene_sanger blank; alias/bridge unadjudicated e.g. TMOD)"
        return True, None

    qual = {g: qualified(g) for g in cov}
    ranked_all = sorted(cov.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ranked = [(g, cs) for g, cs in ranked_all if qual[g][0]]
    diagnostic_candidate = ranked_all[0][0] if ranked_all else None
    report = {
        "generation": "sgen013", "version": 3,
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

    report["endpoint_qualification"] = {
        "covered_genes": len(cov),
        "coverage_qualified_genes": sum(1 for q in qual.values() if q[0]),
        "fully_qualified_genes": 0,
        "qualification_note": "coverage-qualified = passes identity/history screens; FULL qualification additionally requires compatibility + policy-action checks, unmet for every candidate at current coverage; selected endpoint is a diagnostic candidate only",
        "coverage_ranked_diagnostic_candidate": diagnostic_candidate,
        "diagnostic_candidate_qualified": bool(diagnostic_candidate and qual[diagnostic_candidate][0]),
        "disqualifications": {g: q[1] for g, q in qual.items() if not q[0]}}
    if not ranked:
        report.update({"verdict": "FAIL", "failed_requirement": "no QUALIFIED candidate endpoint with component-level L/B coverage",
                       "resource_needed": "independently measured paired-format L/B on matched components + endpoint bridge + source-dependence treatment + confirmation-assay availability metadata"})
        return _finish(report)

    gene, comps = ranked[0]
    n = len(comps)
    lineages = {by_id[comp_model[c]].get("OncotreeLineage") for c in comps}
    lineages.discard(None); lineages.discard("")
    p_cov = 1 + max(0, len(lineages) - 1)  # rank(B) + lineage indicators
    mdr = mdr_one_sample(n, p_cov)
    n_bundles = len(bundles[gene])
    # dependence: screen -> components ownership from the endpoint's paired rows
    screen_owners = defaultdict(set)
    for r in paired:
        if r["gene"] == gene and r.get("axis") == "format" and r.get("model_id") in selected_models:
            for s_ in (r.get("screen_a"), r.get("screen_b")):
                if s_:
                    screen_owners[s_].add(comp_of[r["model_id"]])
    src_screens = set(screen_owners)
    shared = any(len(cs) > 1 for cs in screen_owners.values())
    precision_pass = mdr <= 0.146 and not shared

    # policy feasibility (SPEC): requires DOCUMENTED confirmation-assay
    # availability; an existing screen does NOT establish it;
    # direction must be justifiable outcome-blind from source definitions.
    direction = {
        "proposed": "prioritize components with larger |L| (greater paired-format lability) for confirmation",
        "status": "PROPOSED HYPOTHESIS pending justification: Lock-S evidence is across genes; "
                  "transfer to prioritization across components for one gene is unestablished",
        "outcome_blind": True,
    }
    K = math.ceil(0.10 * n)
    # SPEC requires DOCUMENTED confirmation-assay availability (variable A).
    # No permitted input documents it; an existing screen is not assay
    # availability. Feasibility is therefore NOT established.
    assay_availability_documented = False
    direction_justified = False  # proposed hypothesis only (see direction.status)
    policy_pass = bool(assay_availability_documented and direction_justified and n and K >= 1)

    report.update({
        "selected_endpoint_diagnostic_candidate": gene,
        "selected_endpoint_fully_qualified": False,
        "selected_components": n,
        "distinct_source_bundles": n_bundles,
        "lineages_in_cohort": len(lineages),
        "p_covariates": p_cov,
        "mdr": (round(mdr, 4) if mdr != float("inf")
                else f"undefined: insufficient degrees of freedom (n={n}, p_cov={p_cov}, df={n - 3 - p_cov})"),
        "dependence": {"distinct_source_bundles": n_bundles,
                       "distinct_source_screens": len(src_screens),
                       "shared_screen_dependence_possible": bool(shared),
                       "treatment": "no cap heuristic; shared screens => precision not established"},
        "precision_pass": precision_pass,
        "panel_row_for_endpoint": {k: panel.get(gene, {}).get(k) for k in
                                   ("panel_member", "confirmatory_eligible",
                                    "development_primary_eligible", "atlas_status")},
        "policy": {"K_slots": K, "budget_normalized_units": K,
                   "assay_availability_documented": assay_availability_documented,
                   "direction_justified": direction_justified,
                   **direction, "feasibility_pass": policy_pass},
    })
    s12_detail = s12_audit["model_audit"]
    def chosen_screen(mid):
        ds = sorted(s12_detail.get(mid, {}).get("detail", []), key=lambda d: d["screen"])
        return ds[0]["screen"] if ds else None
    sel_mid = comp_model[next(iter(comps))] if comps else None
    sel_detail = (s12_audit["model_audit"].get(sel_mid, {}).get("detail") or [{}])
    report["variable_registration"] = {
        "L": "atlas/v4 paired_observations delta_a_minus_b, format axis (Dome - Plastic Chronos, medium held)",
        "B": "score_b (Plastic reference-condition Chronos) from the same paired row",
        "source_screens_for_endpoint": sorted({s for pr in bundles[gene] for s in pr if s}),
        "covered_component_lineage": sorted(lineages),
        "selected_screen_context": sel_detail[0] if sel_detail else None,
        "Y_direction": "Chronos gene effect: more negative = stronger dependency (atlas field dictionary: Chronos scores; Lock-S convention)",
        "unresolved_registrations": ["confirmation-assay availability (A)", "priority direction justification"],
    }
    report["cohort_record"] = {
        "covered_components": {str(c): {"model": comp_model[c],
                                        "screen": chosen_screen(comp_model[c])}
                               for c in sorted(comps, key=str)},
        "uncovered_selected_components": len(comp_model) - len(comps),
        "selection_rule": "ascending ModelID per component, then ascending eligible ScreenID (sgen012 audit detail)"}
    ok = precision_pass and policy_pass and report["identity_gate"]["component_level_LB_mapping_exists"]
    report["verdict"] = "PASS" if ok else "FAIL"
    if not ok:
        failed = []
        if not precision_pass:
            failed.append(f"precision (MDR {report['mdr']} vs 0.146 at n={n}; dependence shared={shared})")
        if not policy_pass:
            failed.append("policy feasibility (no documented confirmation-assay availability; direction unjustified)")
        report["failed_requirement"] = "; ".join(failed)
        report["resource_needed"] = ("more independent components with measured paired-format L/B "
                                     "for a single endpoint, or an endpoint with broader paired coverage")
    return _finish(report)


def _finish(report) -> int:
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({k: report.get(k) for k in
                      ("verdict", "coverage", "endpoint_qualification", "selected_endpoint",
                       "selected_components", "mdr", "precision_pass", "failed_requirement")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
