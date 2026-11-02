# sgen004 SPEC - patient-weighting envelope discriminator (terminal mandate 3; NO C outcome access)
Ledger-locked before computation. Uses ONLY retained frozen outputs: locked per-gene coordinates
(lock_s/results/external_v1_gene_displacement.csv: L_g, archived D_g, AdherentMean), cohort model
list + locked donor groups (lock_s/cohort.csv), Passports patient mapping (142; sgen001).
Question: does an assumption-light worst-case envelope prove the archived BOUND decision
(patient-weighted partial Spearman CI within (-0.20, 0)) is grouping-robust, or not?
Frozen method:
1. Model weights: archived w_a(m) = 1/(144 * n_group(m)); patient w_p(m) = 1/(142 * n_patient(m)).
   Per-model normalized displacement d_m in [0,1] by construction (|rank diff|/(207-1) averaged
   within donor first - verify bound from estimator definition in src/confirmatory_estimand.py;
   if the true bound differs, STOP and record).
2. |D_pat - D_arch| <= TV = 0.5 * sum_m |w_a(m)-w_p(m)| (tight for d in [0,1]).
3. Rank envelope: for each gene, max rank movement under any D' with |D'-D_arch|<=TV pointwise:
   genes within 2*TV in D_arch can cross. Bound Spearman rho displacement via the
   sum-of-squared-rank-differences identity under worst-case simultaneous crossings
   (conservative: every gene moves its max feasible positions adversarially in rho-sign direction).
   Partial-Spearman (ranked-residual on ranked |AdherentMean|, unchanged covariate) envelope
   derived from the same rank-movement set; method's conservativeness stated.
4. Interval: archived CI width is NOT reused as patient-level uncertainty. Envelope verdict only
   about point-estimate robustness: PASS iff worst-case |rho_pat| < 0.20 AND sign preserved;
   it cannot certify a patient-level CI or decision (that requires a NEW independent resource).
Verdicts: ENVELOPE_PROVES_POINT_ROBUSTNESS / ENVELOPE_TOO_WIDE / INAPPLICABLE (bound premise fails).
No inferential label is upgraded by this screen regardless of outcome.
