# sgen014 novelty-completion protocol (frozen before screening, 2026-10-29)

## Frozen set
Query: `concept_broad` exactly as recorded in reviews/novelty_v5_searches.json
(Europe PMC; hitCount 3634 at prior run; top-25 already screened there).
Plus for completeness the other recorded queries (all fully screened already:
hitCounts 0/1/15/3/0). Cutoff: 2026-10-29. Re-fetch must use the identical
query string; new hitCount and any delta vs 3634 reported, not silently adopted.

## Dedup + eligibility
Dedupe by Europe PMC id; remove the 25 already-screened records (by id from
the v5 `top` list). Remaining records pass through a deterministic two-stage
screen on TITLE+ABSTRACT text only:
- Stage 1 (machine prefilter, frozen terms): record survives iff BOTH
  (a) format/environment terms: /dome|plastic|matrigel|3d|three-dimensional|spheroid|organoid|culture (medium|media|format)|serum.free|growth format|format.*labil|labil/ AND
  (b) dependency-screen terms: /crispr|dependency|dependencies|essentialit|knockout screen/
  (case-insensitive). Stage-1 exclusions counted, never hand-overridden.
- Stage 2 (lead screen of survivors): plausible-overlap iff title/abstract
  indicates BOTH paired-format/environment lability measurement AND joining
  it to an external/organoid dependency outcome or displacement/transport
  claim. Plausible overlaps get full-text fetch attempts (Europe PMC OA
  only); unavailable full texts recorded as gaps.
- Non-Europe-PMC sources: NOT covered (named residual, as before).

## Outputs
generations/sgen014/novelty_screen_results.json (per-stage counts, survivor
dispositions) + NOVELTY_COMPLETION.md (coverage, exclusions, unavailable
sources, residual novelty uncertainty). FAIL condition (inherited): any
located same-substance analysis -> novelty claim withdrawn/narrowed honestly.
