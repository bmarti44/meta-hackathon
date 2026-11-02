#!/usr/bin/env python3
"""sgen017 repeat-observability census (metadata only)."""
import csv
import json
import datetime
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def truthy(v):
    return str(v).strip().lower() in ("true", "1", "yes")


def main():
    seq = list(csv.DictReader(open(ROOT / "data/ScreenSequenceMap.csv")))
    mc = {r["ModelConditionID"]: r for r in csv.DictReader(open(ROOT / "data/ModelCondition.csv"))}
    elig = [r for r in seq if truthy(r["PassesQC"]) and not truthy(r["DrugTreated"])
            and not truthy(r["IsEngineered"]) and not truthy(r["ExcludeFromCRISPRCombined"])]
    rep = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "sequences_total": len(seq), "sequences_eligible": len(elig),
           "screentype_distribution": dict(Counter(r["ScreenType"] for r in elig))}

    def census(keyfn, label):
        groups = defaultdict(set)
        unqualified = 0
        for r in elig:
            k = keyfn(r)
            if k is None:
                unqualified += 1
                continue
            groups[k].add(r["ScreenID"])
        sizes = Counter(len(v) for v in groups.values())
        repeat = {k: v for k, v in groups.items() if len(v) >= 2}
        out = {"groups": len(groups), "repeat_groups": len(repeat),
               "coverage": (len(repeat) / len(groups)) if groups else None,
               "screens_per_group": dict(sorted(sizes.items())),
               "unqualified_sequences": unqualified,
               "screens_in_repeat_groups": sum(len(v) for v in repeat.values())}
        rep[label] = out
        return repeat

    rep_primary = census(lambda r: (r["ModelID"], r["ModelConditionID"], r["Library"]), "primary")

    def rob_key(r):
        m = mc.get(r["ModelConditionID"])
        if not m or not m.get("CellFormat") or not m.get("FormulationID"):
            return None
        return (r["ModelID"], m["CellFormat"], m["FormulationID"], r["Library"], r["Days"])
    census(rob_key, "robustness")

    # breakdowns on primary repeat groups
    fmt_counter, lib_counter, organoid_groups = Counter(), Counter(), 0
    models_repeat = set()
    for (model, mcid, lib) in rep_primary:
        models_repeat.add(model)
        lib_counter[lib] += 1
        fmt = mc.get(mcid, {}).get("CellFormat", "UNKNOWN")
        fmt_counter[fmt] += 1
        if "organoid" in fmt.lower() or "3d" in fmt.lower():
            organoid_groups += 1
    rep["repeat_breakdown"] = {"by_cellformat": dict(fmt_counter),
                               "by_library": dict(lib_counter),
                               "organoid_format_groups": organoid_groups,
                               "models_in_repeat_groups": len(models_repeat)}
    # patient clustering (ID columns only)
    pp = {}
    for r in csv.DictReader(open(ROOT / "data/passports_model_list_20260921.csv")):
        if r.get("BROAD_ID"):
            pp[r["BROAD_ID"]] = r.get("patient_id", "")
    mapped = {m: pp[m] for m in models_repeat if m in pp and pp[m]}
    rep["patient_clustering"] = {"models_mapped": len(mapped),
                                 "models_unmapped": len(models_repeat) - len(mapped),
                                 "distinct_patients": len(set(mapped.values()))}
    n = rep["primary"]["repeat_groups"]
    rep["verdict"] = "CENSUS_COMPLETE"
    rep["repeat_resource"] = "ABSENT" if n == 0 else ("SPARSE" if n < 50 else "MATERIAL")
    out = ROOT / "generations/sgen017/census_v1.json"
    out.write_text(json.dumps(rep, indent=1))
    print(json.dumps({k: rep[k] for k in ("sequences_eligible", "primary", "robustness",
                                           "repeat_breakdown", "patient_clustering",
                                           "repeat_resource")}, indent=1)[:1600])


if __name__ == "__main__":
    main()
