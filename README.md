# It's the Medium

**Live site: [itsthemedium.com](https://www.itsthemedium.com)** · Demo video (3 min): [`its-the-medium-3min.mp4`](cancer-dependency-rsi/video/out/its-the-medium-3min.mp4) · Extended cut (5 min): [`its-the-medium.mp4`](cancer-dependency-rsi/video/out/its-the-medium.mp4)

An independent audit of two 2026 Nature studies that used organoids (tiny 3D copies of patients' tumours) to find genes cancers can't live without, as leads for new drugs.

## The problem, in one minute

Organoids differ from ordinary flat lab cells in two ways at once: their **3D shape**, and their **food**. Organoids are grown in a clean, lab-made liquid (the "medium") with almost no cholesterol. Flat cells usually get serum, the nutrient-rich part of blood.

So when a gene matters more in an organoid, is that because of the shape (the whole point of organoids), or just the diet?

The public DepMap database already held the control nobody had used: flat cells grown on the organoid medium. Same food, no 3D shape. We ran that check on all 17,525 genes.

**Result:** of the 456 genes that clearly behave differently in organoids, **387 (85%) change just as much in flat cells once they get the organoid food.** The effect follows the food, not the shape. The clearest case is cholesterol: with none in the food, cells must make their own, so cholesterol-making genes such as SQLE suddenly look essential. In a patient, tumours are fed by blood full of cholesterol, so those weaknesses may not exist there at all.

Of the other 69 genes, 68 are unresolved by the data and one (LSM7) leans weakly toward shape. Three Sanger headline genes (SCAP, DDX3X, ITGB1) are in the unresolved group: the more credible leads.

**The cheap test this points to:** put cholesterol back into the organoid medium and see whether these genes stop mattering. About two weeks, no new screen.

## How Meta's models are used

### 1. Muse ran the research loop

Muse Code, Meta's coding agent, was the host agent for the whole audit, under human direction. It ran the orchestration loop: it planned each step, wrote and ran the local analysis code, dispatched candidate generation and reviews, applied fixes, and kept the append-only record of every generation and decision.

- Loop specification and goal: [`cancer_rsi_handoff.txt`](cancer_rsi_handoff.txt), [`GOAL.md`](GOAL.md), [`PLAN.md`](PLAN.md)
- Every research generation, including failures and retractions: [`cancer-dependency-rsi/GENERATIONS.md`](cancer-dependency-rsi/GENERATIONS.md) and [`cancer-dependency-rsi/generations/`](cancer-dependency-rsi/generations/)
- Raw event logs, receipts and verdicts for every model call: [`cancer-dependency-rsi/reviews/`](cancer-dependency-rsi/reviews/)

Candidate generation and adversarial reviews were sent to a separate model (`gpt-6.1-sol` through the Codex CLI, recorded in [`config/host.json`](cancer-dependency-rsi/config/host.json)), so the reviewer was never the model that wrote the work. Reviews ran over five rounds (68 to 95 out of 100), and one early finding that didn't hold up was dropped.

All statistics run locally in Python. No model invents a number.

### 2. Muse is the research assistant on the live site

The site calls **Muse Spark** (`muse-spark-1.3`) through the Meta Model API Responses endpoint, from an AWS Lambda ([`cancer-dependency-rsi/deploy/lambda/index.mjs`](cancer-dependency-rsi/deploy/lambda/index.mjs)). Three features use it:

| Feature | What Muse does |
|---|---|
| **Gene summaries** | Turns one gene's numbers into a short, everyday-language verdict with a section for researchers |
| **Ask the data** | Works as an agent. It picks from three function tools, runs several rounds of searches over the full 17,525-gene table, then answers. Every tool step is shown live, and every gene it names links back to the data. |
| **Check a hit list** | A researcher pastes their own gene list (aliases like HER2 are resolved). The list is checked against the table, and Muse explains which genes look like diet effects and which are worth chasing. |

Tools Muse can call:

- `lookup_genes`: exact results for named genes
- `find_genes`: filtered, ranked searches (by verdict, effect size, published list, or curated pathway sets such as cholesterol synthesis and ribosome genes)
- `check_hit_list`: the full verdict breakdown for a pasted list

Muse only sees the audit through these tools, which keeps its answers tied to the real table. It is told never to give medical advice, and it declines personal treatment questions.

The API key lives only in AWS SSM Parameter Store (SecureString) and is read by the Lambda at runtime. It never reaches the browser or this repo. The Lambda URL only accepts requests through CloudFront, and each route is rate-limited.

## For researchers

- Method, statistics and limits: the "For researchers" and "Method" sections of the [live site](https://www.itsthemedium.com), and [`cancer-dependency-rsi/FINDINGS.md`](cancer-dependency-rsi/FINDINGS.md)
- Data: DepMap 26Q3 Chronos gene effects (Broad NextGen and Sanger organoid catalogues) plus the cited public supplementary tables
- Validation: results checked on held-out patient samples, 150 reruns on reshuffled data, 110 automated tests (`cd cancer-dependency-rsi && .venv/bin/python -m pytest -q`)
- The research log and gate status: [`cancer-dependency-rsi/README.md`](cancer-dependency-rsi/README.md), [`STATUS.md`](cancer-dependency-rsi/STATUS.md)

These are consistency labels from observational data, not proof of cause. This is a research tool, not medical advice.

## Built during the hackathon

All code, analysis, the site and the video were made during the event, starting 28 October 2026. The only older files are third-party public datasets (for example the Sanger supplementary tables in `cancer-dependency-rsi/data/raw/`), used under their published licences (CC BY 4.0) and listed in the data manifests.

Credits: Muse and Codex did much of the research, Muse drafted the first version of the website, and Claude polished it. Narration and music by ElevenLabs.
