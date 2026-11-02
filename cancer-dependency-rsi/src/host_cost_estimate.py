#!/usr/bin/env python3
"""User-authorized host-cost estimation from recorded call history (2026-10-29).

Every model_call receipt records exact token usage. This script re-prices all
receipted calls at published GPT-6.1 Sol API list rates and reconciles the
count against ledger/resources.jsonl reservations. Calls whose receipt is
missing fall back to their .events.jsonl usage records; calls with neither
are listed as UNPRICED (never silently zero).

Price basis (third-party summary of OpenAI list prices, Oct 2026,
developer.puter.com/tutorials/openai-api-pricing/, fetched 2026-10-29):
  GPT-6.1 Sol short context: input $2.00/M, cached input $0.10/M, output $10.00/M
  Long context (request input > 272K tokens): 2x input incl. cached, 1.5x output
    -> $4.00 / $0.20 / $15.00 per M
  Cache writes: $2.50/M
This is an ESTIMATE at list prices. Actual metered spend was $0 (subscription
auth; additional_api_spend_cap_usd = 0). It is an accounting proxy authorized
by the user, not a metered billing witness.
"""
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "ledger/host_cost_estimate_v8_final.json"
CSV_OUT = ROOT / "ledger/host_cost_estimate_v8_final_calls.csv"

SHORT = {"in": 2.00, "cached": 0.10, "out": 10.00}
LONG = {"in": 4.00, "cached": 0.20, "out": 15.00}
CACHE_WRITE = 2.50
LONG_THRESHOLD = 272_000


def price_entry(t) -> float:
    inp = t.get("input_tokens", 0)
    cached = t.get("cached_input_tokens", 0)
    write = t.get("cache_write_input_tokens", 0)
    out = t.get("output_tokens", 0)
    r = LONG if inp > LONG_THRESHOLD else SHORT
    return ((inp - cached) * r["in"] + cached * r["cached"]
            + out * r["out"] + write * CACHE_WRITE) / 1e6


def main() -> int:
    reservations = {}
    for line in (ROOT / "ledger/resources.jsonl").read_text().splitlines():
        d = json.loads(line)
        if d.get("kind") == "reserve" and d["job"].get("model_calls", 0) > 0:
            reservations[d["record_id"]] = d["job"]

    calls = []
    priced_ids = set()
    for rp in sorted(ROOT.rglob("*.receipt.json")):
        if ".venv" in rp.parts:
            continue
        r = json.loads(rp.read_text())
        rid = r.get("reservation_id")
        toks = r.get("tokens") or []
        if not toks:
            continue  # no usage in receipt: events fallback or UNPRICED, never $0
        cost = sum(price_entry(t) for t in toks)
        job = reservations.get(rid, {})
        calls.append({
            "reservation_id": rid, "name": job.get("name") or rp.stem,
            "phase": job.get("phase") or r.get("call_identity", {}).get("phase"),
            "effort": r.get("effort"), "source": "receipt",
            "input_tokens": sum(t.get("input_tokens", 0) for t in toks),
            "cached_input_tokens": sum(t.get("cached_input_tokens", 0) for t in toks),
            "output_tokens": sum(t.get("output_tokens", 0) for t in toks),
            "est_cost_usd": cost,
            "artifact": str(rp.relative_to(ROOT)),
        })
        if rid:
            priced_ids.add(rid)

    # fallback: events files for reservations without receipts
    for ep in sorted(ROOT.rglob("*.events.jsonl")):
        if ".venv" in ep.parts:
            continue
        usages = []
        for line in ep.read_text().splitlines():
            try:
                e = json.loads(line)
            except json.JSONDecodeError:
                continue
            if e.get("type") == "turn.completed" and isinstance(e.get("usage"), dict):
                usages.append(e["usage"])  # each completed turn extracted once
        if not usages:
            continue
        name = ep.name.replace(".events.jsonl", "")
        if any(c["name"] == name for c in calls):
            continue
        # Reconstruction: SUM per-turn usage records. Empirical basis: every
        # events file in this campaign holds exactly one turn.completed equal
        # to its receipt total, so sum == last on all observed data. For
        # hypothetical multi-turn files, summation is the conservative
        # (upper) convention; monotonicity is NOT used to infer cumulative
        # semantics (re-review v2 finding).
        fields = ("input_tokens", "cached_input_tokens", "output_tokens",
                  "cache_write_input_tokens")
        last = {f: sum(u.get(f, 0) for u in usages) for f in fields}
        turns_cost = sum(price_entry(u) for u in usages)  # per-turn rate boundaries
        by_name = {j.get("name"): (rid, j) for rid, j in reservations.items()}
        _rid, _job = by_name.get(name, (None, {}))
        calls.append({
            "reservation_id": _rid, "name": name,
            "phase": _job.get("phase"), "effort": _job.get("effort"),
            "source": "events_per_turn_sum",
            "input_tokens": last.get("input_tokens", 0),
            "cached_input_tokens": last.get("cached_input_tokens", 0),
            "output_tokens": last.get("output_tokens", 0),
            "est_cost_usd": turns_cost,
            "artifact": str(ep.relative_to(ROOT)),
        })

    unpriced = [rid for rid in reservations if rid not in priced_ids
                and not any(c["name"] == reservations[rid].get("name") for c in calls)]

    # xhigh condition: impute unpriced calls at largest audited receipt cost
    # for same phase+effort; campaign maximum otherwise. Frozen at v4.
    receipt_costs = [c for c in calls if c["source"] == "receipt"]
    def impute_for(job):
        same = [c["est_cost_usd"] for c in receipt_costs
                if c["phase"] == job.get("phase") and c["effort"] == job.get("effort")]
        if same:
            return max(same), "max_receipt_phase_effort"
        return max(c["est_cost_usd"] for c in receipt_costs), "campaign_max_receipt"
    imputations = []
    for rid in list(unpriced):
        job = reservations[rid]
        val, rule = impute_for(job)
        imputations.append({"reservation_id": rid, "name": job.get("name"),
                            "phase": job.get("phase"), "effort": job.get("effort"),
                            "imputed_est_cost_usd": val, "rule": rule})
        calls.append({"reservation_id": rid, "name": job.get("name"),
                      "phase": job.get("phase"), "effort": job.get("effort"),
                      "source": "imputed_" + rule, "input_tokens": None,
                      "cached_input_tokens": None, "output_tokens": None,
                      "est_cost_usd": val, "artifact": "ledger/resources.jsonl"})

    by_phase = defaultdict(lambda: {"calls": 0, "est_cost_usd": 0.0})
    for c in calls:
        b = by_phase[c["phase"] or "unknown_phase"]
        b["calls"] += 1
        b["est_cost_usd"] += c["est_cost_usd"]

    report = {
        "method": "receipt token counts x GPT-6.1 Sol list prices (see module docstring)",
        "price_source": "developer.puter.com/tutorials/openai-api-pricing/ (Oct 2026, fetched 2026-10-29)",
        "authorization": "user instruction 2026-10-29: estimate the cost from the chat history",
        "actual_metered_spend_usd": 0.0,
        "reservations_total_model_calls": sum(j.get("model_calls", 0) for j in reservations.values()),
        "receipt_priced_calls": sum(1 for c in calls if c["source"] == "receipt"),
        "events_priced_calls": sum(1 for c in calls if c["source"] == "events_per_turn_sum"),
        "imputed_calls": sum(1 for c in calls if str(c["source"]).startswith("imputed_")),
        "accounted_calls": len(calls),
        "receipt_priced_subtotal_usd": round(sum(c["est_cost_usd"] for c in calls if c["source"] == "receipt"), 2),
        "events_priced_subtotal_usd": round(sum(c["est_cost_usd"] for c in calls if c["source"] == "events_per_turn_sum"), 2),
        "unpriced_reservation_ids": unpriced,
        "imputations": imputations,
        "total_with_imputations_usd": round(sum(c["est_cost_usd"] for c in calls), 2),
        "sensitivity_note": "savings claims must survive 2x and 4x each imputation (xhigh condition)",
        "total_est_cost_usd": round(sum(c["est_cost_usd"] for c in calls), 2),
        "by_phase": {k: {"calls": v["calls"], "est_cost_usd": round(v["est_cost_usd"], 2)}
                     for k, v in sorted(by_phase.items())},
        "caveats": [
            "List-price estimate, not metered billing; subscription actual spend $0.",
            "Long-context schedule applied per usage entry with input_tokens > 272000.",
            "Events-fallback rows sum per-turn prices (rate boundaries preserved); token counts aggregated separately.",
            "Reasoning output tokens are included in output_tokens and priced once.",
        ],
    }
    with OUT.open("x") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    with CSV_OUT.open("x", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(calls[0].keys()))
        w.writeheader()
        w.writerows(sorted(calls, key=lambda c: c["name"]))
    print(json.dumps({"total_est_cost_usd": report["total_est_cost_usd"],
                      "accounted_calls": report["accounted_calls"], "receipt_priced": report["receipt_priced_calls"], "imputed": report["imputed_calls"],
                      "reservations": report["reservations_total_model_calls"],
                      "unpriced": len(unpriced),
                      "by_phase": report["by_phase"]}, indent=2))
    print("script_sha256:", hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main())
