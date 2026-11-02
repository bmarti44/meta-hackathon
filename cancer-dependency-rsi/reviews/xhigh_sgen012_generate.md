SGEN012_GENERATED: YES

# sgen012 — Framing-A screening-environment provenance and identifiability retest

**Status:** Generated for prospective locking; not executed. Save and hash this SPEC before computing new metadata distributions, selecting the primary contrast, or evaluating gates.

**Date:** 2026-10-29.  
**Generation route:** gpt-6.1-sol, xhigh; read-only generation.  
**Parents:** sgen010 established identity/component pool and sgen011 framing-A discriminator, including Amendment v2 and reviews v2/v3.

## 1. Question and scope

Does the newly supplied metadata establish release-recorded screening environments for the established cell-line pool, with enough independent patient components, environmental variation, and within-lineage overlap to justify preparing a separate locked outcome design?

The new provenance chain is:

```text
CRISPRScreenMap.ScreenID
  -> ScreenSequenceMap.ScreenID
  -> ScreenSequenceMap.ModelConditionID
  -> ModelCondition.(CellFormat, GrowthMedia, FormulationID, ...)
```

ModelID must agree across every participating table.

This is a **metadata-only necessary-condition screen**. It does not establish a scientific estimand, calibrated power, a dependency association, environmental causation, transport to organoids, or a complete outcome-analysis design.

The historical sgen011 verdict remains `NEITHER_PASSES` for its original inputs. This generation prospectively retests framing A using additional provenance. Framing B is not retested.

## 2. Inputs and outcome firewall

All paths below are relative to `cancer-dependency-rsi/`, except the mirrored workspace GOAL.

| Input | SHA-256 |
|---|---|
| `data/Model.csv` | `65eb1895800e71a963a3ab56e5d08c8d006cb0d9e7aa68f7e34a3810a2a3cbc7` |
| `data/CRISPRScreenMap.csv` | `43cc528614053d4c5a96729c2d782375227231a0cfea23de6c519b8989fa1252` |
| `data/ModelCondition.csv` | `a1edda78cd60718e5c99690ce8ab80315b65ddc9346643338d2c1c774fc51326` |
| `data/ScreenSequenceMap.csv` | `acaedf0549afda50e5f3df28645c5c2193acbdb9779f9f8099861b763d1be296` |
| `data/DepMap26Q3_README.txt` | `5672d9e04f18320e9ca1d25747427275dcabb44bffe45eba34d196f1b44dd3ec` |
| `data/Gene.csv` — provenance/header only | `5974d0fdecc5047e13bbb33117452c36a5f4bcbd937a025bcf799c0aa707261b` |
| `data/passports_model_list_20260921.csv` | `419f65d1d6534454194f1a744550fab632cd1d7411f6b13411a885735aa37006` |
| `lock_s/cohort.csv` — identity metadata only | `11b1d9a7df6e7700e91129e366e55d99844a4cd96ad6a350fe850bcdc2ab168e` |
| `generations/sgen010/SPEC.md` | `6e091582840a14b88def3ee0bb1ce7a204735fcd9b2cda8adba4b90843401455` |
| `generations/sgen010/screen_v7.json` | `d6e6eb69a9f239ea61671397a16031a8c78be9330f049f17437ce3698832766e` |
| `generations/sgen010/established_pool_v4.json` | `0c1080f8a4330e9be93b1fa0e0821fdf557a7985403b0ffa9d0129a0614bb26b` |
| `src/sgen010_screen_v7.py` — identity algorithm reference | `c61e3f1a64eda20d2c2dac905146cc4fe4808576815b9b1bb8f34951db2a1eb9` |
| `generations/sgen011/SPEC.md` | `d88b74489d5c94450d814f1589bf1dcd9af806136492c4c6d0695f580433d3b3` |
| `generations/sgen011/screen_v3.json` | `625f0582a2c426c33474b14305e1428e48baf69b9ebaf680d35aa1f3c465a953` |
| `reviews/sgen011_high_review_v2.md` | `d371f2e404d006b4f8c2d5aacdac8fb52d463e089b500ec4d8cce938cdbe9d9f` |
| `reviews/sgen011_high_review_v3.md` | `98488ea0c960b01d7de90a9d920f9769ebf7d15e8ce738b71a3d43fbc4f1376a` |
| `GOAL.md` and identical workspace mirror `../GOAL.md` | `f4ea241a97bc7a8857e2e11c36441a80f8c743e6b89eb52864c35f02da6fc31e` |

Enforce hashes before analysis. A mismatch requires reconciliation and a prospectively versioned lock; silently updating expected hashes is prohibited.

`CRISPRGeneEffect.csv` and `ScreenGeneEffect.csv` in `~/Downloads` are outside the project and outside this generation’s input allowlist. Do not open, inspect headers, hash, copy, join, summarize, reference values from, or otherwise use either file. Do not inspect other dependency outcomes or reopen spent cohort-C outcomes.

Gene.csv is unnecessary for the discriminator. Its `essentiality` and `selectivity` columns are excluded, along with all other Gene.csv data-row values. Its presence and header may be documented; it supplies no gene selection, filtering, or biological evidence.

Project only required metadata fields from other tables. Clinical response fields remain unused. No network acquisition, outcome fitting, policy rollout, or outcome-based selection is authorized.

## 3. Frozen population and independence unit

Reconstruct the sgen010 identity graph over **all Model.csv rows**, using its pinned Passports assignments and patient-strict C-exclusion algorithm. Do not construct a new graph solely from environment-complete models or screened models.

Carry forward:

- Unanimous strong identifier routes establish identity.
- Name matches remain candidate evidence and cannot establish identity.
- Confirmed DepMap PatientID↔Passports SIDP links define connected patient components.
- C membership and candidate C evidence propagate at component level.
- Unresolved, name-only, conflicting, and C-overlapping models remain ineligible.
- New ModelCondition records cannot expand the established identity pool.

Verify the reconstructed established membership and screened assignments against `established_pool_v4.json`, and the component counts against `screen_v7.json`. Reproduce the canonical Witness-A mapping hash:

```text
4ddd01592c2d8221eff73d4eded6a051bcac676e1c13fcbd5bc4db91a3ae1f61
```

Required baseline reconstruction:

| Population | Models | Linked patient components |
|---|---:|---:|
| All established screened models | 1,106 | 1,068 |
| Established screened models with `ModelType == "Cell Line"` | 1,095 | 1,057 |

The second row is the framing-A population, denoted \(M_A\) and \(P_A\). Organoids remain excluded, including the 11 established organoids.

A linked patient component is the independence unit. Multiple models, conditions, screens, libraries, sequences, replicates, and timepoints never create additional independent patients.

These population counts are verification targets, not imported effective sample sizes. Reconstruction failure yields `A_STILL_UNRESOLVED`.

## 4. Screen linkage and eligibility

### 4.1 Referential integrity

Begin with ScreenIDs in the pinned CRISPRScreenMap for \(M_A\). Do not infer screens from names, ModelCondition availability, or outcome-matrix membership.

For each ScreenID:

1. Require a matching ScreenSequenceMap record.
2. Require agreement between CRISPRScreenMap.ModelID, ScreenSequenceMap.ModelID, and ModelCondition.ModelID.
3. Require a populated ModelConditionID that resolves directly to a unique ModelCondition record.
4. If ModelCondition.`model_id` is populated, require agreement with ModelCondition.ModelID.
5. Require one ModelConditionID, ScreenType, and Library per ScreenID across its sequence records.

Exact duplicate records may be collapsed and must be counted in diagnostics. Conflicting duplicate keys are unresolved, never resolved by first/last-row selection. A SequenceID assigned to incompatible screens or conditions invalidates the affected screen linkage.

Do not fill condition fields from parent conditions, onboarding fields, another assay, or another screen.

### 4.2 Primary assay and source restrictions

The primary audit admits only:

```text
ScreenType == "2DS"
ModelCondition.DataSource == "Broad"
```

Normalize ScreenType by trimming and uppercasing; normalize DataSource by trimming and casefolding. No additional source aliases are permitted.

The README explicitly defines `2DS` as “2D standard.” It does **not** establish CellFormat, medium, or equivalence between adherent and suspension cultures.

Other documented source/type values are out of scope. Missing or unrecognized source/type annotations are unresolved. Report their losses separately.

### 4.3 QC and treatment exclusions

Boolean parsing is fixed:

```text
TRUE:  true, yes, 1
FALSE: false, no, 0
```

Parsing is case-insensitive after trimming. Blank, unknown, and unrecognized values are unresolved, not false.

A screen requires at least **two distinct SequenceIDs** with:

- `PassesQC == TRUE`;
- `ExcludeFromCRISPRCombined == FALSE`;
- positive numeric `Days`;
- populated Library.

Among these otherwise qualifying rows:

- Any `DrugTreated == TRUE` excludes the screen.
- Any `IsEngineered == TRUE` excludes the screen.
- Missing or unrecognized DrugTreated/IsEngineered values make the screen unresolved.
- Mixed treatment or engineering flags cannot be split into a favorable subset.

Exclude conditions with recorded prescreen or anchor drug exposure. Inspect PrescreenTreatmentDrug, PrescreenTreatmentDrugDays, AnchorDrug, AnchorDrugConcentration, and AnchorDaysWithDrug. Blank fields and explicit absence/zero values indicate no positive exposure record; unknown values or inconsistent drug/duration/concentration fields are unresolved. An affirmative exposure record excludes the condition even if DrugTreated is false.

Exclude a model when Model.csv records engineering, engineered-model details, or cultured drug resistance. Blank model annotations may accompany an explicit false screen-level IsEngineered flag; blank annotations alone do not establish absence of engineering. Unrecognized engineering annotations are unresolved.

Report sequence-level QC support accurately. This input set does not independently verify screen-level QC metrics or guarantee inclusion in any future outcome product.

Known QC failures and known out-of-scope screens are excluded. A potentially in-scope screen with unresolved linkage or eligibility prevents an unambiguous model assignment.

## 5. Screened-environment definition

The primary recorded environment is the joint tuple:

```text
E = (
    ModelCondition.CellFormat,
    ModelCondition.FormulationID,
    ModelCondition.SerumFreeMedia,
    ModelCondition.PlateCoating
)
```

ModelCondition.GrowthMedia is a required description supporting the formulation assignment.

This definition describes a **recorded culture-condition state**. ScreenType is an assay restriction; DataSource is a source restriction. Neither substitutes for an environmental measurement.

### 5.1 Required values and normalization

A complete environment requires:

- CellFormat in `{Adherent, Suspension, Dome, Spheroid, Mixed}`;
- populated FormulationID;
- populated GrowthMedia;
- explicitly parseable SerumFreeMedia;
- PlateCoating in `{Laminin, Matrigel, Collagen, None}`.

`Unknown` and missing values are incomplete. `Mixed` is an explicit recorded category and is not reassigned. `None` is a valid coating value and is not missing.

For categorical fields, trim and casefold for lookup, then emit the canonical labels above. Preserve identifiers after trimming; do not numerically coerce them.

Normalize GrowthMedia only by trimming, collapsing whitespace, and casefolding. Do not infer ingredient concentrations, serum content, medium families, or recipe equivalence from free text.

Within the otherwise relevant screen-linked conditions, a FormulationID must map consistently to one normalized GrowthMedia description and one SerumFreeMedia value. Conflicts make that formulation’s assignment unresolved. Different FormulationIDs are never automatically merged because their descriptions resemble one another.

Do not fall back to GrowthMedia-only grouping when FormulationID is missing.

### 5.2 Provenance interpretation

The pinned README describes ModelCondition as the conditions under which the model was assayed and ScreenSequenceMap as the sequence-to-screen mapping with ModelConditionID. A direct, consistent chain through these tables establishes **release-recorded screening-condition provenance**.

Model.csv GrowthPattern, OnboardedMedia, FormulationID, SerumFreeMedia, and PlateCoating cannot supply missing screening-condition values.

No timestamps are supplied in these schemas. Their absence does not itself invalidate the direct identifier chain, but this generation cannot certify that a recorded recipe was unchanged throughout screening or contemporaneously entered. Evidence that a condition describes only an unrelated sequencing assay, or an incompatible later culture state, makes the affected linkage unresolved.

## 6. Multiple screens, conditions, and patient components

No representative screen or model may be chosen to improve coverage, balance, or precision.

A model is environment-covered only when:

1. It has at least one eligible screen.
2. Every potentially in-scope screen has resolved eligibility and linkage.
3. Every eligible screen has a complete environment.
4. All eligible screens agree on E.

Different ModelConditionIDs with identical E may agree. Different libraries, replicate numbers, or assay days do not add independent observations. Multiple eligible environments produce `MULTI_ENV_MODEL`; exclude that model from primary assignment and retain its records for descriptive reporting.

A patient component is environment-covered only when **every member model in \(M_A\)** is environment-covered and all those models agree on E. Otherwise it is uncovered. This deliberately conservative rule prevents choosing one favorable model from a donor.

A covered component receives one environment assignment and one vote. Components with multiple environments are not reassigned to the larger stratum or counted in both arms. A paired-condition design would require a separate generation.

For lineage analyses, use Model.csv.OncotreeLineage. A component has an ascertainable lineage only when all its \(M_A\) models have the same populated, non-Unknown lineage. Conflicting or missing lineages remain unresolved; do not choose a majority lineage.

## 7. Coverage gates and primary contrast

### 7.1 Fixed coverage denominators

Require both:

```text
covered models / 1,095 >= 0.90
covered linked patient components / 1,057 >= 0.90
```

Use full-precision fractions. The denominators precede source, QC, treatment, engineering, and completeness exclusions. They cannot shrink after exclusions.

Also report corresponding counts and rates for all 1,106 established models / 1,068 components, with organoids clearly separated. Those descriptive totals cannot rescue a framing-A gate.

Coverage below either primary threshold yields `A_STILL_UNRESOLVED`: sufficiently broad screened-environment provenance has not been established under this lock. Itemize whether losses arise from missing records, ambiguity, or known scope exclusions.

### 7.2 Exactly one primary contrast

There is **one** primary metadata contrast, C1.

After environment assignment and before excluding components for lineage overlap:

1. Count distinct covered linked patient components in every E stratum.
2. Rank strata by decreasing component count.
3. Break ties by ascending lexicographic order of the canonical serialized E tuple.
4. Select the first two strata as E0 and E1.
5. Freeze their tuple values and component memberships in the result.

Do not replace either stratum after inspecting overlap or precision. Other pairs are descriptive and cannot produce a passing verdict.

If fewer than two strata exist after the provenance coverage gates pass, reject the candidate.

C1 must differ in CellFormat or FormulationID. A difference only in coating or serum annotation does not satisfy this registered format/formulation contrast.

If the selected strata differ only by FormulationID while CellFormat, normalized GrowthMedia, SerumFreeMedia, and PlateCoating agree, the environmental distinction is unresolved: report `FORMULATION_ALIAS_UNRESOLVED` and obtain authoritative formulation clarification in a later generation. Do not merge or substitute strata.

This selection rule seeks a well-supported candidate contrast using metadata. It does not justify that contrast’s scientific importance or novelty.

### 7.3 Lineage ascertainment and positivity

For **each** selected stratum, require ascertainable lineage for at least 90% of its covered components. Failure yields `A_STILL_UNRESOLVED`.

Let \(N_{\ell e}\) count ascertainable linked components of lineage \(\ell\) in selected environment \(e\), before overlap restriction.

A lineage belongs to the common-support set \(L^*\) iff:

```text
N_l0 >= 20
N_l1 >= 20
0.10 <= N_l1 / (N_l0 + N_l1) <= 0.90
```

Include **all** qualifying lineages. Do not select the most favorable subset or combine rare lineages into “Other.”

Require all of the following:

- At least **three** lineages in \(L^*\).
- At least **80% of each selected stratum’s covered components** retained in \(L^*\); components with unresolved lineage count against retention.
- At least **50 linked patient components per environment** after restriction to \(L^*\).
- Each environment contributes at least **20%** of the final C1 components.

The C1 analysis population is exactly the linked components in E0/E1 and \(L^*\). These are support conventions for this discriminator; they do not prove exchangeability or adequate adjusted power.

## 8. Precision necessary-condition screen

Apply the sgen011 Amendment-v2 convention to C1’s final linked patient components, after all exclusions and common-support restriction.

Let:

```text
n0 = distinct retained components in E0
n1 = distinct retained components in E1
n  = n0 + n1
```

For \(n>3\):

\[
SE_z=\frac{1}{\sqrt{n-3}},
\]

\[
MDR(n)=\tanh\left(
\frac{\Phi^{-1}(0.975)+\Phi^{-1}(0.80)}
{\sqrt{n-3}}
\right).
\]

Require:

```text
MDR(n) <= 0.146
```

Use unrounded values for the gate. Under this formula, the minimum integer n is **366**. Report n0, n1, n, SE_z, MDR, and the threshold comparison.

For \(n\le3\), precision fails; serialize an explicit status with null numerical outputs rather than nonstandard JSON infinity.

There is one primary contrast, so this screen uses two-sided alpha 0.05 and nominal 80% power. No other environment or lineage contrast can inherit that primary status. Adding primary contrasts requires a new prospective lock and multiplicity rule.

The historical pooled 1,057-component bound of approximately 0.0861 is context only. It cannot determine this verdict.

**Interpretation:** This remains an optimistic Fisher-z correlation-size screen. It ignores nuisance estimation, residual confounding, outcome missingness, measurement error, binary-exposure details, ties, and the future estimand’s actual variance. It is not a calibrated power calculation for an environmental effect, difference of correlations, or lineage-adjusted dependency analysis.

The 0.146 value is the inherited early-rejection convention, not a justified scientific target effect. Passing requires a later design to justify its own estimand, margin, multiplicity control, and precision analysis.

## 9. Metadata confounding screen

Report environment×lineage contingency tables at linked-component level for:

1. All environment-covered components with ascertainable lineage, retaining every E stratum.
2. E0/E1 before common-support restriction.
3. Final C1 after common-support restriction.

Use uncorrected Pearson chi-square without continuity correction and report:

\[
V=\sqrt{\frac{\chi^2}{n\min(r-1,c-1)}}.
\]

Report the underlying counts, row/column totals, structural zeros, and number of expected cells below five. Do not report asymptotic significance as evidence for environmental identifiability. If fewer than two nonempty rows or columns exist, report V as undefined, not zero.

Flag `HIGH_LINEAGE_ASSOCIATION` when \(V\ge0.50\). Report selected-environment proportions within every lineage, including excluded lineages.

V is descriptive and has no separate pass/fail cutoff. The exact positivity gates in §7.3 determine the lineage-overlap screen. A large V must remain visible even when those gates pass.

Also report C1 environment×Library counts and assay-Day distributions, counting components rather than sequences wherever components are summarized. Flag disjoint library support. These diagnostics identify additional work for the outcome design; they do not establish technical comparability.

No outcome regression, propensity fitting, or molecular adjustment is performed here.

## 10. Decision labels and precedence

Emit exactly one generation verdict. Preserve individual gate statuses and reasons even when evaluation stops early.

Apply this sequence:

1. **`A_STILL_UNRESOLVED`** if required input integrity, identity reconstruction, or screening-condition semantics cannot be verified; or either §7.1 coverage threshold fails.
2. Otherwise, **`A_REJECTED`** if fewer than two complete E strata exist.
3. Select C1 exactly as specified. Emit **`A_STILL_UNRESOLVED`** for the selected formulation-alias ambiguity. Emit **`A_REJECTED`** if C1 lacks the required CellFormat/FormulationID distinction.
4. Emit **`A_STILL_UNRESOLVED`** if either selected stratum fails the 90% lineage-ascertainment gate or a required calculation remains indeterminate because of metadata ambiguity.
5. Otherwise, emit **`A_REJECTED`** if any positivity, minimum-stratum-size, retention, balance, or precision gate fails.
6. Emit **`A_PROVENANCE_ESTABLISHED`** only if every preceding requirement passes.

`A_REJECTED` rejects this locked candidate contrast under these inputs and conventions. It is not evidence that environmental effects are absent or that every possible framing-A design is infeasible.

`A_PROVENANCE_ESTABLISHED` means:

> Broad, untreated, unengineered, sequence-QC-supported 2DS cell-line records establish sufficiently broad release-recorded screening-condition provenance, and the single selected contrast survives the registered metadata support and optimistic precision screens.

A pass authorizes **preparing a separate locked outcome design**. Outcome access remains closed.

That later design must specify the scientific question, variables, estimand, actual effect margin, patient-level aggregation, screen-to-outcome correspondence, technical nuisance handling, splits, reserved panels, multiplicity, missingness, evaluator, and access controls before outcomes are opened.

A pass does not establish causation, equivalence, organoid transfer, novelty, scientific discovery, policy improvement, or generalization beyond the selected conditions.

**Gate advanced:** screening-environment provenance within C2; necessary structural support toward C3; prospective design specification toward C4. Entire C3/C4 gates remain incomplete. C6, C8, C9, C10, and C13 are not satisfied by this result.

The 2026-10-29 GOAL amendment permits the specified estimated-cost evidence prospectively. It does not waive scientific gates, establish a policy comparison, or authorize rollouts. Scientific-discovery, prediction-improvement, and policy-improvement status fields remain unchanged.

## 11. Failure modes named before execution

| Failure mode | Required handling |
|---|---|
| Condition describes sequencing culture rather than CRISPR screening | Require the direct screen chain and assay-condition semantics; unresolved if contradicted or unsupported. |
| Screens predate condition records, or condition annotations were retrospectively overwritten | Report absent temporal validation. Contradictory evidence invalidates affected provenance; do not infer contemporaneous recording from IDs or Days. |
| Missing ModelConditionID or orphan condition | Uncovered; no onboarding or parent-condition imputation. |
| ModelID disagreement or conflicting duplicate keys | Quarantine affected linkage and report unresolved status. |
| Multiple screened conditions or environments | Apply unanimous model/component assignment; no favorable representative selection. |
| Formulation free-text variation or identifier aliases | Apply only fixed cosmetic normalization; unresolved conflicts/selected aliases require authoritative clarification. |
| ScreenType mistaken for culture format | Keep ScreenType as assay restriction; require ModelCondition.CellFormat. |
| Blank QC, drug, or engineering flags treated as false | Prohibited; use explicit parsing and unresolved statuses. |
| QC-passing sequences mistaken for verified screen-level or outcome-product inclusion | Report the available QC level; defer outcome correspondence to the separate lock. |
| Rare states merged, or failed primary pair replaced | Prohibited; retain exclusions and the original selected pair. |
| Environment nearly determined by lineage | Report association and apply common-support gates; pooled size cannot rescue failure. |
| Library, assay duration, or source confounded with environment | Report metadata diagnostics; no causal or technically adjusted interpretation follows. |
| Multiple SIDPs, models, screens, or sequences counted as independent patients | Reconstruct full linked components and count each retained component once. |
| Model-level outcomes may combine different screened environments | Do not inspect outcomes here; future design must establish compatible indexing and aggregation. |
| Gene.csv outcome summaries leak into selection | Exclude all Gene.csv data-row values. |
| Missing metadata concentrated in particular conditions or lineages | Report missingness and exclusions by lineage/source/type where known; covered-subset claims only. |

## 12. Required execution artifacts and review

A later authorized metadata execution must produce:

- `input_manifest_v1.json`: enforced hashes, SPEC hash, source descriptions, schema checks, parent lineage, and an explicit outcome-access declaration.
- `environment_links_v1.csv`: screen/sequence/condition/model linkage, eligibility states, normalized environment fields, and exclusion reasons.
- `components_v1.json`: reproducible component membership, model assignments, environment/lineage status, and exact C1 membership before and after overlap restriction.
- `confounding_v1.csv`: component-level contingency tables and declared diagnostics.
- `screen_v1.json`: fixed denominators, coverage numerators/rates, all stratum counts, deterministic C1 selection, overlap calculations, precision calculations, gate statuses, reason codes, and exactly one verdict.

Retain raw categorical strings alongside normalized metadata values where needed to audit transformations. Report overlapping exclusion reasons and a deterministic first-failure attrition table. Record all unresolved and out-of-scope screens; do not silently discard them.

The executable must enforce gates directly. Report text cannot substitute for implemented prerequisites.

Run locally within campaign allocations and resource limits, without network or outcome access. Ledger actual resources and generation/review calls under the amended cost-evidence rules; do not fabricate unavailable usage.

Require the campaign’s sol-high review, issue correction, and re-review standard before adopting the result. Any changed threshold, source restriction, environment definition, contrast-selection rule, or input version requires an explicit prospective amendment or new generation.

**Next step after a passing, reviewed result:** a separate locked outcome-design generation. **No outcome access is authorized by sgen012.**