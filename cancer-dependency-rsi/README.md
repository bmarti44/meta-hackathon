# Cancer dependency RSI

Research into measured culture-context dependency lability and retrospective dependency transfer, with a separately evaluated research-policy loop. The authoritative specification is `../cancer_rsi_handoff.txt`; the locked objective and execution plan are `../GOAL.md` and `../PLAN.md`.

**Current state:** scientific Lock-S external evaluation has executed exactly once (archived BOUND under 144 covariate-ID groups = 142 patients; patient-weighted effects unquantified). Evidence atlas v4 complete; C1/C6/C7/C10/C11/C12 PARTIAL, C5/C3 met-narrowed per reviews, C4/C8/C9/C13 unmet. Sol-xhigh ruled ENDPOINT:NO / PGEN004:NO_GO; policy generations pgen001-003 + scientific sgen001-002 recorded in GENERATIONS.md. No policy cycle has run. See STATUS.md / status.json for live state and resume command.

The prescribed Codex/Sol route now works after the user repaired permissions. Earlier initialization failures are preserved as history. Sol-xhigh returned a diagnostic-only recommendation; genuine task feasibility and independent reviews are in progress. No alternate model interface is needed. The external-outcome quarantine remains in force.

## Local commands

From this directory, the existing environment is `.venv` with `uv.lock` and `requirements-lock.txt`. No installation is needed to run the current checks.

```sh
.venv/bin/python -m pytest -q
.venv/bin/python src/cli.py status
.venv/bin/python src/cli.py resume
```

Scientific/policy commands remain gate-locked and fail explicitly. The block below is HISTORICAL (pre-Lock-S); live next action is in status.json. The historical next host-model call was:

```sh
.venv/bin/python src/model_call.py reviews/prompts/g2_unstick_xhigh_1.txt reviews/g2_unstick_xhigh_1_retry2.md --effort xhigh
```

The example output ID is historical and already used; do not redispatch it. The output ID is immutable. Completed or interrupted calls are not redispatched automatically; inspect their event files and receipt and reconcile before proceeding. This call only consults on the unresolved pre-Lock1 uncertainty design; it does not grant G2 or authorize a pilot. Implement legal recommendations, close the remaining OPEN review items, run acceptance tests, and obtain the mandated Sol-high >=90 review before freezing.

The fixed Layer-A readiness diagnostic is `src/g2_safety_probes.py` with retained specification/results in `reviews/`. It has already run and refuses to overwrite its result. Its twelve evaluator calls are **not** a policy cycle or independent biological evidence. Original v2 evaluator bytes are retained with a verified content hash; the unapproved candidate is `src/evaluator_v3.py`.

## Evidence and limits

Published author OLS coefficients reproduce on the released 1,000-gene minipool matrix (worst discrepancy 1.7316e-8). There are six measured models with paired format contrasts, not six verified independent donors. The prospective external endpoint is an association conditional on 207 fixed genes; it does not identify clinical efficacy or a biological mechanism.

HISTORICAL (pre-Lock-S): diagnostics then used Layer-A only. The single locked external evaluation has since executed exactly once (Lock-S); C is spent and evaluate-external now refuses re-execution. Source/data manifests and exposure records live in `data/`. No fresh downloads or separately metered API spending were incurred during this continuation. Host-model monetary costs and historical resource usage remain unknown, so C9 cannot be certified. `ledger/resources.jsonl` records new reservations, failures and reconciliations; historical omissions are disclosed rather than filled with invented measurements.

The project is not complete. Separate scientific, prediction and policy statuses and the exact remaining work are in `status.json` and `STATUS.md`. A clean-room reproduction package, atlas, manuscript and real policy-improvement cycles remain outstanding.

## Provisional atlas and cache audit

`atlas/v4/` is the current completed atlas (250 genes, source-linked dispositions); `atlas/provisional_v1/` is its retained predecessor. `atlas/provisional_v1/genes.csv` inventories all 250 panel genes (historical note); `paired_observations.csv` retains 3,000 original-unit paired observations. `exclusions.csv` lists all 43 confirmatory exclusions. Uncertainty and external-evidence gaps are explicit. These are provisional pre-lock artifacts, not a supported discovery or a completed C7.

`reviews/data_integrity_audit_v2.json` verifies cached release hashes and the 148-model/144-donor metadata cohort. The new `data/split_manifest.json` separates unique donor IDs from the explicit sample-to-donor map; the original approved membership is unchanged and prior manifest bytes are preserved.

`reviews/atlas_component_reproduction_v2.json` records byte-identical regeneration of the atlas CSVs from copied source/inputs, using the existing locked environment and zero model calls. This is component reproduction, not a full C11 clean-room run. New independent audit outputs can be generated with an unused report path:

```sh
.venv/bin/python src/audit_data.py --output reviews/data_integrity_audit_next.json
.venv/bin/python src/reproduce_atlas.py --atlas atlas/provisional_v1 --report reviews/atlas_component_reproduction_next.json
```

The earlier interface-change question was superseded by runtime repair. The prescribed CLI route is used; every scientific gate remains in force.

## Current numerical readiness

The unscored evaluator is `src/evaluator_v4.py`. `src/confirmatory_estimand.py` and `src/donor_kernel.py` implement the fixed external donor estimand as pure-array code; they do not load external outcomes. Scale-relative degeneracy, exact tied-rank displacement, nested-donor grouping and failed-replicate guards have explicit tests.

Frozen synthetic diagnosticv1 failed its constant-input guard; correctedv2 retained the exact same arrays/seeds/thresholds and passed (95/100 null coverage;97/100 at knownrho0.6). See `diagnostics/donor_calibration_v2/results.json`. This is a code diagnostic, not biological evidence or certification of nominal real-world coverage. Current complete suite:52tests pass.

Resource supervision uses a process-group RSS watchdog at50ms intervals and75% of reserved memory, with25% headroom; it is not a hard OS allocation barrier. The scientific600s job ceiling is enforced separately from the recorded1200s host-reasoning allowance. All campaign ceilings remain unchanged.

The old nine-panel policy design was withdrawn as contradictory and nonexecutable. New admissible data/task, useful quality endpoint, coherent comparison design and a passing G2 review are still required. No null-q/synthetic reward may be used to fabricate a policy cycle.
