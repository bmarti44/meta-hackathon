> SUPERSEDED in part by Astra xhigh rounds 1-3 (reviews/astra_review_r*.md + dispositions); kept as the dated internal record. Numbers below predate the v2r2 regeneration.

# Review: GOAL v4 findings (medium_attribution_v2) — one review per finding

Reviewer: lead (self-review, adversarial). Date: 2026-10-29.
Scope: claims in `manuscript/manuscript_draft_v2.md` / FINDINGS v2 section.

## Claim 1 — 84–85% of differential dependencies medium-attributable, 0 format
Evidence: slopes A-on-D 0.88/0.90; F-on-D 0.14; flags with CI support; raw+norm concordant.
Attacks:
- A rests on 9 adherent models, mixed formulations, some singleton lineage cells (lineage adjustment partly cross-lineage for A). Mitigation: LOO slope 0.87–0.92, ≥94% flags retained under any single drop (`medium_attribution_v2_loo.json`); held-out adherent slope 0.88 (independent 5 models). Verdict: stands, caveat retained in text.
- Library offset (27 dual models, FBS-estimated) assumed medium-invariant. Organoid/TSM screens are Humagne-CD, so the offset mainly shifts the FBS baseline per gene; D error = offset estimation error. Humagne-only check underpowered (n0=5, r=0.75). Verdict: stands as primary route; flagged as limitation. A large offset error would have to be pathway-shaped to fabricate the sterol signal, and the Sanger-assay percentile shift (independent library) corroborates the gain side.
- Ratio CIs ignore A–D covariance from the shared baseline; covariance is positive, so CIs are wider than exact → medium flags conservative. OK.
- Hit threshold |Δ|≥0.25 arbitrary: raw scale (520/352 hits) gives 81%/75% — conclusion not threshold-driven.

## Claim 2 — Published fractions (Broad 87% of replicating; Sanger 5/8 headline)
- Denominators are definition-sensitive: Broad replication rate 55% reflects their unadjusted Mann-Whitney vs our lineage-adjusted dev-only test; reported both ways (of published: 48% medium; of replicating: 87%). Text must keep both numbers — it does.
- Sanger headline: 18 listed, 16 in Broad table, 8 replicate. Manuscript now states 16-in-table. SCAP is "unresolved" only by CI criterion (ratio 0.86) — text says so.
- No inferential claim on fractions (descriptive). OK.

## Claim 3 — Weakening is depletion kinetics, not biology
- Broad: "no compression" is partly by Chronos construction — text acknowledges. The load-bearing Broad facts are format-at-fixed-medium ≈ +0.13 vs D +0.90 and adherent reproduction, which normalization does not manufacture.
- Sanger: cross-matrix LFC magnitudes (table 6 vs qnorm EssMatrix) are processing-sensitive; depth ratio 0.63× could partly reflect processing. Percentile analysis (robust) supports: spliceosome pct unchanged, ribosome pct doubles (0.009→0.019). Text leans on percentiles, magnitudes secondary. OK.
- Alternative not excluded: organoid-medium-specific protein-turnover biology. Text says mechanism needs CPD-recorded screens. OK.
- Gene panels are small hand-picked sets (SPL=8, RIBO=12 incl. mitoribo in name-pattern variant). Panel medians could be unrepresentative of KEGG spliceosome/ribosome. Partial mitigation: genome-wide loss-tail behavior (slopes over 209 loss hits) agrees; panels used for magnitude illustration. Acceptable for a technical note; a full MSigDB-set version is future work.

## Claim 4 — ITGB1/DDX3X "survivors"
- Based on point estimates (ratio_A<0.3) with wide CIs + Sanger Δpct for ITGB1. Text frames as candidates, not established format effects (they fail the format-candidate q/ratio joint rule). Survivor table released (`survivor_candidates_v1.csv`, 70 unresolved, 32 format-leaning by point estimate). OK.

## Claim 5 — Wnt genes medium-attributable
- Conflicts with NextGen minipool (FZD5/WLS not medium-sensitive there). Our evidence is formulation-family level (9 adherent models, several formulations). Text flags the conflict. Downgrade risk accepted.

## Process notes
- Held-out contrasts reuse the full FBS baseline (organoid side held out by patient; baseline shared). Interpretation stated accordingly.
- Sanger cohort is spent/exploratory (recomb21 precedent); no confirmatory claim from it.
- Superseded artifacts: sanger_direct_check v1/v2 (wrong matrix, pooled cell lines) — do not cite.

## Overall
Claims 1–3 stand with stated caveats; claim 4–5 correctly hedged. No number in the manuscript failed re-derivation from artifacts (spot-checked: flags, slopes, depths, fractions, held-out). Suitable as a technical-note preprint after author review.
- Addendum: the hand-panel risk was confirmed by panels_curated_v1 — spliceosome complex-wide weakening does not survive curated sets (Broad +0.035; Sanger scaled stronger in organoids); ribosomal residual does. Manuscript corrected 2026-10-29.
