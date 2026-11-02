// itsthemedium.com AI endpoint (Muse Code via api.meta.ai Responses API).
// The API key lives in SSM Parameter Store (SecureString) and is only read here, server-side.
// Routes (served by CloudFront under /api/*):
//   GET /api/brief?gene=SQLE   simple-language + researcher brief for one gene
//   GET /api/ask?q=...         question answered by a tool-using Muse agent over all 17,525 genes
//   GET /api/list?genes=A,B,C  explain a researcher's own hit list (agent, same tools)
import { readFileSync } from "node:fs";
import { SSMClient, GetParameterCommand } from "@aws-sdk/client-ssm";

const MODEL = process.env.MUSE_MODEL || "muse-spark-1.3";
const EFFORT = process.env.MUSE_EFFORT || "low";
const BASE = process.env.MUSE_BASE || "https://api.meta.ai/v1";
const PARAM = process.env.KEY_PARAM || "/itsthemedium/muse-api-key";

const GENES = JSON.parse(readFileSync(new URL("./genes.json", import.meta.url)));
const STATS = JSON.parse(readFileSync(new URL("./stats.json", import.meta.url)));
const BYG = new Map(GENES.map(g => [g.g.toUpperCase(), g]));
const VERDICT = ["below the hit threshold (no meaningful organoid difference)", "medium-consistent", "unresolved", "format candidate (shape-related)"];
const TAGS = { broad_gain: "Broad published gain", broad_loss: "Broad published loss", broad_strict: "Broad strict gain", sanger18: "Sanger headline-18", sanger97: "Sanger exclusive-97" };

let keyPromise = null;
function getKey() {
  if (!keyPromise) {
    keyPromise = new SSMClient({}).send(new GetParameterCommand({ Name: PARAM, WithDecryption: true }))
      .then(r => r.Parameter.Value.trim())
      .catch(e => { keyPromise = null; throw e; });
  }
  return keyPromise;
}

/* ---------- light per-container abuse guard (reserved concurrency is the hard cap) ---------- */
/* gene briefs are cached at the edge per gene, so they get a generous budget; free-text questions a tighter one */
const hits = new Map();
const LIMITS = { brief: 150, ask: 30, list: 20 };
function limited(ip, kind) {
  const now = Date.now(), win = 10 * 60 * 1000, key = kind + "|" + ip;
  const arr = (hits.get(key) || []).filter(t => now - t < win);
  arr.push(now); hits.set(key, arr);
  if (hits.size > 5000) hits.clear();
  return arr.length > LIMITS[kind];
}

const f2 = v => v == null ? "n/a" : (v > 0 ? "+" : "") + Number(v).toFixed(2);
const pct = v => v == null ? "n/a" : Math.round(v * 100) + "%";
function geneFacts(g) {
  return [
    `Gene: ${g.g}`,
    `Verdict: ${VERDICT[g.f]}`,
    `D (organoid minus classic 2D, normalized Chronos; negative = organoids need it more): ${f2(g.D)} (q=${g.Dq == null ? "n/a" : g.Dq.toExponential(2)})`,
    `A (same comparison but flat cells fed organoid-type medium): ${f2(g.A)}`,
    `Share of the organoid effect reproduced by medium alone (A/D): ${g.rA == null ? "n/a" : pct(g.rA)} [90% CI ${g.rAlo == null ? "n/a" : pct(g.rAlo)} to ${g.rAhi == null ? "n/a" : pct(g.rAhi)}]`,
    `F (3D dome vs flat, both in organoid-type medium): ${f2(g.F)}`,
    `S (unrelated serum-free brain-cancer medium): ${f2(g.S)}`,
    `Bootstrap stability of medium-consistent call: ${g.bf == null ? "n/a" : pct(g.bf)} of 150 resamples`,
    `Published list membership: ${(g.tags || []).map(t => TAGS[t] || t).join(", ") || "none"}`,
  ].join("\n");
}

const STUDY = `About the study ("It's the Medium", an independent reanalysis of public data):
- In 2026 the Broad (Neiswender et al., Nature) and Sanger (Herranz-Ors et al., Nature) published CRISPR maps of genes that patient-derived organoids (lab-grown mini-tumours) depend on, and nominated "organoid-specific" drug targets.
- Organoids differ from classic flat (2D) cultures in two ways at once: 3D shape and food. Classic cultures get serum (rich in cholesterol and lipids); organoids get a defined serum-free medium.
- Control used: other cancer models grown flat but fed organoid-type medium. If a gene's organoid effect also appears there, the effect tracks the food, not the shape.
- Result: of 456 genes whose importance differs between organoids and 2D (q<0.01, |effect|>=0.25), 387 (85%) are medium-consistent; 68 are unresolved; 1 (LSM7) is a nominal shape candidate, not significant genome-wide (always keep that qualifier attached when you mention LSM7). 86% of gains and 84% of losses are medium-consistent (75 to 82% under robust statistics). Bootstrap slope 0.90 [0.82 to 0.99]; held-out patients slope 0.96.
- Strongest medium-consistent class: cholesterol/sterol synthesis (SQLE, MSMO1, MVD, IDI1, FDFT1), then fatty-acid and heme synthesis, matching what a lipid-poor diet would stress. Expression shows cholesterol genes switched on in organoid medium; in blood-like medium (HPLM) screens SQLE moves the opposite way.
- Sanger headline-18: 8 of 16 replicate here, 5 medium-consistent (MVD, IDI1, MBTPS1, MBTPS2 on the SREBP/sterol axis), 3 unresolved (SCAP, DDX3X, ITGB1), the more credible follow-ups. Broad published gains: 47% (135/285) medium-consistent.
- "Unresolved" is a catch-all for genes where neither food nor shape explains the effect clearly; it is not an endorsement. Do not call all 68 unresolved genes good targets. The audit names SCAP, DDX3X and ITGB1 (unresolved members of the Sanger headline-18) as the more credible follow-ups.
- Ribosome genes look less essential in organoids; leading but untested explanation is slower growth.
- Proposed test: add LDL cholesterol back to organoid medium. If sterol dependencies are starvation, SQLE-inhibitor and statin sensitivity should collapse (>=5x potency shift) while genuine candidates like ITGB1 do not change.
- Limits: observational consistency labels, not causal proof; 9 flat comparator models across 6 lineages; not medical advice.`;

const STYLE = `Writing rules (strict):
- Hyphenate compound words and modifiers: follow-up, lab-grown, organoid-type medium, food-driven, genome-wide, lipid-poor, add-back, shape-specific, fat-like. Only em dashes and en dashes are banned.
- Say "consistency labels, not proof" when you note the limits.
- Effects are about degree: "needed more" or "needed less". Never say cells survive, die or "can live" without a gene.
- Write for a curious adult with no biology background, then give researchers the precise detail. Never use the phrase "plain English".
- Short sentences. Plain words. Explain any term you must use.
- Never use em dashes or en dashes. Use commas, periods, or parentheses. Write negative numbers with a plain hyphen, like -0.43. Normal hyphens in compound words are fine and expected (nutrient-rich, follow-up, lipid-poor).
- Never write the data codes MED, UNR, FMT or S18. Say "follows the food", "unresolved", "shape candidate" and "Sanger headline-18" instead.
- No hype, no filler, no "In summary", no "It's important to note", no "delve", no emojis.
- Use an analogy only when the question asks for a simple explanation (for a child or a beginner), at most one, and only if it is accurate. Never present an analogy as a literal fact.
- Hyphenate compound modifiers (fat-like molecules, shape-specific, genome-wide, follow-up as a noun, food-driven). End questions with "?". Do not address the reader by role (no "Researchers, ...").
- If the question asks for a simple explanation (for a child or a beginner): under 120 words, no q-values, statistics symbols or effect-size numbers except the 387 of 456 count, no audit labels like "food-driven" or "shape-specific", and at most one example gene.
- Say "3D shape", never "lab-grown shape".
- Grammar: "follows the food" is a verb phrase, so conjugate it: one gene follows the food; several genes follow the food.
- Unresolved genes are not shape genes. Only LSM7 is a (nominal) shape candidate. Do not suggest any other gene is about shape.
- Calm, precise wording. Call serum "serum, the nutrient-rich liquid part of blood"; never "bloody". Avoid slang and gross or dramatic images.
- Be honest about uncertainty. These are consistency labels from observational data, not proof. Never give medical advice.
- Use only the numbers provided. Do not invent statistics, papers or drug names.`;

function briefPrompt(g) {
  return {
    instructions: `You explain one gene's result from a cancer research audit.\n\n${STUDY}\n\n${STYLE}
Output exactly these three sections in Markdown, total under 190 words:
**What this gene does**
One or two sentences on its normal job in the cell, in everyday language (use an analogy if it helps). If you are not confident about this gene's function, say it is less well studied.
**What we found**
Two or three sentences translating the numbers into simple, everyday words: does the organoid effect show up when only the food changes? What does the verdict mean for someone hoping this is a cancer drug target?
**For researchers**
2 or 3 terse bullet points: key values (D, A, A/D with CI, F, bootstrap stability, list membership) and the single most useful next experiment.`,
    input: geneFacts(g),
    max: 520,
  };
}

/* ---------- tools Muse can call: computed rows from all 17,525 genes, never free text ---------- */
const VNAME = ["no real difference", "follows the food", "unresolved", "shape candidate"];
const VKEY = { follows_food: 1, unresolved: 2, shape: 3, no_difference: 0 };
const LISTNAME = { broad_gain: "Broad published gains", broad_loss: "Broad published losses", broad_strict: "Broad strict gains", sanger18: "Sanger headline-18", sanger97: "Sanger exclusive-97" };
const r2 = v => v == null ? null : Math.round(v * 100) / 100;
const share = g => g.rA == null || g.f === 0 ? null : Math.round(g.rA * 100) + "%";
const fullRow = g => ({
  gene: g.g, verdict: VNAME[g.f], D_organoid_vs_2D: r2(g.D), D_q: g.Dq == null ? null : Number(g.Dq.toPrecision(2)),
  A_food_only: r2(g.A), F_shape_only: r2(g.F), S_other_serum_free_diet: r2(g.S),
  share_reproduced_by_food: share(g), share_ci90: g.rAlo == null ? null : `${Math.round(g.rAlo * 100)}% to ${Math.round(g.rAhi * 100)}%`,
  reruns_calling_it_food_driven: g.bf == null ? null : pct(g.bf), lists: (g.tags || []).map(t => TAGS[t] || t),
});
const shortRow = g => `${g.g}: ${VNAME[g.f]}, D ${f2(g.D)}, A ${f2(g.A)}${share(g) ? ", food share " + share(g) : ""}${g.bf != null ? ", called food-driven in " + pct(g.bf) + " of reruns" : ""}${(g.tags || []).length ? ", " + g.tags.map(t => TAGS[t] || t).join("/") : ""}`;
function breakdown(rows) {
  const c = [0, 0, 0, 0]; rows.forEach(g => c[g.f]++);
  return { follows_the_food: c[1], unresolved: c[2], shape_candidate: c[3], no_real_difference: c[0] };
}
function cleanSymbols(arr, max) {
  return [...new Set((Array.isArray(arr) ? arr : []).map(s => String(s).trim().toUpperCase()).filter(s => /^[A-Z0-9][A-Z0-9.-]{0,14}$/.test(s)))].slice(0, max);
}
/* curated pathway sets, so family questions are not answered by loose symbol prefixes */
const SETS = {
  ribosome: { label: "core ribosome proteins", test: g => /^RP[LS]\d+[AXY]?\d?$/.test(g) && !/^RPS6K/.test(g) || ["RPLP0", "RPLP1", "RPLP2", "RPSA"].includes(g) },
  mito_ribosome: { label: "mitochondrial ribosome proteins", test: g => /^MRP[LS]\d+$/.test(g) },
  cholesterol_synthesis: { label: "cholesterol-making enzymes", list: ["ACAT2", "HMGCS1", "HMGCR", "MVK", "PMVK", "MVD", "IDI1", "FDPS", "FDFT1", "SQLE", "LSS", "CYP51A1", "TM7SF2", "LBR", "MSMO1", "NSDHL", "HSD17B7", "EBP", "SC5D", "DHCR7", "DHCR24"] },
  srebp_sterol_sensing: { label: "sterol sensing (SREBP switch)", list: ["SCAP", "SREBF1", "SREBF2", "MBTPS1", "MBTPS2", "INSIG1", "INSIG2", "LDLR", "NPC1", "NPC2"] },
  fatty_acid_synthesis: { label: "fatty-acid-making enzymes", list: ["ACLY", "ACACA", "FASN", "SCD", "ELOVL1", "ELOVL5", "ELOVL6", "FADS1", "FADS2", "HSD17B12", "TECR", "HACD3"] },
  heme_synthesis: { label: "heme-making enzymes", list: ["ALAS1", "ALAD", "HMBS", "UROS", "UROD", "CPOX", "PPOX", "FECH"] },
};
for (const k in SETS) if (SETS[k].list) { const L = new Set(SETS[k].list); SETS[k].test = g => L.has(g); }
const plural = (n, w) => `${n.toLocaleString("en-US")} ${w}${n === 1 ? "" : "s"}`;

const TOOLS = [
  { type: "function", name: "lookup_genes",
    description: "Get the full computed result for specific genes from the study table of 17,525 genes: verdict, effect sizes (D organoid vs 2D, A food only, F shape only, S another serum-free diet; negative means organoids need the gene more), share of the organoid effect reproduced by food alone with its 90% interval, bootstrap stability, q-value and published-list membership.",
    parameters: { type: "object", properties: { symbols: { type: "array", items: { type: "string" }, description: "Official gene symbols, up to 25, e.g. [\"SQLE\",\"ITGB1\"]" } }, required: ["symbols"], additionalProperties: false } },
  { type: "function", name: "find_genes",
    description: "Filter and rank the full table. Returns how many genes match, how the matches split across verdicts, and the top rows. Use it for any 'which' or 'how many' question: which cholesterol genes follow the food (gene_set cholesterol_synthesis), how many ribosome genes changed (gene_set ribosome), how many Broad published gains follow the food, the strongest unresolved genes, or genes organoids need less.",
    parameters: { type: "object", properties: {
      verdict: { type: "string", enum: ["any", "changed", "follows_food", "unresolved", "shape", "no_difference"], description: "\"changed\" means any of the 456 genes that differ between organoids and 2D" },
      direction: { type: "string", enum: ["any", "organoids_need_more", "organoids_need_less"] },
      list: { type: "string", enum: ["any", "broad_gain", "broad_loss", "broad_strict", "sanger18", "sanger97"], description: "Restrict to a published list" },
      gene_set: { type: "string", enum: ["any", ...Object.keys(SETS)], description: "Restrict to a curated pathway set. Prefer this for gene-family questions (ribosome, cholesterol, fatty acids, heme, sterol sensing)." },
      symbol_prefixes: { type: "array", items: { type: "string" }, description: "Keep genes whose symbol starts with any of these. Use only when no gene_set fits." },
      sort: { type: "string", enum: ["strongest_effect", "most_explained_by_food", "least_explained_by_food"] },
      limit: { type: "integer", description: "Rows to return, 1 to 40 (default 15)" },
    }, additionalProperties: false } },
  { type: "function", name: "check_hit_list",
    description: "Classify a researcher's own gene list (for example hits from their organoid screen) against the table. Returns the verdict breakdown, a short row for every gene found, and the symbols not in the table.",
    parameters: { type: "object", properties: { symbols: { type: "array", items: { type: "string" }, description: "Gene symbols, up to 300" } }, required: ["symbols"], additionalProperties: false } },
];

/* each tool returns {data} for the model and {step} as a simple progress line for the reader */
function runTool(name, args) {
  if (name === "lookup_genes") {
    const syms = cleanSymbols(args.symbols, 25);
    const found = syms.filter(s => BYG.has(s));
    return { step: `Looked up ${found.length ? found.slice(0, 6).join(", ") + (found.length > 6 ? ` and ${found.length - 6} more` : "") : "the genes"}${found.length < syms.length ? ` (${syms.length - found.length} not in the table)` : ""}`,
      data: { genes: found.map(s => fullRow(BYG.get(s))), not_in_table: syms.filter(s => !BYG.has(s)) } };
  }
  if (name === "find_genes") {
    let rows = GENES;
    const v = args.verdict || "any", d = args.direction || "any", l = args.list || "any";
    const pre = cleanSymbols(args.symbol_prefixes, 12);
    if (v === "changed") rows = rows.filter(g => g.f > 0); else if (v in VKEY) rows = rows.filter(g => g.f === VKEY[v]);
    if (d === "organoids_need_more") rows = rows.filter(g => g.D < 0); else if (d === "organoids_need_less") rows = rows.filter(g => g.D > 0);
    if (l in LISTNAME) rows = rows.filter(g => (g.tags || []).includes(l));
    const gs = SETS[args.gene_set];
    if (gs) rows = rows.filter(g => gs.test(g.g));
    if (pre.length) rows = rows.filter(g => pre.some(p => g.g.startsWith(p)));
    const s = args.sort || "strongest_effect";
    const fs = g => g.rA == null || g.f === 0 ? null : Math.min(g.rA, 1.5);
    rows = [...rows].sort(s === "strongest_effect" ? (a, b) => Math.abs(b.D) - Math.abs(a.D)
      : (a, b) => { const x = fs(a), y = fs(b); if (x == null) return 1; if (y == null) return -1; return s === "most_explained_by_food" ? y - x : x - y; });
    const lim = Math.max(1, Math.min(40, parseInt(args.limit, 10) || 15));
    const what = [v === "any" ? "" : v === "changed" ? "changed genes" : VNAME[VKEY[v]], d === "any" ? "" : d === "organoids_need_more" ? "needed more by organoids" : "needed less by organoids",
      l in LISTNAME ? "in " + LISTNAME[l] : "", gs ? gs.label : "", pre.length ? "symbol starts " + pre.join(" or ") : ""].filter(Boolean).join(", ");
    return { step: `Searched all 17,525 genes${what ? " (" + what + ")" : ""}: ${rows.length.toLocaleString("en-US")} ${rows.length === 1 ? "match" : "match" + "es"}`,
      data: { total_matching: rows.length, verdict_breakdown: breakdown(rows), rows: rows.slice(0, lim).map(shortRow) } };
  }
  if (name === "check_hit_list") {
    const syms = cleanSymbols(args.symbols, 300);
    const found = syms.filter(s => BYG.has(s)).map(s => BYG.get(s));
    const b = breakdown(found);
    const nf = syms.length - found.length;
    const parts = [[b.follows_the_food, b.follows_the_food === 1 ? "follows the food" : "follow the food"], [b.unresolved, "unresolved"], [b.shape_candidate, "shape candidate"], [b.no_real_difference, "no real difference"], [nf, "not in the table"]].filter(x => x[0]).map(x => x[0] + " " + x[1]);
    return { step: `Checked ${plural(syms.length, "gene")} against the table: ${parts.join(", ")}`,
      data: { checked: syms.length, found: found.length, verdict_breakdown: b, not_in_table: syms.filter(s => !BYG.has(s)),
        rows: found.sort((a, c) => (a.f === 0) - (c.f === 0) || Math.abs(c.D) - Math.abs(a.D)).map(shortRow) } };
  }
  return { step: null, data: { error: "unknown tool" } };
}

const WORK = `How to work:
- Use the tools to get facts before answering. Every number you quote must come from a tool result or the study summary above. Never invent numbers.
- Prefer one to three well-chosen tool calls. For "which" or "how many" questions and gene families, use find_genes (with gene_set when one fits) so the answer covers every matching gene, and give the count in the first sentence. Use lookup_genes for named genes.
- Only make claims that hold for every gene you group together. Group genes by function only when you are sure of each gene's function; otherwise list them as "other genes".
- Do not suggest experiments the data already contains (flat cells fed organoid medium is already measured).
- You may use general biology knowledge about what genes do.
- In tool results, D is the organoid effect versus classic 2D (negative = organoids need the gene more) and A is the same comparison in flat cells fed organoid medium.`;

function askPrompt(q) {
  return {
    instructions: `You answer questions about a cancer research audit. You have tools that query the full computed table of 17,525 genes.\n\n${STUDY}\n\n${STYLE}\n\n${WORK}
If the question is unrelated to this study, cancer biology or how to read the site, do not call any tool; reply in one sentence that you can only answer questions about this audit.
Final answer: under 170 words of Markdown. Lead with a direct one-sentence answer in simple, everyday words, then supporting detail. Mention genes by symbol so readers can look them up.`,
    input: `Question: ${q}`,
    max: 480, tools: true,
  };
}

function listPrompt(syms) {
  return {
    instructions: `A researcher pasted a list of genes, usually hits from their own organoid CRISPR screen or a drug-target shortlist. Your job: tell them which hits look like diet (culture medium) effects and which deserve follow-up.\n\n${STUDY}\n\n${STYLE}\n\n${WORK}
- The check_hit_list result for their list is already in the input. Call lookup_genes for up to 6 key genes if you need their full detail, or find_genes to compare with a published list. Do not call check_hit_list again.
Final answer: Markdown, under 230 words, exactly these sections:
**The short answer**
One or two plain sentences: how much of this list looks like a diet effect, and what that means for them.
**Likely diet effects**
The most important genes that follow the food, grouped by what they do (for example making cholesterol). Say "None" if there are none.
**Worth a closer look**
Unresolved or shape-candidate genes, strongest first, and why they are more promising. Say "None" if there are none.
**For researchers**
2 or 3 terse bullets: key numbers and the single best control experiment (for example cholesterol or lipid add-back, or flat cells in organoid medium).
If many genes were not found or show no real difference, say so in one sentence: the table uses official symbols from DepMap 26Q3, and "no real difference" means the public screens show no organoid-versus-flat change for that gene.`,
    input: `The researcher's list (${syms.length} genes): ${syms.join(", ")}`,
    max: 640, tools: true, seed: { name: "check_hit_list", args: { symbols: syms } },
  };
}

/* em/en dashes are scrubbed even if the model slips; trailing whitespace is held so joins stay clean */
function makeScrubber() {
  let carry = "";
  return {
    push(t) {
      let s = carry + t;
      const m = s.match(/[\s—–]+$/);
      carry = m ? m[0] : "";
      s = m ? s.slice(0, -m[0].length) : s;
      return scrub(s);
    },
    end() { const s = scrub(carry); carry = ""; return s; },
  };
}
function scrub(s) {
  return s.replace(/\s*—\s*/g, ", ").replace(/(\d)\s*–\s*(\d)/g, "$1 to $2").replace(/\s*–\s*/g, ", ");
}

/* one Responses API call, streamed. Visible text is forwarded as it arrives; "commentary" messages
   (the model narrating before a tool call) are held back. Returns the completed output items. */
async function streamRound(body, write, signal) {
  const key = await getKey();
  const res = await fetch(`${BASE}/responses`, {
    method: "POST", signal,
    headers: { authorization: `Bearer ${key}`, "content-type": "application/json", accept: "text/event-stream", "x-client-id": "itsthemedium:web" },
    body: JSON.stringify(body),
  });
  if (!res.ok || !res.body) {
    const t = await res.text().catch(() => "");
    throw new Error(`upstream ${res.status} ${t.slice(0, 200)}`);
  }
  const dec = new TextDecoder(), sc = makeScrubber(), items = [], hidden = new Set();
  let buf = "", wrote = 0, final = null;
  for await (const chunk of res.body) {
    buf += dec.decode(chunk, { stream: true });
    let i;
    while ((i = buf.indexOf("\n\n")) >= 0) {
      const block = buf.slice(0, i); buf = buf.slice(i + 2);
      const data = block.split("\n").filter(l => l.startsWith("data:")).map(l => l.slice(5).trim()).join("");
      if (!data || data === "[DONE]") continue;
      let ev; try { ev = JSON.parse(data); } catch { continue; }
      if (ev.type === "response.output_item.added" && ev.item?.type === "message" && ev.item.phase === "commentary") hidden.add(ev.output_index);
      else if (ev.type === "response.output_text.delta" && ev.delta && !hidden.has(ev.output_index)) {
        const s = sc.push(ev.delta); if (s) { write(s); wrote += s.length; }
      } else if (ev.type === "response.output_item.done" && ev.item) items[ev.output_index] = ev.item;
      else if (ev.type === "response.completed") final = ev.response;
      else if (ev.type === "response.failed" || ev.type === "error") throw new Error("upstream failed: " + JSON.stringify(ev).slice(0, 200));
    }
  }
  const tail = sc.end(); if (tail) { write(tail); wrote += tail.length; }
  return { output: (final?.output?.length ? final.output : items.filter(Boolean)), wrote };
}

/* plain prompt (gene briefs) or a tool-using agent loop (questions, hit lists) */
async function runMuse(p, write, signal) {
  const base = { model: MODEL, instructions: p.instructions, stream: true, store: false, max_output_tokens: p.max + 1600, reasoning: { effort: EFFORT } };
  if (!p.tools) {
    const r = await streamRound({ ...base, input: p.input }, write, signal);
    if (!r.wrote) throw new Error("empty response");
    return;
  }
  let first = p.input, wrote = 0;
  if (p.seed) {
    /* the API only supports tool_choice "auto", so a required first step is run here and handed to the model */
    const t = runTool(p.seed.name, p.seed.args);
    write(`[[step:${t.step}]]\n`);
    first += `\n\n${p.seed.name} result:\n${JSON.stringify(t.data)}`;
  }
  let input = [{ role: "user", content: first }];
  const MAX_ROUNDS = 6;
  for (let round = 0; round < MAX_ROUNDS; round++) {
    if (round === MAX_ROUNDS - 2) input.push({ role: "user", content: "You have enough data. Write the final answer now without calling more tools." });
    const r = await streamRound({ ...base, input, tools: TOOLS, parallel_tool_calls: true }, write, signal);
    wrote += r.wrote;
    const calls = r.output.filter(o => o.type === "function_call");
    if (!calls.length) break;
    const results = calls.map(c => {
      let args = {}; try { args = JSON.parse(c.arguments || "{}"); } catch {}
      const t = runTool(c.name, args);
      if (t.step) { write(`[[step:${t.step.replace(/[\[\]\n]/g, " ")}]]\n`); }
      return { type: "function_call_output", call_id: c.call_id, output: JSON.stringify(t.data) };
    });
    input = [...input, ...r.output.filter(o => o.type !== "message"), ...results];
  }
  if (!wrote) throw new Error("empty response");
}

function open(responseStream, status, cache, extra = {}) {
  return awslambda.HttpResponseStream.from(responseStream, {
    statusCode: status,
    headers: {
      ...extra,
      "content-type": "text/plain; charset=utf-8",
      "cache-control": cache ? "public, max-age=604800, s-maxage=604800" : "no-store",
      "x-content-type-options": "nosniff",
    },
  });
}

export const handler = awslambda.streamifyResponse(async (event, responseStream) => {
  const path = (event.rawPath || "").replace(/\/+$/, "");
  const qs = event.queryStringParameters || {};
  const ip = (event.headers?.["cloudfront-viewer-address"] || event.requestContext?.http?.sourceIp || "").split(":")[0];
  const bad = msg => { const s = open(responseStream, 400, false); s.write(msg); return s.end(); };
  let p = null, kind = null;
  if (path.endsWith("/health")) {
    let ok = false; try { ok = !!(await getKey()); } catch { ok = false; }
    const s = open(responseStream, 200, false); s.write(ok ? "ok" : "off"); return s.end();
  }
  if (path.endsWith("/brief")) {
    const g = BYG.get(String(qs.gene || "").trim().toUpperCase());
    if (!g) return bad("Unknown gene.");
    p = briefPrompt(g); kind = "brief";
  } else if (path.endsWith("/ask")) {
    const q = String(qs.q || "").replace(/\s+/g, " ").trim().slice(0, 300);
    if (q.length < 3) return bad("Please ask a question.");
    p = askPrompt(q); kind = "ask";
  } else if (path.endsWith("/list")) {
    const syms = cleanSymbols(String(qs.genes || "").split(","), 300).sort();
    if (!syms.length) return bad("Please send a list of gene symbols.");
    if (!syms.some(s => BYG.has(s))) return bad("None of these symbols are in the table.");
    p = listPrompt(syms); kind = "list";
  } else return bad("Unknown route.");
  if (limited(ip, kind)) { const s = open(responseStream, 429, false, { "retry-after": "120" }); s.write("Too many requests. Please wait a couple of minutes."); return s.end(); }

  /* headers are sent with the first write, so a failure before any output is a 502 that CloudFront will not cache */
  let out = null;
  const write = s => (out ||= open(responseStream, 200, true)).write(s);
  const ctl = new AbortController(); const timer = setTimeout(() => ctl.abort(), 57000);
  try {
    await runMuse(p, write, ctl.signal);
  } catch (e) {
    console.error("muse error", kind, e?.message);
    if (!out) { out = open(responseStream, 502, false); out.write("The AI service is busy. Please try again."); }
    else out.write("\n\n[[error]]");
  } finally {
    clearTimeout(timer);
    (out || open(responseStream, 502, false)).end();
  }
});
