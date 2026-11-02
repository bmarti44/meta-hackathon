#!/usr/bin/env python3
"""sgen015: Sanger CMP paired-format resource discriminator (metadata only).

Local Passports model list (pinned) + Passports API model-availability
metadata (crispr_ko_available) with per-request receipts. No outcome
matrices are fetched or opened. CMP bucket listing is AccessDenied; the
API is the metadata route (SPEC-permitted).
"""
import csv
import hashlib
import json
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PP_PATH = ROOT / "data/passports_model_list_20260921.csv"
PP_SHA = "419f65d1d6534454194f1a744550fab632cd1d7411f6b13411a885735aa37006"
MAP_SHA = "4ddd01592c2d8221eff73d4eded6a051bcac676e1c13fcbd5bc4db91a3ae1f61"
OUT = ROOT / "generations/sgen015/screen_v3.json"
API = "https://api.cellmodelpassports.sanger.ac.uk/models/{}"

receipts = []


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rows(p: Path):
    with p.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def api_model(mid):
    """One receipt per HTTP request, updated with parse outcome + value."""
    url = API.format(mid)
    t0 = time.monotonic()
    rec = {"url": url, "model_id": mid}
    receipts.append(rec)
    req = urllib.request.Request(url, headers={"Accept": "application/json",
                                                "User-Agent": "cd-rsi-sgen015/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
        rec.update({"status": r.status, "bytes": len(body),
                    "sha256": hashlib.sha256(body).hexdigest(),
                    "wall_s": round(time.monotonic() - t0, 3)})
    attr = json.loads(body)["data"]["attributes"]
    raw = attr.get("crispr_ko_available", "<missing>")
    # strict Boolean only; missing/null/string/other => unknown (never assumed)
    val = raw if isinstance(raw, bool) else None
    rec.update({"crispr_ko_available_raw": raw if isinstance(raw, (bool, type(None))) else str(raw),
                "crispr_ko_available_strict": val, "parse": "ok"})
    return val


def kind(r):
    t = (r.get("model_type") or "").lower()
    if "organoid" in t:
        return "organoid"
    if "cell line" in t:
        return "cell_line"
    return "other"


def main() -> int:
    if sha(PP_PATH) != PP_SHA:
        print("REFUSING: passports list hash mismatch")
        return 1
    cmap_raw = json.loads((ROOT / "generations/sgen010/cohort_C_patient_map_v1.json").read_text())
    cmap = cmap_raw["sample_ID_to_SIDP"]
    canon = json.dumps(dict(sorted(cmap.items())), sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(canon).hexdigest() != MAP_SHA:
        print("REFUSING: C patient map canonical hash mismatch")
        return 1
    c_patients = set(cmap.values())

    pp = rows(PP_PATH)
    by_id = {r["model_id"]: r for r in pp}
    bypat = defaultdict(list)
    for r in pp:
        if r.get("patient_id"):
            bypat[r["patient_id"]].append(r)

    paired_patients = {p: ms for p, ms in bypat.items()
                       if {kind(m) for m in ms} >= {"organoid", "cell_line"}}
    cross_deriv = [r["model_id"] for r in pp
                   if r.get("parent_id") in by_id
                   and kind(by_id[r["parent_id"]]) != kind(r)
                   and {kind(by_id[r["parent_id"]]), kind(r)} == {"organoid", "cell_line"}]

    organoids = [r for r in pp if kind(r) == "organoid"]
    avail = {}
    for r in organoids:
        try:
            avail[r["model_id"]] = api_model(r["model_id"])
        except Exception as e:  # recorded on the same receipt, never assumed
            avail[r["model_id"]] = None
            receipts[-1].update({"parse": "failed", "error": str(e)})
    screened_org = [r for r in organoids if avail.get(r["model_id"])]
    fresh_patients = {r["patient_id"] for r in screened_org
                      if r.get("patient_id") and r["patient_id"] not in c_patients}
    c_patients_screened = {r["patient_id"] for r in screened_org
                           if r.get("patient_id") in c_patients}

    # SPEC verdict population: C-disjoint patients whose pairs are screened
    # on BOTH sides (cell-line availability queried for paired patients only)
    qualified_pairs = 0
    for p, ms in paired_patients.items():
        if p in c_patients:
            continue
        sides_ok = {"organoid": False, "cell_line": False}
        for m in ms:
            k = kind(m)
            if k == "organoid" and avail.get(m["model_id"]):
                sides_ok["organoid"] = True
            elif k == "cell_line":
                try:
                    if api_model(m["model_id"]):
                        sides_ok["cell_line"] = True
                except Exception as e:
                    receipts[-1].update({"parse": "failed", "error": str(e)})
        if all(sides_ok.values()):
            qualified_pairs += 1
    n_pairs = qualified_pairs
    verdict = ("RESOURCE_PRESENT" if n_pairs >= 367 else
               "RESOURCE_PARTIAL" if n_pairs >= 100 else "RESOURCE_ABSENT")
    # identity quality: derivation basis + ambiguity accounting (SPEC item 5)
    def chain_kinds(m):
        out, seen, cur = [], set(), m
        while cur is not None and cur["model_id"] not in seen:
            seen.add(cur["model_id"]); out.append(kind(cur))
            par = (cur.get("parent_id") or "").strip()
            cur = by_id.get(par) if par else None
        return out
    chain_cross = sum(1 for r in pp
                      if {"organoid", "cell_line"} <= set(chain_kinds(r)))
    ambiguous_kind = sum(1 for r in pp if kind(r) == "other")
    report = {
        "generation": "sgen015", "version": 3,
        "inputs": {"passports_model_list_20260921.csv": {"sha256": PP_SHA},
                   "cohort_C_patient_map_canonical_sha256": MAP_SHA,
                   "api": "api.cellmodelpassports.sanger.ac.uk/models/{id} (metadata only)"},
        "pairing": {
            "models_total": len(pp),
            "patients_with_organoid_and_cell_line": len(paired_patients),
            "cross_type_derivation_links": len(cross_deriv),
            "paired_patients_disjoint_from_C": sum(1 for p in paired_patients if p not in c_patients),
            "qualified_two_sided_screened_disjoint_pairs": qualified_pairs,
        },
        "organoid_screen_availability": {
            "organoid_models": len(organoids),
            "crispr_ko_available_true": sum(1 for v in avail.values() if v),
            "crispr_ko_available_false": sum(1 for v in avail.values() if v is False),
            "availability_unknown_errors": sum(1 for v in avail.values() if v is None),
            "screened_patients_in_C": len(c_patients_screened),
            "screened_patients_outside_C": len(fresh_patients),
        },
        "identity_quality": {
            "pairing_basis_same_patient": len(paired_patients),
            "models_with_cross_type_ancestor_chain": chain_cross,
            "ambiguous_model_kind": ambiguous_kind,
            "note": "pairing requires same patient_id with both kinds; derivation chains audited separately"},
        "verdict": verdict,
        "gate_rule": "SPEC: >=367 two-sided screened derivation-matched patients PRESENT; 100-366 PARTIAL; <100 ABSENT",
        "secondary_observation": ("Fresh screened organoid patients outside C are counted above; "
                                  "they do not supply paired-format L/B (no matched 2D side) and "
                                  "are recorded for xhigh target generation only."),
        "organoid_availability_by_model": {k: avail[k] for k in sorted(avail)},
        "screened_nonC_organoid_patients": sorted(fresh_patients),
        "requests": receipts,
    }
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(json.dumps({k: report[k] for k in ("pairing", "organoid_screen_availability", "verdict")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
