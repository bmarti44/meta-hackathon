# PLAN — Executing the Cancer-Dependency RSI Research Loop

**Specification:** `cancer_rsi_handoff.txt` (28 Oct 2026) · **Locked goal:** `GOAL.md` · **Project root:** `cancer-dependency-rsi/`
**Host (verified 2026-10-28):** Apple M5 Max, 18 CPU cores, 128 GB RAM, 532 GiB free disk, macOS 26.6 (arm64); Python 3.14.8, git 2.54, Node available; no R/Julia (install only if a baseline requires it, inside the project env).
**Model access (verified):** Muse configured with `gpt-6.1-sol` (`~/.codex/config.toml`: `model_reasoning_effort="high"`); host agent available for reasoning. All 8 seed URLs (S1–S5 papers/repos/portals) returned HTTP 200 on 2026-10-28 — reachability only; content/methods verification is Phase 1 work, not yet done.

This plan is the execution contract for the loop. It sequences the work so that **no adaptive search happens before identifiability is proven, no policy optimization happens before the evaluator is frozen, and no final outcome is touched before the second lock.** Each phase ends at an evidence gate; failing a gate narrows the question or stops honestly — it never lowers the standard.

---

## 0. Operating rules (bind every phase)

### 0.1 Model routing (user-mandated, enforced in code)
| Role | Model | Reasoning | Invocation pattern |
|---|---|---|---|
| Adversarial review of **everything** (plans, code, contracts, claims, manuscript) | `gpt-6.1-sol` | `high` | `codex exec -m gpt-6.1-sol -c model_reasoning_effort='"high"' -s read-only "<review prompt>"` |
| Generating new generations (policy challengers, hypothesis/analysis candidates) | `gpt-6.1-sol` | `xhigh` | `codex exec -m gpt-6.1-sol -c model_reasoning_effort='"xhigh"' -s workspace-write "<generation prompt>"` |
| Lead-investigator reasoning, statistics, implementation | Host agent | — | Local session; all fitting/evaluation runs locally in Python |

- The **review protocol** is fixed: reviewer must enumerate issues by severity (**low / medium / high / critical**) with file:line evidence and a single **0–100 score**. The lead investigator **verifies each issue against the artifact** (accept / reject with reason), fixes all verified issues, and **re-reviews until score ≥ 90 and zero verified high/critical issues remain**. Review transcripts, verdicts, and fixes are appended to `reviews/` and the experiment ledger. A score is never accepted without its issue list; an issue is never fixed without verification.
- Specialist worker roles are kept distinct: literature/novelty, data provenance, scientific modeling, evaluator implementation, adversarial review. The evaluator process receives a **narrower interface** than the proposer (hashed inputs, no final-outcome paths). This is a logged protocol, **not** a cryptographic security boundary — never described as one.
- Every model call is recorded: model ID, effort, prompt hash, token counts when exposed, wall/CPU seconds, peak RSS, monetary cost or `unknown`. **Additional metered API spend cap = $0** unless the user configures a numeric cap; host/codex access already authorized is used, with unmeasurable cost marked `unknown` (which blocks certifying all-in C9 savings — see §7.3).

### 0.2 Resource envelope (written to `cancer-dependency-rsi/config/resources.json`, enforced by the budget wrapper)
- No GPU. ≤ 2 CPU-heavy jobs concurrently. Aggregate research RSS ceiling = min(8 GiB, 60% RAM) = **8 GiB** on this host.
- Exploratory fit timeout **600 s** default; longer only via explicit recorded allocation from the campaign budget.
- Downloads ≤ min(20 GiB, ¼ free disk) = **20 GiB**. First pilot: **24 real evaluated development nodes + 3 executable challengers + incumbent**, ≤ **8 h** wall (safety ceiling, not a promise).
- No automatic ceiling increases. Budget wrapper **reserves before dispatch, persists before dispatch, reconciles after**; interrupted ⇒ stays `reserved` until reconciled; completed paid/host calls are never repeated on resume.

### 0.3 Persistence & honesty primitives
- Append-only JSONL ledgers: `ledger/experiments.jsonl`, `ledger/resources.jsonl`, `ledger/reviews.jsonl`. Node states: `proposed → dispatched → completed|failed → committed`. Checkpoint after **every** completed experiment.
- Every discovery node stores: immutable parent ID, artifact bytes + SHA-256, input-context hash, data hash, split hash, evaluator hash, generator model+effort+prompt hash, seeds, result, validity diagnostics, failures, measured costs.
- `STATUS.md` + `status.json` always carry: phase, incumbent policy ID, spend, three separate status fields (`scientific_discovery`, `prediction_improvement`, `policy_improvement`), unmet gates (C1–C13), **next action**, and **exact resume command**. Never claim the loop is "running" without a live PID/job ID + recent heartbeat.
- Terminal states only from the GOAL list. A failed final test stays failed; downstream work on its outcomes is exploratory.

### 0.4 The trajectory system — how tried directions are tracked, scored, kept, recombined (Dream-RSI adaptation)

This is the engine of the loop, adapted from Google's Dream-RSI (arXiv:2609.14858; `google-research/dream-rsi`): accumulated discovery history acts as a **replay simulator** over the realized search space; policies are improved **offline by "dreaming" in replay worlds** and only then redeployed online; base generator, evaluator, and task stay fixed while only the exploration policy changes. Departures required by the cancer specification (faithful-replay-only, fixed evaluator/splits/margins, no invented outcomes) are binding and disclosed — where they force a change from the paper, the method is labeled a **Dream-RSI-inspired adaptation**.

**0.4.1 Units of record (nothing tried is ever lost or rewritten).**
- **Node (attempt):** one evaluated artifact — the atomic unit. Fields per §0.3 plus: `direction_id`, `branch_id`, `generation`, `origin` (see 0.4.4), evaluator score vector (quality endpoints, validity, cost), `outcome_class` ∈ {`success`, `conceptual_failure`, `implementation_failure`, `invalid_result`, `unsupported`, `unknown`}, and free-text `lesson` (what this attempt ruled in/out).
- **Branch / trajectory:** an ordered root-to-leaf chain of refinements: root artifact + up to `REFINE` children, mirroring Dream-RSI's `BRANCHES × (REFINE+1)` tree shape (paper default 10×11; here scaled to the pilot budget, e.g. pilot = 24 nodes arranged as branches of depth ≤ 4 — exact `BRANCHES`/`REFINE` frozen at Lock 1). A trajectory is the unit of "a tried direction pursued over time"; its score trajectory (best-so-far curve vs cumulative cost) is stored, not just its endpoint.
- **Discovery tree:** all branches grown in one round under one policy on one task panel. On round completion the tree is frozen (content-hashed) and appended to the **trace pool** as a **replay world** (`trace_pool/<round>/` + `manifest.json`, mirroring `trace_pool.py`): frozen worlds are never mutated; the pool only grows.
- **Direction:** a semantically coherent research line spanning many nodes/branches (e.g. "lipid-metabolism genes under medium change, genotype-conditioned"). Directions are the unit the system reasons about when choosing what to try next.

**0.4.2 The direction catalog (the memory of what was tried).** Maintained at `directions/catalog.json` (versioned, append-only snapshots `directions/history/iterNNN.json`), adapted from Dream-RSI's direction schema. Each direction record carries: canonical name + description; **status** ∈ {`unexplored`, `underexplored`, `promising`, `promising_but_fragile`, `promising_but_underexplored`, `well_explored`, `saturated`, `failed_but_recoverable`, `unpromising`}; linked node/branch IDs (evidence attempts); best/median evaluator quality; quality-vs-cost slope; failure taxonomy counts; heterogeneity/robustness notes; `avoid_repeating` list (exact dead ends: invalid transforms, leaked features, refuted sub-claims); open bottlenecks. Status transitions are rule-based from recorded outcomes (thresholds frozen at Lock 1), not vibes: e.g. `saturated` requires ≥ K refinements with best-so-far improvement < ε over the last k attempts; `promising_but_fragile` requires top-quartile quality that collapses under a prespecified sensitivity check. An extraction step (sol-xhigh, schema-validated JSON, mirroring `directions/extract.py` + `validate.py`) maps each new attempt into the catalog; invalid extractions are rejected and ledgered, never silently coerced.

**0.4.3 Seeing which directions work best (trajectory scoring & the frontier).** After every round the runner recomputes, deterministically from the ledger (no LLM in this path):
- per-trajectory **best-valid-quality**, **cost-to-threshold**, **area-over-the-curve** (quality vs cumulative measured cost), and **validity rate**;
- per-direction aggregates (above) + a **Pareto frontier** over (scientific quality, total cost, robustness) — directions/trajectories on the frontier are the keepers; dominated ones are candidates for pruning;
- a **direction summary** (sol-xhigh, mirroring Dream-RSI's `GUIDANCE` ablation): compact natural-language digest of explored directions, what worked, what failed and why, and what is conspicuously untried. This summary is injected into the next round's generation prompts so new generations are explicitly conditioned on everything already tried. Summaries are artifacts (hashed, versioned); they guide generation but never alter scores.

**0.4.4 Keeping, recombining, and generating the next generation (sol-xhigh as the proposer).** Each new generation of candidates is produced by `gpt-6.1-sol` at `xhigh` from a fixed proposer prompt whose inputs are: the direction catalog, the direction summary, the Pareto frontier, remaining budget, and the locked hypothesis/transformation spaces. Every candidate must declare one **origin** (adapted from Dream-RSI's candidate origins) with machine-checked lineage:
- `new` — opens an `unexplored` direction inside the locked spaces;
- `underexplored` — extends a direction whose evidence is thin relative to its promise;
- `combination` (**recombination**) — merges ≥ 2 named parent trajectories/directions (e.g. Parent A's feature family + Parent B's conditioning structure), recording **both parent node IDs** — the child is a DAG node with multiple parents, each parent's contribution stated; recombination may only combine elements that are each legal under Lock 1, and the combined artifact is re-validated from scratch (parents' scores never transfer);
- `repair` — revives a `failed_but_recoverable` direction by fixing its recorded failure mode (e.g. implementation bug, support violation) while preserving its scientific idea; the failure being repaired must be cited by node ID.
Candidates also carry: priority score, target bottleneck, related direction IDs, `avoid_repeating` acknowledgements, and evidence-attempt citations. The runner **rejects** candidates that (a) fall outside locked spaces, (b) duplicate an existing node context-hash, (c) cite nonexistent parents/evidence, or (d) repeat an `avoid_repeating` dead end without a `repair` justification. Rejections are ledgered with reasons — the proposer sees them next round.

**0.4.5 Selection: who decides what runs next (policy vs proposer — kept distinct).** Two different decisions must never be conflated:
- **Proposal** (sol-xhigh): *what artifacts/directions could be tried* (0.4.4) and *what policy rewrites could be tried* (challengers, Phase 4).
- **Selection** (the executable **policy** + frozen rules): *which legal action executes next* given observed history, legal actions, and remaining budget. The incumbent policy consumes the catalog/frontier (e.g. "refine frontier branches with steepest recent slope until marginal gain < ε, then open the highest-priority underexplored direction; reserve x% for `new`") — but the choice is made by versioned code, replayable and auditable, not by an unrecorded LLM judgment. LLM priority scores are **inputs** to the policy, never the decision itself. This preserves the spec's requirement that improvement mean *changed executed decisions by an executable policy*, while still using sol-xhigh to pick the most promising candidate trajectories to put before the policy.
- **Keep/prune rule (frozen at Lock 1):** frontier trajectories are kept refinable; `saturated`/`unpromising` directions are pruned from the legal-action set (but never deleted from history); `promising_but_fragile` trajectories may only be refined via prespecified robustness diagnostics. Pruning decisions are ledgered so replay can reproduce exactly which actions were legal when.

**0.4.6 Dreaming: offline policy improvement in replay worlds.** Policy challengers (sol-xhigh rewrites of the policy module, `M = incumbent + ≥3 rewrites`, mirroring the paper's M=4) are evaluated by **replaying them over every frozen world in the trace pool**, once per **budget preference** ρ ∈ {0, 0.25, 0.5, 0.75, 1} (ρ interpolates quality-vs-cost emphasis in the replay objective, paper Eq. 1 adapted to the locked endpoints). Hard constraints from the specification override the paper where they conflict: replay reveals **only recorded outcomes along the trajectory**; a recorded child replays only on **exact context-hash match** (immutable parent + fixed context), else the action is `unsupported` and scored as unsupported — never imputed; policies are compared on **common support** with coverage reported; replay is a **screen**, and promotion additionally requires fresh online rollouts (Phase 4). Both the learned-policy arm and the **Recursive Fixed Exploration** baseline start from the **same shared first round E0** (explored with the hand-designed starting policy, copied read-only into each arm), so the comparison isolates the value of policy learning itself.

**0.4.7 Lineage & audit views.** The runner can emit at any time (`status --trajectories`): the full lineage DAG (every node's parents incl. recombination parents), per-direction status board, frontier plot data (quality vs cost per trajectory, colored by generation), generation-over-generation table (best quality, cost-to-threshold, validity rate, support coverage, incumbent ID), and the "graveyard" (pruned directions + why). These views are derived deterministically from the append-only ledger; if a view and the ledger disagree, the ledger wins and the view is a bug.

### 0.5 Generation protocol — the per-generation operating loop (modeled on the proven `~/bufferright/business` LOOP)

The business workspace ran 48 generations of an RSI-style loop (`data/research/paths/LOOP/`: `gen1…gen48/`, `LOOP-LEDGER.md`, `engine_loop_v1…v6.py`, `battery.py`) under the rule *"Sol xhigh proposes, Sol high reviews each generation"*, with review score trails like 54→76→92 and explicit family closures. This project adopts that battle-tested operating discipline, translated to the cancer domain (business term → here): **sleeve pool → direction/analysis-family pool; blend → recombination; screen → cheap screen + replay screen; battery → full evaluator battery; PREREG hash → generation-spec hash; forward ledger → frozen predictions; anchor → baseline anchor**.

**0.5.1 Anatomy of one generation (`generations/genNNN/`, never reused, never overwritten).**
1. **`SPEC.md` + hash, locked before any run.** States: the question this generation discriminates, candidate families to enumerate, screen metric, battery definition, pass bar, stop rules, and trial budget. SHA-256 recorded in the ledger *before* execution (business precedent: `PREREG-*.md` hashes locked pre-download). Amendments are new versioned files (`SPEC-amendment-1.md` + hash + reason), never edits — and any amendment touching locked science follows the new-study-ID rule.
2. **Enumerate from the pool.** Candidates are systematic combinations/mutations of pool elements (feature families × conditioning structures × estimators), each with declared origin + parents per §0.4.4. Sol-xhigh proposes the enumeration and any genuinely new mechanisms; the runner validates legality (locked spaces, dedup by context hash, parent existence).
3. **Screen (cheap, ranking only).** One fast evaluator pass (development panels and/or replay) ranks candidates; screen metrics are approximations and are **labeled as such** — screen-positives are never claims (business precedent: curve metrics marked approximate; pass/fail only at battery).
4. **Recombine winners.** Screen survivors are recombined (`combination` origin, both parents recorded) and mutated around winners (business precedent: "recombine winners", Gen2 weight mutations around G01). Recombinations re-enter at screen; no score inheritance.
5. **Battery (finalists only, decisive).** Full frozen evaluator + validity diagnostics + matched controls + prespecified ablations on fresh development rollouts. *Every* screen-positive gets batteried before any "no candidate passes" verdict (business precedent: M1 remediations completing batteries for all screen-positives).
6. **Verdict + family bookkeeping.** Each family gets an explicit disposition: `ADVANCES`, `DEAD` (with numbers), `CLOSED` (family exhausted; reopening requires new data or a named repair), `INVALID` (defective run — **preserved as a defective record**, never deleted; business precedent: Gen46 v1 look-ahead preserved, corrected in v2/v3), or `BLOCKED-DATA` (needed data unavailable; no proxy substitution without downgrading the claim).
7. **Sol-high review of the generation** (score 0–100, severity-tagged issues) → verify → fix → re-review until **≥ 90**; remediation entries appended per issue (`CONFIRMED+FIXED` / `ACCEPTED-as-implemented with claim downgrade` / `REJECTED with evidence`), exactly as the business ledger records C1/H1/M1 dispositions. The generation is not "complete" below 90.
8. **Ledger the generation** in `GENERATIONS.md` (human-readable, append-only; machine truth remains the JSONL ledgers): candidates screened/batteried, numbers for every finalist, failures with numbers, lessons (e.g. business precedent: "always verify tail direction before screening" → here: "always verify score direction + pairing before screening"), cumulative **trial accounting** (total configurations ever screened — correlated configs are not independent trials, and the count is reported, never hidden), next generation's mandate, and explicit **stop-rule checks** (e.g. leakage found ⇒ dependent mutations cancelled, business precedent: Gen1 look-through cancelling Gen2 weight mutations).

**0.5.2 Cross-generation invariants borrowed from the business loop.**
- **Anchor regression:** a frozen reference result (here: the development baseline reproduction) must reproduce **byte-identically / within tolerance** after every engine/evaluator change, or the change does not land (business: C06 anchor `0.02506618343648448` identical across engine versions). Engine/evaluator versions are preserved side-by-side (`evaluator_v1.py, v2.py…`), never overwritten.
- **Provenance-stamped runs:** every run file stamps SHA-256 of engine, spec, data, splits, evaluator, and each input artifact; caches invalidate on any mismatch; unstamped rows are exploratory-only (business M6 remediation).
- **Frozen forward evidence:** once a candidate is frozen (Lock 2 predictions), it is judged **only** on untouched outcomes; post-hoc discoveries (e.g. a control arm outperforming its hypothesis — business Gen8/Gen9 controls) are flagged post-hoc, may be frozen for forward judging, and are **never promotable on consumed data**.
- **Negative-EV stop judgments are first-class outcomes:** sol-xhigh + lead investigator may jointly declare further search on consumed panels negative-EV (business Gen5/Gen6 precedent) — recorded as a research judgment with reasons, triggering pivot to new-data directions or honest terminal states rather than endless tuning.
- **One fixed specification for falsification probes:** cheap decisive diagnostics run exactly as specified with no variants (business Gen6 seasonality precedent) — a failed cheapest-falsification closes the family without a variant hunt.
- **Matched controls before mechanism claims:** a new ingredient is credited only against a same-construction control lacking it (business: matched CBOP controls, coverage-matched controls); construction changes without matched controls cannot be decomposed and must be disclosed as such.

**0.5.3 How sol picks the next trajectories (end-to-end, one generation boundary).**
`ledger + catalog + frontier` → (deterministic) trajectory scores & status board → sol-xhigh writes the **direction summary** and the **ranked next-generation proposal**: which frontier trajectories to keep refining, which two+ parents to recombine (with the scientific rationale for why the combination could work where each parent stalled), which `failed_but_recoverable` lines to repair, which `unexplored` directions to open, and what to prune — each item citing node/direction IDs and the recorded evidence → incumbent **policy code** converts the proposal + budget into the executed action sequence (§0.4.5) → runs execute → extraction updates the catalog → sol-high reviews the generation to ≥ 90 → `GENERATIONS.md` entry + trace-pool append. The loop therefore always generates from the full tried history: nothing is proposed without lineage, nothing survives without battery numbers, and nothing is forgotten — failures remain searchable evidence for every future generation.

### 0.6 Autonomy, unstick protocol & terminal determination (user-mandated)

- **Continue autonomously.** The executor does not stop for routine decisions, failed generations, retained incumbents, or negative results. Work proceeds generation after generation within the resource envelope until a terminal determination (below) is reached. The only legitimate pauses are: (a) a hard authorization gate (missing credential, spending authority, unavailable required file — spec §2), (b) budget/ceiling exhaustion, or (c) explicit user stop. "No promising direction right now" is **not** a stopping condition — it triggers the unstick protocol.
- **Unstick protocol (sol-xhigh):** whenever the executor is stuck — no legal next action is obvious, a gate fails unexpectedly, all live directions are `saturated`/`unpromising`/`BLOCKED-DATA`, results contradict each other, or the same failure recurs twice — it **must** invoke `gpt-6.1-sol` at `xhigh` with the full state packet (STATUS, catalog, frontier, last 3 generation entries, exact blocker + what was tried) and request: ranked unblock options, the cheapest discriminating experiment for each, and a recommended next generation SPEC. The executor verifies the recommendation against the locked contract (sol-xhigh cannot authorize contract changes, ceiling increases, final-outcome access, or standard-lowering), records the consultation + disposition in the ledger, and **continues working** on the best legal option. If sol-xhigh's options are all illegal/infeasible, iterate the consultation with the rejection reasons included (max 3 rounds), then take the smallest legal evidence-gathering action available (data audit, diagnostic, literature check) rather than idling. Business-loop precedent: sol-xhigh's ranked-hypothesis + negative-EV pivot judgments (Gen5/Gen6) redirected the search instead of ending it.
- **Terminal determination (sol-xhigh as judge, evidence as law):** the campaign ends only when `gpt-6.1-sol` at `xhigh`, given the complete evidence package (ledgers, contract + both locks, atlas, battery results, policy comparison, reproduction report, review trail), **determines that the goal has been satisfied** — i.e. certifies in writing, gate by gate (C1–C13), that documentary evidence supports a `COMPLETE_*` terminal state, with a 0–100 score ≥ 90 and zero unresolved high/critical objections. Sol-xhigh's determination is necessary **in addition to**, never instead of, the evidence: it may not waive a gate, accept missing artifacts, or reinterpret insufficient evidence as success (spec §1/§12/§14 bind the judge too). If sol-xhigh finds gates unmet, its output becomes the next mandate list and the loop continues. If the campaign hits budget exhaustion or a hard blocker first, sol-xhigh instead certifies the honest non-complete terminal state + exact unmet gates + smallest concrete next step. Either way, **no self-declared completion**: the executor never marks the goal satisfied on its own authority.

---

## Phase 0 — Bootstrap & provenance skeleton (Gate G0)

**Do:**
1. Create `cancer-dependency-rsi/` with: `README.md`, `GOAL.md` (copy/symlink policy: canonical copy + hash), `PROTOCOL.md` (stub → filled at Lock 1), `STATUS.md` + `status.json`, `config/resources.json`, `src/` (adapters, baselines, evaluator, policies, replay, runner, budget), `data/` (cache + manifests), `ledger/`, `reviews/`, `artifacts/`, `tests/`, `manuscript/`. Init git; commit scaffold separately from science.
2. Create project Python env (`cancer-dependency-rsi/.venv`, `uv` or `python3 -m venv`), pin deps (`pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `pyarrow`, `pydantic`, `pytest`, `httpx`); write lockfile. Verify `pytest` green on placeholder tests (score-direction, grouping, cost-accounting stubs).
3. Implement the **budget wrapper + ledger writer + hashing utilities first** (they gate everything else) and the CLI skeleton: `bootstrap, audit-data, reproduce-baselines, run-pilot, run-cycle, evaluate-policy, lock-science, evaluate-external, reproduce, status, resume` (initially `status`/`resume` functional, others fail loudly with "not yet unlocked: <gate>").
4. Record host fingerprint (CPU/RAM/disk/OS, Python, codex version, model IDs) into `config/host.json` **without printing secrets**.

**Gate G0:** `status` prints phase/incumbent/spend/next-action/resume; ledgers append + verify; resource config enforced on a dummy job (timeout + RSS ceiling demonstrably kill an over-budget job). Review (sol-high) ≥ 90 on scaffold + config.

---

## Phase 1 — Source verification & data/identifiability audit (Gate G1 → C1–C3)

**Do (verify, never assume — every seed is a claim until checked against the primary source):**
1. **Read methods + data availability + supplements** for S1 (Broad NextGen, PMC13581591 / doi:10.1038/s41586-026-10843-7), S2 (Sanger organoids, PMC13581617 / doi:10.1038/s41586-026-10830-y), S3 (Oct 2026 transferability study, PMC13664187 / doi:10.3390/biology15191782 + Zenodo 22472622 code), S5 (Dream-RSI, arXiv:2609.14858 + google-research/dream-rsi). Extract: exact environmental design (screens × models × contrasts), gene-selection rule, score definitions/directions, QC flags, reported lipid/adhesion/state findings (= controls, not discoveries).
2. **Resolve current data routes via official manifests only** (DepMap 26Q3 data page + forum guidance; figshare 29472362 / 28339340; Cell Model Passports; Sanger DataMiner docs). For each file actually retrieved: source URL, release/commit, retrieval date, license, bytes, SHA-256 → `data/source_manifest.csv`. **Never invent a download URL/file ID.** If a portal blocks unattended retrieval, use official alternatives; never bypass a challenge. Prefer **study-specific releases** over the integrated 26Q3 release for development (audit whether 26Q3 corrections used external outcomes; if so, rebuild development-only or treat claims as transductive with limited wording).
3. **Build the provenance table + crosswalk:** biological model, donor, lineage, sample origin, lab, library, medium, format, replicate, release, outcome — across Broad/HCMI/Sanger/author IDs (`data/model_crosswalk.csv`). Uncertain donor identity ⇒ `uncertain`, never assumed independent. **Count independent models/donors**; verify the seed counts (147 Broad screens; 162 Sanger organoids; environmental panel: 250 genes × 18 screens × **7 models**, 7 format + 5 medium matched contrasts) against row-level data; record attrition (models that failed to grow, genes dropped) in `data/eligibility_registry.csv`.
4. **Assay audit per source:** Chronos vs Sanger fitness — direction, dynamic range, controls, missingness, QC. Confirm paired row-level outcomes + replicates + metadata actually exist for the intended contrasts; if a required pairing is not released, record it as a blocker **before** modeling. Check lab↔biology confounding explicitly (a batch correction cannot separate confounded effects).
5. **Novelty audit v1 (claim ledger):** dated literature search with preserved queries/exclusions (`reviews/novelty_audit.md` + `ledger/claims.jsonl`). For each candidate claim: nearest prior result, what's established, precise remaining uncertainty, evidence needed, consequence if supported/refuted. Explicitly rule out: generic 2D→organoid transfer, published environmental/biomarker findings.

**Gate G1 (identifiability):** a **named, falsifiable question in a named subset** with counted independent units and a documented paired contrast (or a documented narrower question within the same objective if the original is unsupported — broader goal then recorded unmet for that component). No adaptive search before G1. Sol-high review ≥ 90 on provenance package + novelty audit.

---

## Phase 2 — Smallest valid vertical slice + baselines + Lock 1 (Gate G2 → C4–C5)

**Do:**
1. **Estimators (development data only):** paired within-model environmental contrasts in original units (report both conditions, **all individual paired changes**, uncertainty, heterogeneity — a near-zero mean hiding opposing effects must be visible); transfer models with preprocessing/feature selection/tuning **inside development folds only**; uncertainty clustered at donor/model level with effective sample sizes (few clusters ⇒ justify or downgrade the interval/test).
2. **Baselines (same eligible rows, same permitted info):** lineage-only; genotype-only; state/expression-only; genotype+state; +context/assay covariates; regularized linear predictor modeled on the S3 transfer study (reproduce from its Zenodo code where possible). Compare against the **strongest** baseline; prespecify the environmental-information **ablation**. Reproduction needing final outcomes is deferred until after Lock 2.
3. **Evaluator (fixed, separate module, narrow interface):** scores artifacts by effect sizes + calibrated predictive/uncertainty endpoints on development panels. **Never** rewards p-value size, discovery count, or narrative confidence. Includes validity diagnostics + invalid-result rules (leakage, direction flips, support violations ⇒ `invalid`, not zero).
4. **Lock 1 — freeze the research contract** (`PROTOCOL.md` + `contract.json`, SHA-256 hashed with evaluator code + split manifests): exact question + falsifiable alternatives; population/environments/targets/generalization; eligibility; data/ID versions; **A/B/C partitions** (development / reserved policy / final external — donor/model-blocked, overlap recorded); feature & transformation rules; primary/secondary endpoints with fixed direction; practical-effect / equivalence margins with justification (no defensible margin ⇒ no "invariant" label, continuous effects only); multiplicity (default: Holm, familywise α=0.05, small confirmatory family) + uncertainty methods; baselines; invalid rules; success/failure/inconclusive/budget-exhaustion conditions; policy endpoint choice (§7.3). Changing a locked contract ⇒ **new study ID** + new evaluation evidence.
5. **Tests:** identity leakage (donor overlap across A/B/C fails the build), score direction, grouping integrity, estimator behavior on synthetic known-effects (code/calibration only), cost accounting, resume idempotence, unsupported-replay handling, final-outcome access guard (C-layer paths unreadable by proposer code paths; access attempts logged).

**Gate G2:** baselines reproduced on development data closely enough to establish direction/cohort/measurement integrity (discrepancies resolved or bounded in writing); contract + evaluator + splits hashed and committed. Sol-high review ≥ 90 on contract + evaluator + tests. **No policy optimization before G2.**

---

## Phase 3 — Pilot: fixed policy → first replay world (Gate G3 → C13 started)

**Do:**
1. Define the **initial fixed exploration policy** as an executable module: `policy(history, legal_actions, remaining_budget) → action`. Legal actions: open a predefined analysis family, choose a branch, refine an artifact, run a permitted diagnostic, stop. Policy can alter branching/prioritization/explore-vs-refine/stopping — **never** labels, splits, metrics, margins, corrections, success criteria.
2. Run it on real development tasks to the pilot target: **24 evaluated nodes** (generator = sol-xhigh for candidate generation; evaluator fixed; every node ledgered with full hashes + costs + failures). Environmental sensitivity estimates carry uncertainty downstream via a justified measurement-error/resampling/sensitivity treatment — noisy estimates are never treated as exact.
3. Freeze the resulting discovery trees as **Replay World v1** (immutable snapshot + manifest). Replay engine rules: reveal only recorded outcomes along the trajectory; refinement requires immutable parent + **exact context-hash match** (else `unsupported`); never invent counterfactual outcomes; compare policies on **common support** and report support coverage.

**Gate G3:** 24 real nodes committed (or precise blocker recorded), replay world hashed, support-coverage report written. **First substantive report** issued here (see §9). Sol-high review ≥ 90.

---

## Phase 4 — Policy-improvement cycles (Gate G4 → C8)

Each cycle below is executed as one or more **generations** under the §0.5 protocol (SPEC-hash → enumerate → screen → recombine → battery → verdict → sol-high ≥ 90 → `GENERATIONS.md` entry). Repeat per cycle (≥ 2 genuine cycles; promotions not required — retained incumbent is a valid outcome):
1. **Generate ≥ 3 executable challengers** with sol-xhigh (+ unchanged incumbent = 4-way comparison). Challengers are code, not narratives; a reflection that changes no executed decision is not a challenger.
2. **Replay** all four under identical resource constraints + support rules on the current replay world (development histories only; final Sanger outcomes never enter the pool).
3. **Select** by the frozen selection rule; **fresh-rollout test** the selected challenger vs fixed exploration (same generator, same evaluator, same ceilings). Charge rewriting + replay + failures + promotion trials to the improving system; baselines may spend the equivalent on search.
4. **Promote only** if the preregistered criterion is met; otherwise **retain incumbent** and keep failed challengers in the ledger. Append only development histories; rebuild replay world version.
5. If replay support is inadequate: preserve that finding, judge by fresh rollouts, and label the method **"Dream-RSI-inspired adaptation"** with departures disclosed.

**Gate G4:** ≥ 2 cycles fully ledgered (challengers, replay results incl. unsupported rates, rollout comparisons, promotion/retention decisions with reasons). Sol-high review ≥ 90 per cycle record.

---

## Phase 5 — Reserved policy evaluation (Gate G5 → C9)

1. Freeze the best admissible policy + selection criterion **before** touching Layer-B panels. Compare: learned policy vs original fixed exploration vs ≥1 fixed-allocation/random strategy — same generator, evaluator, initial artifacts, information permissions, ceilings; blocked panels with recorded model/donor/gene/pathway overlap (splits of the 250 genes are **not** hundreds of independent tasks).
2. **Primary endpoint (locked at Lock 1):** default = total measured cost to reach a predeclared scientific-quality threshold (threshold set from development evidence, attainable by competent baselines). Ambitious target: **≥ 20% lower total cost vs strongest fixed baseline, one-sided 95% lower bound ≥ 20%** (point estimate > 20% with lower bound merely > 0 = "some improvement", **not** C9). Non-attainment within budget = censored per frozen rule, never an invented exact cost. Report full quality-vs-cost curves + both end-to-end (incl. learning overhead) and deployment-only views. Seeds quantify execution variability, not biological replication.
3. **Cost-measurability rule:** if host-model cost is material and unmeasurable, C9 cannot be certified on a CPU/token proxy — record `policy_improvement: unresolved_cost_gate` and report the alternative locked endpoint honestly. Never switch endpoints after seeing results.

**Gate G5:** frozen-policy comparison complete with uncertainty; C9 marked met / not-met / unresolved with evidence. Sol-high review ≥ 90.

---

## Phase 6 — Lock 2 & single external evaluation (Gate G6 → C6, C10)

1. **Lock 2:** commit exact claim family (bounded, predeclared — gene classes with measured sensitivity + adequate overlap, not an unconstrained scan), predictions, fitted artifacts, inferential code + hashes (`lock-science`). Repeat the novelty audit for each surviving exact claim.
2. **Evaluate once** on Layer C (independently filtered Sanger cohort after donor-overlap/provenance/assay/representation checks) via `evaluate-external`. State precisely which component each dataset validates: transfer confirmation ≠ medium/format validation ≠ causal mediation. If the claim needs independent environmental confirmation and no suitable public controlled-environment dataset exists, **narrow the claim or keep the gate unmet** — never split genes from the same 7 models to fake independence. Word as **retrospective** external validation (pretraining/literature exposure recorded).
3. **Adversarial battery (prespecified):** multiplicity correction as locked; donor/lineage sensitivity; platform sensitivity; leave-one-model-out; negative controls; leakage checks; grouping-respecting permutations only; environmental ablation. Invariance claims require positive dependency evidence **and** interval-inside-margin equivalence evidence. Conclusions that flip across plausible sensitivity estimates are reported as fragile.

**Gate G6:** each locked claim marked supported / refuted / inconclusive under frozen rules. A failed test stays failed. Sol-high adversarial review ≥ 90 (reviewer explicitly tasked with trying to kill each claim).

---

## Phase 7 — Atlas, manuscript & reproducibility package (Gate G7 → C7, C11–C12)

1. **Evidence atlas** (`atlas/evidence_atlas.parquet` + CSV): every eligible panel gene — dependency strength (both conditions), environmental change, uncertainty, heterogeneity, biomarker evidence, transfer evidence, prior knowledge, missingness; every excluded gene with reason. Expansion beyond the 250-gene panel labeled exploratory.
2. **Manuscript** (`manuscript/`): question, estimands, provenance, contract history (both locks), baselines, results incl. failures, policy-loop results incl. retained incumbents, limitations (7-model design, selected genes, assay non-interchangeability, retrospective validation, cost measurability), terminal state + unmet gates. No clinical-efficacy/safety claims from screens alone.
3. **Clean reproduction** (`reproduce`): fresh checkout + env from lockfile regenerates primary estimates, figures, atlas decisions, and policy comparison within documented tolerances **without rerunning stochastic LLM search** (frozen artifacts + deterministic code only). Emit `reproducibility_report.md` with tolerances + diffs.

**Gate G7:** reproduction green; package complete per §8 inventory. Sol-high review ≥ 90 on manuscript + atlas + reproduction report. **Then** assign the terminal state (both `COMPLETE_*` states require C1–C13 incl. C9; otherwise the honest state + unmet-gate list).

---

## 8. Artifact & command inventory (acceptance checklist)

**Files:** `README.md` · `GOAL.md` · `PROTOCOL.md` + `contract.json` (hashed) · `STATUS.md` + `status.json` · `GENERATIONS.md` (append-only generation ledger, §0.5) · `generations/genNNN/{SPEC.md,screen/,battery/,sol-review-*.txt}` · `directions/{catalog.json,history/iterNNN.json,extraction/*.jsonl,summaries/}` · `trace_pool/<round>/` + `manifest.json` (frozen replay worlds) · `data/{source_manifest,model_crosswalk,eligibility_registry,split_manifest_*}` · `ledger/{claims,experiments,resources,reviews}` · `src/{adapters,baselines,evaluator,policies,replay,runner,budget}` (evaluator/engine versions preserved side-by-side) · immutable `artifacts/` + checksums · frozen predictions/models/policies · `atlas/evidence_atlas.*` · figures · `manuscript/` + limitations + adversarial-review report · env lock + licenses/attribution · `reproducibility_report.md` · `tests/` (leakage, direction, grouping, estimator, cost, resume, replay-support, final-access, anchor-regression, lineage/DAG integrity, catalog-schema validation).

**Commands (each documented in README, each ledgering its run):**
`bootstrap` → `audit-data` → `reproduce-baselines` → `run-pilot` → `run-cycle` → `evaluate-policy` → `lock-science` → `evaluate-external` → `reproduce` · `status` · `resume`. Commands refuse out-of-order execution by gate (e.g., `run-cycle` before G2, `evaluate-external` before Lock 2) with the missing gate named.

## 9. Reporting cadence

- **First substantive report (at G3):** verified data (manifest + counts), identifiable first question, baseline results, real experiments completed (node count + outcomes), replay support (coverage + unsupported rate), policy retained/promoted, measured resource use (incl. `unknown` costs), next discriminating experiment, exact resume command. If a gate blocks the first cycle: the precise blocker + all completed independent work. Never claim the loop "started" on scaffolding alone.
- **Per-phase:** measured results, unresolved risks, next discriminating experiment. No progress theater (file counts, unexecuted plans).
- **Final:** terminal state, C1–C13 evidence table, three separate status fields, full costs + failures.

## 10. Risks & precommitted responses

| Risk | Precommitted response |
|---|---|
| Paired environmental outcomes not actually released at row level | Stop at G1; document narrower identifiable question; do not model the missing contrast |
| 7 models ⇒ underpowered / non-identifiable environmental claim | Report continuous effects + heterogeneity; claim only refutations/bounds the precision supports; seek additional public controlled-environment data or keep gate unmet |
| Donor overlap Broad↔Sanger destroys "independent" cohort | Crosswalk-driven filtering; if independence unattainable, downgrade wording + claim scope; never assume independence |
| Integrated-release leakage (outcome-guided corrections) | Study-specific releases + development-fitted transforms; else transductive disclosure with limited claims |
| Assay mismatch (Chronos vs Sanger scores) | Within-study contrasts in original units; cross-study via justified rank/calibration only |
| Replay support too thin to screen challengers | Fresh rollouts decide; label Dream-RSI-inspired adaptation; disclose departures |
| Host-model costs unmeasurable | C9 stays `unresolved_cost_gate`; no all-in savings claim; CPU/token proxies reported separately |
| Portal blocks unattended download | Official alternative routes; documented local-cache install; never bypass access controls |
| Reviewer score stalls < 90 | Fix verified issues only; if reviewer demands scope the spec forbids, record rejection with spec citation; escalate genuine conflicts to the user |
| Budget/time exhausted mid-campaign | Checkpoint, `BUDGET_EXHAUSTED` + unmet gates + smallest concrete next step; never auto-raise ceilings |

## 11. Immediate next actions (in order)

1. `create_goal` with the GOAL.md objective verbatim; scaffold per Phase 0; commit.
2. Phase 1 source verification: fetch S1/S2/S3/S5 methods + supplements; draft provenance table skeleton; resolve DepMap 26Q3 vs study-specific file routes from official manifests (record, don't guess).
3. First data pull (smallest processed files that prove pairing + score direction), checksum into manifest; run direction/QC smoke checks.
4. G1 review (sol-high, ≥ 90) → Phase 2 baselines → Lock 1 → pilot.
