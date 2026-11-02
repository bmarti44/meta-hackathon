**Adjudication: YES_WITH_NAMED_CONDITIONS. The proposed zero-call rollout is admissible in principle; the present evidence still gives `NO_GO` for acquisition and policy optimization.**

Zero host calls during rollout removes deployment inference expenditure and the earlier Phase-5 call-count conflict. It does **not** remove the generation, review, replay and promotion costs required to produce the frozen policy.

This is a read-only determination and prospective design. No experiments, ledger amendments or independent Sol-high reviews were executed in this consultation.

**What §11 and C9 permit**

[Handoff §11](/Users/bmarti44/github/bufferright/research/cancer_rsi_handoff.txt:295) explicitly permits an alternative primary resource endpoint. It also requires charging policy rewriting, replay, failures and promotion trials to the improving system, and reporting end-to-end and deployment-only performance separately.

| Proposed variant | Determination |
|---|---|
| Start the epoch at frozen-policy rollout; omit generation from its primary result | Valid deployment-only experiment. **Cannot satisfy end-to-end C9.** |
| Charge both arms an identical declared allowance or maximum number of generation/review calls | **Insufficient.** Equal ceilings do not establish equal realized expenditure. |
| Count generation TOK descriptively and use measured local CPU as primary | **Insufficient while material host expenditure remains unknown and unmatched.** |
| Measure comparison-relevant host expenditure, include all learning overhead, and prospectively justify CPU as primary | **Potentially admissible.** CPU savings remain a resource-specific claim, not demonstrated dollar savings. |
| Obtain an authoritative witness establishing genuinely identical host charges across complete counterfactual systems, including learning and failures | **Potentially admissible**, with useful corresponding search opportunities for fixed baselines. Artificially adding learned overhead to baseline accounts is insufficient. |

The **exact missing accounting witness** remains the one required by [the prior adjudication](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/reviews/pgen004_design_xhigh_v1.md): measured host expenditure, or authoritative strict matching covering generation, review, failures, retries, routing, caching and any overages. It must cover the entire invocation, not merely successful responses. Historical maximum-call imputation remains rejected.

There is a second, narrower measurement requirement. [`cpu_meter.py`](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/src/cpu_meter.py:1) honestly measures **waited-child CPU**. Before calling the endpoint *total local CPU*, the new wrapper must demonstrate scoped accounting for the controller, workers, descendants, monitoring, replay and failed jobs, without omission or double counting. Concurrent unrelated children must not contaminate measurements. Preserve LOCK2-pinned `budget.py`; implement this prospectively outside its frozen bytes.

A qualifying contract therefore needs all of these conditions:

1. **A new study and initial contract**, frozen before policy optimization. Deterministic scientific action code replaces any online hosted generator; changing only the policy module does not eliminate calls made by a remaining LLM generator.
2. **Complete end-to-end accounting**, including both cycles and this generation/review dependency chain. Epoch boundaries cannot reset learning costs.
3. **The host-cost witness above**, with enforced whole-invocation bounds where applicable. For uncertain costs, certification uses learned-cost upper bounds and fixed-cost lower bounds.
4. **Equal information and useful resource opportunities** for competent fixed strategies. No forced calls, redundant fits or artificial baseline padding.
5. **A CPU endpoint justified before optimization**, with the same 20% practical margin and a prespecified uncertainty rule. Other material resources remain measured or strictly matched.
6. **Sol-high ≥90 with zero unresolved high/critical findings**, followed by actual qualifying experiments.

This preserves the alternative-endpoint provision; it does not approve the current proposal or repair pgen002.

**The main feasibility risk is now shared processing cost**

Let \(S\) be shared CPU production cost, \(H\) learned-system overhead, and \(L,F\) learned and strongest-fixed deployment CPU over **one actual reserved campaign**. Twenty-percent end-to-end savings requires

\[
S+H+L\le0.8(S+F),
\qquad
F\ge0.25S+1.25(H+L).
\]

Raw normalization, reference construction and shared pilot production belong in \(S\), even if performed before rollout. All learning and review dependencies belong in the end-to-end accounting.

This task has inexpensive mean, shrinkage and ridge predictors. Consequently, ≥20% CPU savings is **unwitnessed and presently doubtful**: shared processing may dominate the small amount of scientific search that a competent static strategy needs. Avoiding deliberately wasteful branches would not establish improvement against the strongest fixed baseline.

The next generations should test that inequality before attempting a ceremonial policy cycle.

**Common prospective rules**

Use new immutable SPECs and ledger entries; retain every rejected design and unsuccessful attempt. Record component parents separately from scientific-evidence parents. Cross-study components need new compatible artifacts; their old scores cannot transfer.

The ledger currently reserves **812/1,200 evaluated nodes and 33/400 model calls**, leaving 388 nodes and 367 calls. Phase 2 has six calls remaining; one protected terminal slot remains. This consultation has an outstanding reservation, so its caller must reconcile the receipt before dispatching successors. These balances supersede stale fields in `status.json`.

The following are **maximum reservations**, not consumption forecasts:

| Generation | Host calls | Local CPU ceiling | New transfer ceiling |
|---|---:|---:|---:|
| G-A / `pgen004d` | 5 | 18,000 CPU-s | Within a **shared 3 GiB W1 acquisition reservation** |
| G-B / `sgen006` | 4 | 4,200 CPU-s | 32 MiB screen; conditional 1 GiB battery |
| G-C / `pgen005d` | 6, including protected terminal determination | 36,000 CPU-s | Remainder of the same W1 3 GiB reservation |

Reserve battery resources before screening; release them on failure. Count failed transfers and retries. Preserve the existing $0 additional metered-API cap, memory and concurrency limits, ten-minute exploratory-job limit, phase ceilings and eight-hour first-pilot ceiling. Review failure beyond a reserved tranche means `PENDING`, not an automatic budget increase.

**G-A — `pgen004d`: deterministic CPU-policy feasibility, then cycle one**

**Parents:** W1 identities/raw acquisition route + W2 honest measurement + W3 reproduction + W5 fail-closed acquisition. W4 supplies fixed environmental covariates and scientific limitations; its archived C result supplies no policy reward.

**SPEC skeleton.** New study `CL-RD-RAW-CPU-v1`; fixed 207-coordinate displacement-prediction task, deterministic action executor, frozen evaluator, preprocessing and legal action library. Zero hosted calls during pilot/replay/fresh rollout execution. Sol-xhigh writes policy challengers between epochs; their calls and Sol-high reviews remain charged learning overhead.

Preserve the prior metadata partition, subject to ancestry verification:

| Partition | Patients | Lines | Files | Listed member payload bytes |
|---|---:|---:|---:|---:|
| A0: reference/fitting | 50 | 51 | 168 | 424,971,538 |
| A1: feasibility/pilot | 20 | 20 | 52 | 132,613,289 |
| A2: cycle-one fresh rollouts | 10 | 10 | 27 | 68,882,593 |
| A3: cycle-two fresh rollouts | 10 | 10 | 27 | 68,876,661 |
| B: final policy evaluation | 160 | 160 | 536 | 1,358,834,183 |

Freeze the literal seed bytes `2ea967015ccfbcf7`, ordering patients by `SHA256(seed_bytes || UTF8(patient_id))`, with patient-ID tie breaking. Assign B round-robin into 16 ten-patient panels. Preserve PEO1/PEO4 together. Additional relatedness invalidates these proposed counts and requires a metadata-only revision before outcomes.

**Cheapest screen, in order:**

1. **Accounting and measurement witness.** No raw acquisition until this passes.
2. **Schema witness:** at most four A0 members, ≤16 MiB compressed, covering documented layouts. Require authoritative guide→gene mapping, endpoint/plasmid roles, matched library/batch controls, replicate/lane/time interpretation, integer counts and sufficient guides for all fixed coordinates. No separately named plasmid member has yet been witnessed. Missing controls means `BLOCKED-DATA`.
3. **Independent processing and throughput:** sum documented lanes within replicate; independently normalize samples; retain uniquely mapped guides with plasmid CPM ≥1; compute plasmid-relative LFC with pseudocount 0.5; aggregate guides, replicates and patients as frozen in the prior design. No cross-line fitted normalization or B-informed filtering.
4. **A-only shortcut, headroom and precision test.**

For patient \(i\), use patient-equal, coordinate-equal MSE on

\[
D_{ig}=|\operatorname{rank}_{207}(x_i)_g-r_{0g}|/206,
\qquad q=1-\mathrm{MSE},
\]

with average ties and line-level displacement averaged within related patients. Build \(r_0\) from A0 alone; rebuild references inside training folds.

Retain the competent baseline grid: patient mean; tissue shrinkage `{1,5,10,20,50,∞}`; ridge λ `{0.01,0.1,1,10,100}` with and without lability. Use five patient-grouped A0 folds. The fixed comparators may use the best admissible A-selected strategy directly.

Retain the proposed threshold:

\[
e_\tau=\min(0.90E_0,\;1.05E_*),\qquad \tau=1-e_\tau.
\]

Require \(E_*\le0.90E_0\), nondegenerate outcomes and useful baseline attainment. **This construction already makes the best listed baseline attain the A1 threshold.** The unresolved question is whether adaptive allocation saves meaningful *additional* CPU on fresh panels.

**Screen pass bar:** all four witnesses pass; measured costs support the headroom inequality against the strongest static shortcut; an A-only planning calculation supports ≥80% power at a stated 35% savings alternative for the eventual 20% margin, with 16 panels and three fixed comparators. Planning assumptions must be labeled. No threshold adjustment after policy results.

**Battery gate:** ledger-first SPEC, accounting approval and G2/Lock1 Sol-high ≥90/no high-critical findings.

Then execute:

- **E0: 24 real evaluated nodes**, for example eight metadata-defined A1 histories with three prelisted root artifacts each.
- Unchanged incumbent plus ≥3 executable challengers: cost-aware branch ordering, tissue-conditioned ordering, and refinement/stopping allocation.
- Parent-local deterministic artifact generation, with canonical hashes frozen before E0. Replay exposes only observed prefixes and actual recorded outcomes.
- Retain the existing support requirement: ≥8 episodes and ≥50% common support at every positively weighted budget fraction. Unsupported refinements receive no invented reward; the frozen fresh-rollout fallback applies.
- Cycle one on A2: selected challenger versus incumbent versus original fixed exploration, ≤36 fresh evaluated nodes. Freeze the promotion rule before replay; retain the incumbent when it fails.

**Kill criteria:** missing accounting/plasmids; unsupported independent processing; insufficient quality; strongest-static shortcut eliminates 20% headroom; inadequate precision; or allocation failure. Do not rescue the design by making fixed search expensive, omitting shared production, or consuming B.

**G-B — `sgen006`: independent biological-resource discriminator**

**Parents:** W4’s bounded scientific question + W3’s reproducible estimator + sgen004’s verified failure to recover patient inference from retained aggregates.

**Current finding:** I have **not verified an accessible new cohort adequate to repair patient-level inference for the same organoid endpoint**. This is a bounded search result, not a claim that no such resource exists.

Three concrete candidates deserve dispositions:

| Resource | Verified relevance | Present limitation |
|---|---|---|
| Khalili et al., 2025, colon-organoid dependency landscape | Public supplementary screen data; genome-wide F147T experiment and focused F130T validation | One genome-wide tumour background; TP53 derivatives and replicates do not create independent patients. [Primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC11906589/) |
| Lo et al., 2025, gastric-organoid CRISPR platform | Public source data/code and engineered gastric-organoid perturbation screens | Perturbation modes, gene-drug endpoints and donor representation require audit; not yet an equivalent organoid-transfer cohort. [Primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC12354852/) |
| Han et al., 2020, paired 2D/3D lung-cancer screens | Independent controlled-environment evidence | Cell-line spheroids rather than a new patient-organoid cohort; the retest library was selected from earlier hits. [Primary paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7368463/) |

Han is a plausible future **environmental-portability** generation. It cannot silently replace the organoid inference required here.

**SPEC skeleton.** First perform a metadata-only source/identity/assay audit: ≤40 requests, ≤32 MiB, ≤600 CPU-s. Extract donor provenance, culture relationships, perturbation type, eligible gene identities, controls, processing dependencies, licenses and exact source manifests. No C re-decoding or C-derived sample-size planning. Do not count republication or reprocessing as biological independence.

**Screen pass bar:** a candidate must provide:

- Genuinely new, adequately identified patients disjoint from consumed C and other evaluation populations.
- Compatible measured dependency outcomes and fixed scientific covariates, without outcome-fitted processing leakage.
- The fixed 207-coordinate endpoint, or an independently justified new scientific contract explicitly identifying its changed scope.
- Sufficient independent biological units and a defensible prospective uncertainty procedure. A numerical donor floor alone does not establish precision.
- A source-specific novelty disposition for the exact proposed claim.

The currently identified candidates **do not yet pass this bar**.

**Conditional battery:** only a metadata-positive resource receives a prospective scientific lock. Preserve patient-equal aggregation, fixed environmental lability and baseline-strength adjustment, \(\delta=0.20\), 5,000 patient-cluster bootstrap draws, seed `20261028`, and the same substantive SIGNAL/NEGATIVE/BOUND/INCONCLUSIVE interpretation where justified. Require estimator-validity and precision review before confirmatory access. Freeze multiplicity and sensitivity analyses; a failed primary cannot be rescued by another subset.

Reserve ≤12 evaluated scientific artifacts and ≤3,600 additional CPU-s within the generation ceiling. New external outcomes never enter policy replay or reward.

**Kill criteria:** only one or two biological backgrounds; unresolved donor identity; incompatible drug/activation endpoints; selected-hit data insufficient for the fixed panel; inaccessible required measurements; or unjustified uncertainty. Record `NO_QUALIFYING_RESOURCE_IN_SCREEN`; retain C3/C6/C10/C11 as partial. Neither an environmental replication nor a new case study retroactively repairs the archived 144-group interval.

**G-C — `pgen005d`: recombine verified decisions, complete cycle two, then reserved evaluation**

**Parents:** G-A’s executed policy histories and measured cost results; W3’s immutable artifact machinery; W5’s acquisition safeguards. Incorporate G-B’s verified provenance/assay checks only as shared validity machinery. **G-B scientific outcomes are never policy-training parents.**

This generation is conditional on G-A’s screen. If G-A fails, do not execute a nominal second cycle. Continue independent source/scientific generations while preserving that failure.

**SPEC skeleton.** Freeze the same scientific generator, evaluator, action library, threshold and information permissions. Propose incumbent plus three executable recombinations:

1. The best verified ordering component plus diagnostic-first allocation.
2. The best verified tissue-conditioned component plus refinement allocation.
3. The best verified ordering component plus a stopping rule based solely on revealed history and frozen development evidence.

Use actual immutable parent IDs when available; record each carried component. All baselines receive the same diagnostic helpers and valid stopping opportunities. A universally useful code optimization is shared infrastructure, not a learned-policy advantage.

**Screen pass bar:** faithful replay under the frozen common-support rule; lower measured cost without losing valid attainment; no benefit depending on withheld outcomes, discarded failures or unsupported actions. Use the existing frozen tie ordering and fresh-rollout fallback.

**Cycle-two battery:** A3, ≤36 fresh nodes, challenger versus incumbent versus original fixed exploration. Promotion requires the preregistered comparison with the incumbent; failure retains it. Two executed cycles can satisfy the cycle-count component without either promotion, but cannot establish C9.

**Final battery gate:** two genuine cycles, reviewed histories, adequate A-only precision, reconciled accounting and frozen final policies. Keep B unused until this gate passes.

Evaluate four policies on all 16 B panels:

- Final learned policy.
- Original fixed exploration.
- Predeclared fixed-allocation strategy.
- Strongest A-selected static strategy.

Cap each rollout at four evaluated candidate artifacts, giving **256 maximum B nodes and zero hosted rollout calls**. Stop fixed strategies promptly when they attain quality; do not force all four actions.

For comparator \(j\), freeze

\[
s_j=1-\frac{S+H+\sum_{b=1}^{16}L_b}
                 {S+\sum_{b=1}^{16}F_{jb}}.
\]

Include actual arm-specific baseline search costs where incurred. Charge shared production once per counterfactual arm and learning once over this single campaign.

Use 10,000 paired whole-panel bootstrap resamples, seed `2026102804`; hold the recorded shared and learning costs fixed. Require simultaneous one-sided 95% lower savings bounds ≥20% against all three fixed comparators—for example, Bonferroni one-sided \(\alpha=0.05/3\) bounds. This inference is conditional on the frozen training artifacts.

For the simplest conservative certification rule, **any unresolved nonattainment prevents the primary C9 claim**. Preserve right censoring and report quality-versus-cost curves; never replace nonattainment with an invented exact attainment cost.

An illustrative evaluated-artifact allocation is:

\[
17\ \text{feasibility configurations}
+24\ E0
+36+36\ \text{fresh cycles}
+256\ B
+12\ \text{scientific artifacts}
=381.
\]

That leaves seven of the currently remaining 388 nodes. This allocation works only if each CV configuration is genuinely one predefined aggregate artifact; every separately evaluated artifact must still be charged. Replay lookup adds measured learning CPU, not fabricated fresh evaluations. If actual counting exceeds this reservation, reduce the prospective design before outcomes or retain `PENDING`; do not hide trials.

**Kill criteria:** failure of the cumulative end-to-end headroom test; replay leakage; insufficient final precision; nonattainment; or any comparator’s savings bound below 20%. Apply the existing two-cycle no-progress assessment rather than generating indefinite minor variants.

**Present determination**

W1–W5 support a coherent new experiment, but do not establish its missing witnesses. C1’s novelty determination and C7 stand; the unresolved patient inference remains unresolved. There are still zero genuine policy cycles and no qualifying C9 result. No `GOAL COMPLETE_*` determination is warranted.

The cheapest next action is G-A’s **accounting-and-metering discriminator**, with no raw acquisition. A negative result there should immediately route effort to G-B’s independent-resource screen.

ENDPOINT_V2: YES_WITH_NAMED_CONDITIONS, current NO_GO; NEXT_GENERATION: pgen004d — ledger-first host-cost and total-local-CPU witness before schema or acquisition; RECOMBINE: W1+W2+W3+W5, with W4 scientific constraints