"""Bounded METADATA-ONLY 26Q3 route probe (SPEC reviews/prompts/g2_task_route_probe_v1.json).

Run only via run_g2_task_route_probe.py (run_bounded reservation). Enforces in-process:
<=6 requests (redirects counted, never auto-followed), 30 s/request, 32 MiB total,
280 s internal deadline (300 s outer), filename allow/deny lists, HTML-guard, no
dependency-matrix access, no C outcome access. Writes reviews/g2_task_route_probe_v1.json.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'reviews/prompts/g2_task_route_probe_v1.json'
OUT = ROOT / 'reviews/g2_task_route_probe_v1.json'
RAW = ROOT / 'data/route_probe_26q3_v1'
UA = 'cancer-dependency-rsi-metadata-probe/1.0 (research; no browser emulation)'
MAX_REQ, REQ_TIMEOUT, MAX_BYTES, DEADLINE_S = 6, 30, 32 * 1024 * 1024, 280
ALLOWED_HOSTS = {'forum.depmap.org', 'depmap.org', 'storage.googleapis.com'}
ALLOW = {'Model.csv', 'CRISPRScreenMap.csv', 'ScreenSequenceMap.csv', 'ModelCondition.csv'}
DENY = re.compile(r'(?i)(GeneEffect|GeneDependency|Chronos|LFC|LogFold|ReadCount|Score|Effect|Essential|Fitness|BAGEL|Expression|Mutation|CopyNumber|Omics)')
SIX_FORMAT = ['ACH-000108', 'ACH-000178', 'ACH-001418', 'ACH-002958', 'ACH-003040', 'ACH-003052']
MINIPOOL_ALL = SIX_FORMAT + ['ACH-000048']
START = time.monotonic()


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


OPENER = urllib.request.build_opener(NoRedirect)
REQUESTS: list[dict] = []
BYTES = 0


def public_url(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, '', ''))


def fetch(url: str, purpose: str, cap: int, follow: int = 1):
    """One counted GET; follows <= `follow` redirects (each counted) within allowed hosts."""
    global BYTES
    hops = 0
    while True:
        rec = {'n': len(REQUESTS) + 1, 'purpose': purpose, 'url_public': public_url(url),
               'url_sha256': hashlib.sha256(url.encode()).hexdigest()}
        host = urllib.parse.urlsplit(url).hostname or ''
        if len(REQUESTS) >= MAX_REQ:
            return None, {'refused': 'request budget exhausted', **rec}
        if host not in ALLOWED_HOSTS:
            return None, {'refused': f'host {host} not allowed', **rec}
        remaining_t = DEADLINE_S - (time.monotonic() - START)
        if remaining_t < 5:
            return None, {'refused': 'deadline', **rec}
        cap = min(cap, MAX_BYTES - BYTES)
        REQUESTS.append(rec)
        t0 = time.monotonic()
        body, status, headers, err = b'', None, {}, None
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': '*/*'})
            with OPENER.open(req, timeout=min(REQ_TIMEOUT, remaining_t)) as r:
                status, headers = r.status, dict(r.headers)
                while True:
                    if time.monotonic() - t0 > REQ_TIMEOUT:
                        err = 'per-request wall timeout during body'; break
                    chunk = r.read(65536)
                    if not chunk:
                        break
                    body += chunk
                    if len(body) > cap:
                        err = f'byte cap {cap} exceeded; truncated, discarded'; break
        except urllib.error.HTTPError as e:
            status, headers = e.code, dict(e.headers or {})
            try:
                body = e.read(min(cap, 65536))
            except Exception:  # noqa: BLE001
                body = b''
            if not (300 <= e.code < 400):
                err = f'HTTP {e.code}'
        except Exception as e:  # noqa: BLE001
            err = f'{type(e).__name__}: {e}'
        BYTES += len(body)
        rec.update({'status': status, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                    'content_type': headers.get('Content-Type') or headers.get('content-type'),
                    'wall_s': round(time.monotonic() - t0, 3), 'error': err})
        if status and 300 <= status < 400:
            loc = headers.get('Location') or headers.get('location')
            rec['redirect_to_public'] = public_url(urllib.parse.urljoin(url, loc)) if loc else None
            if loc and hops < follow:
                hops += 1
                url = urllib.parse.urljoin(url, loc)
                continue
            return None, rec
        if err and 'byte cap' in err:
            return None, rec
        return (body if not err else None), rec


def looks_html(body: bytes) -> bool:
    head = body[:2048].lstrip().lower()
    return head.startswith(b'<!doctype html') or head.startswith(b'<html') or b'<html' in head[:512]


def save(name: str, body: bytes) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / name).write_bytes(body)
    return {'file': os.path.relpath(RAW / name, ROOT), 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}


def read_csv_bytes(body: bytes) -> list[dict]:
    return list(csv.DictReader(io.StringIO(body.decode('utf-8-sig', errors='replace'))))


def main() -> int:
    spec_sha = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    res: dict = {'spec': str(SPEC.relative_to(ROOT)), 'spec_sha256': spec_sha, 'q': None,
                 'admissible_for_policy': False, 'G2': 'FAIL', 'C_outcomes_accessed': False,
                 'dependency_matrix_accessed': False, 'requirements': {}, 'notes': []}

    # ---------- S0 offline (cached metadata only) ----------
    braw = ROOT / 'data/raw/broad_figshare'
    mm = list(csv.DictReader(open(braw / 'model_metadata.csv', encoding='utf-8-sig')))
    sm = list(csv.DictReader(open(braw / 'screen_metadata.csv', encoding='utf-8-sig')))
    ng_screens = [r for r in sm if r.get('IsNextGen') == 'TRUE']
    ng_org_screens = [r for r in ng_screens if r.get('ScreenType') in ('2DO', '3DO')]
    exposed_models = sorted({r['ModelID'] for r in ng_screens})
    exposed_screen_ids = sorted({r['ScreenID'] for r in ng_screens})
    split = json.loads((ROOT / 'data/split_manifest.json').read_text())
    C = split['C_external']
    c_samples = set(C['sample_ids'])
    c_donors = {str(d) for d in C['donor_ids']} | {str(d) for d in C['excluded_broad_overlap_donors']}
    xw = list(csv.DictReader(open(ROOT / 'data/crosswalk_sanger_screened.csv', encoding='utf-8-sig')))
    res['S0_offline'] = {
        'manuscript_nextgen_screens': len(ng_screens),
        'manuscript_nextgen_organoid_screens_2DO_3DO': len(ng_org_screens),
        'manuscript_nextgen_screened_models': len(exposed_models),
        'manuscript_nextgen_organoid_screened_models': len({r['ModelID'] for r in ng_org_screens}),
        'screen_type_counts': {t: sum(r.get('ScreenType') == t for r in ng_screens) for t in sorted({r.get('ScreenType') for r in ng_screens})},
        'model_metadata_has_donor_column': any(k.lower() in ('patientid', 'donorid', 'patient_id') for k in mm[0].keys()),
        'model_metadata_columns': list(mm[0].keys()),
        'C_models': len(c_samples), 'C_donors_plus_excluded_overlap': len(c_donors),
        'sanger_crosswalk_rows': len(xw),
        'exposure_basis': 'manuscript NextGen screens feed released aggregate organoid-vs-2D tables already inspected/used in Layer A (fixed 2D ordering source table, T_g, Tier-A selection, estimators)'}

    # ---------- R1 forum staff post ----------
    body, rec = fetch('https://forum.depmap.org/t/organoid-dependency-data/4671.json', 'R1 staff post topic JSON', 4 * 1024 * 1024)
    post7, links = None, []
    if body and not looks_html(body):
        res['R1_saved'] = save('forum_topic_4671.json', body)
        try:
            topic = json.loads(body)
            for p in topic.get('post_stream', {}).get('posts', []):
                if p.get('post_number') == 7:
                    post7 = p
            if post7:
                cooked = post7.get('cooked', '')
                links = sorted(set(re.findall(r'href="([^"]+)"', cooked)))
                res['R1_post7'] = {k: post7.get(k) for k in ('username', 'name', 'staff', 'admin', 'moderator', 'primary_group_name', 'user_title', 'created_at', 'updated_at')}
                res['R1_post7']['cooked_sha256'] = hashlib.sha256(cooked.encode()).hexdigest()
                res['R1_post7']['links'] = [public_url(u) for u in links]
                res['R1_post7']['text'] = re.sub(r'<[^>]+>', ' ', cooked)[:3000]
        except ValueError as e:
            rec['parse_error'] = str(e)
    authoritative = bool(post7 and (post7.get('staff') or post7.get('admin') or post7.get('moderator')))
    res['requirements']['primary_route_authoritative_staff_post'] = authoritative if post7 else 'UNRESOLVED'

    # ---------- R2 official release manifest ----------
    manifest_rows, rel26, relng = None, [], []
    body, rec = fetch('https://depmap.org/portal/api/download/files', 'R2 official portal release-file manifest', 12 * 1024 * 1024)
    if body is not None and looks_html(body):
        rec['guard'] = 'HTML received where CSV expected (verification/challenge?); stopped, no bypass'
        res['R2_html_head_sha256'] = hashlib.sha256(body[:4096]).hexdigest()
        body = None
    if body:
        res['R2_saved'] = save('portal_download_files.csv', body)
        manifest_rows = read_csv_bytes(body)
        cols = list(manifest_rows[0].keys()) if manifest_rows else []
        rcol = next((c for c in cols if c.lower() in ('release', 'release_name')), None)
        fcol = next((c for c in cols if c.lower() in ('filename', 'file_name', 'file')), None)
        ucol = next((c for c in cols if c.lower() in ('url', 'download_url')), None)
        releases = sorted({r.get(rcol, '') for r in manifest_rows}) if rcol else []
        rel26 = [r for r in manifest_rows if rcol and '26Q3' in r.get(rcol, '')]
        relng = [r for r in manifest_rows if rcol and 'nextgen' in r.get(rcol, '').lower()]
        strip = lambda r: {k: (public_url(v) if k == ucol else v) for k, v in r.items()}  # noqa: E731
        res['R2_manifest'] = {'columns': cols, 'n_rows': len(manifest_rows), 'release_col': rcol, 'file_col': fcol,
                              'url_col': ucol, 'releases_matching_26Q3': sorted({r[rcol] for r in rel26}) if rcol else [],
                              'releases_matching_nextgen': sorted({r[rcol] for r in relng}) if rcol else [],
                              'n_releases': len(releases),
                              'rows_26Q3': [strip(r) for r in rel26], 'rows_nextgen': [strip(r) for r in relng]}
    res['requirements']['release_manifest_obtained'] = bool(manifest_rows)

    def pick(rows, name):
        if not rows:
            return None
        fcol = res['R2_manifest']['file_col']
        hits = [r for r in rows if r.get(fcol) == name]
        return hits[0] if hits else None

    def get_meta(rows, name, tag):
        row = pick(rows, name)
        if row is None:
            return None, f'{name} not listed'
        if name not in ALLOW or DENY.search(name):
            return None, f'{name} refused by outcome guard'
        url = row[res['R2_manifest']['url_col']]
        b, rr = fetch(url, f'{tag} {name}', 16 * 1024 * 1024)
        if b is None:
            return None, rr.get('error') or rr.get('refused') or 'no body'
        if looks_html(b):
            rr['guard'] = 'HTML instead of CSV; stopped'
            return None, 'HTML instead of CSV'
        return b, None

    model_rows = screen_rows = None
    for tag, rows in (('26Q3', rel26), ('NextGenManuscript2026', relng)):
        if model_rows is not None:
            break
        if not rows:
            continue
        b, why = get_meta(rows, 'Model.csv', f'R3[{tag}]')
        res.setdefault('R3_attempts', []).append({'release': tag, 'file': 'Model.csv', 'failure': why})
        if b:
            res['R3_saved'] = save(f'Model_{tag}.csv', b)
            model_rows, res['R3_release'] = read_csv_bytes(b), tag
            for nm in ('CRISPRScreenMap.csv', 'ScreenSequenceMap.csv'):
                if pick(rows, nm) is None:
                    res.setdefault('R4_attempts', []).append({'release': tag, 'file': nm, 'failure': 'not listed'})
                    continue
                b2, why2 = get_meta(rows, nm, f'R4[{tag}]')
                res.setdefault('R4_attempts', []).append({'release': tag, 'file': nm, 'failure': why2})
                if b2:
                    res['R4_saved'] = save(f'{nm[:-4]}_{tag}.csv', b2)
                    screen_rows = read_csv_bytes(b2)
                    break
    if manifest_rows is None and len(REQUESTS) < MAX_REQ:
        b, rr = fetch('https://depmap.org/portal/data_page/?tab=allData', 'R5 publication-declared fallback route', 2 * 1024 * 1024)
        res['R5_fallback_route'] = {'served_html': bool(b) and looks_html(b), 'note': 'SPA/HTML page cannot itself provide a machine-readable file-set manifest; contents not parsed beyond HTML detection'}

    # ---------- eligibility audit ----------
    evidence: list[dict] = []
    if model_rows:
        cols = list(model_rows[0].keys())
        res['R3_columns'] = cols
        org_fields = [c for c in cols if c in ('GrowthPattern', 'DepmapModelType', 'ModelType', 'OncotreeCode', 'ModelSubtypeFeatures', 'ModelDerivationMaterial', 'CulturedType', 'IsNextGen')]
        donor_col = next((c for c in cols if c.lower() in ('patientid', 'donorid')), None)
        hcmi_col = next((c for c in cols if c.lower() in ('hcmiid',)), None)
        sanger_col = next((c for c in cols if c.lower() in ('sangermodelid',)), None)
        name_cols = [c for c in cols if c in ('CellLineName', 'StrippedCellLineName', 'CCLEName', 'PublicComments')]

        def is_org(r):
            txt = ' '.join(str(r.get(c, '')) for c in org_fields + ['ModelType']).lower()
            return 'organoid' in txt or r.get('GrowthPattern') in ('Dome', 'Organoid') or r.get('ModelType', '').lower() == 'organoid'
        screened = None
        if screen_rows:
            sc = list(screen_rows[0].keys())
            res['R4_columns'] = sc
            mcol = next((c for c in sc if c.lower() == 'modelid'), None)
            scol = next((c for c in sc if c.lower() == 'screenid'), None)
            screened = {}
            for r in screen_rows:
                screened.setdefault(r.get(mcol), set()).add(r.get(scol))
        donors_of = {}
        for r in model_rows:
            donors_of[r['ModelID']] = (r.get(donor_col) or '').strip() if donor_col else ''
        exposed_donors = {donors_of.get(m) for m in exposed_models if donors_of.get(m)}
        input_donors = {donors_of.get(m) for m in MINIPOOL_ALL if donors_of.get(m)}
        for r in model_rows:
            if not is_org(r):
                continue
            m = r['ModelID']
            d = donors_of.get(m, '')
            ids_txt = ' '.join(str(r.get(c, '')) for c in [hcmi_col, sanger_col] + name_cols if c)
            c_hit = any(s in ids_txt for s in c_samples) or bool(re.search(r'HCM-SANG-\d{4}', ids_txt))
            row = {'ModelID': m, 'donor': d or None,
                   'E1_crispr_screen_26Q3': (m in screened) if screened is not None else 'UNKNOWN',
                   'new_screen_ids_vs_manuscript': sorted(screened.get(m, set()) - set(exposed_screen_ids)) if screened is not None else 'UNKNOWN',
                   'E2_documented_donor': bool(d),
                   'E3_not_broad_input': m not in MINIPOOL_ALL and (not d or d not in input_donors),
                   'E4_not_C': (not c_hit) if (hcmi_col or sanger_col) else 'UNKNOWN',
                   'E5_unexposed_donor': (m not in exposed_models) and (not d or d not in exposed_donors)}
            for k in ('ModelType', 'GrowthPattern', 'DepmapModelType', 'OncotreeLineage'):
                if k in r:
                    row[k] = r[k]
            if hcmi_col:
                row['HCMIID'] = r.get(hcmi_col)
            evidence.append(row)
        elig = [e for e in evidence if e['E1_crispr_screen_26Q3'] is True and e['E2_documented_donor'] and e['E3_not_broad_input'] and e['E4_not_C'] is True and e['E5_unexposed_donor']]
        elig_donors = sorted({e['donor'] for e in elig})
        res['eligibility_summary'] = {
            'organoid_models_in_Model_csv': len(evidence),
            'organoid_models_with_26Q3_crispr_screen': sum(e['E1_crispr_screen_26Q3'] is True for e in evidence),
            'organoid_screened_models_exposed_manuscript': sum(e['E1_crispr_screen_26Q3'] is True and not e['E5_unexposed_donor'] for e in evidence),
            'organoid_screened_models_with_new_screen_ids': sum(bool(e['new_screen_ids_vs_manuscript']) and isinstance(e['new_screen_ids_vs_manuscript'], list) for e in evidence),
            'organoid_screened_models_C_overlap': sum(e['E1_crispr_screen_26Q3'] is True and e['E4_not_C'] is False for e in evidence),
            'donor_column': donor_col, 'hcmi_column': hcmi_col, 'sanger_column': sanger_col, 'organoid_fields_used': org_fields,
            'eligible_unexposed_models': len(elig), 'eligible_unexposed_independent_donors': len(elig_donors),
            'E8_floor': 80, 'E8_floor_met': len(elig_donors) >= 80}
        res['evidence_table'] = evidence
    res['requests'] = REQUESTS
    res['resources'] = {'requests_used': len(REQUESTS), 'bytes_transferred': BYTES, 'wall_s': round(time.monotonic() - START, 3)}
    OUT.write_text(json.dumps(res, indent=1, sort_keys=False))
    print(json.dumps({'requests': len(REQUESTS), 'bytes': BYTES, 'wall_s': res['resources']['wall_s'],
                      'manifest': res['requirements'].get('release_manifest_obtained'),
                      'summary': res.get('eligibility_summary')}, default=str))
    return 0


if __name__ == '__main__':
    sys.exit(main())
