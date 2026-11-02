# GOAL — Cancer Dependency RSI (locked goal statement)

> **Goal-tool objective (copy verbatim into `create_goal`):**
> Discover and independently support a previously unreported, precisely bounded explanation of when molecularly defined cancer dependencies persist or fail across measured culture environments — and prove, under a fixed scientific evaluator and matched total resources, that a learned research policy beats strong fixed exploration by a preregistered practical margin. Do not stop at a plan, scaffold, leaderboard, or narrative: run real experiments on verified public data, complete at least two genuine policy-improvement cycles with faithful replay and fresh rollouts, evaluate one locked claim family once on independent external outcomes, and ship a reproducible evidence atlas, manuscript, and reproducibility package. If any gate fails, report the exact unmet gates — never reinterpret insufficient evidence as success.

- **Project:** `cancer-dependency-rsi/` (isolated under this workspace)
- **Specification:** `cancer_rsi_handoff.txt` (28 Oct 2026) — the research specification; this file is its locked goal projection. On conflict, the specification wins.
- **Execution plan:** `PLAN.md`
- **Status / resume:** `cancer-dependency-rsi/STATUS.md` (append-only ledgers alongside it)

## The ambition (all five, not any one)

1. **A new explanatory finding.** At least one previously unreported, precisely bounded, externally supported result — a positive conditional dependency rule, a convincing refutation of a meaningful dependency claim, or an informative bound that changes how a target should be interpreted. It must resolve a specific predeclared uncertainty. A better benchmark score, a rediscovered association, or a nonsignificant p-value does not count.
2. **A complete evidence atlas.** Every eligible gene in the controlled environmental panel (250 selected genes) with support, contradiction, heterogeneity, uncertainty, missing evidence, and every exclusion with its reason.
3. **A defensible environment→transfer connection.** Measured environmental sensitivity linked to transfer behavior in an independently filtered organoid cohort, beyond lineage and the strongest appropriate baseline — only where the evidence supports it, with distinct evidence labels for intervention vs. association.
4. **A real policy-improvement loop.** Executable policies, faithful historical replay on recorded outcomes only, fresh-rollout promotion tests, incumbent retention on failure, ≥2 genuine cycles, and a final frozen-policy comparison on reserved panels against fixed exploration and a fixed-allocation/random strategy.
5. **Demonstrated efficiency + a review-ready package.** Preregistered practical improvement under matched total resources including learning overhead (default target: ≥20% lower total measured cost to a predeclared quality threshold, one-sided 95% lower bound meeting the margin), plus manuscript and full reproducibility package with all failures, limitations, and costs disclosed.

**Stretch (not a substitute):** multiple convergent findings across adequately represented lineages/pathways. Never trade one strong finding for a quota of weak associations; never force claims about sparsely represented cancer types.

## Scientific question (to be narrowed at the identifiability gate)

Does measured sensitivity to culture conditions (medium, growth format), together with genotype and tumor state, explain failures of dependency transfer from conventional cancer models to patient-derived organoids beyond lineage and technical variation alone?

- **Direct environmental estimand:** within-model change in a gene's measured dependency between environment A and B holding the other measured condition fixed; medium and format analyzed separately where the design permits; original assay units for within-study paired contrasts.
- **Transfer estimand:** extent to which a prespecified genotype / tumor-state / context relationship predicts dependency behavior in an independently filtered organoid cohort beyond lineage and the strongest baseline.
- Generic cell-line→organoid prediction is already studied (October 2026 transferability study, 20 genes) and **cannot** be the novelty claim. Recovering published lipid/adhesion/state findings is a control, not a discovery.

## Non-negotiables

- Scientific evaluator, splits, practical margins, multiplicity control, and success criteria are **frozen before** policy optimization and before final evaluation. The policy may change branching, prioritization, refinement, and stopping — never labels, metrics, margins, or success criteria.
- Three evaluation layers stay separate: **(A)** development panels, **(B)** reserved policy-evaluation panels, **(C)** final external biological evaluation (independently filtered Sanger cohort preferred). Final outcomes are never a replay reward and are touched only after the second lock commits hypotheses, predictions, artifacts, and inferential code.
- Count independent biological models/donors correctly. Genes, guides, wells, cultures, and replicates are not patients. Broad Chronos effects and Sanger fitness scores are different measurement systems — never subtracted directly.
- Never reward small p-values, discovery counts, or persuasive narratives. Never invent outcomes for unexplored actions; unsupported replay actions stay unsupported. Synthetic data tests code only, never biology.
- All scientific fitting, simulation, evaluation, and data processing run locally on this laptop (Apple M5 Max, 18 cores, 128 GB RAM, macOS 26.6); hosted frontier-model reasoning is used only through the already-authorized host/codex interface. No GPU, ≤2 CPU-heavy jobs, research memory ≤ min(8 GiB, 60% RAM), 10-min default exploratory timeout, ≤20 GiB downloads, first pilot ≤8 h, additional metered API spend cap = $0 unless the user sets a numeric cap; downloads ≤ min(20 GiB, available disk/4). Allocations bound the campaign from Phase 0 (pre-lock budgets, retry limits, terminal-review reserve in `config/allocations.json`), refined at Lock 1; ceilings never auto-increase.
- Separate status fields, always: `scientific_discovery`, `prediction_improvement`, `policy_improvement`. One never establishes another.

## Completion — all 13 gates (C1–C13) must hold

| Gate | Requirement (abbreviated; specification §12 is authoritative) |
|---|---|
| C1 | Current novelty audit: precise unresolved question, distinguished from Aug resources + Oct transfer study |
| C2 | Legitimate public data only; full provenance, licensing, ID crosswalks, reproducible retrieval/cache |
| C3 | Identifiable paired contrast / conditional relationship in a named population; correct independent-unit counts |
| C4 | Contract, eligibility, splits, baselines, margins, evaluator, confirmatory procedures frozen before optimization/final eval |
| C5 | Baselines reproduced closely enough to establish direction, cohort integrity, measurement interpretation |
| C6 | ≥1 previously unreported explanatory finding passes frozen criteria + external tests (refutation/bound can qualify) |
| C7 | Evidence atlas covers all eligible panel genes; every exclusion listed; evidence types distinguished |
| C8 | ≥2 real policy cycles: executable challengers, faithful replay, fresh rollouts, retained failures, final reserved-panel comparison |
| C9 | Learned policy meets preregistered practical-improvement criterion vs strongest fixed baseline, end-to-end incl. overhead |
| C10 | Conclusions survive multiplicity correction, uncertainty analysis, ablations, adversarial checks; invariance needs positive + equivalence evidence |
| C11 | Clean reproduction from frozen artifacts within tolerances; no stochastic LLM rerun required |
| C12 | Manuscript + machine-readable evidence, manifests, histories, versions, measured resources, failures, limitations, reproduce/resume commands |
| C13 | First meaningful end-to-end cycle actually executed (plan/scaffold/mock is insufficient) |

## Terminal states (use exactly one; list unmet gates otherwise)

`COMPLETE_SUPPORTED_DISCOVERY` · `COMPLETE_SUPPORTED_REFUTATION_OR_BOUND` (both require every relevant gate incl. C9) · `SCIENTIFIC_RESULT_WITHOUT_RSI_EVIDENCE` · `RSI_RESULT_WITHOUT_SCIENTIFIC_DISCOVERY` · `INCONCLUSIVE` · `BLOCKED` · `BUDGET_EXHAUSTED`

A completed computational campaign is not a completed scientific goal. Insufficient power is not equivalence. A polished manuscript is not a discovery.

## Model routing (user-mandated)

- **Review / adversarial audit of everything:** `gpt-6.1-sol` at `high` reasoning via `codex exec` — must enumerate low/medium/high/critical issues and score 0–100; verified issues are fixed; re-review until score ≥ 90.
- **Generating new generations** (policy challengers, hypothesis/analysis generations): `gpt-6.1-sol` at `xhigh` reasoning. Sol-xhigh works from the full tried history via the locked context/retrieval contract (exhaustive history index + episode-admissible catalog/frontier views + ID-cited full records, PLAN §0.1/§0.4), picks the most promising trajectories to keep, recombines 2+ recorded parents into new candidates with machine-checked DAG lineage, refines winners, repairs recoverable failures, and opens unexplored directions (PLAN §0.4–0.5, after Google Dream-RSI and the `~/bufferright/business` 48-generation LOOP). The whole generator protocol is frozen per comparison; executed selection remains versioned policy code under the fixed evaluator — sol proposes, the policy disposes.
- Every model call is ledgered (model ID, effort, prompt hash, tokens when exposed, wall/CPU time, cost or `unknown`). Unknown material cost ⇒ C9 all-in savings cannot be certified; the gate stays unresolved rather than assumed.

## Autonomy & terminal determination (user-mandated)

- **Never idle, never self-certify.** Work continues autonomously, generation after generation, through failures and negative results, within Lock-1 campaign allocations. When stuck, consult `gpt-6.1-sol` at `xhigh` with the full state packet for ranked unblock options + cheapest discriminating experiments (PLAN §0.6 unstick protocol), then keep working on the best legal option. Stopping is legitimate only at a hard authorization gate, allocation/budget exhaustion, explicit user stop, the locked no-progress/negative-EV determination, or terminal determination — indefinite retries are forbidden (spec §14).
- **Sol-xhigh determines satisfaction.** The goal counts as satisfied only when `gpt-6.1-sol` at `xhigh`, reviewing the complete evidence package, determines gate-by-gate (C1–C13) that a `COMPLETE_*` state is documented — score ≥ 90, zero unresolved high/critical objections. Its determination supplements the evidence; it can never waive a gate or substitute for missing artifacts. Unmet gates become the next mandate list while allocations remain; when they don't, sol-xhigh certifies the honest non-complete terminal state + exact unmet gates (a pre-reserved terminal-review slice guarantees affordability; if the call still cannot run, mechanical `BLOCKED`/`BUDGET_EXHAUSTED` checkpointing is permitted, but positive completion always requires sol-xhigh).

## Definition of done for this goal

Terminal state is one of the two `COMPLETE_*` states with documentary evidence for C1–C13, a clean-room reproduction passing within tolerances, and the first-substantive-report contents (verified data, identifiable question, baseline result, real experiments, replay support, retained/promoted policy, measured resources, next discriminating experiment) all superseded by final locked results. Anything less is reported under its honest terminal state with the precise unmet gates and the smallest concrete next step.

## Execution status (v3 note, 2026-10-28 — objective above unchanged)

Scientific-only Lock-S has executed the external test once (BOUND, ρ=−0.146 [−0.175,−0.114]); C6 awaits novelty adjudication (audit v4). The policy route is stopped before acquisition: C9 is structurally unresolved (host expenditure `unknown`, strict matching undemonstrable) and no admissible task with independent reserved panels is witnessed. The goal is **not satisfied**; it becomes satisfied only on a sol-xhigh gate-by-gate `COMPLETE_*` determination. Current mandates, gates, and resume command: `PLAN.md` §11 + `cancer-dependency-rsi/status.json`.

## Amendment 2026-10-29 (user-authorized, prospective): C9 cost evidence

The user authorizes the following prospective change to the cost-evidence rule
above ("Unknown material cost ⇒ C9 all-in savings cannot be certified"):

- For host model calls, cost may be established by the campaign's
  estimated-cost basis: exact recorded token counts from call receipts,
  re-priced at published GPT-6.1 Sol list prices under a frozen price
  schedule, with unpriced calls imputed under the frozen sol-xhigh rule
  (max audited receipt cost per phase+effort) and savings claims required to
  survive 2x/4x imputation sensitivity. The estimator and its versioned
  outputs live in `cancer-dependency-rsi/src/host_cost_estimate.py` and
  `cancer-dependency-rsi/ledger/host_cost_estimate_v*.json`.
- Actual metered spend (currently $0, subscription auth) must still be
  reported alongside every estimated figure; estimates are never presented
  as metered billing.
- All other C9 requirements are unchanged (preregistered criterion,
  strongest fixed baseline, end-to-end overhead, matching witnesses).
- This amendment is prospective from 2026-10-29; it does not retroactively
  certify any prior comparison (none has run). Final C9 satisfaction is
  still determined gate-by-gate by sol-xhigh at terminal adjudication.
