# STATUS — cancer-dependency-rsi

- **Phase:** 0 (bootstrap) — founding documents under sol-high review (target ≥ 90)
- **Incumbent policy:** none yet (hand-designed fixed exploration to be defined at Lock 1 / Phase 3)
- **Spend:** $0 additional API (cap $0); host/codex costs unmeasurable → `unknown` (C9 unresolved-cost gate noted)
- **Separate status fields:** `scientific_discovery: not_started` · `prediction_improvement: not_started` · `policy_improvement: not_started`
- **Unmet gates:** C1–C13 all unmet (no evidence yet). Loop has **not** started — scaffolding only; no real experiment has run.
- **Verified so far (2026-10-28):** host = Apple M5 Max / 18 cores / 128 GB / macOS 26.6 / Python 3.14.8; codex configured `gpt-6.1-sol`; 8/8 seed URLs HTTP 200 (reachability only — methods/content verification is Phase 1).
- **Next action:** finish sol-high review loop on PLAN.md/GOAL.md to ≥ 90 → Phase 0 env + budget/ledger/health code → Phase 1 source verification (S1/S2/S3/S5 methods) + official-manifest data-route resolution.
- **Resume command:** `cd /Users/bmarti44/github/bufferright/research && cat PLAN.md GOAL.md cancer-dependency-rsi/STATUS.md` then continue from "Next action" above; goal is registered in the goal tool (objective in GOAL.md).
- **Autonomy rule:** continue generation after generation; when stuck invoke sol-xhigh unstick protocol (PLAN §0.6); goal satisfied only on sol-xhigh gate-by-gate determination vs C1–C13 evidence.

## Update 2026-10-28 (Phase 1 in progress; PLAN v2 under review r3)
- Review trail: v1 = 53/100 (35 issues, all verified+fixed in v2). Round 3 running.
- Measured: minipool 7 models/18 screens/5+7 matched contrasts; direction vs published r=0.91/0.96; heterogeneity 91-98% sign-flipping genes.
- Data on disk (manifested+hashed): Broad minipool set (Layer-A); Sanger BAGEL+covariates (quarantined; de-minimis structural glimpse logged in data/exposure_log.jsonl).
- Open: ACH-003052 lineage, HCM-SANG<->ACH crosswalk, genome-wide Layer-A import, novelty audit v1 written (reviews/novelty_audit_v1.md) awaiting G1 review.
- Loop NOT started (no policy cycle yet). C1-C13 unmet. Next: r3 >=90 -> G0 completion -> G1 gate review -> Phase 2/Lock 1.

## Update 2026-10-28b — PLAN APPROVED 92/100
- Sol-high trail: 53 -> 76 -> 86 -> 92 (zero high/critical open). Approved PLAN sha256 5e4e6051bd2e... Residuals: reviews/lock1_residuals.md (binding at Lock 1/comparison).
- Next action: Gate G1 review (sol-high on data/provenance_v1.md + reviews/novelty_audit_v1.md + reviews/g1_question_candidate.md + identifiability_audit) -> G1 closure -> Phase 2.

## Update 2026-10-28c — G1 remediation v2 under re-review
- G1 round 1: 56 FAIL. All reviewer checkable claims independently verified TRUE. Heterogeneity claim retracted; counts corrected (medium 4 models, format 6).
- Sol-xhigh unstick: six-model format route; selection overlap 26/250 independently reproduced -> 223 joined eligible genes.
- Exploratory feasibility ONLY: rho(L,T)=0.167, partial 0.086; a BOUND (delta=0.20 candidate) may be feasible, a SIGNAL claim is not promised.
- Exposure adjudicated: 0 organoid outcomes seen (6 glimpsed IDs are 2D lines). Manifests completed+pinned (figshare v1 both). Audit regenerates fully (5 tests green).
- G1 re-review (sol-high) RUNNING on v2 package. Loop still not started; C1-C13 unmet.

## Update 2026-10-28d — GATE G1 PASS-WITH-NARROWING (90/100)
- Approved question: across fixed 207-gene panel, is measured format lability (6 Broad models) associated with donor-averaged displacement from fixed 2D consensus ordering in metadata-filtered Sanger cohort (148 organoids/144 donors)?
- Binding Lock-1 corrections recorded in provenance_v3_addendum (Table-6 graph correction, library rule, null-calibrated displacement sensitivity, uncertainty target, delta wording, missing-cell registry).
- Next: Phase 2 (estimators/baselines/evaluator/tests) -> Lock 1 -> pilot E0. Loop not started; C1 partially evidenced (question+narrowing), C2/C3 substantially evidenced pending Lock-1 freeze; C4-C13 unmet.

## Update 2026-10-28e — Phase 2 started: C5 minipool baseline EXACT
- Authors' OLS design recovered from DepMap-NextGen-Public @5c6f1e0 (model fixed effects + format + serum + interaction). Reproduction from released Chronos matrix: max |diff| < 1e-8 on all environmental coefficients (src/baseline_ols.py + test; 6 tests green). Earlier no-FE fit (r=0.87-0.95) superseded — discrepancy resolved, not merely bounded.
- Next: estimators/baselines/evaluator build -> Lock 1 draft -> sol-high G2 review.

## Update 2026-10-28f — resumed goal; G2 safety remediation; required model interface unavailable

- The root GOAL objective has been registered verbatim in the current goal tool. It remains active and **not achieved**.
- Latest preexisting G2 review: **round 2 = 74/100 FAIL** (round 1 = 54). Lock1 is still a draft. All issue dispositions and the precise next mandate are in `reviews/g2_r2_dispositions_v1.md`.
- Implemented and locally verified: atomic budget transactions with real cross-process/thread contention tests; total/phase accounting and terminal reserve; reconciliation validation; raw nonfinite guards; exact frozen gene membership; failure-class dominance and recovery from `dead`; parent-object DAG compatibility. These repairs still await the required independent re-review.
- **30/30 tests passed** after evaluator-version separation and added launch-failure/resume checks (6.80 s pytest time; ledgered bounded invocation 7.05 s).
- Fixed diagnostic actually executed: six prelisted E0 root configs x retired-v2/safety-v3 = 12 Layer-A evaluator calls, same seed, no optimization. Retired v2 called all six valid; five have diagnostic null coverage only 64–80%, and one has 96%. The safety draft rejects those five. The sixth clears this diagnostic only; all six remain inadmissible for policy use. Results: `reviews/g2_safety_probe_results_v1.json` (38.84 s wall, 39.28 s CPU, peak RSS 179,830,784 bytes). This is a readiness diagnostic, **not** a pilot/cycle or calibration certificate. v3 remains `admissible_for_policy=false` on every result; a justified calibration target/design is still required.
- Original v2 evaluator bytes retained and SHA-verified in `src/evaluator_v2.py` and the content-addressed artifact store; v3 remains an unapproved draft. v1/v2 quality scores are invalidated for policy selection. No prior policy outcomes exist to invalidate.
- **C5 wording correction:** all environmental OLS terms reproduce within 1.7316e-8 (interaction is the maximum), not <1e-8 as the earlier update stated. The exact baseline test remains green.
- Required xhigh unstick consultation was attempted through the mandated host/codex interface; both installed 0.165.0 and 0.164.0 fail before a model response with `failed to initialize in-process app-server client: Operation not permitted (os error 1)`. Failed attempt logs/reservations retained and reconciled. No Sol recommendation or passing re-review is claimed. Further identical retries are not useful inside this permission context.
- Resource limitation found: macOS rejects this wrapper's address-space cap. CPU-heavy bounded jobs now fail closed on that launch failure instead of silently ignoring it; timeout-only utility/test dispatch works. Working scientific memory-enforcement acceptance remains open. The small readiness diagnostic reports measured peak RSS separately; no CPU-heavy campaign job was dispatched.
- External validation outcome values were not accessed. No fresh downloads. Additional metered API spend remains $0; host USD unknown. Historical work predating the new resource ledger remains unmeasured, not backfilled.
- **Separate statuses:** `scientific_discovery: exploratory_only_unconfirmed` · `prediction_improvement: not_evaluated_no_prediction_claim` · `policy_improvement: not_started`.
- **Completion:** no `COMPLETE_*` determination; C1–C3 have partial/substantial evidence, C5 has its exact baseline anchor, C4 and C6–C13 remain unmet; C9 retains unresolved host costs and lack of independent reserved biological panels. Gate-by-gate final adjudication has not run.
- **Next action:** execute the retained xhigh consultation in an authorized host terminal, implement the legal uncertainty redesign and OPEN G2 remediations, run the remaining acceptance suite, and obtain Sol-high G2 >=90 with zero unresolved high/critical before locking or piloting.
- **Exact resume:** `cd /Users/bmarti44/github/bufferright/research/cancer-dependency-rsi && .venv/bin/python src/cli.py resume`. Next consultation (new immutable attempt ID): `.venv/bin/python src/model_call.py reviews/prompts/g2_unstick_xhigh_1.txt reviews/g2_unstick_xhigh_1_retry2.md --effort xhigh`. This is not a permission waiver or a passing G2.

## Update 2026-10-28g — provisional atlas and reproducible metadata audit

- Previous and current goal turns classify as **progress**: new evidence/artifacts, not status-only restatements. Goal remains active and incomplete; the same required model-interface blocker is observed across two visible goal turns. No positive completion or terminal determination is claimed.
- Built `atlas/provisional_v1/genes.csv` with all 250 selected genes and explicit evidence gaps; retained 3,000 individual paired measurements in `paired_observations.csv` (7 format and 5 medium contrasts per gene). Exclusion registry covers 43 confirmatory exclusions; development-primary=216 and confirmatory=207. No inferential CI, novelty, mechanistic, vulnerability or equivalence claim is inferred from this inventory. C7 is partially implemented, not complete.
- Data/cache audit PASS: all pinned source/manifest entries verify; cohort regenerates from metadata as 178 library screens / 162 models -> 148 eligible models / 144 donors. Raw outcomes were never parsed; opaque checksum access to C containers was logged. The first auditor's false duplicate-library flags are preserved and corrected in audit v2.
- Metadata representation corrected without changing membership: original split `donor_ids` was a 148-entry per-model list with 144 unique values. New pre-lock v2 has exactly 144 unique donor IDs plus explicit `sample_to_donor` for all 148 unchanged models; all assignments verified against the original. Prior split/data manifests are archived; the future Lock1 must hash the new representation.
- Provisional atlas component reproduced byte-identical CSVs in an isolated input/source copy, no stochastic model call (`reviews/atlas_component_reproduction_v2.json`). Current environment reused; full clean-room C11 remains unmet. Reproduction v1's overstrong boundary label is withdrawn: no external files were copied, but the subprocess is not filesystem-sandboxed.
- **35 tests passed** in 8.47 s (bounded ledgered invocation 8.80 s), including unequal model/pair weighting, exact panel counts, pinned exposure-prefix integrity, donor mapping and overlap rejection.
- Official OpenAI Docs workflow checked normal exec/ephemeral/JSON interfaces; no verified initialization remedy was established for the observed permission error. No permissions broadened, no provider changed, no credentials relocated. No identical model-launch retry was spent.
- **Pending user choice:** may the same mandated Sol models/efforts run through built-in agents instead of `codex exec`? This is a route change to GOAL.md Model routing / PLAN §0.1. Until an actual answer arrives, no substitution or agent spawning is authorized. The exact CLI route remains available only through a host context that can initialize it.
- Separate statuses unchanged: scientific_discovery=exploratory_only_unconfirmed; prediction_improvement=not_evaluated_no_prediction_claim; policy_improvement=not_started. No pilot, genuine policy cycle or external evaluation has run. C4/C6/C8–C10/C13 unmet; C1–C3/C5/C7/C11/C12 remain partial or awaiting final adjudication; C9 still has unknown host costs and no independent reserved biological evidence.
- Next: resolve model-interface choice, get xhigh uncertainty redesign, finish OPEN G2 issues and high review >=90 before freeze/pilot. Details: `reviews/continuation2_findings.md`. Resume: `.venv/bin/python src/cli.py resume` from this project directory.

## Update 2026-10-28h — mechanical BLOCKED checkpoint after three goal turns

- The previous turn was progress (atlas/data audit/component reproduction). This turn revalidated the same required model-interface failure without scientific progress. The blocker has persisted across three consecutive visible goal turns.
- Final bounded revalidation: `reviews/g2_unstick_xhigh_1_retry2.receipt.json`, returncode1, 0.260 s wall, no model response; stderr again reports in-process app-server initialization `Operation not permitted`. Three dispatched attempts are retained; no successful model response, no fresh outcome access, no additional metered spend. Identical retries stop here.
- No answer to the pending interface-choice question has arrived. Generic automatic continuation is not approval to replace the explicitly required CLI route. No agents spawned or protocol requirement waived.
- **Terminal checkpoint: BLOCKED (mechanical; goal not achieved).** Required Sol-xhigh terminal determination cannot execute through the same unavailable interface; GOAL permits this honest fallback, never positive completion. Gate-by-gate remaining evidence and exact next step are in `reviews/blocked_audit_v1.json`. C1–C13 have not been terminally certified; C5's exact baseline component is supported, while the complete scientific/policy goal remains unmet.
- No legal next step through uncertainty redesign/G2 review is executable without an interface/runtime change. Independent inventory/audit/reproduction work is preserved. The atlas remains provisional, 35 tests have passed, and no pilot, policy cycle or external evaluation has run.
- **Smallest next step:** answer the pending choice permitting built-in Sol models/efforts, or restore a permitted host context where `codex exec` initializes. After actual runtime repair, use a fresh immutable attempt ID (see status.json); do not reuse the failed retry2 output ID.
- Scientific discovery, prediction improvement and policy improvement remain separate and unchanged. All measured-job reservations are reconciled. No success claim, spend-cap increase or final-outcome access is authorized by this checkpoint.

## Update 2026-10-28i — resumed after permissions repair

- User reactivated the goal and changed the outer permission context. The prescribed `codex exec` route now initializes: live Sol-xhigh consultation has tool-execution events, wrapper PID97409, Codex PID97420, session65243 at the recorded heartbeat in status.json. The previous BLOCKED checkpoint is historical; no substitute interface is needed or authorized.
- Fresh blocked audit starts at zero after resume. Scientific gates, budgets and outcome quarantine remain unchanged. Next: finish consultation, implement legal uncertainty design and remaining G2 fixes, obtain required Sol-high review before Lock1/pilot.

## Update 2026-10-28j — Sol route restored; scientific task gate remains failed

- Initial initialized Sol-xhigh consultation exhausted600s; transcript retained. A focused full-state followup returned successfully (314.41s) using the recorded1200s host-reasoning allowance inside existingPhase2 ceilings. Scientific exploratory timeout remains600s; totalcampaign caps unchanged.
- Sol-xhigh finding: **no meaningful scientific policy optimization task exists in the current fixeddevelopment assets**. Current evaluatorv4 has q=null and admissible_for_policy=false everywhere. Old permutationcoverage/sharpness compositeq is retired; no conversionofnulltozero orfakepilot.
- Exact external donor estimator implemented as pure-array code,withoutdataaccess. Integer rank-displacement aggregation preserves donor/model representationinvariance; fractional reference-rank correction fixed. Productionbootstrapkernel has scale-relative residualguards,5%failurethreshold andnonpositivewidth rejection. Broadcovariates fixed; no normalizationuncertainty propagated.
- Prescribed syntheticdiagnostics actuallyran:100null+100nonzero datasets,5000draws each,144donorsrepresentedby148models. V1 overallFAIL dueconstant-rankprojectionroundoff. V2 narrowbugfix usedidenticalfrozenarrays/seeds/acceptance:95/100null and97/100nonzero coverage;allintervalsvalid,nestinginvariant,constant/nonfiniteguardspass. Syntheticonly:neitherbiology nor nominalcoveragecertification. Bothruns/sourceversionsretained.
- Resource enforcement now has verified RSSwatchdogkilltest:50ms process-groupsampling,killat75%reservedbudget,observerfailurekillsjob. NotahardOSallocationbarrier. Scientific600sceiling enforcedseparately fromhostreasoningallowance. Allobservedresearchjobsremainedbelowreservedmemory;max2CPUjobs enforced.
- IndependentSol-high readinessreview=91/100,G2FAIL. Verified6medium/lowfindingsfixed;strictbatchschema/evidence-domainchecks andmodel-callfullidentity/responsehashchecks added. **52tests pass** (7.47s). Secondhighreviewandfinalfocusedxhigh task-feasibilityconsultationareliveatPIDs/sessionhandlesinstatus.json. Asoftwarescore>=90cannotgrantG2.
- Inconsistentnine-panelengineeringdraftwithdrawninbothcontract/episodes;oldbytesretained. ThisisnotawaiverofC8/C9:newgenuineadmissibletask/usefulqualityendpoint,coherentpanels/baselines/seeds/precision,andindependentreviewstillrequired. No policycycle or externaltesthasrun.
- First-partydata-routeaudit:studyFigsharecataloghasaggregatedminipoolChronos+QC/guideannotations,notindividualreplicatecounts;officialportalrechecktimedout. SourceExtendedFig9authoritativelinkresolvedfromPMC,butdownloadreturnednon-XLSXcontent;guardstoppedwithoutbypass. Candidateoutcomecellswerenotparsed. No Cdependencyvaluesaccessed.
- Separate scientific/prediction/policystatusesremainunchanged. Next:finishreviews,executecheapestlegalvalid-taskdiscriminator,orapplythelockedno-progress/negative-EVprotocolifnolegalroutehaspositivevalue. Fullgoalandsuccesscriteriaremainunchanged.

## Update 2026-10-28k — user-requested handoff

- Sol-high re-review completed: **95/100 code/evidence integrity; G2 FAIL**. All5verifiedcodedefectsresolved; contradictorycomparisonwithdrawnwithfreezeobligationopen. Itsnewlowfinding(stalestatus.json)iscorrectedbythischeckpoint.
- Sol-xhigh task-feasibilityconsultation completed: `reviews/task_feasibility_unstick_xhigh_v1.md`. **Next authorized action** is oneboundedmetadata-onlyprobeoftheofficial26Q3release,withpublication-declaredNextGenfilesetmanifestassinglefallback:300stotal,6networkrequests,30s/request,32MiB,1CPUjob/1GiB,nooutcomedownloads. Write the proposedSPECbeforeexecution. VerdictCANDIDATE_FOUND/INELIGIBLE/UNRESOLVED; nopilotorgatewaiver.
- CandidateendpointproposedbySolispredictiveMSEofdonor-levelrankdisplacementonnewdonor-disjointpanels,withdevelopmentdonor-meanpergenebaseline. Itisaproposalonly,notadmitted. Donormapping,overlapvsC/Broad,genecoverage,processingindependence,precisionandall-inresourcesmustfirstbewitnessed.
- SourceExtendedFig9linkwasresolvedfromPMCbutnon-XLSXdownloadguardstopped; nooutcomecellsparsed. Solstatesadditionalmeasurementsinsame5donorscannotsupplyindependentreservedpanels; do notdownloadfor thisblocker.
- No agent-startedjobsremainrunning;allresource reservationsreconciled. Fullsuite52passed. NoG2freeze,policycycleorfinalexternaltesthasrun. Theuserrequestedahandoffprompt;goalnotachieved andnotmarkedcompleteorpaused. Currentstateandnextstepareinstatus.json.

## Update 2026-10-28l — bounded 26Q3 metadata route probe: UNRESOLVED (stop criterion met)

- Goal note: this agent session has no goal-registration tool; the GOAL.md objective remains the governing objective (user may register it via `/goal`). Goal active, NOT achieved.
- SPEC frozen and hashed before execution: `reviews/prompts/g2_task_route_probe_v1.json` (sha256 1fc891be…). Dispatched via run_bounded (1 CPU job, 1 GiB, 300 s): 3/6 requests, 38,093 B, 1.17 s wall, peak RSS 38.6 MB; no outcome parsing, no dependency matrix, no C access, no bypass.
- Staff/admin forum post 7 retrieved: the temporary "NextGen Model Manuscript 2026" dataset was removed; 26Q3 organoid data are the paper's screens reprocessed with all CRISPR screens ("26Q3+Score, Chronos"). Official manifest `api/download/files` and the publication-declared data_page served HTML (verification) → inventory not obtained.
- Verdict **UNRESOLVED** (`reviews/g2_task_route_probe_v1.json`); fallback ineligible as an independent route; adverse indications: reprocessed manuscript screens already exposed via Layer-A aggregate table; Score jointly processed (E7 risk).
- Independent Sol-high review: 92/100, verdict upheld, G2 FAIL (`reviews/g2_task_route_probe_high_review_v1.md`; dispositions `reviews/g2_task_route_probe_v1_dispositions.json`; 3 dormant medium defects recorded, executed bytes retained unpatched).
- 52 tests pass (bounded, 8.5 s). Next: joint Sol-xhigh + lead no-progress/negative-EV assessment (`reviews/prompts/joint_no_progress_xhigh_v1.txt`) running.

## Update 2026-10-28m — TERMINAL DETERMINATION: BLOCKED (goal NOT achieved)

- Joint no-progress/negative-EV assessment: Sol-xhigh `reviews/joint_no_progress_xhigh_v1.md` (CONCUR_NONCOMPLETE_TERMINAL; BLOCKED; O1) + lead concurrence `reviews/lead_concurrence_joint_no_progress_v1.json`.
- Sol-xhigh terminal determination (1 of 3 reserved terminal slots; phase6_7, 600 s cap, 194 s): `reviews/terminal_determination_xhigh_v1.md` — **TERMINAL_STATE: BLOCKED; GOAL_COMPLETE: NO; SCORE 95** (support for the non-complete determination only). MET: C3 (narrowed conditional), C5 (OLS anchor). UNMET/PARTIAL: C1, C2, C4, C6, C7, C8, C9, C10, C11, C12, C13.
- Blocking condition: no admissible development task, useful fixed quality endpoint, or independent reserved biological panels without consuming C; official 26Q3 inventory not obtainable unattended (verification page; no bypass). Probe verdict UNRESOLVED ≠ nonexistence.
- C NOT consumed. Statuses unchanged: scientific_discovery=exploratory_only_unconfirmed · prediction_improvement=not_evaluated_no_prediction_claim · policy_improvement=not_started.
- Remaining: ~119 h 12 m / 388 nodes / 389 model calls (2 terminal slots protected); $0 spend; ceilings unchanged.
- **Reopening:** (1) user supplies official 26Q3 `Model.csv` + `CRISPRScreenMap.csv` (browser download, with release provenance) → new versioned metadata SPEC fixing the 3 dormant probe defects; or (2) explicit user authorization of a scientific-only track (separately reviewed locks before consuming C; cannot satisfy the joint goal).

## Update 2026-10-28n — v3 execution: sci fixes, generations pgen001–003, Sisyphus mandate
- User mandate: keep generating generations until GOAL.md is determined fully satisfied by sol-xhigh; no terminal give-up. Session goal active (goal-01a18499…).
- PLAN v3/GOAL v3 reconciled+mirrored (PLAN sha256 24ef676c…, GOAL f57499d3…). Test fix: evaluate-external refusal test updated for post-Lock-S single-execution state. **72 passed, 1 skipped.**
- Sci-package 82 fixes: novelty v4+v5 (S3 §2.10.1/§3.7 corrected; P3/P5 screened from abstracts; Europe PMC searches retained novelty_v5_searches.json; C1/C6 PARTIAL pending adjudication); atlas v4 (per-gene S1 tested/significant dispositions, CDK6 Fig3, WNT consistency; tests green). C10 = MET (narrow) per sci review.
- Sol-high v3 package review: **84/100** (reviews/v3_package_high_review_v1.md); all 8 issues independently verified; fixes above + this checkpoint address them; re-review pending.
- Generations: pgen001 FAILS-SCREEN (exploratory, ledger lock unwitnessed — downgraded honestly); pgen002 PENDING (measured-token accounting PASS under predeclared charge, 14,566,608 TOK historical; raw route receipted PASS); pgen003 FAILS-SCREEN vs frozen bar (Witness A PASS 148/148 C→142 patients; B 252/360 lines). Eligible resolved universe: **251 lines / 250 patients / 810 count files, full-C overlap 0, KP3 excluded**. No outcome/count values accessed in any generation.
- Next: sol-xhigh pgen004 design + endpoint adjudication (running) → pgen004 SPEC (ledger-first) → sol-high re-review ≥90 → battery. Resume: `cd /Users/bmarti44/github/bufferright/research/cancer-dependency-rsi && .venv/bin/python src/cli.py resume`.

## Update 2026-10-28o — endpoint NO accepted; sgen001 adjudicated 87; fixes applied
- Sol-xhigh consult complete: **ENDPOINT:NO, PGEN004:NO_GO** (reviews/pgen004_design_xhigh_v1.md). Accepted without waiver: TOK as written cannot certify C9 (unknown unmatched host expenditure; max-call imputation not a bound; CPU was unrecorded). Reopening witnesses named in status.json. No policy cycle run; no endpoint switch.
- sgen001: identity **CONFIRMED** — 148 models = 142 patients (SIDP01937/01939 same-patient longitudinal samples; Passports authoritative). Archived Lock-S BOUND used 144 covariate-ID groups splitting two patients; effects on patient-weighted estimate/interval/decision **unquantified**; execution preserved. Sol-high re-review **87/100** (C1/C6/C7 PARTIAL; primary-point reproduction PASS exact).
- Fixes for all verified 87-review issues: atlas v4 CDK6 separate qualifications (q=0.28 nonsignificant retained) + regression assertions; pgen002 PASS labels removed (DISPOSITION_v3); acquisition-deviation record (compressed-payload overfetch, no decoded outcomes; pgen001 non-exposure qualified unverified); novelty v6 (bibliography 76/103/41 vs API subsets; Han 2020 disposition; S2 forward citations; S3 Zenodo verified, contents outstanding); client CPU measurement implemented as NEW module src/cpu_meter.py (RUSAGE_CHILDREN; LOCK2-pinned budget.py edit reverted byte-exactly after the gate correctly refused — incident ledgered) + test; manuscript caveat corrected (unquantified incl. point weighting); GENERATIONS pgen001 index correction appended. Tests: see status.json.
- Next: sol-high re-review to ≥90 → sgen002 reproduction/package → next legal generation. Resume: `cd /Users/bmarti44/github/bufferright/research/cancer-dependency-rsi && .venv/bin/python src/cli.py resume`.

## Update 2026-10-28p — sgen002 reviewed 86 -> fixes -> 91; terminal determination next
- sgen002 reproduction: v3→v4 isolated rebuild + primary point + figure PASS (report v3, exclusive creation, hashes ledgered); upstream rebuild is a ledgered scope deviation (not in runner; reviewer verified in-memory); OLS global-tolerance FAIL recorded with frozen 1e-6 component exception (417/3000).
- Sol-high: 86 → fix review **91/100**, zero high/critical. Gate snapshot: C5/C7 MET; C1/C2/C3/C4/C6/C10/C11/C12 PARTIAL; C8/C9/C13 UNMET. Manuscript headline now archived-grouping-accurate; identity CONFIRMED (142 patients).
- Next: sol-xhigh terminal determination (protected slot 2/3), then generations per its mandate list. Resume: `.venv/bin/python src/cli.py resume`.

## Update 2026-10-28q — TERMINAL DETERMINATION v2: ACTIVE_NOT_TERMINAL (95)
- Sol-xhigh (protected slot 2/3): GOAL_COMPLETE NO. MET C5, C7; PARTIAL C1-C4, C6, C10-C12; UNMET C8, C9, C13. Remaining ≈118 h / 388 nodes / 373 model calls (phase2: 7; phase6_7: 26 incl. final terminal slot). Claim ledger populated (6 claims). Ranked mandates 1-8 recorded in reviews/terminal_determination_xhigh_v2.md; mandate 1 (reconciliation) done here.
- Next: sgen003 novelty completion → sgen004 no-C inference discriminator → attainable reproduction → pgen004 only on new accounting evidence. Resume: `.venv/bin/python src/cli.py resume`.

## Update 2026-10-29r — recombination generations: pgen004d METERING_ONLY, sgen006 no qualifying resource
- Sol-xhigh recombination: ENDPOINT_V2 YES_WITH_NAMED_CONDITIONS (still NO_GO without host-cost witness). pgen004d: scoped tree-CPU meter built + validated (review loop 76 -> 80 -> 84 -> **92**, double-count fixed: fork fixture 1.03-1.21 total vs ~1.0 work); Witness A FAIL (ChatGPT subscription, no per-call cost surface). No acquisition.
- sgen006: NO_QUALIFYING_RESOURCE_IN_SCREEN (Khalili 1 avatar; Lo cisplatin endpoint; droplet preprint no donor cohort; Han cell lines).
- Reviews at >=90: v3 package 91, sgen002 91, sgen003 90, sgen004/5 94, meter 92. Tests 87 passed/1 skipped. Gates: MET C1(novelty disposition)/C5/C7; PARTIAL C2/C3/C4/C6/C10/C11/C12; UNMET C8/C9/C13. Remaining blockers are external: (1) measured host expenditure or strict-matching witness (user-supplied), (2) new independent patient-organoid resource (none found in bounded screen).
- Loop continues on attainable fronts (packaging/provenance depth) pending either witness. Final terminal slot (3/3) preserved. Resume: `.venv/bin/python src/cli.py resume`.
- MANDATE CLOSED 2026-10-29: sgen006 NO_QUALIFYING_RESOURCE (91); sgen009 TRACEABILITY_PASS v17 (91, 3 named P2 residuals). Determination v2 ACTIVE_NOT_TERMINAL stands; slot 3/3 preserved for a future candidate COMPLETE package. Next capital: host-cost witness decision (C8/C9) or new patient resource (C6/C10) - both external.
- sgen010 CLOSED 2026-10-29 (user-supplied DepMap 26Q3 Model.csv + CRISPRScreenMap.csv): POOL_IDENTIFIED on established/confirmed-identity basis - 1,106 CRISPR-screened models / 1,069 Passports patients donor-disjoint from spent cohort C (148 models/142 patients, Witness A reproduced + canonical-hash pinned). 253 unresolved + 2 name-only excluded; organoids 11 established / 97 NOT established (named residual). Sol-high 68 -> 84 -> 90; v7 shipped (lead-verified, 96 tests pass), final byte re-review pending exhausted phase allocations (not waived). Fresh patient-level evaluation pool now exists on metadata; evaluation design is a future locked generation. C8/C9 unchanged: metered host-cost witness still required (user decision).
- 2026-10-29 user decisions applied: allocations raised (total 2,000 model calls; ledgered amendment); host cost estimated from recorded receipts (list-price v4: $26.70 priced + 6 frozen imputations = $32.95; actual metered $0). Sol-xhigh consult v2: COST_BASIS YES_WITH_NAMED_CONDITIONS (proxy accounting only - original measured-cost C9 remains UNMET), PGEN005 GO_WITH_CONDITIONS (SPEC locked, no rollouts, witness gate open), SGEN011 framing C executed: NEITHER_PASSES - framing A lacks screened-environment provenance in supplied metadata (precision would pass, MDR 0.086); framing B has 11 established organoid patients vs ~366 required for |rho|=0.146 (more than all 108 screened organoids). Outcome generation rejected on current metadata; next capital is an organoid identity crosswalk and/or screening-environment provenance. sgen010 final review arc 68->84->90->92 closed.
- sgen011 CLOSED 2026-10-29: NEITHER_PASSES (arc 82->91->96; estimator v7 micro-review 100, accounted $34.18/66 calls). Framing A: no screening-environment provenance in supplied metadata (precision bound 0.0861 is optimistic-only). Framing B: 11 organoid patients vs ~366 required - infeasible at Lock-S scale within DepMap 26Q3 screened organoids (108 total). Next capital is external: screening-environment provenance source and/or organoid crosswalk; original measured-cost C9 would additionally need a GOAL.md amendment to accept the estimated-cost basis (user decision).
- GOAL.md C9 amended 2026-10-29 at user instruction (both copies, sha f4ea241a...): estimated-cost basis (recorded tokens x list prices, frozen imputations, 2x/4x sensitivity) is admissible C9 cost evidence prospectively; metered spend ($0) still reported alongside. C9 remains UNMET empirically until a preregistered policy comparison runs under pgen005 witnesses.
- sgen013 CLOSED 2026-10-29: FAIL (arc 80->89->91->98). One-sample transport infeasible: atlas paired-format coverage = 1 component (ACH-000178) per endpoint vs >=367 required. With sgen012's structural two-arm impossibility, no locked outcome design is currently instantiable on the established pool; outcome work stops per SPEC posture. External unblock: independently measured paired-format L/B at scale.
- sgen014 closure package 2026-10-29: S1 MOESM1 visually inspected 5/5 pages (zero figure panels; guide to 4 spreadsheet tables); novelty completion over the full 3,634-record broad set (331 stage-1 survivors stage-2 screened with dispositions; 0 plausible overlaps; nearest-3 excluded on abstract); C9 amended-rule adjudication recorded ($34.18 estimated / $0 metered; C9 still empirically UNMET); manuscript/limitations/packet refreshed incl. allocations-incident record; evidence-linked gate table at generations/sgen014/gate_update.json (MET C1,C2,C5,C7; PARTIAL C3,C4,C6,C10,C11,C12; UNMET C8,C9,C13). Terminal slot 3/3 preserved.
- FINAL DETERMINATION 2026-10-29 (slot 3/3, user-directed): sol-xhigh TERMINAL_LABEL=INCONCLUSIVE, GOAL_COMPLETE: NO, DETERMINATION_SCORE 98 (reviews/terminal_determination_xhigh_v3.md). Gates MET C1,C2,C5,C7; PARTIAL C3,C4,C6,C10,C11,C12; UNMET C8,C9,C13. SCIENTIFIC_RESULT_WITHOUT_RSI_EVIDENCE not established (patient-level inference unresolved). Final cost snapshot $42.44 estimated / 85 calls, $0 metered (ledger/host_cost_estimate_v8_final.json). Campaign closed; reopening conditions enumerated in the determination.


## pgen007-pgen010 (2026-10-29)
- pgen007 cycle SPEC (xhigh) stopped SPEC_INVALID (cost rates); pgen008 (attribution flattened); pgen009 (paraphrased quotes); pgen010 PRERUN PASS 100.
- pgen010 cycle EXECUTED: verdict FAIL BELOW_QSTAR. q=0.00037 vs Q*=0.020; gains vs I/F/R = +0.00037/+0.00781/+0.00140 macro with per-model sign flips vs I/R. Exact 14,900-node accounting; deterministic; host calls $0.56 estimated (shared_equally). No C13/C8/C9 credit.
- Next action: sol-high close-out review, then xhigh new targets (Sanger manifest probe; repeat-instability construct).

### Correction (2026-10-29, close-out review REJECT 68)
"Valid execution" above is withdrawn: the locked pgen007-pgen010 SPEC was truncated at item 65 (lead save error); full 79-item source survives in reviews/. Sealed numerical results were independently reproduced by the reviewer (q=0.00037, selections, 14,900 schedule) and FAIL BELOW_QSTAR stands, with added labels MODEL_REGRESSION, LEAKAGE(accessibility-only), EXECUTION_FAILURE(attempt-1). Compliance claims do not stand.


## Frontier close-out (2026-10-29)
- sgen016 Sanger manifest probe: FAIL_TO_ESTABLISH (closed 94). sgen017 repeat census: NEAR_ABSENT_UNVERIFIED, 1 candidate ACH-000614 (closed 98). sgen018 condition-history: ABSENT (closed 100).
- Sol-xhigh v3: FRONTIER_EXHAUSTED_UNDER_CONSTRAINTS; no executable discriminating generation remains. Question A (processed-vector patient-level sensitivity) is UNTESTED/ACCESS-GATED; conditional sgen019 recorded, activation needs user portal bundle (file listing + linkage metadata first; outcomes stay unopened).
- Determination v3 INCONCLUSIVE stands; terminal slot 3/3 spent. Goal NOT complete.
- Resume: cd cancer-dependency-rsi && .venv/bin/python src/cli.py resume


## Direct phase (2026-10-29, user: no ceremony)
- Downloads authorized as development data; 981-patient reserve sequestered before value access (organoid subset since opened once, logged).
- Broad v2 (signed-mean endpoint): null (rho=-0.02) - NOT the Lock-S estimand.
- Harmonized Lock-S estimand in Broad 26Q3: dev rho=-0.053 [-0.098,-0.007] (82 models/80 patients); held-out rho=-0.076 [-0.150,-0.008] (28/26). Same direction as Sanger Lock-S (-0.146), ~half magnitude; raw rho -0.19/-0.21 (baseline carries much of it). Kill criterion (CI within +-0.20) MET: no material (>=0.20) association claim.
- Sol-xhigh honest review: OVERALL NOT_PROMISING 18/100; GOAL probability ~1%; policy thread DEAD under current design.

## Recombination phase (2026-10-29)
See FINDINGS.md. Headline: sterol-dependency formulation law (held-out replicated); medium-not-format attribution; dome-specific spliceosome/ribosome weakening (open mechanism, proliferation-index lower in org media 5.25 vs 6.37). Sol-xhigh backend 401 x6 (many-lines consults failing); lead queue executing.

## Recombination update (2026-10-29, later)
Mev law: lineage-homogeneous, lineage-adjusted atlas v2 saved. Loss side: all tested mediators excluded (depth, days, proliferation, target expression, lineage, protein half-life). Sol backend 401 x11 (high+xhigh) - consults queued, lead execution continues. Tests 99 passed/1 skipped.

## Direct-phase consolidation (2026-10-29)
FINDINGS.md is the current results record. Mev formulation law: dev + held-out + lineage-homogeneous + Sanger cross-system consistent. Loss-side mechanism open after exhaustive mediator exclusion. Xhigh/high backend 401 x13; consults queued.

## Consolidation point (2026-10-29)
Mev law near-universal (73/77). TSM-specific cut confirms splice loss is dome-formulation-specific. GDSC corollary dropped (infra gone, weak design). Sol backend 401 x15.

## Update 2026-10-29 (GOAL v4) — deliverables 1–3 computed; manuscript v2 + wet-lab one-pager drafted
- Attribution v2 (src/medium_attribution_v2.py): 17,524 genes, flags + ratio CIs, dev patients; 240 gains/209 losses (norm), 85%/84% medium-attributable, 0 format-candidates. Held-out confirms (slope 0.97, 100% same-sign).
- Deliverable 2: Broad published gains replicating under lineage adjustment: 87% medium-attributable; Herranz-Ors headline 18: 8 replicate, 5 medium (sterol/SREBP axis), 3 unresolved (SCAP/DDX3X/ITGB1).
- Deliverable 3: essential depth identical dome vs FBS (ratio 1.0006, 24 vs 21 days); spliceosome/ribosome weakening (+0.90/+0.64) is complex-specific and formulation-family (reproduces adherent +0.64), NOT global doubling compression. CPD recorded for 1/1,241 screens — true per-doubling correction impossible in 26Q3; stated plainly in manuscript. Corrects FINDINGS' earlier dome-only reading of losses.
- Drafts: manuscript/manuscript_draft_v2.md (GOAL v4 framing), manuscript/wetlab_proposal_v1.md, generations/RELEASE_README.md. FINDINGS.md updated.
- Remaining (user/external): post preprint, send wet-lab proposal to collaborator. Optional: direct Sanger-screen re-analysis (currently published-table audit only). 99 tests pass.
- Sanger direct check added (src/sanger_direct_check3.py): mevalonate percentile 0.099 (organoids) vs 0.394 (Sanger 2D); Sanger organoid essential depth 0.63x — spliceosome weakening explained by global compression there, ribosome residue remains; Broad residue is the post-normalization complex-specific part. ITGB1 best non-medium candidate (Sanger dpct -0.233). Manuscript v2 + FINDINGS updated. Remaining: user posts preprint / sends wet-lab proposal.
- Robustness + figures: LOO over 9 adherent models stable (slope 0.87-0.92, >=94% flags retained); 3 manuscript figures generated and visually checked; survivor table (70 unresolved); finding review written (reviews/goal_v4_finding_review_v1.md). Internal deliverables complete; preprint posting + collaborator outreach remain user actions.
- CORRECTION via curated BAGEL panels (panels_curated_v1.json): hand-panel spliceosome +0.90 was selection-biased; curated Broad medians: spliceosome +0.035, ribosomal +0.146 (baseline +0.031). Sanger depth-scaled: spliceosome no residual weakening (1.34 vs 1.11), ribosomal residue persists (1.25 vs 1.57). Manuscript/Fig2/FINDINGS corrected; genome-wide claims unchanged.
- Release bundle assembled: release_v1/ + release_v1.zip (manuscript, figures, tables, code, review, README with reproduction inputs). Ready for user to post/upload.
- Audit pass: manuscript stale-number grep clean (top-loss magnitude corrected +0.9 -> +1.2, EFTUD2 1.19); unit tests for bh/flag rules added (tests/test_medium_attribution.py, 3 tests); release zip refreshed. All internal deliverables verified; posting + outreach remain user actions (2nd consecutive external-only turn).
- Hardening round (2026-10-30): Sanger t5 own-call audit = calls robust (median freq 0.80/0.69), critique narrowed to attribution. Expression triangulation confirms sterol-starvation mirror (mev expr +0.36 vs dep -0.36); heme/FA expr opposite. Manuscript updated; release refreshed.
- Downloads: DepMap portal + PMC supp files are verification/captcha-walled from scripts (no bypass attempted past one cookie retry). HPLM (Rossiter 2021) Table S1 located at PMC8172426 supplements; manual-download README in data/raw/hplm_rossiter2021/. GEO GSE164693 = RNA-seq only.
- HPLM reverse test done (user downloaded PMC8172426 supplements): corr(HPLM-RPMI, D_org)=0.04 genome-wide; SQLE opposite direction (+0.44 relieved in HPLM vs -0.84 gain in organoid medium); RPMI-only essentials enriched 4.6x for medium-attributable set (p=3e-4). Manuscript + release updated. DepMap 26Q3 confirmed newest by user — no re-run needed.
- Submission package finalized (2026-10-30): release validated 29/29 (src/validate_release.py, VALIDATION.json w/ hashes); manuscript_v2.pdf rendered (7 pp, src/render_pdf.py, author placeholders); biorxiv_fields.txt (abstract 271w), supplementary_tables.zip, wetlab_cover_email.txt, SUBMISSION_CHECKLIST.md in release_v1/. Terminal publish/propose acts require user accounts/identity.
- Astra xhigh r1: 68/100 (0 critical, 3 high, 6 med, 2 low). All verified true; fixes implemented as v2r2 (dev-only calibration, symmetric format rule -> LSM7 sole format candidate, HC3 82/75%, joint bootstrap slope 0.90 [0.81,0.98], disjoint held-out 0.96, common-support 0.89, screen-level Humagne n=7 corr 0.78, %.6g export, t5 model-collapse, HPLM direction-separated). Manuscript rewritten (medium-consistent language, scoped title, kinetics as hypothesis). 104 tests pass; validator 31/31. Round 2 dispatched.
- Astra r2: 82/100. Fixes: bootstrap rewritten (shared multiplicities, main-identical preprocessing, identity check 0 mismatches; slope 0.90 [0.82,0.99]); LOO refits F (min retention 93.54%); validator now checks archived contents by gene both scales (33/33, hashes verified post-append); docs/figures synced (LSM7 class). Dispositions: reviews/astra_review_r2_dispositions.md. Round 3 dispatched.
- Astra r3: 89/100. Fixed: bootstrap NaN-poisoned offsets (MAU2 0.7%->48%, identity via weighted path, regression test), wet-lab docs synced, shorthand purged, PDF regenerated. Validator 33/33, tests 105 pass. Round 4 dispatched.
- Astra r4: 89/100 (no computational defects). Fixed residual transfer language (email/proposal/intro now use cultured-model scope) + stale literals (17,525 genes, 289w abstract, 33/33). Round 5 dispatched.
- Astra r5: 95/100 SHIP IT (no issues at low+). Review loop closed: 68 -> 82 -> 89 -> 89 -> 95. All verified issues fixed across rounds; dispositions in reviews/astra_review_r{1,2,3,4}_dispositions.md. Remaining: user fills authors, posts preprint, sends wet-lab email (SUBMISSION_CHECKLIST.md).
- Astra deep-web novelty audit (uncapped rerun, 230+ searches): VERDICT PARTIALLY TRUE. No Class A source; narrow catalogue-audit claim defensible with moderate confidence. Framing corrected per Astra (title -> medium-consistency audit; precedent paragraph crediting Lagziel/Joly/Pacini/Dempster/Liang/Zaidi-Sawyers; sentence-level fixes). Manuscript now v2r3. Note: a Zannix Labs web report claiming similar scope has a fabricated arXiv ID (excluded by Astra; minipool-only anyway).

## Update 2026-11-01 — WEBSITE LIVE: www.itsthemedium.com
- Domain itsthemedium.com registered (Route 53, account 087630439073);
  hosted zone Z02889802R8L6IJOUS457; ACM cert (apex+www) ISSUED.
- Site: site/index.html — WebGL scrollytelling (17,525 genes as GPU
  particles: dish -> flat/dome split -> real (D,A) diagonal -> survivor
  ring), full gene explorer (search/filter/sort/detail/per-gene citation/
  DepMap links, #gene= deep links), findings, creation story, methods,
  sources, downloads (incl. release_v1.zip). Vendored three/gsap/lenis.
- Hosting: S3 bucket itsthemedium-site-087630439073 (private, OAC
  E3IAADSX8J5TJ) + CloudFront E25F95NV3DTSL4 (d1rmy9bod3nu3c.cloudfront.net);
  www.itsthemedium.com canonical; apex 301 -> www via CloudFront Function
  itsthemedium-apex-redirect. Redeploy: aws s3 sync site/ (exclude
  apex_redirect.js) + create-invalidation /*.
- Review: Codex gpt-6.1-sol xhigh, 6 rounds 76 -> 84 -> 89 -> 89 -> 92
  -> 94/100 SHIP IT confirmed, zero issues >= low remaining.
  Trail: reviews/site_sol_review_r1..r6.md + dispositions.
  Regression guards: tests/test_site_data.py (suite: 110 passed, 1 skipped).
  Headless browser gates (check_page desktop+phone + playthrough): clean,
  60fps desktop.
- Figure 1 annotations gained white backing (contrast); figures + PDF +
  release bundle regenerated and revalidated 33/33.
- Remaining user-external items unchanged: fill manuscript authors,
  regenerate PDF, post bioRxiv preprint, send wet-lab proposal.
  Site/copyable citations state "unpublished draft" until then.
