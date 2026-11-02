`RESOURCE_ABSENT` is supported by the pinned metadata. I found **3 medium and 1 low issue; no high or critical issues**. The defects do not change this snapshot’s verdict.

Read-only review completed without API calls or filesystem writes.

1. **Medium — Verdict uses the wrong population.** [Lines 100–102](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen015_screen.py:100) apply the correct 367/100 thresholds to all patients with both model types. SPEC requires C-disjoint patients with qualified, two-sided screened pairs. Cell-line availability is never queried, and neither screening nor C exclusion feeds the verdict. In-memory execution confirmed that 367 unscreened candidates yield `RESOURCE_PRESENT`, while 100 candidates entirely in C yield `RESOURCE_PARTIAL`. Current impact is zero because there are no candidates.

2. **Medium — Availability parsing assumes values.** [Line 90](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen015_screen.py:90) uses `bool(attr.get("crispr_ko_available"))`. Missing/null fields become definite `False`; the string `"false"` becomes `True`. Thus “never assumed” holds for caught exceptions, but not malformed or incomplete successful responses. Require an actual Boolean; classify missing/null/invalid values as unknown.

3. **Medium — Receipts cannot reproduce availability assignments.** [The receipt writer](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen015_screen.py:44) retains response hashes, sizes and statuses, but neither response bodies nor extracted availability values. Consequently, `requests[]` alone cannot establish which 162 models were screened or which 13 non-C patients they represent. Local crosswalk metadata independently corroborates those totals, but does not establish what each hashed API response contained. Preserve per-model values and patient assignments alongside receipts.

4. **Low — A failed response parse can produce two request entries.** The success receipt is appended before JSON/schema parsing; the caller appends another entry on failure ([lines 44–47](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen015_screen.py:44), [91–93](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen015_screen.py:91)). One HTTP request can therefore become two `requests[]` records. This did not occur in the recorded run. Update one receipt with its parsing outcome.

Independent recomputation produced:

| Check | Result |
|---|---|
| CSV SHA-256 | Matches pinned `419f65d1…aa37006` |
| C-map canonical SHA-256 | Matches pinned `4ddd0159…ae1f61` |
| C map | 148 entries, 142 patients; all re-resolve consistently |
| Models | 2,266 unique IDs: 2,010 cell lines, 256 organoids |
| Patients with both types | **0** |
| Cross-type direct links / ancestor chains | **0 / 0** |
| Missing parents / parent cycles | **0 / 0** |
| C-disjoint paired patients | **0** |
| Receipts | **256 unique organoid URLs, all HTTP 200, no recorded errors** |

Classification by `model_type` follows SPEC’s fixed computation. Omitting `growth_properties` from `kind()` is **not a demonstrated classification violation**: every organoid has `Unknown` growth properties; cell lines have Adherent, Semi-Adherent, Suspension or Unknown values. None explicitly supplies a second format.

Alternate-route checks found **zero cross-type matches** through sample IDs, exact or normalized model names, tokenized synonyms, or external identifiers. All 120 populated parent links connect cell lines; full ancestor traversal also finds no cross-type pair.

The proposed **BROAD_ID→DepMap bridge supplies no missed pair here**: no organoid has a BROAD_ID, and no BROAD-linked Passports patient belongs to the organoid patient set. Supplemental DepMap metadata checks found 19 organoid matches through HCMI, including 11 screened models; all are annotated Organoid/Dome, with no screened cell-line counterpart sharing their DepMap patient. A genuine same-patient, Sanger-linked screened 2D counterpart would merit consideration regardless of its DepMap identifier. A bridge merely identifying the same organoid—or an unrelated 2D model—does not satisfy SPEC.

The **13 screened non-C organoid patients are accurate** against `data/crosswalk_sanger_screened.csv`: 178 library records resolve unambiguously to **162 models / 155 Passports patients**, comprising **142 C patients and 13 outside C**. Those 13 patients represent **14 models**. This corroborates 162 true and 94 false availability counts, while leaving the per-response audit limitation above.

SGEN015_SCORE: 88