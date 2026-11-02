**COST_BASIS: YES_WITH_NAMED_CONDITIONS.**  
**PGEN005: GO_WITH_CONDITIONS — feasibility screen first.**  
**SGEN011: C — an organoid identity and processing-independence discriminator.**

The user’s decisions reopen substantive work. They do not establish C9, authorize reuse of consumed C, or turn prior feasibility generations into policy cycles.

**A) Cost basis**

C9 requires improvement against the strongest fixed baseline, **end-to-end including overhead**. Its purpose is to prevent apparently cheap deployment from concealing expensive learning. An auditable, consistently applied replacement-cost estimate can serve that purpose under the user-authorized accounting amendment. It cannot be described as measured API expenditure. [GOAL.md](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/GOAL.md:50)

However, **the present $26.34 artifact is not yet a complete accounting witness**:

- Its 59 “priced” calls include **four receipts with `tokens: null`**, which the script converts to zero. One is a 600-second timeout with recorded tool activity; another failed after approximately 50 seconds with activity. Those zeros are unsupported.
- The separately flagged early call and two null-usage retries have retained initialization-error logs. They can receive zero hosted-token cost **if their pre-dispatch failure is verified and recorded**.
- The report therefore contains **55 usage-bearing calls**, rather than 59 calls with measured usage.
- Receipt totals aggregate an agent invocation. For example, one receipt contains 1,252,530 input tokens, exceeding a single request’s context capacity. Applying the long-context tier to that aggregate is a conservative convention, not exact request-level repricing.
- The current script also needs reservation-ID deduplication, validated event-counter semantics, and correct long-context cache-write pricing. Its “last usage record” fallback must not silently omit earlier turns. [host_cost_estimate.py](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/host_cost_estimate.py:37)

The official Standard schedule supports $2/$0.10/$10 per million input/cached-input/output tokens, with long-request multipliers of 2× input/cache and 1.5× output above 272,000 input tokens. Cache writes also require their applicable tier. Subscription usage has no long-context surcharge; consequently, this campaign’s API valuation is explicitly a **replacement-cost index**, separate from its $0 additional metered spend. [Official GPT-6.1 Sol documentation](https://developers.openai.com/api/docs/models/gpt-6.1-sol)

Lock these conditions as `cost_basis_v3`:

1. **Keep three separate fields:** `additional_metered_spend_usd`, `estimated_host_replacement_cost_usd`, and measured local resources. Freeze the price schedule dated 2026-10-29; retain its source bytes and hash.
2. **Reconcile every reservation:** completed, failed, retried, interrupted, and pending. Use reservation IDs and retained call identities, not filename matching alone. Recompute after this consultation and the latest review; the 60-call snapshot is already historical.
3. **Classify missing usage explicitly:** verified pre-dispatch zero; recovered usage; bounded unknown; or unresolved unknown. An existing receipt with null usage is not a priced call.
4. **For aggregate usage without request-level tiers**, retain a price interval. For the original snapshot’s 55 usage-bearing calls, all-short and all-long Standard valuations give **$14.8188448–$27.0891196**, before missing usage. The reported $26.34 lies within that interval.
5. **Certification uses learned-upper/fixed-lower treatment.** Unknown learned costs must not disappear; uncertain fixed costs must not inflate its denominator. Report additional learned-side multipliers **1, 1.5, and 2**, with 2 as the required robustness scenario. A multiplier is sensitivity analysis, **not proof that an unbounded missing call is bounded**.
6. **Resolve the two activity-bearing usage gaps** by recovering usage or establishing a genuine historical request-count/token bound from retained execution records and applicable limits. Future caps cannot retroactively bound them. If neither is possible, retain an unresolved cumulative host component for C9.
7. **Prospective invocation limits:** reserve at most **2,000,000 aggregate input tokens, 50,000 aggregate output tokens, 16 model requests, and 1,200 seconds**, with shorter phase limits taking precedence. These are admissible bounds only if the authorized interface enforces them across retries and in-flight requests. Otherwise, record them as declarations, not bounds, and stop dependent certification.
8. Include the entire comparison-relevant dependency chain: generation, extraction, summaries, replay, reviews, repairs, unstick calls, failed attempts, promotion tests, shared data production, and earlier histories actually consumed. No epoch reset or hypothetical deployment amortization.

**Text conflict:** GOAL/PLAN and handoff §11 currently reject a token-price proxy while material host expenditure remains unknown. The new user instruction authorizes replacing that billing requirement with estimated accounting. Append that amendment explicitly; preserve the old documents and rulings. The user has already authorized the change—another permission request is unnecessary. The practical margin, strongest-baseline requirement, cumulative overhead, and uncertainty requirements remain binding.

Thus: **the accounting convention is acceptable; the current implementation and incomplete receipts do not yet close its conditions. C9 remains UNMET.**

**B) Pgen005**

Use a new study, **`CL-RD-RAW-CPU-EST-v1`**, recombining pgen003’s identity-resolved raw route, pgen004d’s validated CPU meter, the retained reproduction machinery, and the verified acquisition safeguards. Record component lineage without inheriting scientific scores.

Pgen005 is a **necessary-condition feasibility generation**, with no policy optimization, B access, or claim of a completed cycle.

| SPEC field | Locked value |
|---|---|
| Population | Existing resolved universe: **251 lines / 250 patients / 810 count files**, KP3 excluded |
| Partition seed | Literal bytes represented by hex `2ea967015ccfbcf7` |
| Ordering | `SHA256(seed_bytes || UTF8(patient_id))`, patient-ID tie-break |
| Development | A0=50 patients; A1=20; A2=10; A3=10 |
| Reserved evaluation | B=160 patients, assigned round-robin to **16 panels of 10** |
| Patient grouping | Preserve PEO1/PEO4 together; additional relatedness requires a metadata-only revision before outcomes |
| Primary resource | **Total scoped local CPU seconds**, including shared production and all learning overhead |
| Other resources | Host replacement-cost ledger under `cost_basis_v3`; wall, memory, transfer, attempts, and evaluator calls |
| Deployment count | **One actual 16-panel campaign** |

This is an archival cell-line engineering task. It does not supply organoid validation.

For each line, obtain independently processed gene scores \(x_{ig}\). Construct the reference from A0 only: patient-equal mean scores, then average-tie ranks \(r_{0g}\). Define

\[
D_{ig}=\frac{|\operatorname{rank}_{207}(x_i)_g-r_{0g}|}{206}.
\]

Average line-level displacement vectors equally within patient. Predict the fixed **207-coordinate** vector; score patient-equal, coordinate-equal MSE, with predictions clipped to \([0,1]\) and \(q=1-\mathrm{MSE}\).

Freeze **17 predictor configurations**:

- One A0 patient-mean predictor.
- Six tissue shrinkage predictors, shrinkage counts `{1,5,10,20,50,∞}`.
- Ridge predictors with λ `{0.01,0.1,1,10,100}`, each with and without lability.

For ridge, use A0-derived gene-mean displacement, signed reference strength, absolute reference strength, tissue indicators, and their tissue interactions; add measured lability and its tissue interactions only in the lability version. Standardize continuous features within training folds; unpenalized intercept; objective `mean squared error + λ × squared coefficient norm`. Missing tissue is `UNKNOWN`; conflicting within-patient tissue labels are `MIXED`. Remove all lability terms in the matched ablation.

Use five patient-grouped A0 folds, assigned round-robin in the frozen patient order. Rebuild all outcome-derived references and features inside each training fold. Cache fitted artifacts; ordinary reuse and vectorized prediction are available to every arm.

Let \(E_0\) be the mean predictor’s A1 MSE and \(E_*\) the lowest A1 MSE among the 17 configurations. Require \(E_*\le0.90E_0\), then freeze

\[
e_\tau=\min(0.90E_0,1.05E_*),\qquad \tau=1-e_\tau.
\]

Failure is `FAILS-SCREEN`; do not move the threshold.

The prospective deterministic policy space is:

\[
s_a=(1-\alpha)E_a+\alpha E_a(t)
       +\beta\,c_a/\max_b c_b,
\]

with \(\alpha\in\{0,.25,.5,.75,1\}\), \(\beta\in\{0,.01,.1,1\}\), plus a pure-cost ordering. Choose the unattempted action with smallest score; break ties by immutable configuration ID. Here:

- \(E_a\): development MSE;
- \(E_a(t)\): panel-tissue-weighted development MSE, tissue estimates shrunk toward global MSE with **five patient-equivalents**;
- \(c_a\): measured development prediction-and-scoring CPU per patient, floored at \(10^{-6}\) seconds.

Stop immediately on valid attainment of τ. Failed actions consume resources and remain in history. No hosted calls occur inside a rollout.

The initial challenger templates are pure-cost ordering, \((\alpha,\beta)=(0,0)\), and \((1,.01)\). Their trained statistics and executable bytes must be frozen after admissible development evidence exists.

Fixed comparators are:

1. Original fixed exploration: mean, tissue configurations in listed order, then no-lability ridge and lability ridge in ascending λ.
2. Fixed random order: sort configurations by `SHA256(UTF8("2026102905") || panel_id || config_id)`.
3. Strong static: start with the A-selected best predictor, then remaining predictors by A1 MSE, configuration-ID ties.

The strong static arm receives cached fits, efficient batching, ordinary stopping, and the same useful information. No forced calls or redundant fits.

Pgen005’s screens run **in this order**:

1. **Accounting:** implement and independently review `cost_basis_v3`.
2. **Identity/ancestry:** pin complete manifests and verify separation from C, exposed Broad models, and related patients.
3. **Schema:** inspect at most **four A0 members / 16 MiB compressed**. Require authoritative guide mapping, endpoint/plasmid roles, matched controls, lane/replicate/time interpretation, integer counts, and at least two usable guides for every fixed coordinate. Missing controls produce `BLOCKED-DATA`.
4. **Independent processing:** sum documented lanes; independently normalize samples; retain uniquely mapped guides with plasmid CPM≥1; compute plasmid-relative log2 fold changes with pseudocount 0.5; median guides, median replicates, then patient aggregation. No jointly fitted correction or B-informed filtering.
5. **Throughput, usefulness, shortcut, and precision:** A0/A1 only. Measure the cheapest competent static route first.

For shared CPU \(S\), learned overhead \(H\), and deployment CPU \(L,F\), the headroom requirement is

\[
S+H+L\le .8(S+F).
\]

The direct static shortcut is the principal threat. Its cached prediction cost may be too small to repay learning overhead. A failed headroom screen closes **this tested specification**, without consuming B.

Retain the prior planning requirements: **16 independent panels, 35% total-savings planning alternative, 20% margin, ≥80% power, simultaneous protection across three comparators**. Use A-only measured variability; label extrapolation assumptions. No precision certification from headcount or repeated seeds alone.

Reserve before screening:

- **6 host calls**: this generation consultation plus at most five Sol-high review rounds.
- **17 aggregate configuration artifacts**, retaining every fold’s fits, predictions, failures, and costs.
- **12,000 CPU-s**, **12 h aggregate wall**, **3 GiB total new raw-route transfer including retries**, **8 GiB disk**, **2 GiB RSS/job**, ≤2 heavy jobs, ≤600 s/exploratory chunk.
- The 3 GiB transfer envelope is shared with later acquisition, not renewed per generation.

Passing requires Sol-high ≥90, zero unresolved high/critical findings, and G2/Lock1 before optimization. Failure or exhausted review allowance yields a scoped failure or `PENDING`.

The subsequent execution contract must retain:

- **E0:** eight A1 panels assigned round-robin, three actions each: **24 real nodes**.
- Replay fractions `{0,.25,.5,.75,1}`, equal weights; common support ≥8 episodes and ≥50% at every positive-weight fraction. Preserve exact-context checks and unsupported transitions.
- Each fresh cycle: two five-patient panels from A2, then A3; at most three actions per rollout. Testing all three challengers plus incumbent and fixed exploration uses at most **30 nodes**, within the existing **36-node cycle cap**.
- Promotion only if both fresh panels attain τ, pooled challenger CPU is ≤95% of incumbent CPU, and neither panel exceeds incumbent CPU by more than 5%. Otherwise retain incumbent. Multiple qualifying challengers order by pooled CPU, then listed challenger order.
- Final B: four policies ×16 panels ×four-action ceilings = **256 maximum nodes**, zero hosted rollout calls.

Final savings use the cumulative allocation above, **10,000 paired whole-panel bootstrap resamples, seed `2026102804`**, holding recorded shared/learning costs fixed. Require Bonferroni one-sided \(0.05/3\) lower savings bounds ≥20% against every comparator. Any unresolved nonattainment prevents the primary C9 claim; retain censoring.

This endpoint supports a **total-local-CPU efficiency claim under the amended host accounting convention**. It does not establish dollar savings.

**C13 closes after the first genuine fresh policy cycle and substantive report. C8 closes only after two such cycles and the frozen B comparison.** Metadata screens, E0 alone, replay alone, and passing software reviews close neither.

**C) Sgen011**

**Select C, narrowed to an organoid identity and processing-independence screen.**

A is a different cell-line association question. Growth pattern or onboarded medium across different models does not identify an environmental intervention or establish an organoid transfer result. B is premature: its identities and independence remain unestablished.

Lock **`ORG-FRESH-IDENTITY-01`**:

- **Question:** Does the supplied 26Q3 organoid inventory contain a sufficiently identified, previously unexposed patient cohort supporting the fixed lability/displacement question through an admissible processing route?
- **Population:** Exactly the **108 screened organoid models**: 11 established and 97 not established. The latter correspond to 91 DepMap PatientIDs, not 97 established independent patients. Build relatedness components using **all 2,554 Model.csv rows**, preserving sgen010’s conservative propagation.
- **Inputs:** Pinned sgen010 metadata, established-pool assignments, authoritative Passports/primary-source identity records, all 142 C patients, exposed Broad identities, policy-patient manifests, exposure records, and processing documentation/code.
- **Access:** Identity, assay, provenance, annotation, and processing metadata only. No dependency values, outcome matrix decoding, or C re-access.

Use the existing unanimous strong-ID rule. Names remain candidate evidence; conflicts and unresolved identities remain quarantined. A new identity resource may supply strong edges, but absence from a crosswalk never proves disjointness.

Produce, for every organoid:

1. Source-linked patient assignment and conservative component.
2. C/Broad/policy/exposure overlap disposition.
3. Evidence that the recorded culture metadata describe the screened culture.
4. Documented availability of the fixed 207 coordinates.
5. Processing dependency graph: which outcomes influenced normalization, pretrained parameters, correction, selection, or reference construction.

**Decision rule:**

- `METADATA_POSITIVE`: ≥**30 conservatively grouped, confirmed, unexposed organoid patients**, a documented route covering all 207 coordinates, and processing independence established or a documented development-only/raw reconstruction route.
- `IDENTITY_INSUFFICIENT`: fewer than 30 qualifying patients.
- `PROCESSING_INELIGIBLE`: outcome-informed coupling cannot be removed under an admissible route.
- `UNRESOLVED`: required evidence remains inaccessible or ambiguous.

Thirty is this screen’s operational floor, **not a power certificate**. Do not lower it after inspecting counts or close the entire scientific family on its failure.

A positive result advances **C3 and preparation for C4**. It does not close C6. Metadata alone cannot establish power for a correlation across 207 gene summaries; using \(1/\sqrt{n_{\text{patients}}-3}\) would misidentify the statistic’s sampling structure.

The successor outcome generation must separately freeze patient-equal aggregation, a contamination-free reference, the strongest justified adjustment/baseline, δ=0.20, patient-cluster uncertainty, multiplicity, and estimator-validity checks. Keep inference conditional on the six measured Broad models unless a justified joint uncertainty procedure supports broader claims.

Reserve **6 host calls**, **120 requests including failures/retries**, **32 MiB transfer**, **3,600 CPU-s**, **8 h wall**, **2 GiB RSS/job**, and ≤600 s/chunk. At most one retry per resource. Retain row-level dispositions and all receipts.

A new cohort result would provide new evidence. It would **not repair or replace** the archived 144-group interval for 142 patients.

**D) Sequence and final terminal slot**

| Order | Generation | Deliverable |
|---|---|---|
| 1 | **pgen005** | Reconciled accounting → schema → independent processing → A-only shortcut/headroom/precision decision |
| 2 | **sgen011** | Organism-model identity, exposure, and processing-independence discriminator above |
| 3 | **pgen006**, conditional on pgen005 | Reviewed Lock1, real E0, ≥3 executable challengers, faithful replay, first fresh cycle, retention/promotion decision, substantive report |

If pgen005 fails, generation three becomes **sgen012** only when sgen011 supports a separately reviewed scientific outcome lock; otherwise execute the next bounded identity/processing discriminator identified by its retained failure. Do not manufacture a nominal policy cycle. **Pgen007 or a later generation remains necessary for cycle two and final B evaluation.**

Preserve the final protected terminal slot until a candidate package contains:

- A qualifying novel scientific finding/refutation/bound with valid patient-level external support.
- Two real, reviewed policy cycles and the frozen reserved-panel comparison.
- The preregistered ≥20% lower-bound result against the strongest fixed strategies, including cumulative overhead and the resolved amended accounting basis.
- Frozen contracts, complete atlas/exclusions, adversarial checks, reconciled resources and failures, manuscript, and clean reproduction of scientific and policy decisions without stochastic LLM reruns.
- A documentary C1–C13 crosswalk and Sol-high package review ≥90 with zero unresolved high/critical findings.

Current disposition remains **ACTIVE_NOT_TERMINAL**. The latest supported MET gates are C1/C2/C5/C7; C8/C9/C13 remain UNMET. This consultation supplies prospective designs and conditions, not a terminal certification.