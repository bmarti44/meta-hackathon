#!/usr/bin/env python3
"""sgen014 novelty completion: exhaustive screen beyond relevance top-25.

Protocol frozen in generations/sgen014/NOVELTY_PROTOCOL.md BEFORE this run.
Fetches the identical concept_broad Europe PMC query (cursor pagination),
dedupes, removes the 25 previously screened, applies the frozen stage-1
keyword prefilter, and emits stage-2 survivors for lead screening.
Receipts recorded for every request. $0, official API only.
"""
import hashlib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "generations/sgen014/novelty_screen_results.json"
API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
STAGE1_A = re.compile(r"dome|plastic|matrigel|3d|three-dimensional|spheroid|organoid|"
                      r"culture (medium|media|format)|serum.free|growth format|format.*labil|labil", re.I)
STAGE1_B = re.compile(r"crispr|dependency|dependencies|essentialit|knockout screen", re.I)

receipts = []


def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    t0 = time.monotonic()
    req = urllib.request.Request(url, headers={"User-Agent": "cd-rsi-sgen014/1.0",
                                                "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        body = r.read()
        receipts.append({"url": url, "status": r.status, "bytes": len(body),
                         "sha256": hashlib.sha256(body).hexdigest(),
                         "wall_s": round(time.monotonic() - t0, 3)})
    return json.loads(body)


def main() -> int:
    prior = json.loads((ROOT / "reviews/novelty_v5_searches.json").read_text())
    q = prior["concept_broad"]["query"]
    screened_ids = {str(t.get("id")) for t in prior["concept_broad"].get("top") or []}

    records, cursor = {}, "*"
    first_hitcount = None
    while True:
        page = get({"query": q, "format": "json", "pageSize": 1000,
                    "cursorMark": cursor, "resultType": "core"})
        if first_hitcount is None:
            first_hitcount = page.get("hitCount")
        for r in page.get("resultList", {}).get("result", []):
            records[str(r.get("id"))] = r
        nxt = page.get("nextCursorMark")
        if not nxt or nxt == cursor or not page.get("resultList", {}).get("result"):
            break
        cursor = nxt

    novel = {i: r for i, r in records.items() if i not in screened_ids}
    survivors, excluded = [], 0
    for i, r in novel.items():
        text = ((r.get("title") or "") + "\n" + (r.get("abstractText") or ""))
        if STAGE1_A.search(text) and STAGE1_B.search(text):
            survivors.append({"id": i, "pmid": r.get("pmid"), "pmcid": r.get("pmcid"),
                              "title": r.get("title"), "year": r.get("pubYear"),
                              "abstract": (r.get("abstractText") or "")[:2000]})
        else:
            excluded += 1

    out = {
        "query": q,
        "hitcount_now": first_hitcount,
        "hitcount_prior": prior["concept_broad"].get("hitCount"),
        "fetched_unique": len(records),
        "previously_screened_top": len(screened_ids),
        "novel_records": len(novel),
        "stage1_excluded": excluded,
        "stage1_survivors": len(survivors),
        "survivors": survivors,
        "requests": receipts,
    }
    with OUT.open("x") as f:
        json.dump(out, f, indent=2)
        f.write("\n")
    print(json.dumps({k: out[k] for k in ("hitcount_now", "hitcount_prior", "fetched_unique",
                                          "novel_records", "stage1_excluded", "stage1_survivors")}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
