
codex
**Recommend one fixed, panel-wide association using the six-model format contrast and independently evaluated molecular-prediction loss.** It is potentially G1-passable after resolving data access and preprocessing provenance. **Nothing currently establishes a G1 pass**, and an imprecise null would not rescue the gate.

The [review’s three critical failures](/Users/bmarti44/github/bufferright/research/reviews/g1_review_r1_verdict.md:1) require an operational endpoint, separation from selection outcomes, and an audited processing dependency graph.

1. **Preferred: format lability versus external prediction loss.** Retains the scientific connection between controlled environmental measurements and molecular transfer. Requires individual-level conventional-model data, Sanger continuous outcomes and molecular covariates, and the provenance audit described below.
2. **Matrix-saving alternative: transfer of a fixed 2D consensus target ordering.** Use `AdherentMean` as the frozen source ranking and evaluate its ordering errors across genes within Sanger organoids. This avoids fitting conventional-model predictors. It is a different question: consensus target prioritization, with no claim about loss of genotype/expression relationships or improvement beyond S3’s molecular baseline.
3. **Processing fallback: independent public measurements or pre-joint-correction processed outputs.** Retain the first route’s estimand but replace evidence whose processing crosses the development/evaluation boundary. This remains conditional on locating suitable public observations; “reprocess independently” is not a concrete solution when required inputs are unavailable.

A correlation between minipool effects and the downloaded Broad group-comparison table is useful development evidence. It cannot clear the independent-transfer gate.

**1. One primary estimand for the preferred route**

Choose **format**, based on its six model supports. The intervention bundle is **plastic culture versus Matrigel-dome culture, holding the recorded medium fixed**. It does not isolate geometry from matrix exposure.

For gene \(g\), define measured format lability:

\[
s_g=\frac{1}{6}\sum_{m=1}^{6}
       \frac{1}{|K_m|}\sum_{k\in K_m}
       \left|Y_{mgk,\mathrm{Dome}}-Y_{mgk,\mathrm{Plastic}}\right|.
\]

Here \(K_m\) contains the observed matched media. ACH-003040’s two medium-specific contrasts receive half its model weight each; every other model contributes one contrast. Each model therefore receives weight \(1/6\).

The target family is the **224 test genes outside the exact 200-gene selection tail**, subsequently restricted only by frozen identifier, assay-coverage and source-estimability rules. This is one selected family, with equal target weights.

For transfer:

- Train a molecular dependency predictor \(f_g\) using conventional models only.
- Reserve conventional reference donors \(R\) disjoint from training donors \(T\).
- Apply the **same fitted predictor** to \(R\) and donor-disjoint Sanger organoids \(C\).
- Evaluate within colorectal, oesophageal, gastric, ovarian and pancreatic groups, with equal prespecified group weights. Required source coverage must be demonstrated before locking these groups.
- Retain one sample/library per donor using an outcome-independent selection hierarchy.

For domain \(D\in\{R,C\}\), define target-specific donor-ordering accuracy:

\[
C_g^D=\frac15\sum_{\ell=1}^{5}
 P\!\left[
 (f_g(X_i)-f_g(X_j))(Y_{ig}-Y_{jg})>0
 \mid i,j\text{ distinct donors in group }\ell
 \right],
\]

with ties receiving half credit. Then define transfer loss:

\[
d_g=C_g^R-C_g^C.
\]

Positive values mean worse ordering in organoids. This compares ordering accuracy without subtracting Chronos from Sanger LFC.

The **single primary parameter** is the finite-panel linear-projection coefficient

\[
\boxed{\displaystyle
\beta=
\frac{a^\top M_Xd}{a^\top M_Xa},
\qquad a_g=s_g/\operatorname{IQR}(s).
}
\]

\(M_X\) removes the fixed baseline covariates: source dependency mean and SD, source ordering accuracy, signed and absolute Broad selection-table `MeanDifference`, and the library’s functional-class indicators. Use their fixed column space; overlapping classes do not justify adaptive variable selection.

**Interpretation:** additional loss of correct donor ordering per one-IQR increase in measured format lability, conditional on those baselines, this target family and these environmental supports.

The predictor comparison must include lineage-only, genotype-only, S3-style expression Elastic Net, and genotype-plus-expression models, using the same permitted observations. Select the predictor family and tune it entirely within \(T\), then freeze it before evaluating \(R\) and \(C\). Environmental scores enter the explanatory association, not external predictor selection.

This route still needs the individual-level source matrix. Published group means cannot supply \(C_g^R\).

**2. Selection circularity: exact exclusion plus conditional external evaluation**

The downloaded trace supports this reproducible rule:

1. In `organoids_vs_2d_gene_dependency_tests_full.csv`, retain `DropEssential=False`.
2. Sort by signed `MeanDifference`.
3. Take the lowest 100 and highest 100 genes. **Do not substitute an FDR cutoff.**
4. Match the table’s `SYMBOL (EntrezID)` identifiers to library genes.
5. Exclude their intersection with `All test genes=True`.

That removes **26 of 250 test genes**, leaving **224** before other eligibility exclusions. The tail boundaries have no ties.

However, **224 does not mean selection-independent genes**. Whole functional classes were chosen using the same comparison. The [library documentation](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/data/raw/broad_figshare/README.txt:1) and enrichment trace make that pathway-level selection explicit.

The remaining protection is therefore:

- Condition the claim on the entire historical panel-selection process and fixed family.
- Use the Broad comparison table only as development information and frozen baseline covariates.
- Obtain the evaluation outcome from Sanger donors excluded from all overlapping Broad environmental, selection, training and reference cohorts.
- Exclude uncertain donor matches from confirmatory eligibility.
- Establish that Sanger evaluation outcomes did not influence any source predictor, selection artifact or environmental-score processing artifact.

This can neutralize **reuse of the selection outcome as confirmation**. It cannot identify a genome-wide, selection-unconditional association. Adjusting for `MeanDifference` alone would not establish independence.

**3. Independent units and achievable precision**

Format supplies **seven contrasts across six models**, at most six independent environmental donors pending crosswalk completion. Medium supplies five contrasts across four models; restricting medium to dome gives four clean supports.

The 224 genes are correlated targets. They are not 224 environmental experiments.

There are two different inferential ambitions:

- **Conditional on the six measured environmental supports:** a panel-wide association is feasible in principle. External donors provide repeated evaluations of a fixed vector of measured lability scores. Cross-target dependence must be retained by resampling complete donor outcome vectors.
- **For latent biological sensitivity or new environmental models:** technical measurement error and environmental-model sampling matter. Neither is resolved by having many genes. With collapsed screen estimates and unaudited replicate uncertainty, the latent-sensitivity coefficient remains unidentified.

A rough precision check illustrates the limitation. If a model-cluster influence SD were \(s_u\), an approximate 95% half-width would be:

\[
t_{.975,5}s_u/\sqrt6\approx1.05s_u
\]

for format, versus \(1.59s_u\) for four-model medium. An influence SD of 0.10 already produces approximately ±0.105 for format, before other uncertainty. These are feasibility illustrations, not calibrated intervals for deliberately selected models.

For external ordering accuracy, under a simple independent-donor null, its SE is approximately \(1/(3\sqrt N)\): about 0.027 at 150 donors. A difference between two equally sized domains has SE around 0.038 per target under those assumptions. Donor pairs are dependent; their quadratic count does not provide quadratic precision.

A shared coefficient can be more precise than individual target losses, but that depends on the **actual joint covariance**, residual lability variation after conditioning, and environmental-score uncertainty.

**Verdict:** a conditional panel-wide parameter is plausible. “Only a bound” is not forced by \(n=6\), and a useful bound is not guaranteed. No actual precision claim is defensible before the eligible donor counts and joint uncertainty are established. A bound on *true biological sensitivity* additionally needs a defensible measurement-error model.

**4. Sanger’s permitted role**

Sanger can provide external evidence for the frozen association after establishing continuous-outcome identities, target coverage, donor crosswalks, library selection and processing provenance. Do not inherit S3’s cohort count as this study’s eligible count.

Its pipeline fits spline corrections using cross-sample LFC means and applies ComBat across libraries. Those operations use outcomes and can alter ranks. If fitted wholly within the external cohort, they do not automatically contaminate Broad training, but they couple external observations and require processing-aware uncertainty or a clearly conditional processed-cohort interpretation. If evaluation outcomes influenced development artifacts, the affected processing must be reconstructed or replaced. [Sanger processing code](https://raw.githubusercontent.com/Garnett-Lab/SangerOrganoidBiobank/main/scripts/CRISPR_pipeline.R).

The quarantined BAGEL matrix cannot supply this continuous ordering endpoint. Its 930-column schema also does not establish the intended organoid cohort.

Recover the 18 displayed cell identifiers from retained transcripts without reopening values. Map them to donors and targets. Conservatively exclude implicated external donors, record target exposure, and assess whether that exposure influenced family or endpoint choices. Unrecoverable exposure prevents an intact outcome-unseen claim; it does not automatically invalidate the entire resource.

Sanger cannot identify a causal culture contribution to transfer loss. Platform, library, population and processing differences remain alternative explanations.

**5. Falsification, inconclusive and invalid-result rules**

Propose **\(\delta=0.10\) ordering-accuracy loss per lability IQR**.

Its justification is experimental prioritization: ten additional incorrect orderings per 100 donor comparisons materially degrade a ranking tool; a drop from 0.60 accuracy to 0.50 removes its useful discrimination. This is a proposed decision-based margin, not an established clinical threshold. Its utility rationale must be accepted before evaluation and cannot be enlarged to match attainable precision.

Using one prespecified joint 95% interval \([L,U]\):

| Result | Decision |
|---|---|
| \(L>0.10\) | Support the practically meaningful positive association. |
| \(U<0.10\) | Falsify the claim of an association at least this large. |
| Entire interval lies inside \((-0.10,0.10)\) | Support practical equivalence for this conditional parameter. |
| \(U<-0.10\) | Support a practically meaningful association in the opposite direction. |
| \(L\le0.10\le U\) | Inconclusive about the primary meaningful-positive claim. |

A small positive estimate can therefore falsify the meaningful-positive claim. A nonsignificant estimate with a wide interval cannot.

Additional rules:

- Unresolved provenance, donor identity, score direction or joins: **invalid for confirmation**.
- No demonstrated above-chance source prediction: **no established source relationship whose transfer can be assessed**.
- Zero residual lability variation after baseline conditioning: parameter undefined.
- Material dependence on one environmental model or plausible measurement-error assumptions: no robust biological interpretation; report that limitation.
- One primary coefficient receives the confirmatory decision. Target-specific, pathway and medium analyses remain exploratory.

A bound here concerns the usefulness of the **measured lability score** for explaining this transfer endpoint. It does not bound the total causal contribution of culture conditions.

**6. Novelty sentence**

*The candidate contribution is a selection-conditioned estimate, or informative bound, of the association between measured plastic-to-Matrigel-dome dependency lability and independently evaluated loss of within-lineage donor-ordering accuracy from frozen molecular dependency predictors.*

That distinguishes the estimand from S1’s environmental findings, S2’s dependency/biomarker maps and S3’s transfer evaluation. It remains a candidate novelty claim until the outstanding supplement/code audit checks this exact relationship.

Taking this route requires recording the following limits against the ambitious goal:

- Drop causal attribution to culture, isolated geometry/serum effects, and genotype × state × context discovery.
- Drop genome-wide and new-environmental-model generalization.
- Drop intrinsic heterogeneity and invariance claims unsupported by replicate-level uncertainty.
- Retain an atlas of all 250 test genes, explicitly marking the 26 primary-family exclusions and every subsequent exclusion.
- Keep **C6 unmet** until an externally supported finding or sufficiently precise bound actually passes.
- Keep **C8/C9 unmet**: this narrowed study does not establish policy improvement or 20% resource savings, and exposed Layer A cannot become untouched Layer B through a later split.
- Record that a G1 design approval would not complete the broader explanatory goal or the RSI objective.

No files were edited, and no additional Sanger outcome values were inspected.
tokens used
86,160
**Recommend one fixed, panel-wide association using the six-model format contrast and independently evaluated molecular-prediction loss.** It is potentially G1-passable after resolving data access and preprocessing provenance. **Nothing currently establishes a G1 pass**, and an imprecise null would not rescue the gate.

The [review’s three critical failures](/Users/bmarti44/github/bufferright/research/reviews/g1_review_r1_verdict.md:1) require an operational endpoint, separation from selection outcomes, and an audited processing dependency graph.

1. **Preferred: format lability versus external prediction loss.** Retains the scientific connection between controlled environmental measurements and molecular transfer. Requires individual-level conventional-model data, Sanger continuous outcomes and molecular covariates, and the provenance audit described below.
2. **Matrix-saving alternative: transfer of a fixed 2D consensus target ordering.** Use `AdherentMean` as the frozen source ranking and evaluate its ordering errors across genes within Sanger organoids. This avoids fitting conventional-model predictors. It is a different question: consensus target prioritization, with no claim about loss of genotype/expression relationships or improvement beyond S3’s molecular baseline.
3. **Processing fallback: independent public measurements or pre-joint-correction processed outputs.** Retain the first route’s estimand but replace evidence whose processing crosses the development/evaluation boundary. This remains conditional on locating suitable public observations; “reprocess independently” is not a concrete solution when required inputs are unavailable.

A correlation between minipool effects and the downloaded Broad group-comparison table is useful development evidence. It cannot clear the independent-transfer gate.

**1. One primary estimand for the preferred route**

Choose **format**, based on its six model supports. The intervention bundle is **plastic culture versus Matrigel-dome culture, holding the recorded medium fixed**. It does not isolate geometry from matrix exposure.

For gene \(g\), define measured format lability:

\[
s_g=\frac{1}{6}\sum_{m=1}^{6}
       \frac{1}{|K_m|}\sum_{k\in K_m}
       \left|Y_{mgk,\mathrm{Dome}}-Y_{mgk,\mathrm{Plastic}}\right|.
\]

Here \(K_m\) contains the observed matched media. ACH-003040’s two medium-specific contrasts receive half its model weight each; every other model contributes one contrast. Each model therefore receives weight \(1/6\).

The target family is the **224 test genes outside the exact 200-gene selection tail**, subsequently restricted only by frozen identifier, assay-coverage and source-estimability rules. This is one selected family, with equal target weights.

For transfer:

- Train a molecular dependency predictor \(f_g\) using conventional models only.
- Reserve conventional reference donors \(R\) disjoint from training donors \(T\).
- Apply the **same fitted predictor** to \(R\) and donor-disjoint Sanger organoids \(C\).
- Evaluate within colorectal, oesophageal, gastric, ovarian and pancreatic groups, with equal prespecified group weights. Required source coverage must be demonstrated before locking these groups.
- Retain one sample/library per donor using an outcome-independent selection hierarchy.

For domain \(D\in\{R,C\}\), define target-specific donor-ordering accuracy:

\[
C_g^D=\frac15\sum_{\ell=1}^{5}
 P\!\left[
 (f_g(X_i)-f_g(X_j))(Y_{ig}-Y_{jg})>0
 \mid i,j\text{ distinct donors in group }\ell
 \right],
\]

with ties receiving half credit. Then define transfer loss:

\[
d_g=C_g^R-C_g^C.
\]

Positive values mean worse ordering in organoids. This compares ordering accuracy without subtracting Chronos from Sanger LFC.

The **single primary parameter** is the finite-panel linear-projection coefficient

\[
\boxed{\displaystyle
\beta=
\frac{a^\top M_Xd}{a^\top M_Xa},
\qquad a_g=s_g/\operatorname{IQR}(s).
}
\]

\(M_X\) removes the fixed baseline covariates: source dependency mean and SD, source ordering accuracy, signed and absolute Broad selection-table `MeanDifference`, and the library’s functional-class indicators. Use their fixed column space; overlapping classes do not justify adaptive variable selection.

**Interpretation:** additional loss of correct donor ordering per one-IQR increase in measured format lability, conditional on those baselines, this target family and these environmental supports.

The predictor comparison must include lineage-only, genotype-only, S3-style expression Elastic Net, and genotype-plus-expression models, using the same permitted observations. Select the predictor family and tune it entirely within \(T\), then freeze it before evaluating \(R\) and \(C\). Environmental scores enter the explanatory association, not external predictor selection.

This route still needs the individual-level source matrix. Published group means cannot supply \(C_g^R\).

**2. Selection circularity: exact exclusion plus conditional external evaluation**

The downloaded trace supports this reproducible rule:

1. In `organoids_vs_2d_gene_dependency_tests_full.csv`, retain `DropEssential=False`.
2. Sort by signed `MeanDifference`.
3. Take the lowest 100 and highest 100 genes. **Do not substitute an FDR cutoff.**
4. Match the table’s `SYMBOL (EntrezID)` identifiers to library genes.
5. Exclude their intersection with `All test genes=True`.

That removes **26 of 250 test genes**, leaving **224** before other eligibility exclusions. The tail boundaries have no ties.

However, **224 does not mean selection-independent genes**. Whole functional classes were chosen using the same comparison. The [library documentation](/Users/bmarti44/github/bufferright/research/cancer-dependency-rsi/data/raw/broad_figshare/README.txt:1) and enrichment trace make that pathway-level selection explicit.

The remaining protection is therefore:

- Condition the claim on the entire historical panel-selection process and fixed family.
- Use the Broad comparison table only as development information and frozen baseline covariates.
- Obtain the evaluation outcome from Sanger donors excluded from all overlapping Broad environmental, selection, training and reference cohorts.
- Exclude uncertain donor matches from confirmatory eligibility.
- Establish that Sanger evaluation outcomes did not influence any source predictor, selection artifact or environmental-score processing artifact.

This can neutralize **reuse of the selection outcome as confirmation**. It cannot identify a genome-wide, selection-unconditional association. Adjusting for `MeanDifference` alone would not establish independence.

**3. Independent units and achievable precision**

Format supplies **seven contrasts across six models**, at most six independent environmental donors pending crosswalk completion. Medium supplies five contrasts across four models; restricting medium to dome gives four clean supports.

The 224 genes are correlated targets. They are not 224 environmental experiments.

There are two different inferential ambitions:

- **Conditional on the six measured environmental supports:** a panel-wide association is feasible in principle. External donors provide repeated evaluations of a fixed vector of measured lability scores. Cross-target dependence must be retained by resampling complete donor outcome vectors.
- **For latent biological sensitivity or new environmental models:** technical measurement error and environmental-model sampling matter. Neither is resolved by having many genes. With collapsed screen estimates and unaudited replicate uncertainty, the latent-sensitivity coefficient remains unidentified.

A rough precision check illustrates the limitation. If a model-cluster influence SD were \(s_u\), an approximate 95% half-width would be:

\[
t_{.975,5}s_u/\sqrt6\approx1.05s_u
\]

for format, versus \(1.59s_u\) for four-model medium. An influence SD of 0.10 already produces approximately ±0.105 for format, before other uncertainty. These are feasibility illustrations, not calibrated intervals for deliberately selected models.

For external ordering accuracy, under a simple independent-donor null, its SE is approximately \(1/(3\sqrt N)\): about 0.027 at 150 donors. A difference between two equally sized domains has SE around 0.038 per target under those assumptions. Donor pairs are dependent; their quadratic count does not provide quadratic precision.

A shared coefficient can be more precise than individual target losses, but that depends on the **actual joint covariance**, residual lability variation after conditioning, and environmental-score uncertainty.

**Verdict:** a conditional panel-wide parameter is plausible. “Only a bound” is not forced by \(n=6\), and a useful bound is not guaranteed. No actual precision claim is defensible before the eligible donor counts and joint uncertainty are established. A bound on *true biological sensitivity* additionally needs a defensible measurement-error model.

**4. Sanger’s permitted role**

Sanger can provide external evidence for the frozen association after establishing continuous-outcome identities, target coverage, donor crosswalks, library selection and processing provenance. Do not inherit S3’s cohort count as this study’s eligible count.

Its pipeline fits spline corrections using cross-sample LFC means and applies ComBat across libraries. Those operations use outcomes and can alter ranks. If fitted wholly within the external cohort, they do not automatically contaminate Broad training, but they couple external observations and require processing-aware uncertainty or a clearly conditional processed-cohort interpretation. If evaluation outcomes influenced development artifacts, the affected processing must be reconstructed or replaced. [Sanger processing code](https://raw.githubusercontent.com/Garnett-Lab/SangerOrganoidBiobank/main/scripts/CRISPR_pipeline.R).

The quarantined BAGEL matrix cannot supply this continuous ordering endpoint. Its 930-column schema also does not establish the intended organoid cohort.

Recover the 18 displayed cell identifiers from retained transcripts without reopening values. Map them to donors and targets. Conservatively exclude implicated external donors, record target exposure, and assess whether that exposure influenced family or endpoint choices. Unrecoverable exposure prevents an intact outcome-unseen claim; it does not automatically invalidate the entire resource.

Sanger cannot identify a causal culture contribution to transfer loss. Platform, library, population and processing differences remain alternative explanations.

**5. Falsification, inconclusive and invalid-result rules**

Propose **\(\delta=0.10\) ordering-accuracy loss per lability IQR**.

Its justification is experimental prioritization: ten additional incorrect orderings per 100 donor comparisons materially degrade a ranking tool; a drop from 0.60 accuracy to 0.50 removes its useful discrimination. This is a proposed decision-based margin, not an established clinical threshold. Its utility rationale must be accepted before evaluation and cannot be enlarged to match attainable precision.

Using one prespecified joint 95% interval \([L,U]\):

| Result | Decision |
|---|---|
| \(L>0.10\) | Support the practically meaningful positive association. |
| \(U<0.10\) | Falsify the claim of an association at least this large. |
| Entire interval lies inside \((-0.10,0.10)\) | Support practical equivalence for this conditional parameter. |
| \(U<-0.10\) | Support a practically meaningful association in the opposite direction. |
| \(L\le0.10\le U\) | Inconclusive about the primary meaningful-positive claim. |

A small positive estimate can therefore falsify the meaningful-positive claim. A nonsignificant estimate with a wide interval cannot.

Additional rules:

- Unresolved provenance, donor identity, score direction or joins: **invalid for confirmation**.
- No demonstrated above-chance source prediction: **no established source relationship whose transfer can be assessed**.
- Zero residual lability variation after baseline conditioning: parameter undefined.
- Material dependence on one environmental model or plausible measurement-error assumptions: no robust biological interpretation; report that limitation.
- One primary coefficient receives the confirmatory decision. Target-specific, pathway and medium analyses remain exploratory.

A bound here concerns the usefulness of the **measured lability score** for explaining this transfer endpoint. It does not bound the total causal contribution of culture conditions.

**6. Novelty sentence**

*The candidate contribution is a selection-conditioned estimate, or informative bound, of the association between measured plastic-to-Matrigel-dome dependency lability and independently evaluated loss of within-lineage donor-ordering accuracy from frozen molecular dependency predictors.*

That distinguishes the estimand from S1’s environmental findings, S2’s dependency/biomarker maps and S3’s transfer evaluation. It remains a candidate novelty claim until the outstanding supplement/code audit checks this exact relationship.

Taking this route requires recording the following limits against the ambitious goal:

- Drop causal attribution to culture, isolated geometry/serum effects, and genotype × state × context discovery.
- Drop genome-wide and new-environmental-model generalization.
- Drop intrinsic heterogeneity and invariance claims unsupported by replicate-level uncertainty.
- Retain an atlas of all 250 test genes, explicitly marking the 26 primary-family exclusions and every subsequent exclusion.
- Keep **C6 unmet** until an externally supported finding or sufficiently precise bound actually passes.
- Keep **C8/C9 unmet**: this narrowed study does not establish policy improvement or 20% resource savings, and exposed Layer A cannot become untouched Layer B through a later split.
- Record that a G1 design approval would not complete the broader explanatory goal or the RSI objective.

No files were edited, and no additional Sanger outcome values were inspected.
