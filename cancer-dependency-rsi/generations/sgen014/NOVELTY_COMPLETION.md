# Novelty completion screen — sgen014 workstream 2 (2026-10-29)

Protocol: generations/sgen014/NOVELTY_PROTOCOL.md (frozen before screening).
Machine records: novelty_screen_results_v2.json (fetch+receipts), v3 (v2 + dispositions), v4 (replay-complete: full screening texts for survivors AND all 3,278 excluded records; stage-1 decisions independently recomputable).

## Coverage
- Query concept_broad (identical string to reviews/novelty_v5_searches.json):
  hitCount 3,634 then and now; 3,634 unique records fetched (cursor pagination, 5 successful requests: 4 populated pages + 1 empty terminal page, all 200).
- Previously screened (relevance top-25): 25 removed -> 3,609 novel records.
- Stage 1 (frozen keyword prefilter, title+abstract): 3,278 excluded,
  331 survivors.
- Stage 2 (lead screen of all 331; per-record dispositions in
  stage2_dispositions.json / results v3+v4): **0 plausible overlaps.**
  QUALIFIED DEVIATION from the frozen title+full-abstract stipulation: every
  title plus lead and signal-bearing abstract sentences were read for all 331;
  full abstracts were read for the nearest 3 and the 9 strong-signal records
  (indices 106, 125, 129, 149, 151, 253, 255, 301, 314 = PMIDs 41614813,
  40460119, 41218124, 40498663, 41591383, 38472198, 42923632, 38340720,
  41799521 - all excluded: reviews, drug-resistance, differentiation/plasticity
  biology; none joins paired-format lability to an external displacement
  endpoint). Sentence selection was deterministic keyword-based, not
  predeclared in the frozen protocol - recorded as a deviation; the
  completion claim is qualified accordingly. Nearest three, excluded on abstract:
  - PMID 40326560 (3D vs 2D cellular fitness, MYC murine liver): within-model
    context-specific fitness genes; no paired-format lability joined to an
    external displacement endpoint, no baseline-adjusted transport.
  - PMID 38433235 (ROS1+ NSCLC 2D vs 3D): differential DRUG sensitivity of
    engineered resistance variants; not dependency lability.
  - PMID 38360902 (tissue-location transcription programs, colon): anatomical
    location programs (CDX2), not culture-format lability.
- Other recorded queries were already fully screened (hitCounts 0/1/15/3/0).
- Non-Europe-PMC sources: NOT covered (residual, unchanged from v8).
- No full-text fetch was triggered (no plausible overlap at stage 2).

## Disposition
No same-substance analysis located in the completed set. The residual claim
(joining measured paired-format lability to external organoid rank
displacement, baseline-adjusted) remains *not located* in: S1/S2/S3 full
texts + S3 code contents + S1 supplement (text + visual, 5/5 pages, zero
panels) + complete concept_broad set (3,634) at title/abstract level.
Residual uncertainty: non-Europe-PMC sources, main-article Extended Data
figure pixels, and records whose abstracts omit methods detail. C6 remains
PARTIAL on its other grounds (patient-level inference), independent of novelty.
