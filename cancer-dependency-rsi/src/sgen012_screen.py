#!/usr/bin/env python3
"""sgen012: framing-A provenance retest (SPEC locked, sol-xhigh generated).

Metadata only. Implements generations/sgen012/SPEC.md literally. Note on field
semantics (verified at implementation): in ModelCondition.csv the GrowthMedia
column carries MF- codes and FormulationID carries descriptive media text;
the SPEC names FormulationID as the medium identifier, so the environment
tuple uses normalized FormulationID text, with GrowthMedia codes used only
for the SPEC's unique-mapping fill and reported as audit strata. Gene.csv and
all outcome files are never read.
"""
import csv
import hashlib
import json
import math
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parent.parent
PINS = {
    "data/Model.csv": "65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7",
    "data/CRISPRScreenMap.csv": "43cc528614053d4c5a96729c2d782375227231a0cfea23de6c519b8989fa1252",
    "data/ModelCondition.csv": "a1edda78cd60718e5c99690ce8ab80315b65ddc9346643338d2c1c774fc51326",
    "data/ScreenSequenceMap.csv": "acaedf0549afda50e5f3df28645c5c2193acbdb9779f9f8099861b763d1be296",
    "generations/sgen010/established_pool_v4.json": "0c1080f8a4330e9be93b1fa0e0821fdf557a7985403b0ffa9d0129a0614bb26b",
    "generations/sgen010/screen_v7.json": "d6e6eb69a9f239ea61671397a16031a8c78be9330f049f17437ce3698832766e",
}
OUT = ROOT / "generations/sgen012/screen_v1.json"
DOCUMENTED_SCREENTYPES = {"2DS", "2DD", "2DN", "3DN", "2DND", "3DND", "2DO", "3DO"}
Z = 1.959964 + 0.841621


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(rel):
    with (ROOT / rel).open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def norm_text(s) -> str:
    s = unicodedata.normalize("NFKC", str(s or "")).casefold()
    return " ".join(s.split())


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


def flag(v):
    """Documented encodings in these files: 'True'/'False'; else unknown."""
    if v == "True":
        return True
    if v == "False":
        return False
    return None


def main() -> int:
    for rel, want in PINS.items():
        if sha(ROOT / rel) != want:
            print(f"REFUSING: pin mismatch {rel}")
            return 1
    models = rows("data/Model.csv")
    screenmap = rows("data/CRISPRScreenMap.csv")
    seqmap = rows("data/ScreenSequenceMap.csv")
    conds = rows("data/ModelCondition.csv")
    pool = json.loads((ROOT / "generations/sgen010/established_pool_v4.json").read_text())
    v7 = json.loads((ROOT / "generations/sgen010/screen_v7.json").read_text())

    by_id = {m["ModelID"]: m for m in models}
    assign = pool["assignments_screened"]
    est_ids = pool["established_model_ids"]
    est = [by_id[i] for i in est_ids]
    cell_lines = [m for m in est if m.get("ModelType") == "Cell Line"]
    denom_models = {m["ModelID"] for m in cell_lines}

    # components reconstructed deterministically from pinned assignments,
    # asserted equal to pinned v7 counts (preservation, per sgen011 v2 method)
    dsu = DSU()
    for m in est:
        node = ("DM", m.get("PatientID") or "")
        dsu.find(node)
        pat = assign[m["ModelID"]].get("patient")
        if pat:
            dsu.union(node, ("SIDP", pat))
    comp_of = {m["ModelID"]: dsu.find(("DM", m.get("PatientID") or "")) for m in est}
    n_comp_total = len({comp_of[m["ModelID"]] for m in est})
    n_comp_cl = len({comp_of[m["ModelID"]] for m in cell_lines})
    assert n_comp_total == v7["classification"]["established"]["linked_patient_components"]
    assert len(cell_lines) == 1095 and n_comp_cl == 1057, (len(cell_lines), n_comp_cl)

    # component lineage: unique pinned lineage across its established models
    comp_lineage = {}
    for m in est:
        comp_lineage.setdefault(comp_of[m["ModelID"]], set()).add(m.get("OncotreeLineage") or "")
    comp_lineage = {c: (next(iter(s)) if len(s) == 1 and "" not in s else None)
                    for c, s in comp_lineage.items()}

    cond_by_id = {c["ModelConditionID"]: c for c in conds}

    def chain(cond):
        """Return (chain_list, ok). Broken/cyclic -> ok=False."""
        out, seen, cur = [], set(), cond
        while cur is not None:
            cid = cur["ModelConditionID"]
            if cid in seen:
                return out, False
            seen.add(cid)
            out.append(cur)
            par = (cur.get("ParentModelConditionID") or "").strip()
            if not par:
                return out, True
            cur = cond_by_id.get(par)
            if cur is None:
                return out, False
        return out, True

    def chain_drug_free(chain_list):
        return all(not (c.get("PrescreenTreatmentDrug") or "").strip()
                   and not (c.get("AnchorDrug") or "").strip() for c in chain_list)

    # harmonization map: (norm CellFormat, norm GrowthMedia) -> FormulationID(norm)
    # built ONLY from explicit pairs in pinned metadata; published in report.
    gm_map = defaultdict(set)
    for c in conds:
        if c.get("GrowthMedia") and c.get("FormulationID"):
            gm_map[(norm_text(c.get("CellFormat")), norm_text(c["GrowthMedia"]))].add(
                norm_text(c["FormulationID"]))
    gm_unique = {k: next(iter(v)) for k, v in gm_map.items() if len(v) == 1}

    def environment(cond):
        cf = norm_text(cond.get("CellFormat"))
        if not cf or cf == "unknown":
            return None, "missing_cellformat"
        fid = norm_text(cond.get("FormulationID"))
        if not fid:
            fill = gm_unique.get((cf, norm_text(cond.get("GrowthMedia"))))
            if not fill:
                return None, "unresolved_formulation"
            fid = fill
        return (cf, fid), None

    screens_of = defaultdict(list)
    for r in screenmap:
        if r["ModelID"] in denom_models:
            screens_of[r["ModelID"]].append(r["ScreenID"])
    seq_by_screen = defaultdict(list)
    for r in seqmap:
        seq_by_screen[r["ScreenID"]].append(r)

    reasons = Counter()
    model_env = {}       # ModelID -> tuple (assignable)
    model_audit = {}
    for mid in sorted(denom_models):
        eligible_envs, n_unresolved, n_eligible, detail = set(), 0, 0, []
        seqs = []
        for sid in screens_of.get(mid, []):
            seqs.extend(seq_by_screen.get(sid, []))
        # duplicate SequenceID handling
        by_seq = {}
        for r in seqs:
            key = r["SequenceID"]
            sig = tuple(sorted(r.items()))
            if key in by_seq and by_seq[key][0] != sig:
                by_seq[key] = (None, r)  # conflicting duplicate
            else:
                by_seq[key] = (sig, r)
        for sig, r in by_seq.values():
            if sig is None:
                n_unresolved += 1; reasons["conflicting_duplicate_sequence"] += 1; continue
            if r.get("ModelID") != mid:
                n_unresolved += 1; reasons["model_identity_mismatch_seqmap"] += 1; continue
            st = (r.get("ScreenType") or "").strip()
            if st not in DOCUMENTED_SCREENTYPES:
                n_unresolved += 1; reasons["unknown_screentype"] += 1; continue
            qc, ex, drug, eng = (flag(r.get("PassesQC")), flag(r.get("ExcludeFromCRISPRCombined")),
                                 flag(r.get("DrugTreated")), flag(r.get("IsEngineered")))
            if qc is False or ex is True or drug is True or eng is True:
                reasons["explicitly_disqualified"] += 1; continue
            if qc is not True or ex is not False or drug is not False or eng is not False:
                n_unresolved += 1; reasons["unknown_flag_encoding"] += 1; continue
            cond = cond_by_id.get((r.get("ModelConditionID") or "").strip())
            if cond is None:
                n_unresolved += 1; reasons["SCREEN_WITHOUT_MODELCONDITIONID"] += 1; continue
            if cond.get("ModelID") != mid and cond.get("model_id") != mid:
                n_unresolved += 1; reasons["model_identity_mismatch_condition"] += 1; continue
            ch, ok = chain(cond)
            if not ok:
                n_unresolved += 1; reasons["PARENT_CONDITION_DEPENDENCE"] += 1; continue
            if not chain_drug_free(ch):
                reasons["drug_exposure_in_chain"] += 1; continue
            if not (cond.get("DataSource") or "").strip():
                n_unresolved += 1; reasons["missing_datasource"] += 1; continue
            env, why = environment(cond)
            if env is None:
                n_unresolved += 1; reasons[why] += 1; continue
            eligible_envs.add(env); n_eligible += 1
            detail.append({"seq": r["SequenceID"], "cond": cond["ModelConditionID"],
                           "env": list(env), "screentype": st,
                           "datasource": cond.get("DataSource")})
        if n_eligible and not n_unresolved and len(eligible_envs) == 1:
            model_env[mid] = next(iter(eligible_envs))
        model_audit[mid] = {"eligible": n_eligible, "unresolved": n_unresolved,
                            "envs": sorted(list(e) for e in eligible_envs), "detail": detail}

    # components in multiple environments excluded from all arms
    comp_envs = defaultdict(set)
    for mid, env in model_env.items():
        comp_envs[comp_of[mid]].add(env)
    multi_comps = {c for c, s in comp_envs.items() if len(s) > 1}
    retained = {mid: env for mid, env in model_env.items()
                if comp_of[mid] not in multi_comps}
    retained_comps = {}
    for mid, env in retained.items():
        retained_comps.setdefault(comp_of[mid], env)
    assert all(retained_comps[comp_of[m]] == e for m, e in retained.items())

    est_models_n = len(retained)
    est_comps_n = len(retained_comps)
    cov_models = est_models_n >= 986
    cov_comps = est_comps_n >= 952

    strata = Counter(retained_comps.values())
    ranked = sorted(strata.items(), key=lambda kv: (-kv[1], kv[0][0].encode(), kv[0][1].encode()))
    gates = {"coverage_models_ge986": cov_models, "coverage_components_ge952": cov_comps}
    selected = None
    if len(ranked) >= 2:
        (envA, nA), (envB, nB) = ranked[0], ranked[1]
        gates["contrast_exists"] = True
        gates["arm_size_ge100_each"] = nA >= 100 and nB >= 100
        both = Counter()
        linA = Counter(comp_lineage[c] for c, e in retained_comps.items() if e == envA and comp_lineage[c])
        linB = Counter(comp_lineage[c] for c, e in retained_comps.items() if e == envB and comp_lineage[c])
        pos = [l for l in set(linA) & set(linB) if linA[l] >= 20 and linB[l] >= 20]
        gates["positivity_ge3_lineages_k20"] = len(pos) >= 3
        if nA > 3 and nB > 3:
            B = Z * math.sqrt(1 / (nA - 3) + 1 / (nB - 3))
            mdr = math.tanh(B)
        else:
            mdr = float("inf")
        gates["precision_mdr_le_0.146"] = mdr <= 0.146
        selected = {"armA": {"env": list(envA), "components": nA},
                    "armB": {"env": list(envB), "components": nB},
                    "mdr_two_arm": round(mdr, 4) if mdr != float("inf") else None,
                    "positivity_lineages": sorted(pos),
                    "lineage_counts_A": dict(linA.most_common()),
                    "lineage_counts_B": dict(linB.most_common())}
    else:
        gates["contrast_exists"] = False

    def cramers_v(pairs):
        rows_ = sorted({a for a, _ in pairs}); cols = sorted({b for _, b in pairs})
        if len(rows_) < 2 or len(cols) < 2 or not pairs:
            return None
        n = len(pairs)
        obs = Counter(pairs)
        rt = Counter(a for a, _ in pairs); ct = Counter(b for _, b in pairs)
        chi = sum((obs.get((a, b), 0) - rt[a] * ct[b] / n) ** 2 / (rt[a] * ct[b] / n)
                  for a in rows_ for b in cols)
        return round(math.sqrt(chi / (n * min(len(rows_) - 1, len(cols) - 1))), 4)

    conf_pairs = [(str(e), comp_lineage[c]) for c, e in retained_comps.items() if comp_lineage[c]]
    arm_dist = {}
    if selected:
        for label, env in (("A", tuple(selected["armA"]["env"])), ("B", tuple(selected["armB"]["env"]))):
            sts, dss = Counter(), Counter()
            for mid, e in retained.items():
                if e == env:
                    for d in model_audit[mid]["detail"]:
                        if tuple(d["env"]) == env:
                            sts[d["screentype"]] += 1; dss[d["datasource"]] += 1
            arm_dist[label] = {"ScreenType_sequences": dict(sts), "DataSource_sequences": dict(dss)}

    evaluable = True  # README basis recorded below; locks/semantics auditable
    all_gates = evaluable and all(gates.get(k) for k in
                                  ("coverage_models_ge986", "coverage_components_ge952",
                                   "contrast_exists", "arm_size_ge100_each",
                                   "positivity_ge3_lineages_k20", "precision_mdr_le_0.146"))
    verdict = "A_PROVENANCE_ESTABLISHED" if all_gates else "A_REJECTED"

    report = {
        "generation": "sgen012", "version": 1,
        "inputs": {k: {"sha256": v} for k, v in PINS.items()},
        "provenance_audit_basis": ("DepMap26Q3_README: ModelCondition = 'condition(s) under which the model "
                                   "was assayed'; ScreenSequenceMap = Achilles (CRISPR) pipeline Pre-Chronos map "
                                   "linking SequenceID->ScreenID+ModelConditionID. Taken as screening-time "
                                   "basis, explicitly disputable at review."),
        "field_semantics_note": ("In ModelCondition.csv, GrowthMedia carries MF- codes and FormulationID "
                                 "carries descriptive media text (name-swapped vs SPEC assumption); SPEC "
                                 "implemented literally on FormulationID text."),
        "gene_csv_excluded": "Gene.csv never read (outcome-derived essentiality/selectivity columns).",
        "denominator": {"cell_line_models": 1095, "components": 1057,
                        "components_reconstruction_asserted_vs_v7": True},
        "establishable": {"models": est_models_n, "components": est_comps_n,
                          "models_before_multienv_component_exclusion": len(model_env),
                          "multi_environment_components_excluded": len(multi_comps)},
        "exclusion_reasons_sequences": dict(reasons.most_common()),
        "harmonization_map_unique_entries": len(gm_unique),
        "ranked_strata_top10": [{"env": list(e), "components": n} for e, n in ranked[:10]],
        "selected_contrast": selected,
        "gates": gates,
        "confounding": {"cramersV_env_x_lineage_all": cramers_v(conf_pairs),
                        "arm_distributions": arm_dist},
        "verdict": verdict,
        "authorization": ("Pass authorizes only preparation+locking of a separate outcome design; "
                          "no outcome access (SPEC)."),
    }
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({"verdict": verdict, "establishable": report["establishable"],
                      "gates": gates, "selected": selected,
                      "top_strata": report["ranked_strata_top10"][:4],
                      "cramersV": report["confounding"]["cramersV_env_x_lineage_all"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
