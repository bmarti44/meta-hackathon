#!/usr/bin/env python3
"""sgen017 census v3 (versioned regeneration of reviewed v2 corrections).

Strict explicit-false eligibility; pDNA excluded; CellFormat=unknown
unqualified; content key headline; independence unverified.
"""
import csv
import json
import datetime
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    seq = list(csv.DictReader(open(ROOT / "data/ScreenSequenceMap.csv")))
    mc = {r["ModelConditionID"]: r for r in csv.DictReader(open(ROOT / "data/ModelCondition.csv"))}
    ex = lambda v, tf: str(v).strip().lower() == tf
    base = [r for r in seq if r["ModelID"] != "pDNA" and r["ScreenType"] != "pDNA"]
    strict = [r for r in base if ex(r["PassesQC"], "true") and ex(r["DrugTreated"], "false")
              and ex(r["IsEngineered"], "false") and ex(r["ExcludeFromCRISPRCombined"], "false")]
    missing = sum(1 for r in base if ex(r["PassesQC"], "true")
                  and (r["DrugTreated"].strip() == "" or r["IsEngineered"].strip() == ""))

    def census(rows, keyfn):
        g, unq_screens, unq_seq = defaultdict(set), set(), 0
        for r in rows:
            k = keyfn(r)
            if k is None:
                unq_seq += 1
                unq_screens.add(r["ScreenID"])
                continue
            g[k].add(r["ScreenID"])
        rep = {k: v for k, v in g.items() if len(v) >= 2}
        return {"groups": len(g), "repeat_groups": len(rep),
                "coverage": len(rep) / len(g) if g else None,
                "unqualified_sequences": unq_seq, "unqualified_screens": len(unq_screens),
                "repeat_keys": [list(k) for k in rep]}

    def rob(r):
        m = mc.get(r["ModelConditionID"])
        if not m:
            return None
        f = (m.get("CellFormat") or "").strip().lower()
        fo = (m.get("FormulationID") or "").strip()
        if f in ("", "unknown") or not fo:
            return None
        return (r["ModelID"], m["CellFormat"], m["FormulationID"], r["Library"], r["Days"])

    rob_c = census(strict, rob)
    screens = {r["ScreenID"] for r in strict}
    out = {
        "version": 3, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sequences_base_no_pDNA": len(base), "sequences_strict": len(strict),
        "missing_flag_sequences_excluded": missing,
        "primary_strict": census(strict, lambda r: (r["ModelID"], r["ModelConditionID"], r["Library"])),
        "robustness_strict": rob_c,
        "headline": (f"One candidate repeat among {rob_c['groups']} qualified condition-library-day "
                     f"groups ({100*rob_c['coverage']:.4f}%); "
                     f"{100*rob_c['unqualified_sequences']/len(strict):.2f}% of strict-eligible sequences "
                     f"and {100*rob_c['unqualified_screens']/len(screens):.2f}% of screens unassessable "
                     "under the content key; execution independence unverified."),
        "candidate": ("ACH-000614 (SC-000614.AV01 vs SC-002875.AV01): identical ModelCondition content "
                      "except ID; Avana d21; pDNABatch Avana-3/4; passage name hints p5/p6, structured "
                      "PassageNumber blank; patient SIDP01038; independence unverified"),
        "verdict": "CENSUS_COMPLETE",
        "repeat_resource": "NEAR_ABSENT_UNVERIFIED (descriptive label for observed strict-eligible qualified groups only; unassessable screens excluded from the scope of this label)",
        "independence": "Distinct annotated ScreenIDs; independent initiation NOT established by metadata.",
        "nonclaims": "No instability/persistence measurement; rerun reasons unknown; outcome estimand needs new locked design.",
    }
    (ROOT / "generations/sgen017/census_v3.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("headline", "robustness_strict")}, indent=1)[:900])


if __name__ == "__main__":
    main()
