DESIGN_CLASS: ONE_SAMPLE_TRANSPORT
ESTIMAND: Across independent patient components, partial Spearman correlation between source measured paired-format lability and one prespecified CRISPR dependency endpoint, adjusting for source baseline and lineage.
NEXT_GENERATION: sgen013 — metadata screen.
POLICY_TASK_INSTANTIABLE: NO — component-level predictor coverage and a concrete actionable endpoint remain unverified.

SPEC_ID: sgen013
TITLE: Outcome-blind feasibility of component-level lability transport to CRISPR dependency
STATUS: METADATA SCREEN ONLY; no authorization to inspect CRISPR outcomes.

PURPOSE
Determine whether a baseline-adjusted external association and a budgeted confirmation-priority task can be instantiated.
ONE_SAMPLE_TRANSPORT is the candidate design; its feasibility is not established by the nominal component count.
The scientific question concerns measured paired-format lability as an incremental predictor of genetic dependency.
Generic cell-line-to-organoid prediction supplies no novelty credit.

POPULATION AND UNIT
Start with the 729 established models representing 724 patient components with eligible environment-linked screens.
The 1,095-model/1,057-component established pool is a coverage ceiling, not the current analyzable cohort.
Use one observational unit per patient component.
Select one eligible model and screen per component by ascending canonical ModelID, then ScreenID.
Apply this ordering after metadata eligibility and before outcome access.
Repeated screens, models, perturbations, or source measurements must not inflate independent n.
Do not extrapolate organoid measurements to unrelated cell lines through lineage membership.

PERMITTED INPUTS
Use metadata manifests, dictionaries, stable identifiers, provenance records, and existing coverage indicators.
Do not open, preview, summarize, or derive missingness from outcome-bearing files.
Leave the CRISPR files in ~/Downloads unread; acquisition belongs to a subsequent locked design.
Do not inspect predictor values to choose a cohort, endpoint, sign, transformation, or policy.

VARIABLES TO REGISTER
c: patient-component identifier, with model-to-component provenance.
m,s: canonical model and eligible screen identifiers.
t: one biologically justified CRISPR endpoint identifier.
L: existing measured paired-format lability for component c and endpoint t.
B: the corresponding source baseline, retaining its original definition.
Z: documented lineage categories.
F,M: CellFormat and formulation-family metadata, retained as descriptive context.
Y: the future CRISPR dependency outcome for t, with score direction documented from its dictionary.
A: metadata establishing that each selected component can receive the proposed confirmation assay.
C: estimated confirmation cost; use one normalized cost unit per assay unless documented estimates exist.

IDENTITY AND SCIENTIFIC-COMPATIBILITY GATE
Require a documented component-level mapping for L and B and a defensible bridge to endpoint t.
A gene-level or compound-level lability value copied across models does not establish component-level lability.
Reject ambiguous biological mappings, unsupported drug-to-gene substitutions, and newly fitted lability proxies.
The source definition of L must genuinely measure paired-format behavior.
Do not construct L from the six multi-environment established models.
Register source reuse explicitly: Lock-S is spent and does not provide an independent new discovery.
The new claim must concern the target CRISPR endpoint and incremental information beyond B.

ENDPOINT SELECTION RULE
Enumerate candidate endpoints using metadata and existing source provenance only.
Retain candidates satisfying the identity, compatibility, coverage, and policy-action requirements.
Choose the candidate with the largest eligible independent component count.
Break ties by ascending canonical endpoint identifier.
If no candidate qualifies, return FAIL; do not substitute an unrelated endpoint.

CANDIDATE ESTIMAND
Rank L, B, and Y across the selected independent components using midranks.
Residualize rank(L) and rank(Y) against an intercept, rank(B), and fixed lineage indicators.
The estimand is the Pearson correlation of those residuals: the specified partial Spearman correlation.
It describes the observed eligible population and its environment mixture.
It does not identify a media effect, a format effect, or a within-model environmental response.
CRISPR dependency alone does not establish rank displacement; that would require a separately justified reference.

PRECISION RULE
Require the prespecified one-sample Fisher-z MDR to be <=0.146.
Use the authorized calculation and account for covariate degrees of freedom and relevant dependence.
The supplied MDR≈0.104 at 724 components establishes nominal feasibility only.
Recalculate prospectively for the metadata-qualified cohort.
Shared source sampling or other dependence must be addressed; patient-component counting alone is insufficient.
Do not borrow the 1,057-component ceiling or the organoid observation count.
Do not claim that an interaction or subgroup analysis escapes the failed two-arm gate.

POLICY FEASIBILITY RULE
The candidate action is allocation of confirmation assays among eligible patient components.
Set K=ceiling(0.10*n) confirmation slots and an estimated budget of K normalized cost units.
Require documented assay availability and usable source predictors for every candidate action.
Require an outcome-blind scientific rationale fixing the direction in which L prioritizes confirmation.
If direction cannot be justified, the policy gate fails; do not choose it from CRISPR results.
The later lock must specify the exact priority score, tie rule, equal-budget comparator, and outcome metric.
Estimated costs are permitted; monetary ROI and causal benefit are not established by this task.
Policy status becomes instantiated only when the selected endpoint, action set, budget, and score are populated.

SCREEN DECISION
PASS only if one endpoint satisfies identity, compatibility, independent-n precision, and policy feasibility.
Report the exact selected endpoint, cohort count, exclusions, provenance, estimated costs, and MDR calculation.
Otherwise report FAIL with the failed requirement and the resource needed to resolve it.
A metadata PASS authorizes preparation of a separate outcome-design lock, not outcome inspection.

SUBSEQUENT LOCK PREREQUISITES
Freeze endpoint, cohort, mappings, transformations, covariates, exclusions, missingness handling, and inference.
Freeze dependence treatment, effect-direction hypothesis, multiplicity, policy evaluation, and success thresholds.
Do not import Lock-S’s delta=0.20 as a new success criterion without an explicit scientific justification.
Register exact acquisition provenance, release identifiers, file hashes, code version, and execution command.
Hash-pin acquired outcome files before parsing their values.
Run one locked execution; retain its complete output, including failures.
No previews, endpoint swaps, threshold revisions, or selective reruns after outcome access.
Any material correction requires a versioned amendment and explicit treatment of prior outcome exposure.

GATES ADVANCED
Preserve the recorded MET status of C1,C2,C5,C7.
Attach qualifying metadata evidence to C3,C4,C6,C10,C11,C12 without automatic promotion.
Advance C9 only if its amended criterion is satisfied by the populated feasibility-selected policy task.
C8 and C13 remain UNMET unless their original acceptance criteria are independently satisfied.
Metadata feasibility supplies no outcome, transport-success, or policy-performance evidence.

FAILURE AND TERMINAL POSTURE
Principal failures are absent component-level L/B, invalid endpoint mapping, insufficient independent n,
unhandled source dependence, nonactionable confirmation choices, or novelty limited to prior art.
Environment confounding remains a limitation; environment comparisons are not a fallback design.
If FAIL cannot be repaired with existing metadata, stop outcome work on this pool.
A useful external resource would supply independently measured paired-format L/B on matched components,
a defensible CRISPR endpoint bridge, and sufficient independent coverage for the precision gate.
Record the campaign as scientifically unresolved with this branch infeasible; do not present a negative result.
END_SPEC