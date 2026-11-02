# pgen010 cycle SPEC (separately frozen repair, 2026-10-29)

## Repair note (lead)
pgen007 stopped SPEC_INVALID (rates unenumerated); pgen008 (attribution
flattened); pgen009 (attribution paraphrased). This SPEC adopts pgen007's
items verbatim; changes: SPEC_ID/seed token read pgen010; host-call schedule
= lead documentary repairs + ONE pgen010 pre-run review; cost section below
REPLACES items 64-65's reference.

## Cost rates and attribution (replacing items 64-65 reference)
RATES from src/host_cost_estimate.py (estimator v8 final): per-1M-token USD;
SHORT tier (entry input_tokens <= 272,000): input 2.00, cached 0.10, output
10.00; LONG tier: input 4.00, cached 0.20, output 15.00; cache-write 2.50 both
tiers. Entry price = ((inp-cached)*in + cached*cached_rate + out*out_rate
+ write*2.50)/1e6; multi-entry receipts sum entries; events fallback sums
per-turn prices; residual imputation: same-phase median, else campaign max.
Unpriced after fallback+imputation fails COST_UNRESOLVED.

ATTRIBUTION RULES, quoted byte-exact from
generations/pgen006/readiness_v8.json key cost_table/host_call_attribution:
- shared_equally: "substrate/E0 production + evaluator construction calls (charged equally to every arm)"
- arm_attributed: "policy-generation, policy-specific review, and unstick calls (charged to the arm that caused them; learning overhead NOT shared)"
- unresolved: "conservative learned-arm attribution per pgen005"
- basis: "amended estimated-cost schedule (estimator v8); metered $0 reported alongside"
- matching: "exact evaluated-node equality across arms at cycle lock"

PER-CALL MAPPING (frozen here): pgen007 xhigh generation call = evaluator
construction (it fixed Q*, the evaluator, comparators, and the candidate
family for every arm; it produced no arm's fitted policy - fitted parameters
are selected by deterministic DEV replay at zero scheduled host calls) =>
shared_equally. Each pre-run review call (pgen007/pgen008/pgen009 sunk;
pgen010 scheduled) = evaluator-construction gate for the whole cycle =>
shared_equally. No policy-generation, policy-specific review, or unstick
call is scheduled; any such call is an UNSCHEDULED_HOST_CALL failure and,
if incurred, arm_attributed per the quoted rule, with unresolved cases to
the learned arm per the quoted fallback. Sunk prior-cycle calls are reported
with the same mapping, priced identically. Nodes per items 56-58/66.

## pgen007 items (verbatim)



SPEC_ID: pgen010 — FIRST_ENGINEERING_PILOT_CYCLE (separately frozen repair)
STATUS: Execution specification; no results asserted. ENGINEERING_PILOT_SEPARATE framing applies; Determination v3 stands.

01. Freeze atlas v4, catalogue membership, recorded patient linkage, this specification, and the pgen006 v8 amended cost table before fitting. Record their hashes. No policy, threshold, partition, seed, or accounting changes after evaluation begins.
02. DEV comprises ACH-000108, ACH-000178, ACH-003040: 1,000 format actions and 1,000 medium actions in total. Only these 2,000 outcomes may train or select policies.
03. EVAL comprises the 500 format actions from ACH-001418 and ACH-002958. ACH-000048 medium actions are excluded from this cycle, including training. ACH-003052 remains quarantined.
04. Preserve the recorded DEV/EVAL patient disjointness across six distinct PatientIDs. This is linkage-based separation, without a claim that unresolved donor identities have been independently established.
05. A node is exactly (gene, axis, model, held_condition). Treat identifiers as exact strings, without trimming, case folding, or inferred synonyms. Canonical order is Python lexicographic tuple order on these four strings.
06. Require unique node keys, the stated partition counts, valid paired records, and finite recorded deltas. A duplicate, missing required field, linkage contradiction, or count mismatch fails DATA_INTEGRITY; never silently remove or replace a node.

07. Ground truth uses the stored delta verbatim, without recomputing its orientation from Chronos scores. Parse its recorded decimal representation with decimal.Decimal; do not round or apply a tolerance.
08. Class order is (-2,-1,0,+1,+2): -2 if delta ≤ -0.10; -1 if -0.10 < delta < 0; 0 if delta = 0; +1 if 0 < delta < 0.10; +2 if delta ≥ 0.10.
09. Thus ±0.10 belong to the strong-magnitude classes; signed decimal zero belongs to class 0. Equal deltas always receive equal classes. These cutoffs are engineering conventions, without biological interpretation.
10. Every policy emits five probabilities in that class order. If a hard label is reported, choose the first maximum in this order. Classification accuracy is descriptive; normalized Brier loss is the selection and success metric.

11. Create five episodes per model-axis stratum. Within each stratum, sort distinct genes; assign gene at zero-based position i to fold i mod 5.
12. Episode f has target set T containing every action for genes in fold f, and query pool Q containing all remaining actions in that stratum. All held conditions for a gene stay together.
13. Require all five target sets to be nonempty and every query pool to contain at least 20 nodes; otherwise fail EPISODE_INFEASIBLE. Do not shrink the budget or change folds.
14. Each episode permits exactly B=20 distinct query attempts, selected sequentially. A successful query returns its recorded paired observation, including delta and Chronos scores; the predictor below uses only its derived class.
15. Targets cannot be queried in their own episode. Each action is a target exactly once across the five folds. This scores all 500 EVAL-format nodes on identical support across arms.
16. Start every episode with empty revealed set R. Discard R afterward. No outcomes, posterior counts, or predictions may transfer between episodes, models, folds, arms, or random seeds.
17. At decision time, available inputs are catalogue metadata, T/Q membership, frozen DEV summaries, and previously revealed observations in this episode. Unqueried outcomes and scorer state are inaccessible.
18. Model identifiers determine grouping and seed identity only; they are not predictive lookup features. EVAL outcomes may condition the prescribed within-episode calculation, but cannot update persistent parameters or select policies.

19. Implement all probabilities, acquisition scores, Brier losses, and selection comparisons with fractions.Fraction. This prevents floating-point tie ambiguity. Decimal is used only to classify recorded deltas.
20. For training set D, count classes in five groups relevant to node x: all D; matching axis; matching (gene,axis); matching (axis,held_condition); matching (gene,axis,held_condition).
21. For any group S, define q_S,c=(n_S,c+1)/(n_S+5). An absent group therefore gives five probabilities of 1/5.
22. Define prior pi_c(x) as the arithmetic mean of those five group probability vectors. Build these summaries solely from D.
23. Predictor parameters are theta=(kappa,wg,wh). Define w(x,r)=1+wg*I[gene_x=gene_r]+wh*I[held_x=held_r], where I is the indicator function.
24. Define d_R(x)=kappa+sum_{r in R}w(x,r), and p_c(x|R)=(kappa*pi_c(x)+sum_{r in R}w(x,r)*I[class_r=c])/d_R(x).
25. For an eligible query q, define U_R(q)=1-sum_c p_c(q|R)^2; W(q)=sum_{t in T}w(t,q); V_R(q)=sum_{t in T}w(t,q)/d_R(t).
26. Adaptive acquisition always chooses the eligible node with largest prescribed score, breaking ties by ascending canonical node key. Remove the attempted node from eligibility before the next decision.
27. After 20 attempts, emit p(t|R) for every target. All emitted probabilities must be nonnegative and sum exactly to one.

28. Initial policy I uses theta0=(4,3,3), with acquisition score U_R(q).
29. DEV assessment is leave-one-model-out: when assessing episodes of DEV model m, construct D from the other two DEV models only. Use their format and medium outcomes.
30. For an arm, concatenate its five folds’ target predictions within each model-axis stratum and compute mean target loss there. Define J as the mean across three models of the equal-weight mean of their format and medium losses.
31. Predictor candidates, in tie-breaking order, are (4,3,3), (4,0,0), (4,3,0), (4,0,3), (16,3,3).
32. First create one canonical-ascending query transcript for every DEV episode. Assess all five predictor candidates on these same transcripts; choose theta_hat with minimum J, breaking exact ties by candidate order.
33. Next assess six policy candidates in this order: initial I; theta_hat with U_R; theta_hat with W; theta_hat with V_R; theta_hat with U_R*W; theta_hat with U_R*V_R.
34. The LEARNED update selects the candidate with minimum J, breaking exact ties by that order. Selection of I is permitted and recorded as NO_UPDATE; it receives no learning-success exemption.
35. These are exhaustive candidate sets. No extra features, parameter search, candidate invention, or host-generated modifications are permitted.
36. Once selection finishes, rebuild priors from all 2,000 DEV outcomes. Freeze theta_hat, selected acquisition rule, summaries, and their hashes before any EVAL replay.
37. DEV selection scores are optimization results, not independent performance estimates. EVAL format and excluded EVAL medium outcomes cannot influence any selection step.

38. The strong fixed-order comparator uses theta_hat and selects one of six static ordering recipes on DEV, minimizing J with ties resolved by recipe number.
39. Recipes are: K0 canonical ascending; K1 canonical descending; K2 descending U_empty(q); K3 ascending U_empty(q); K4 descending W(q); K5 descending U_empty(q)*W(q).
40. For K2–K5, break equal scores by ascending canonical key. Compute each episode’s entire order before its first query, using metadata and frozen DEV summaries. Never reorder from revealed outcomes.
41. The seeded uniform-random comparator uses theta_hat and 20 separate runs, seeds s=0 through 19. Predictions are scored separately; do not ensemble their probabilities.
42. Use Python 3.12 standard-library random.Random. For each episode/run, serialize ["pgen010",s,model,axis,f] with json.dumps(ensure_ascii=True,separators=(",",":")), encode as ASCII, and SHA-256 hash.
43. Interpret the digest as a big-endian unsigned integer, seed a fresh Random instance, shuffle canonical-sorted Q, and query its first 20 nodes. No other operation consumes that generator.
44. Refit fixed-comparator DEV priors using the same leave-one-model-out rule. Final fixed and random comparators use the same all-DEV priors as the learned arm.

45. EVAL arms are initial I, selected policy L, DEV-selected fixed F, and random R_s for all 20 seeds. Execute in that order; within each arm, sort models and axes lexicographically, then folds 0 through 4.
46. Each EVAL arm/run attempts exactly 200 nodes: two models times five episodes times 20. Successful matching requires exactly 20 successful distinct query nodes per episode, with zero target queries.
47. Exact matching concerns query counts and scoring support; policies intentionally choose different query identities. Each arm scores the identical 500 target node keys exactly once. No tolerance, rescaling, or unmatched-node deletion is allowed.
48. For target t, loss b(t)=sum_c(p_c(t)-I[y_t=c])^2/2, bounded by 0 and 1. For model m, L_a,m is mean b across that model’s target nodes.
49. The primary metric is (L_a,m1+L_a,m2)/2, giving equal weight to the two models regardless of their action counts. Random model loss is L_R,m=(sum_s L_R_s,m)/20.
50. For comparator c in {I,F,R}, define gain g_c,m=L_c,m-L_L,m and macro gain G_c=(g_c,m1+g_c,m2)/2. Define q=min(G_I,G_F,G_R).
51. Performance passes only if q≥0.020 and every g_c,m≥0. The threshold is a prospective minimum useful engineering improvement, not a significance cutoff or empirically calibrated biological effect.
52. Report each model’s losses and gains, both-model means, and observed model ranges. For random runs also report seed means and ranges; seed variation is computational variation.
53. There are only two EVAL models. Do not treat nodes, folds, held conditions, or seeds as independent model replicates. Report no population p-value, node-bootstrap interval, or claimed informative population confidence interval.
54. The performance gate is a finite-benchmark decision about these recorded models. Their observed range is descriptive and cannot establish performance on new models or patients.

55. Log every query attempt with cycle, phase, arm, episode, step, exact node key, acquisition score/order position, returned class or failure, and charged cost.
56. Every policy query attempt costs one evaluated node, including failed attempts and repeat identities across episodes or arms. No cross-episode, cross-arm, or cache discount is allowed.
57. Charge the one-time release of 2,000 DEV source labels and 500 EVAL scorer labels separately, at one node each. The scorer’s label cache remains inaccessible to policies.
58. Reusing released labels for arithmetic summaries or scoring creates no additional action; replay query attempts remain charged even when their recorded labels are cached.
59. The completed DEV schedule contains 30 episodes: 600 queries for the shared predictor-selection transcripts; 3,600 for six policy candidates; 3,600 for six fixed-order candidates. Total DEV replay queries: 7,800.
60. The completed EVAL schedule contains 23 arm/runs times 200 queries: 4,600. Together with the 2,500 source/scorer releases, the completed cycle charges 14,900 evaluated nodes.
61. Run every scheduled candidate and arm even when two implementations select identical sequences. The sole shared query transcript is the predictor-selection transcript explicitly specified above.
62. Host-call schedule: this specification-generation call and one pre-run review call. The review receives frozen specification, metadata, and cost-table definitions, without outcomes; its permitted result is PASS or identified execution defects.
63. The review cannot amend algorithms or generate candidates. A defect stops this cycle as SPEC_INVALID. No policy-time host calls, repair calls, or generation retries are scheduled.
64. Price generation, review, and any attempted failed or unscheduled calls using the pgen006 v8 amended estimated-cost table verbatim, including its shared versus arm-attributed rules. Record estimator inputs, call IDs, outcomes, allocations, and estimated charges.
65. Preserve that table’s native units and conversions. Do not substitute one host call for one node, zero-price reused calls, or replace estimated charges with a different token/time basis. Missing rates or unresolved attribution fail COST_UNRESOLVED.



