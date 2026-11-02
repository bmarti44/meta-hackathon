#!/usr/bin/env python3
"""Validate release_v1.zip ARCHIVED contents against recomputed expectations
(Astra r2 M2). Numeric checks read tables from inside the zip, compare hit
gene sets per scale against generations/, and verify bootstrap/manuscript
numbers. Writes release_v1/VALIDATION.json with SHA-256 of every archive
entry except VALIDATION.json itself (append it afterwards:
`zip release_v1.zip release_v1/VALIDATION.json` from repo root... paths:
run `cd release_v1 && zip ../release_v1.zip VALIDATION.json` is NOT used;
the bundle zip stores paths as release_v1/<file>, so append with
`zip release_v1.zip release_v1/VALIDATION.json` from cancer-dependency-rsi/).
"""
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
chk = []


def ok(name, cond, detail=""):
    chk.append({"check": name, "pass": bool(cond), "detail": detail})


def main():
    z = zipfile.ZipFile(ROOT / "release_v1.zip")
    ok("zip integrity", z.testzip() is None)
    names = {n.rsplit("/", 1)[-1]: n for n in z.namelist() if not n.endswith("/")}

    def zcsv(f):
        return pd.read_csv(io.BytesIO(z.read(names[f])), index_col=0)

    def zjson(f):
        return json.loads(z.read(names[f]))

    man = z.read(names["manuscript_draft_v2.md"]).decode()
    tabs = {}
    for scale in ("norm", "raw"):
        t = zcsv(f"medium_attribution_v2_{scale}.csv")
        tabs[scale] = t
        hit_rt = t[(t.D_org_q < 0.01) & (t.D_org.abs() >= 0.25)]
        ok(f"{scale}: archived hit rule round-trips by gene",
           set(hit_rt.index) == set(t[t.flag != "not_a_hit"].index),
           f"{len(hit_rt)} vs {int((t.flag != 'not_a_hit').sum())}")
        gen = pd.read_csv(ROOT / f"generations/medium_attribution_v2_{scale}.csv", index_col=0)
        ok(f"{scale}: archive == generations flags",
           bool((t.flag.values == gen.flag.values).all() and (t.index == gen.index).all()))
    t = tabs["norm"]
    g = t[(t.flag != "not_a_hit") & (t.D_org < 0)]
    l = t[(t.flag != "not_a_hit") & (t.D_org > 0)]
    ok("norm 249 gains / 207 losses (archived)", (len(g), len(l)) == (249, 207), f"{len(g)}/{len(l)}")
    ok("norm 86%/84% medium (archived)", abs((g.flag == "medium_attributable").mean() - 0.859) < 0.01
       and abs((l.flag == "medium_attributable").mean() - 0.836) < 0.01)
    ok("1 format candidate LSM7; 0 under flag_fdr (archived)",
       t[t.flag == "format_candidate"].index.tolist() == ["LSM7"]
       and int((t.flag_fdr == "format_candidate").sum()) == 0)
    rep = zjson("medium_attribution_v2.json")
    ok("archived JSON hit counts match archived CSV",
       rep["norm"]["gains"]["n_hits"] == len(g) and rep["norm"]["losses"]["n_hits"] == len(l))
    ok("archived JSON revision v2r2", "v2r2" in str(rep.get("revision", "")))
    ok("library calibration models = 22 (dev-only)", rep["library_offset_models"] == 22)
    b = zjson("medium_attribution_v2_boot.json")
    hits = t[t.flag != "not_a_hit"]
    slope_pt = float(np.polyfit(hits.D_org, hits.A_adh, 1)[0])
    ok("bootstrap identity check passed", b["identity_check"]["matches"] is True)
    ok("bootstrap CI contains archived point slope",
       b["slope_A_on_D"]["ci95"][0] <= slope_pt <= b["slope_A_on_D"]["ci95"][1],
       f"point {slope_pt:.3f} CI {b['slope_A_on_D']['ci95']}")
    bf = zcsv("medium_attribution_v2_boot_freq.csv")
    ok("boot freq rows == hits, values in [0,1]",
       len(bf) == len(hits) and bool(bf.iloc[:, 0].between(0, 1).all()))
    s = zjson("sanger_tables_audit_v1.json")
    ok("sanger freq medians 0.802/0.698 (tight)",
       abs(s["exclusive97"]["freq_median"] - 0.8025) < 0.002
       and abs(s["headline18"]["freq_median"] - 0.6975) < 0.002)
    h = zjson("hplm_reverse_test_v1.json")
    ok("HPLM corr ~0.04, SQLE +0.44 (archived)", abs(h["corr_delta_Dorg"] - 0.044) < 0.01
       and abs(h["named"]["SQLE"]["delta"] - 0.442) < 0.01)
    held = zjson("medium_attribution_v2_heldout.json")
    ok("held-out disjoint baseline n0=78", held["norm"]["n"]["D_heldout"][1] == 78)
    cited = sorted(set(re.findall(r"`((?:generations|src|manuscript|figures|data)/[^`]+)`", man)))
    missing = [c for c in cited if not (ROOT / c).exists() and c.rsplit("/", 1)[-1] not in names
               and "{" not in c and "*" not in c]
    ok("manuscript cited paths exist", not missing, f"cited={len(cited)} missing={missing[:5]}")
    for f in ("fig1_attribution.png", "fig2_weakening.png", "fig3_catalogues.png", "manuscript_v2.pdf",
              "supplementary_tables.zip", "biorxiv_fields.txt", "SUBMISSION_CHECKLIST.md",
              "wetlab_cover_email.txt", "medium_attribution_v2_boot.py", "sanger_essdepth.py"):
        ok(f"bundle has {f}", f in names)
    for pat in (r"\+0\.90 and \+0\.64", r"1\.53 vs 1\.45", r"449 differential", r"981 essentials"):
        ok(f"no stale '{pat}' in manuscript", not re.search(pat, man))
    abs_text = man.split("## Abstract")[1].split("## Introduction")[0]
    ok("abstract <= 300 words", len(abs_text.split()) <= 300, f"{len(abs_text.split())} words")

    hashes = {}
    for n in sorted(z.namelist()):
        if n.endswith("/") or n.endswith("VALIDATION.json"):
            continue
        hashes[n] = hashlib.sha256(z.read(n)).hexdigest()
    out = {"n_checks": len(chk), "n_pass": sum(c["pass"] for c in chk), "checks": chk,
           "sha256_excluding_this_file": hashes,
           "note": "Append this file to the zip after validation; it is excluded from its own inventory."}
    (ROOT / "release_v1/VALIDATION.json").write_text(json.dumps(out, indent=1))
    print(f"{out['n_pass']}/{out['n_checks']} checks pass")
    for c in chk:
        if not c["pass"]:
            print("FAIL:", c)


if __name__ == "__main__":
    main()
