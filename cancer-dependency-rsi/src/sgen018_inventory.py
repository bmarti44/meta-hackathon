#!/usr/bin/env python3
"""sgen018 condition-history return-pair inventory (metadata only)."""
import csv
import json
import datetime
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    mcs = {r["ModelConditionID"]: r for r in csv.DictReader(open(ROOT / "data/ModelCondition.csv"))}
    seq = list(csv.DictReader(open(ROOT / "data/ScreenSequenceMap.csv")))
    ex = lambda v, tf: str(v).strip().lower() == tf
    screened_libs = defaultdict(set)  # ModelConditionID -> libraries
    for r in seq:
        if r["ModelID"] == "pDNA" or r["ScreenType"] == "pDNA":
            continue
        if (ex(r["PassesQC"], "true") and ex(r["DrugTreated"], "false")
                and ex(r["IsEngineered"], "false") and ex(r["ExcludeFromCRISPRCombined"], "false")
                and r["Library"].strip()):
            screened_libs[r["ModelConditionID"]].add(r["Library"])

    def key(mid):
        m = mcs.get(mid)
        if not m:
            return None
        f = (m.get("CellFormat") or "").strip().lower()
        fo = (m.get("FormulationID") or "").strip()
        if f in ("", "unknown") or not fo:
            return None
        return (m["CellFormat"], m["FormulationID"])

    def chain(mid):
        """Root->node list of ModelConditionIDs within same ModelID; [] if cycle/broken."""
        path, seen = [], set()
        cur = mid
        while cur and cur in mcs and cur not in seen:
            seen.add(cur)
            path.append(cur)
            cur = (mcs[cur].get("ParentModelConditionID") or "").strip()
            if cur and cur in mcs and mcs[cur]["ModelID"] != mcs[mid]["ModelID"]:
                break
        if cur in seen:
            return []
        return list(reversed(path))

    depths = Counter()
    patterns = Counter()
    qualified = {}  # ModelID -> detail
    by_model = defaultdict(list)
    for mid in mcs:
        by_model[mcs[mid]["ModelID"]].append(mid)
    for model, nodes in by_model.items():
        ret, main = {}, {}  # (ancestor, library) -> terminals
        for node in nodes:
            ch = chain(node)
            depths[len(ch)] += 1
            keys = [key(n) for n in ch]
            if len(ch) < 3 or keys[-1] is None:
                continue
            # last three qualified nodes ending at this terminal
            last3 = keys[-3:]
            if any(k is None for k in last3):
                continue
            x, y, z = last3
            if z != x:
                continue
            pat = "maintained" if y == x else "return"
            patterns[pat] += 1
            libs = screened_libs.get(node, set())
            if not libs:
                continue
            patterns[pat + "_screened"] += 1
            for lib in libs:
                (main if pat == "maintained" else ret).setdefault((ch[-3], lib), []).append(node)
        for k_ in set(ret) & set(main):
            qualified[model] = {"ancestor": k_[0], "library": k_[1],
                                "return_terminals": ret[k_], "maintained_terminals": main[k_]}
    n = len(qualified)
    out = {"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
           "model_conditions": len(mcs), "models": len(by_model),
           "chain_depth_distribution": dict(sorted(depths.items())),
           "patterns": dict(patterns),
           "qualified_models": n,
           "qualified_detail_capped": dict(list(qualified.items())[:10]),
           "verdict": "INVENTORY_COMPLETE",
           "history_resource": "ABSENT" if n == 0 else ("SPARSE" if n < 10 else "MATERIAL"),
           "nonclaims": "Feasibility only; no dates/elapsed-time fields; branch randomization unknown; hysteresis is an established concept."}
    (ROOT / "generations/sgen018/inventory_v1.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("chain_depth_distribution", "patterns",
                                           "qualified_models", "history_resource")}, indent=1))


if __name__ == "__main__":
    main()
