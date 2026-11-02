#!/usr/bin/env python3
"""Render manuscript_draft_v2.md to a submission-ready PDF (fpdf2).
Author block left as placeholders for the submitting author.
"""
import re
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "manuscript/manuscript_draft_v2.md"
OUT_DIR = ROOT / "release_v1"
FIGS = [("Figure 1. Attribution of organoid-vs-2D differential dependencies. Left: adherent organoid-formulation-family effect (A) vs dome effect (D). Right: dome vs adherent within the organoid-medium family (F) vs D. Dashed: identity.",
         ROOT / "manuscript/figures/fig1_attribution.png"),
        ("Figure 2. Core-essential weakening with curated BAGEL reference sets. Left: Broad median delta-Chronos by contrast. Right: Sanger essential depth and depth-scaled panel ratios.",
         ROOT / "manuscript/figures/fig2_weakening.png"),
        ("Figure 3. Flag composition of published organoid-specific hit lists (Broad figshare table; Herranz-Ors supplementary table 4).",
         ROOT / "manuscript/figures/fig3_catalogues.png")]


def clean(s):
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"\*([^*]+)\*", r"\1", s)
    s = s.replace("`", "")
    for a, b in (("—", "-"), ("–", "-"), ("≈", "~"), ("≥", ">="), ("≤", "<="), ("×", "x"),
                 ("Δ", "Delta-"), ("⁻", "-"), ("−", "-"), ("‘", "'"), ("’", "'"), ("“", '"'), ("”", '"')):
        s = s.replace(a, b)
    return s.encode("latin-1", "replace").decode("latin-1")


def main():
    md = SRC.read_text()
    md = md.split("## Figures")[0]
    pdf = FPDF(unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_margins(22, 20, 22)

    def para(text, size=10.5, style="", gap=2.2, align="J"):
        pdf.set_font("helvetica", style, size)
        pdf.multi_cell(0, 5.2, clean(text), align=align)
        pdf.ln(gap)

    lines = md.splitlines()
    title = lines[0].lstrip("# ").strip()
    pdf.set_font("helvetica", "B", 17)
    pdf.multi_cell(0, 8, clean(title), align="C")
    pdf.ln(6)
    para("[AUTHORS - to be completed by submitting author]", 11, "", 1, "C")
    para("[Affiliations]", 10, "I", 1, "C")
    para("Corresponding author: [name, email]", 10, "", 6, "C")

    buf = []
    def flush():
        if buf:
            para(" ".join(buf))
            buf.clear()
    for ln in lines[1:]:
        s = ln.strip()
        if s.startswith("*Technical note"):
            continue
        if s.startswith("## "):
            flush(); para(s[3:], 13, "B", 2.5, "L")
        elif s.startswith("### "):
            flush(); para(s[4:], 11.5, "B", 2, "L")
        elif s.startswith("- "):
            flush(); para("  -  " + s[2:], 10.5, "", 1.2, "L")
        elif re.match(r"^\d+\. ", s):
            flush(); para("  " + s, 10.5, "", 1.2, "L")
        elif s == "":
            flush()
        else:
            buf.append(s)
    flush()

    pdf.add_page()
    para("Figures", 13, "B", 3, "L")
    for cap, path in FIGS:
        if pdf.get_y() > 175:
            pdf.add_page()
        pdf.image(str(path), x=22, w=166)
        pdf.ln(2)
        para(cap, 9, "I", 6, "L")
    para("Supplementary data: per-gene attribution tables (raw and normalized), held-out contrasts, "
         "survivor candidates, and analysis code accompany this preprint (release bundle v1). "
         "Inputs: DepMap 26Q3 (portal), Broad NextGen figshare (doi:10.6084/m9.figshare.29472362), "
         "Sanger figshare supplementary tables, Rossiter et al. 2021 Table S1 (PMC8172426).", 9.5)

    out = OUT_DIR / "manuscript_v2.pdf"
    pdf.output(str(out))
    print("wrote", out, out.stat().st_size, "pages:", pdf.pages_count)


if __name__ == "__main__":
    main()
