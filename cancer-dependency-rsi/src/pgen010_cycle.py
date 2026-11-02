#!/usr/bin/env python3
"""pgen010 engineering pilot cycle executor (generations/pgen010/SPEC.md).

Deterministic Fraction arithmetic; Decimal delta classification. DEV=LOMO
selection; EVAL = 2 models x format; arms I/L/F/R(s=0..19); sealed
predictions; exact-node accounting 2,500+7,800+4,600=14,900.
"""
import csv
import hashlib
import json
import random
import sys
import datetime
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLASSES = (-2, -1, 0, 1, 2)
CIDX = {c: i for i, c in enumerate(CLASSES)}
DEV_MODELS = ["ACH-000108", "ACH-000178", "ACH-003040"]
EVAL_MODELS = ["ACH-001418", "ACH-002958"]
B = 20
failures = []
NODE_LOG = []  # every charged node: (kind, key)


def classify(delta_str):
    d = Decimal(delta_str)
    if d <= Decimal("-0.10"):
        return -2
    if d >= Decimal("0.10"):
        return 2
    if d == 0:
        return 0
    return -1 if d < 0 else 1


def load():
    nodes = {}
    with open(ROOT / "atlas/v4/paired_observations.csv", newline="") as f:
        for row in csv.DictReader(f):
            key = (row["gene"], row["axis"], row["model_id"], row["held_condition"])
            if key in nodes:
                failures.append("DATA_INTEGRITY")
                continue
            nodes[key] = classify(row["delta_a_minus_b"])
    return nodes


class Priors:
    def __init__(self, data):  # data: dict key->class (subset D)
        self.groups = {}
        def add(gk, c):
            self.groups.setdefault(gk, [0] * 5)[CIDX[c]] += 1
        for (g, ax, m, h), c in data.items():
            add(("all",), c); add(("axis", ax), c); add(("ga", g, ax), c)
            add(("ah", ax, h), c); add(("gah", g, ax, h), c)

    def pi(self, key):
        g, ax, m, h = key
        vecs = []
        for gk in (("all",), ("axis", ax), ("ga", g, ax), ("ah", ax, h), ("gah", g, ax, h)):
            n = self.groups.get(gk, [0] * 5)
            tot = sum(n)
            vecs.append([Fraction(n[i] + 1, tot + 5) for i in range(5)])
        return [sum(v[i] for v in vecs) / 5 for i in range(5)]


def w_of(x, r, wg, wh):
    return Fraction(1 + (wg if x[0] == r[0] else 0) + (wh if x[3] == r[3] else 0))


def predict(x, R, priors, theta, labels):
    kappa, wg, wh = theta
    pi = priors.pi(x)
    num = [Fraction(kappa) * pi[i] for i in range(5)]
    d = Fraction(kappa)
    for r in R:
        w = w_of(x, r, wg, wh)
        d += w
        num[CIDX[labels[r]]] += w
    return [v / d for v in num]


def loss(p, y):
    return sum((p[i] - (1 if CLASSES[i] == y else 0)) ** 2 for i in range(5)) / 2


def episodes(nodes, model, axis):
    stratum = sorted(k for k in nodes if k[2] == model and k[1] == axis)
    genes = sorted({k[0] for k in stratum})
    out = []
    for f in range(5):
        tg = {genes[i] for i in range(len(genes)) if i % 5 == f}
        T = [k for k in stratum if k[0] in tg]
        Q = [k for k in stratum if k[0] not in tg]
        out.append((sorted(T), sorted(Q)))
    return out


def run_episode(T, Q, priors, theta, labels, mode, kind, rng_seq=None):
    """Returns (predictions dict target->p, transcript list). Charges nodes."""
    if not T or len(Q) < B:
        failures.append("EPISODE_INFEASIBLE")
        return {}, []
    R = []
    transcript = []
    kappa, wg, wh = theta
    if mode == "ascending":
        order = list(Q[:B])
    elif mode == "descending":
        order = list(sorted(Q, reverse=True)[:B])
    elif mode == "random":
        order = list(rng_seq[:B])
    elif mode.startswith("fixed:"):
        recipe = mode.split(":")[1]
        def U0(q):
            p = predict(q, [], priors, theta, labels)
            return 1 - sum(v * v for v in p)
        def W(q):
            return sum(w_of(t, q, wg, wh) for t in T)
        if recipe == "K2":
            order = sorted(Q, key=lambda q: (-U0(q), q))[:B]
        elif recipe == "K3":
            order = sorted(Q, key=lambda q: (U0(q), q))[:B]
        elif recipe == "K4":
            order = sorted(Q, key=lambda q: (-W(q), q))[:B]
        else:  # K5
            order = sorted(Q, key=lambda q: (-(U0(q) * W(q)), q))[:B]
        order = list(order)
    else:  # adaptive: U, W, V, UW, UV
        avail = list(Q)
        order = None
        seq = []
        for _ in range(B):
            def score(q):
                p = predict(q, R, priors, theta, labels)
                U = 1 - sum(v * v for v in p)
                if mode == "U":
                    return U
                Wq = sum(w_of(t, q, wg, wh) for t in T)
                if mode == "W":
                    return Wq
                if mode == "UW":
                    return U * Wq
                Vq = Fraction(0)
                for t in T:
                    d = Fraction(kappa) + sum(w_of(t, r, wg, wh) for r in R)
                    Vq += w_of(t, q, wg, wh) / d
                return Vq if mode == "V" else U * Vq
            best = max(avail, key=lambda q: (score(q), tuple(-ord(c) for s in q for c in s)))
            # tie-break: max score, ascending key -> implement explicitly
            bs = score(best)
            cands = [q for q in avail if score(q) == bs]
            best = min(cands)
            seq.append(best)
            avail.remove(best)
            R.append(best)
            transcript.append(best)
            NODE_LOG.append((kind, best))
        preds = {t: predict(t, R, priors, theta, labels) for t in T}
        return preds, transcript
    for q in order:
        R.append(q)
        transcript.append(q)
        NODE_LOG.append((kind, q))
    preds = {t: predict(t, R, priors, theta, labels) for t in T}
    return preds, transcript


def stratum_losses(nodes, model, axis, priors, theta, labels, mode, kind):
    tot, n = Fraction(0), 0
    for T, Q in episodes(nodes, model, axis):
        preds, _ = run_episode(T, Q, priors, theta, labels, mode, kind)
        for t, p in preds.items():
            tot += loss(p, labels[t]); n += 1
    return tot / n


def main():
    nodes = load()
    labels = nodes
    report = {"frozen_hashes": {}, "nodes_total": len(nodes)}
    for p in ("atlas/v4/paired_observations.csv", "generations/pgen010/SPEC.md",
              "generations/pgen006/readiness_v8.json"):
        report["frozen_hashes"][p] = hashlib.sha256((ROOT / p).read_bytes()).hexdigest()
    dev_data = {k: v for k, v in nodes.items() if k[2] in DEV_MODELS}
    assert len(dev_data) == 2000, len(dev_data)
    for k in dev_data:
        NODE_LOG.append(("dev_source_release", k))
    eval_fmt = {k: v for k, v in nodes.items() if k[2] in EVAL_MODELS and k[1] == "format"}
    assert len(eval_fmt) == 500, len(eval_fmt)
    for k in eval_fmt:
        NODE_LOG.append(("eval_scorer_release", k))

    # ---- DEV LOMO: shared ascending transcripts -> predictor selection
    CANDS = [(4, 3, 3), (4, 0, 0), (4, 3, 0), (4, 0, 3), (16, 3, 3)]
    def J_of(theta_mode_pairs):
        # theta_mode_pairs: callable per-model returning (theta, mode)
        per_model = []
        for m in DEV_MODELS:
            D = {k: v for k, v in dev_data.items() if k[2] != m}
            pr = Priors(D)
            ls = []
            for ax in ("format", "medium"):
                theta, mode = theta_mode_pairs[m]
                ls.append(stratum_losses(nodes, m, ax, pr, theta, labels, mode,
                                         "dev_replay"))
            per_model.append(sum(ls) / 2)
        return sum(per_model) / 3
    # shared transcripts: run ascending once per episode with candidate 1 to
    # charge 600; predictions for all candidates from same R sequences.
    cand_scores = {str(t): [] for t in CANDS}
    for m in DEV_MODELS:
        D = {k: v for k, v in dev_data.items() if k[2] != m}
        pr = Priors(D)
        for ax in ("format", "medium"):
            for T, Q in episodes(nodes, m, ax):
                R = []
                for q in Q[:B]:
                    R.append(q); NODE_LOG.append(("dev_shared_transcript", q))
                for t in CANDS:
                    s = sum(loss(predict(x, R, pr, t, labels), labels[x]) for x in T)
                    cand_scores[str(t)].append((m, ax, s, len(T)))
    def J_from(rows):
        pm = []
        for m in DEV_MODELS:
            pl = []
            for ax in ("format", "medium"):
                s = sum(r[2] for r in rows if r[0] == m and r[1] == ax)
                n = sum(r[3] for r in rows if r[0] == m and r[1] == ax)
                pl.append(s / n)
            pm.append(sum(pl) / 2)
        return sum(pm) / 3
    Jc = {str(t): J_from(cand_scores[str(t)]) for t in CANDS}
    theta_hat = min(CANDS, key=lambda t: (Jc[str(t)], CANDS.index(t)))
    report["theta_hat"] = list(theta_hat)
    report["predictor_J"] = {k: float(v) for k, v in Jc.items()}

    # ---- DEV policy candidates (6) and fixed recipes (6)
    POL = [("I", (4, 3, 3), "U"), ("L_U", theta_hat, "U"), ("L_W", theta_hat, "W"),
           ("L_V", theta_hat, "V"), ("L_UW", theta_hat, "UW"), ("L_UV", theta_hat, "UV")]
    Jp = {}
    for name, theta, mode in POL:
        Jp[name] = J_of(dict.fromkeys(DEV_MODELS, (theta, mode)))
    sel_name = min(POL, key=lambda x: (Jp[x[0]], POL.index(x)))[0]
    report["policy_J"] = {k: float(v) for k, v in Jp.items()}
    report["selected_policy"] = sel_name
    if sel_name == "I":
        failures.append("NO_UPDATE")
    sel = dict((n, (t, mo)) for n, t, mo in POL)[sel_name]
    FIX = [("K0", "ascending"), ("K1", "descending")] + [(f"K{i}", f"fixed:K{i}") for i in range(2, 6)]
    Jf = {}
    for name, mode in FIX:
        Jf[name] = J_of(dict.fromkeys(DEV_MODELS, (theta_hat, mode)))
    fix_name = min(FIX, key=lambda x: (Jf[x[0]], FIX.index(x)))[0]
    report["fixed_J"] = {k: float(v) for k, v in Jf.items()}
    report["selected_fixed"] = fix_name
    fix_mode = dict(FIX)[fix_name]

    # ---- freeze all-DEV priors
    priors_all = Priors(dev_data)
    report["prior_summary_hash"] = hashlib.sha256(
        json.dumps(sorted((str(k), v) for k, v in priors_all.groups.items())).encode()).hexdigest()

    # ---- EVAL arms (sealed predictions)
    arms = [("I", (4, 3, 3), "U", None), ("L", sel[0], sel[1], None),
            ("F", theta_hat, fix_mode, None)] + \
           [(f"R{s}", theta_hat, "random", s) for s in range(20)]
    sealed = {}
    transcripts = {}
    for name, theta, mode, seed in arms:
        preds_all = {}
        trs = {}
        for m in sorted(EVAL_MODELS):
            for fi, (T, Q) in enumerate(episodes(nodes, m, "format")):
                rng_seq = None
                if mode == "random":
                    ser = json.dumps(["pgen010", seed, m, "format", fi],
                                     ensure_ascii=True, separators=(",", ":"))
                    dg = hashlib.sha256(ser.encode("ascii")).digest()
                    rng = random.Random(int.from_bytes(dg, "big"))
                    rng_seq = list(Q)
                    rng.shuffle(rng_seq)
                preds, tr = run_episode(T, Q, priors_all, theta, labels, mode,
                                        "eval_replay", rng_seq)
                preds_all.update(preds)
                trs[f"{m}|{fi}"] = ["|".join(q) for q in tr]
        sealed[name] = {"|".join(k): [str(v) for v in p] for k, p in preds_all.items()}
        transcripts[name] = trs
    seal_path = ROOT / "generations/pgen010/sealed_predictions.json"
    seal_path.write_text(json.dumps({"predictions": sealed, "transcripts": transcripts}))
    report["sealed_sha256"] = hashlib.sha256(seal_path.read_bytes()).hexdigest()

    # ---- determinism: recompute I arm from scratch, exact equality
    chk = {}
    saved = len(NODE_LOG)
    for m in sorted(EVAL_MODELS):
        for T, Q in episodes(nodes, m, "format"):
            preds, _ = run_episode(T, Q, priors_all, (4, 3, 3), labels, "U", "recheck")
            chk.update({"|".join(k): [str(v) for v in p] for k, p in preds.items()})
    NODE_LOG[saved:] = []  # recompute makes no oracle requests
    if chk != sealed["I"]:
        failures.append("NONDETERMINISM")

    # ---- scoring
    def model_losses(name):
        out = {}
        for m in EVAL_MODELS:
            ts = [k for k in eval_fmt if k[2] == m]
            tot = Fraction(0)
            for t in ts:
                p = [Fraction(v) for v in sealed[name]["|".join(t)]]
                tot += loss(p, labels[t])
            out[m] = tot / len(ts)
        return out
    L = {name: model_losses(name) for name, *_ in arms}
    Rmean = {m: sum(L[f"R{s}"][m] for s in range(20)) / 20 for m in EVAL_MODELS}
    def macro(d):
        return sum(d.values()) / 2
    gains = {}
    for comp, d in (("I", L["I"]), ("F", L["F"]), ("R", Rmean)):
        g = {m: d[m] - L["L"][m] for m in EVAL_MODELS}
        gains[comp] = {"per_model": {m: float(v) for m, v in g.items()}, "macro": float(macro(g))}
    q = min(macro({m: d[m] - L["L"][m] for m in EVAL_MODELS})
            for d in (L["I"], L["F"], Rmean))
    perf_pass = q >= Fraction(2, 100) and all(
        v >= 0 for comp in gains for v in
        ({m: (L[comp] if comp != "R" else Rmean)[m] - L["L"][m] for m in EVAL_MODELS}).values())
    if not perf_pass:
        failures.append("NO_GAIN" if q <= 0 else "BELOW_QSTAR")

    # ---- accounting
    kinds = {}
    for k, _ in NODE_LOG:
        kinds[k] = kinds.get(k, 0) + 1
    report["node_charges"] = kinds
    report["node_total"] = len(NODE_LOG)
    expected = {"dev_source_release": 2000, "eval_scorer_release": 500,
                "dev_shared_transcript": 600, "dev_replay": 7200, "eval_replay": 4600}
    if kinds != expected:
        failures.append("NODE_MISMATCH")
    # host-call pricing (shared_equally): generation + 4 pre-run reviews
    SHORT = {"in": 2.00, "cached": 0.10, "out": 10.00}
    LONG = {"in": 4.00, "cached": 0.20, "out": 15.00}
    def price_entry(t):
        inp = t.get("input_tokens", 0); cached = t.get("cached_input_tokens", 0)
        write = t.get("cache_write_input_tokens", 0); out = t.get("output_tokens", 0)
        r = LONG if inp > 272_000 else SHORT
        return ((inp - cached) * r["in"] + cached * r["cached"] + out * r["out"] + write * 2.50) / 1e6
    host = {}
    for rn in ("xhigh_pgen007_cycle_generate", "pgen007_prerun_review",
               "pgen008_prerun_review", "pgen009_prerun_review", "pgen010_prerun_review"):
        r = json.load(open(ROOT / f"reviews/{rn}.receipt.json"))
        toks = r.get("tokens") or []
        host[rn] = {"usd": sum(price_entry(u) for u in toks) if toks else None,
                    "attribution": "shared_equally"}
        if host[rn]["usd"] is None:
            failures.append("COST_UNRESOLVED")
    report["host_calls"] = host
    report["host_total_usd"] = sum(v["usd"] for v in host.values() if v["usd"])
    report["metered_spend_usd"] = 0.0
    report["q"] = float(q)
    report["gains"] = gains
    report["L"] = {n: {m: float(v) for m, v in d.items()} for n, d in
                   list(L.items())[:3]}
    report["R_macro_seeds"] = [float(macro(L[f"R{s}"])) for s in range(20)]
    report["failures"] = sorted(set(failures))
    report["verdict"] = "PASS" if not failures else "FAIL"
    report["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    out = ROOT / "generations/pgen010/cycle_result.json"
    out.write_text(json.dumps(report, indent=1))
    print(json.dumps({"verdict": report["verdict"], "q": report["q"],
                      "failures": report["failures"],
                      "selected": sel_name, "fixed": fix_name,
                      "theta_hat": report["theta_hat"],
                      "nodes": kinds, "host_usd": round(report["host_total_usd"], 2)}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
