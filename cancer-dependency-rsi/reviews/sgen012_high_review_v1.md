The reported arithmetic reproduces independently, but the implementation does not complete the frozen SPEC audit. **The quantitative rejection is robust; `A_STILL_UNRESOLVED` is the more faithful formal audit label until the missing audit basis is resolved.** No critical issues found.

This review was read-only. I did not read Gene.csv or anything in ~/Downloads.

**Independent recomputation**

All six SHA-256 locks match. The established population is 1,106 models, 1,069 SIDP patients, and 1,068 linked components. The cell-line denominator is correctly **1,095 models / 1,057 components**, with coverage thresholds **986 / 952**.

| Quantity | Recomputed result |
|---|---:|
| Pinned cell-line screens | 1,337 |
| Joined sequence records | 2,976 |
| Distinct joined SequenceIDs | 2,976 |
| Distinct linked conditions | 1,310 |
| Eligible, environment-assigned sequences under implemented rules | 1,976 |
| Unresolved formulation | 688 |
| Missing/unknown CellFormat | 230 |
| Unknown flag encoding | 52 |
| Explicitly disqualified, as classified by code | 24 |
| Unknown ScreenType, as classified by code | 6 |
| Assigned models before component exclusions | 727 |
| Components before component exclusions | 714 |
| Components spanning multiple retained environments | 8 |
| Models removed with those components | 16 |
| Final models / components | **711 / 706** |
| Assignable environment strata | 130 |

There are no duplicate ModelIDs, ModelConditionIDs, SequenceIDs, or ScreenIDs in their respective input tables. All 2,976 joined records agree across screen-map ModelID, sequence ModelID, condition ModelID, and condition model_id.

All joined conditions have single-record parent chains: no joined parent histories, cycles, broken chains, or nonempty treatment fields. Two broken parent chains exist elsewhere in ModelCondition.csv; they do not affect this denominator.

Six models have multiple eligible environments; four also have unresolved records. The remaining model exclusions partition into 363 models with unresolved records, two with multiple known environments only, and three with no eligible records.

The selected contrast and gates reproduce:

| Gate or statistic | Independent result |
|---|---|
| Model coverage | 711/1,095 = **64.93%**; fails |
| Component coverage | 706/1,057 = **66.79%**; fails |
| Arm A | Adherent, RPMI + 10% FBS: **183 components / 185 models** |
| Arm B | Adherent, DMEM + 10% FBS: **86 components / 86 models** |
| Selected coverage | 269/1,057 components = **25.45%**; 271/1,095 models = **24.75%** |
| Arm-size gate | Fails: B < 100 |
| Shared lineages with ≥20 components per arm | **Zero**; fails |
| Fisher-z benchmark B | **0.3717118265** |
| Two-arm MDR | **0.3554881215**; fails 0.146 threshold |
| All-stratum Cramer’s V | **0.5755393767** |
| Selected-contrast Cramer’s V | **0.5090453762** |

Ranking by component count and the implemented UTF-8 tie-break are correct. Selection precedes positivity and precision calculations. Lung is 38/2 across A/B, while CNS/Brain is 8/22; neither satisfies positivity.

For Cramer’s V, the all-stratum table is 130×28, N=706, χ²=6314.203134. The selected table is 2×25, N=269, χ²=69.705215. The reported 0.5755 is correct.

**High issues**

1. **The decision logic cannot produce `A_STILL_UNRESOLVED`.** `evaluable=True` is hardcoded, and the verdict expression has only pass/reject branches. Even changing `evaluable` to false would produce `A_REJECTED`. This bypasses the SPEC’s required precedence for unresolved global semantics or audit basis. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:292)

2. **Blank treatment names are treated as documented absence without establishing that convention.** `chain_drug_free()` accepts empty drug-name fields. The supplied README describes those fields but does not establish “blank means none.” `DrugTreated=False` does not independently document absence of historical pretreatment. This affects the eligibility basis for every retained assignment, although it cannot rescue the failed quantitative gates. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:136), [SPEC requirement](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen012/SPEC.md:38)

3. **The SPEC’s precision gate is impossible within its frozen population.** Even allocating all 1,057 components optimally, 528/529, gives minimum MDR **0.1711347103**, above 0.146. Passing requires at least **1,458 components**, balanced 729/729. The formula is implemented correctly; the specification guarantees precision failure. This is defensible as an intentional feasibility rejection, but the specification should disclose that no metadata repair can produce a pass. [SPEC](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen012/SPEC.md:71)

**Medium issues**

4. **Lead deviation: components are reconstructed despite “do not reconstruct.”** The code constructs a new DSU graph and checks aggregate counts. Equal totals do not establish preserved component membership or identifiers. Neither inherited JSON supplies an explicit frozen model-to-component mapping, so the SPEC also lacks the artifact needed to satisfy its preservation instruction literally. My independent graph calculation finds the same partition using the available broader graph; no current numerical partition error was demonstrated. That does not remove the fidelity deviation. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:95), [SPEC](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen012/SPEC.md:14)

5. **Unknown flags block models even when they cannot change environment assignment.** The SPEC blocks unresolved records that *could change* assignment; the code blocks every model with any unresolved record. Twenty excluded models have unknown-flag sequences whose fully known environment equals their eligible sequences’ unique environment. Without imputing favorable flags, allowing those assignments yields **729 models / 724 components**, nine excluded multi-environment components, arms **190/86**, and MDR **0.353563**. Positivity remains zero and every currently failed gate still fails. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:219), [SPEC](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen012/SPEC.md:47)

6. **Lead deviation: DataSource consistency is never checked.** Only nonmissingness is tested. Independently, the joined library/source combinations are consistent with the available provenance: Avana/BROAD 2,000; Humagne-CD/BROAD 52; KY/SANGER 904; Brunello/OTHER 13; TKOv3/OTHER 7. Thus no observed mismatch changes these results, but the mandatory consistency check and documented source crosswalk are absent. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:210)

7. **ScreenType scope is asserted rather than demonstrably inherited.** screen_v7.json defines the integrated screened population but supplies no explicit ScreenType allowlist. The lead introduces eight codes without recording the derivation. Interpreting inherited scope as all pinned integrated screens is defensible; treating it as 2DS-only is another possible reading that should have been settled explicitly. Independently restricting to 2DS leaves final assignments, arms, and gates unchanged. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:32), [SPEC](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen012/SPEC.md:42)

8. **The required audit is not published.** The JSON omits join cardinalities, model/component exclusion membership, complete sequence/screen/replicate trails, preserved raw environment values, and the full ranked strata. It publishes ten of 130 strata. These omissions prevent verification from the delivered report alone. [Report construction](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:299)

9. **The harmonization mapping itself is missing.** Only its size, 270, is published. Independently, all 270 `(CellFormat, GrowthMedia)` keys map uniquely; none is ambiguous, and **zero joined eligible sequences require a fill**. The mapping is constructed before counting, but the required frozen crosswalk is not delivered. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:140)

10. **The confounding report is incomplete.** The all-stratum environment-by-lineage component table is absent, as is selected-contrast Cramer’s V, independently **0.509045**. The selected arm lineage dictionaries do permit reconstruction of the selected table. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:320)

**Low issues**

11. **The condition identity test allows an undocumented alias bypass.** Matching model_id can override a conflicting canonical ModelID without an established alias mapping. No actual disagreement occurs in these inputs. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:203)

12. **Parent traversal checks structure and drug names, but not parent identity or provenance consistency.** The SPEC requires all three. No joined record has a parent, so this is an unexercised implementation gap. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:119)

13. **Treatment exposure indicators are ignored.** PrescreenTreatmentDrugDays, AnchorDrugConcentration, and AnchorDaysWithDrug cannot trigger exclusion independently of drug names. They are all blank in the joined records, so this produces no current difference. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:136)

14. **Six definitively engineered sequences are classified as unresolved ScreenType.** ScreenType is checked before explicit disqualification. All six 2DR records have `IsEngineered=True`. Checking known disqualification first gives **30 explicitly disqualified / zero unresolved solely from ScreenType**, with identical retained counts. [Code](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/sgen012_screen.py:191)

15. **Required context distributions are omitted.** Across retained eligible sequences, SerumFreeMedia is False 1,418 / True 4; PlateCoating is None 1,422; PassageNumber is blank 1,420 / 10+ 2; Morphology is blank 1,422. All retained sequences are BROAD. None of those overall context distributions is published.

16. **Selected-arm coverage is not explicitly reported.** Arm counts are present, but the required selected coverage fractions are absent: **24.75% of models and 25.45% of components**. [SPEC](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/generations/sgen012/SPEC.md:65)

17. **The README used to justify evaluability is unpinned and not verified by the program.** The implementation embeds its interpretation without reading or hashing that evidentiary input. This weakens reproducibility of the provenance decision.

**Environment semantics and verdict**

Literal use of FormulationID text is **defensible for this pinned snapshot**. Within CellFormat, explicit normalized descriptions and MF codes are one-to-one in both directions. Recomputing with GrowthMedia codes preserves every retained assignment, component count, selected arm, positivity result, MDR, and Cramer’s V. Lower-ranked ties reorder because textual and code identifiers sort differently. The field-name mismatch therefore does **not** demonstrate environment misoperationalization here; the missing published crosswalk and consistency audit remain defects.

The README provides meaningful screening-assay evidence: ModelCondition describes conditions under which models were assayed, and the Achilles Pre-Chronos mapping connects sequences to screens and conditions. “Pre-Chronos” denotes pipeline position; it does not make the condition annotation sequencing-only. I would **not** prefer `A_STILL_UNRESOLVED` solely because of timing or ScreenType.

I prefer that label for the **unfinished frozen audit**: component preservation cannot be verified as specified from the inherited artifacts, the drug-null convention is unestablished, required checks are omitted, and evaluability is hardcoded. Conditional on resolving those requirements, **`A_REJECTED` is quantitatively secure**. Ordinary record missingness alone would not justify an unresolved global label.

SGEN012_SCORE: 68