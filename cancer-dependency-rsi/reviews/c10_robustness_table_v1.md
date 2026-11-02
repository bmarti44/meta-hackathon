# C10 conclusion-by-analysis robustness table (scientific-only track)

> **Grouping qualification (sgen001, applies to every row):** all estimates/intervals/decisions below are the archived locked analyses over 144 covariate-ID groups representing 142 patients; patient-weighted estimate, interval and decision are unverified (unknown size/direction). Robustness statements describe the archived analyses only.

Source: `lock_s/results/external_v1.json` (single locked run); result review `reviews/external_result_high_review_v1.md`.

| analysis | role | estimate | interval / range | sign negative? | magnitude < 0.20? |
|---|---|---|---|---|---|
| Primary (confirmatory207 / mean_abs_delta / base_strength) | decision | −0.146 | donor 95% [−0.175, −0.114] | yes | **yes (BOUND)** |
| S1 null-calibrated displacement | Holm secondary | −0.209 | [−0.230, −0.187] | yes (Holm p 0.0016) | no (straddles −0.20) |
| S2 TMOD1-alias 208 | Holm secondary | −0.145 | [−0.175, −0.113] | yes (0.0016) | yes |
| S3 v1_1 library for 13 dual models | Holm secondary | −0.151 | [−0.178, −0.115] | yes (0.0016) | yes |
| S4 unadjusted | Holm secondary | −0.217 | [−0.245, −0.185] | yes (0.0016) | no |
| Broad model-cluster bootstrap (6 models) | stability | — | [−0.208, −0.035] | yes | not robust |
| Leave-one-Broad-model-out | stability | −0.166 … −0.082 | — | yes (all 6) | yes (all 6 points) |
| Lineage-cluster bootstraps (multi-cluster scenarios only) | stability | — | split [−0.209, −0.032]; Pancreas [−0.186, −0.001]; Ovary [−0.146, −0.001]; Esophagus/Stomach [−0.171, −0.075] | yes | mostly; split crosses |
| `all_possibly_shared` (single cluster) | — | degenerate | — | **excluded: no stability information** | — |
| Pathway-block bootstrap (11 gene blocks) | stability | — | [−0.264, −0.016] | yes | not robust |

## Surviving conclusions

1. **Robust:** the panel-level conditional association is negative (opposite to the positive conjecture) across all secondaries and all informative composition analyses.
2. **Primary-definition only:** |ρ| < 0.20 (BOUND) for the frozen primary and the S2/S3 data-handling sensitivities. It is **not** robust to endpoint definition (S1, S4) or to Broad-model and gene-block composition.
3. **Not supported:** dependency invariance or equivalence (no positive-dependency, equivalence or assay-sensitivity evidence), causal or mechanistic claims, per-gene inference, or population inference over Broad models (donors unresolved).

## Uncertainty and multiplicity accounting

- Single primary parameter; Holm FWER 0.05 over exactly 4 preregistered secondaries; all other analyses descriptive.
- The donor interval ignores gene/pathway sampling and normalization uncertainty (Sanger spline/ComBat within the organoid cohort; Broad Chronos). These are disclosed, not propagated.
- No adversarial check found an execution defect (result review: valid; 30 locked hashes match; single run).
- Any further outcome-dependent analysis of C is exploratory (C consumed).
