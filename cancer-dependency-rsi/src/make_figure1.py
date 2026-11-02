"""Figure 1 (SVG, dependency-free): per-gene coordinates + locked primary/Holm intervals.
Generated only from retained frozen outputs (external_v1_gene_displacement.csv, external_v1.json)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ext = pd.read_csv(ROOT / 'lock_s/results/external_v1_gene_displacement.csv')
    res = json.loads((ROOT / 'lock_s/results/external_v1.json').read_text())
    W, H = 980, 440
    # left scatter panel
    x0, y0, pw, ph = 70, 50, 400, 300
    lx, hx = float(ext['L_g'].min()), float(ext['L_g'].max())
    ly, hy = float(ext['D_g'].min()), float(ext['D_g'].max())
    def X(v): return x0 + (v - lx) / (hx - lx) * pw
    def Y(v): return y0 + ph - (v - ly) / (hy - ly) * ph
    pts = ''.join(f'<circle cx="{X(r.L_g):.1f}" cy="{Y(r.D_g):.1f}" r="2.2" fill="#333" opacity="0.65"/>'
                  for r in ext.itertuples())
    # right forest panel
    fx0 = 560
    rows = [('Primary', res['primary']['estimate'], res['primary']['ci95_donor_percentile'])]
    rows += [(k, v['estimate'], v['ci95_donor_percentile']) for k, v in res['secondary_holm_family'].items()]
    lo, hi = -0.30, 0.05
    def FX(v): return fx0 + (v - lo) / (hi - lo) * 360
    forest = ''
    for i, (name, est, ci) in enumerate(rows):
        yy = 90 + i * 55
        forest += (f'<text x="{fx0}" y="{yy - 8}" font-size="11" fill="#222">{name}</text>'
                   f'<line x1="{FX(ci[0]):.1f}" y1="{yy + 6}" x2="{FX(ci[1]):.1f}" y2="{yy + 6}" stroke="#333" stroke-width="2"/>'
                   f'<circle cx="{FX(est):.1f}" cy="{yy + 6}" r="4" fill="#111"/>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif">
<rect width="{W}" height="{H}" fill="white"/>
<text x="{x0}" y="30" font-size="13" font-weight="bold" fill="#111">Per-gene coordinates (207 genes, descriptive)</text>
<line x1="{x0}" y1="{y0 + ph}" x2="{x0 + pw}" y2="{y0 + ph}" stroke="#888"/>
<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 + ph}" stroke="#888"/>
<text x="{x0}" y="{y0 + ph + 22}" font-size="11" fill="#222">Measured format lability L_g ({lx:.2f} to {hx:.2f})</text>
<text x="{x0}" y="{y0 - 6}" font-size="11" fill="#222">Displacement D_g ({ly:.2f} to {hy:.2f})</text>
{pts}
<text x="{fx0}" y="30" font-size="13" font-weight="bold" fill="#111">Locked primary + Holm secondaries</text>
<line x1="{FX(0):.1f}" y1="60" x2="{FX(0):.1f}" y2="370" stroke="#999"/>
<line x1="{FX(-0.20):.1f}" y1="60" x2="{FX(-0.20):.1f}" y2="370" stroke="#b00020" stroke-dasharray="5 4"/>
<text x="{FX(-0.20) - 12:.1f}" y="388" font-size="11" fill="#b00020">-0.20 (delta)</text>
<text x="{FX(0) - 3:.1f}" y="388" font-size="11" fill="#666">0</text>
{forest}
<text x="70" y="408" font-size="10" fill="#444"><tspan x="70" dy="0">Intervals: archived 95% donor-percentile intervals over 144 covariate-ID groups (=142 patients, sgen001);</tspan><tspan x="70" dy="13">patient-weighted effects unquantified. Holm adjusts secondary tests; plotted intervals are ordinary 95% percentile intervals.</tspan></text>
</svg>'''
    out = ROOT / 'manuscript/figures/figure1_primary.svg'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(f'wrote {out} ({len(svg)} bytes, {len(ext)} points, {len(rows)} intervals)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
