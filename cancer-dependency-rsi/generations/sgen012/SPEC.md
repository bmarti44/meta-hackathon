# sgen012 SPEC (sol-xhigh generated 2026-10-29; saved verbatim from reviews/xhigh_sgen012_generate_v2.md lines 2+)

SPEC: sgen012 framing A metadata-only necessary-condition screen
Execution status: unrun; this specification asserts no empirical gate result.

INPUTS + PINS
- data/ModelCondition.csv SHA-256: a1edda78cd60718e5c99690ce8ab80315b65ddc9346643338d2c1c774fc51326
- data/ScreenSequenceMap.csv SHA-256: acaedf0549afda50e5f3df28645c5c2193acbdb9779f9f8099861b763d1be296
- Inherit sgen010 full-file locks: data/Model.csv (65eb1895...), data/CRISPRScreenMap.csv (43cc5286...).
- Inherit established_pool_v4.json (0c1080f8...) and screen_v7.json (d6e6eb69...) from sgen010.
- Prefixes identify inherited locks; they are not substitutes for full hashes. Missing full-lock verification prevents a pass.
- Preserve the established population: 1,106 models, 1,069 SIDP, 1,068 linked patient components.
- Restrict this screen to its pinned cell-line subset: 1,095 models and 1,057 linked patient components.
- Preserve pinned membership, component identifiers, lineage annotations, and exclusions; do not reconstruct components.
- Gene.csv is excluded entirely because its essentiality/selectivity values are outcome-derived.
- CRISPR outcomes in ~/Downloads remain unread. No outcome access, summaries, proxies, or outcome-guided choices are permitted.

ENVIRONMENT DEFINITION
- Primary medium identifier: FormulationID from the condition explicitly linked to the screened exposure.
- Environment is the tuple (normalized CellFormat, canonical FormulationID).
- GrowthMedia supplies a metadata-only consistency check and narrowly defined missing-ID harmonization.
- Normalize text by Unicode normalization, case folding, trimming, and collapsing whitespace; preserve raw values.
- Fill a missing FormulationID only when normalized GrowthMedia maps uniquely to one explicit FormulationID within the same CellFormat in pinned metadata.
- Freeze and publish that deterministic mapping before counting strata; ambiguous mappings remain unresolved.
- Do not merge distinct formulation IDs, invent media synonyms, or infer CellFormat from Morphology.
- An explicit contradiction between media description and documented formulation identity makes the record unresolved.
- Missing CellFormat or unresolved formulation identity prevents environment assignment.
- ScreenType describes assay context only: retain it as a stratifier and audit variable, never an environment field.
- Report SerumFreeMedia, PlateCoating, PassageNumber, Morphology, and source distributions as additional context.
- A ModelConditionID join alone does not prove screening-time exposure; sequencing-time annotation is insufficient.

SCREEN ELIGIBILITY
- Start with the immutable established screened cell-line denominator; every subsequent exclusion remains in coverage denominators.
- Join pinned screens to sequences and their explicit ModelConditionID, then to ModelCondition and canonical ModelID.
- Require canonical model identity to agree across joins; use model_id only through an established alias mapping.
- Require PassesQC=true, ExcludeFromCRISPRCombined=false, DrugTreated=false, and IsEngineered=false.
- Decode flags using documented encodings; blanks or undocumented codes are unknown, never favorable defaults.
- Require the linked condition and its parent history to contain no prescreen or anchor drug exposure.
- Drug names or exposure indicators exclude the record; blank drug fields mean “none” only where documented.
- DataSource must be nonmissing and consistent with the linked screen's documented source.
- Retain every documented source meeting these rules; report source counts and exclude unresolved source mappings.
- Keep the ScreenType scope inherited from screen_v7.json; unknown context codes remain unresolved.
- Collapse duplicate SequenceID records only if their metadata agree; conflicting duplicates are unresolved.
- Collapse eligible sequences, screens, and replicates to one model contribution, retaining their complete audit trail.
- Multiple eligible conditions with the same environment tuple yield one model assignment.
- A model with multiple eligible environment tuples is excluded; do not select a preferred condition or replicate.
- An unresolved potentially eligible record that could change a model's assignment prevents that assignment.
- Traverse parent conditions for identity, treatment history, and provenance checks; reject cycles and broken chains.
- Never inherit missing current-condition environment fields from a parent.
- Components represented in multiple retained environments are excluded from all arms before ranking.
- Count each remaining linked patient component once; retain model counts separately.

FIXED SINGLE-CONTRAST SELECTION
- Rank all assignable environment tuples by descending number of distinct linked patient components.
- Break ties lexicographically by normalized CellFormat, then canonical FormulationID, using UTF-8 byte order.
- Select the first two tuples once: rank 1 is arm A; rank 2 is arm B.
- Perform selection before examining lineage positivity or precision results.
- Fewer than two strata fails the contrast-existence gate.
- No alternative pairing, runner-up substitution, source restriction, or threshold change may rescue a failed contrast.

COVERAGE AND POSITIVITY GATES
- Establishable means eligible, screening-time environment assigned, and retained after model/component ambiguity exclusions.
- Require establishable coverage of at least 90% of the 1,095 models and independently 90% of the 1,057 components.
- Thus require at least 986 models and 952 components across all assignable environments.
- Report selected-arm coverage separately; assignment elsewhere does not increase either selected arm's sample size.
- Require at least 100 distinct linked patient components in each selected arm.
- Require at least three lineage categories with at least k=20 components in EACH arm.
- Use pinned lineage labels without regrouping; unknown or conflicting component lineage contributes to no positivity cell.
- Freeze these thresholds; do not relax them after viewing metadata counts.

PRECISION GATE FOR THE SELECTED CONTRAST
- Let n_A and n_B be the distinct, disjoint linked patient component counts in the selected arms.
- Freeze a two-independent-arm Fisher-z benchmark: B=(1.959964+0.841621)*sqrt(1/(n_A-3)+1/(n_B-3)).
- Define the reference-zero correlation-equivalent MDR as tanh(B); n_A<=3 or n_B<=3 fails.
- Require MDR<=0.146, equivalently B<=atanh(0.146), using 80% power and two-sided alpha=.05.
- The 0.146 threshold is a screen convention, not an observed effect or a universal raw-correlation difference.
- This independent-component, unadjusted precision bound is optimistic and never establishes outcome-design feasibility.
- A pooled-population bound may be reported descriptively but cannot determine retest or override contrast failure.

CONFOUNDING REPORT
- Publish component-count environment-by-lineage tables for all assignable strata and for the selected contrast.
- Report Cramer's V=sqrt(chi-square/[N*min(rows-1,columns-1)]); mark degenerate tables undefined.
- Treat V as descriptive: no V threshold, p-value selection, or contrast replacement is permitted.
- Also report ScreenType and DataSource distributions by arm; these cannot redefine the environment.

DECISION LABELS AND AUTHORIZATIONS
- First establish whether the mandatory provenance audit and every gate are evaluable under the frozen rules.
- A_STILL_UNRESOLVED: an input lock, global field semantics, screening-time provenance, or required audit basis remains unevaluable.
- Record-level missingness or ambiguity is excluded and counted against coverage; it alone does not make the audit unevaluable.
- A_REJECTED: the audit is evaluable and any contrast-existence, coverage, arm-size, positivity, or precision gate fails.
- A_PROVENANCE_ESTABLISHED: the audit is evaluable, retained assignments have screening-time provenance, and every gate passes.
- A_PROVENANCE_ESTABLISHED authorizes only preparation and locking of a separate outcome design.
- Advanced C3/C4 remain gated behind both this pass and that separately locked design; this generation authorizes no outcome access.

PREDECLARED FAILURE MODES AND AUDIT
- CONDITION_RECORDED_AT_SEQUENCING: timing does not establish screening exposure.
- FREE_TEXT_MEDIA_HARMONIZATION: media text cannot identify an unambiguous formulation.
- SCREEN_WITHOUT_MODELCONDITIONID: no direct screen-linked condition assignment exists.
- PARENT_CONDITION_DEPENDENCE: assignment requires unsupported inheritance or an invalid parent chain.
- Publish hashes, join cardinalities, exclusion reasons, harmonization map, ranked strata, gate values, and the resulting label.
- Hash-pinned metadata repairs file provenance only; it does not by itself establish exposure timing or pass any gate.

## Lead amendment note (2026-10-29, before v2; SPEC text unchanged)
v1 implementation deviations found at sol-high review (68) are corrected in
src/sgen012_screen_v2.py without changing any gate, threshold, or rule above:
real evaluability logic (A_STILL_UNRESOLVED reachable); unknown-flag records
block only when they could change assignment; DataSource consistency audit;
ScreenType derivation recorded from README batches; full audit publication
(join cardinalities, exclusion membership, all ranked strata (132 at v2), harmonization
crosswalk, selected-contrast Cramer V, context distributions, selected
coverage); strict condition ModelID identity; parent identity/source checks;
exposure-indicator fields honored; explicit disqualifiers classified before
unknown ScreenType; README hash-pinned. Two audit-basis gaps cannot be
completed from supplied artifacts and keep evaluability false: (a) blank
drug-name = none is not documented in the README; (b) no frozen
model-to-component mapping artifact exists (deterministic reconstruction
asserted equal to pinned counts is used and disclosed). Also disclosed: the
precision gate is structurally unattainable in this population (optimal
1057-split MDR 0.171 > 0.146; needs >=1,458 components) - a SPEC property,
reported, not altered.

## Close-out (lead, 2026-10-29)
A_STILL_UNRESOLVED (v4). Provenance chain works (729 models / 724 components
establishable) but every quantitative gate fails, and the two-arm precision
gate is structurally unattainable in this population (best MDR 0.1711 at an
optimal split of 1,057; >=1,458 components required). Media environment is
strongly lineage-confounded (Cramer V 0.568). Review arc 68 -> 84 -> 97.
Consequence: no two-arm formulation contrast at Lock-S scale is viable on the
established pool; next design generation requires a different design class
(sol-xhigh recombination), not metadata repair.
