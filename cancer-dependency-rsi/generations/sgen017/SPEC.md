# sgen017 — Same-condition repeat-observability census (metadata only)
(sol-xhigh Rank-2 target, reviews/xhigh_next_targets_v2.md)

## Construct (measurable from metadata alone)
Repeat coverage: among eligible same-condition groups, the fraction containing
>=2 independent screen executions. Metadata CANNOT measure dependency
instability, persistence, direction, or mechanism. Novelty risk: high
(repeat-screen reproducibility is established); this is a feasibility census.

## Sources (local metadata only; no outcome files)
data/ScreenSequenceMap.csv, data/ModelCondition.csv, data/CRISPRScreenMap.csv,
data/passports_model_list_20260921.csv (patient clustering, ID columns only).

## Eligibility (pre-committed)
Sequence rows with PassesQC true; DrugTreated false; IsEngineered false;
ExcludeFromCRISPRCombined false; ScreenType recorded (report distribution).
A screen execution = distinct ScreenID. Replicates within a ScreenID do NOT
count as repeats.

## Condition keys
Primary: (ModelID, ModelConditionID, Library).
Robustness: (ModelID, CellFormat, FormulationID, Library, Days) via
ModelCondition join; missing join fields => group counted as unqualified,
reported separately.

## Outputs
Eligible screens/sequences; groups total and repeat groups (>=2 ScreenIDs);
coverage fraction both keys; screens-per-group distribution; breakdown by
CellFormat and Library; organoid-format repeat groups; patient-level counts
(models in repeat groups mapped to Passports patient_id; unmapped reported).
Decision labels: CENSUS_COMPLETE (always, descriptive) with REPEAT_RESOURCE
{ABSENT: 0 repeat groups | SPARSE: 1-49 | MATERIAL: >=50} on the primary key.
Thresholds are descriptive census bands, not power claims.

## Non-claims
No instability/persistence inference; rerun reasons (QC/scheduling) unknown;
any outcome estimand requires a new locked design + precision plan first.
Sol-high review >=90 before close.

## Correction addendum (lead, 2026-10-29)
"Independent screen executions" above is corrected to: distinct annotated
ScreenIDs; independent initiation is NOT established by metadata (v1 review
HIGH). Primary key is identifier-degenerate in this release; the content
(robustness) key is the headline. Closed as census_v3.
