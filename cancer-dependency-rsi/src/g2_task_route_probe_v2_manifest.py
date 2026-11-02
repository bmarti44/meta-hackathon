"""Manifest-only probe v2 (SPEC reviews/prompts/g2_task_route_probe_v2_manifest.json). No data files fetched."""
from __future__ import annotations
import csv, hashlib, io, json, socket, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'reviews/prompts/g2_task_route_probe_v2_manifest.json'
OUT = ROOT / 'reviews/g2_task_route_probe_v2_manifest.json'
RAW = ROOT / 'data/route_probe_26q3_v2'
URL = 'https://depmap.org/portal/api/no-captcha/download/files'
UA = 'cancer-dependency-rsi-metadata-probe/1.0 (research; no browser emulation)'
CAP, TIMEOUT = 8 * 1024 * 1024, 30
WANT = ['Model.csv', 'CRISPRScreenMap.csv', 'ScreenSequenceMap.csv', 'ModelCondition.csv', 'CRISPRGeneEffect.csv']


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def pub(u: str) -> str:
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc, p.path, '', '')) if p.scheme else u


def main() -> int:
    if OUT.exists():
        raise SystemExit('immutable output exists')
    t0 = time.monotonic()
    socket.setdefaulttimeout(TIMEOUT)
    rec = {'n': 1, 'url': URL}
    body, status, ctype, err = b'', None, None, None
    try:
        req = urllib.request.Request(URL, headers={'User-Agent': UA, 'Accept': 'text/csv,*/*'})
        with urllib.request.build_opener(NoRedirect).open(req, timeout=TIMEOUT) as r:
            status, ctype = r.status, r.headers.get('Content-Type')
            while time.monotonic() - t0 < TIMEOUT:
                chunk = r.read(min(65536, CAP + 1 - len(body)))
                if not chunk:
                    break
                body += chunk
                if len(body) > CAP:
                    err = 'byte cap exceeded'; body = b''; break
            else:
                err = 'wall timeout'
    except urllib.error.HTTPError as e:
        status, err = e.code, f'HTTP {e.code} (redirects not followed)'
    except Exception as e:  # noqa: BLE001
        err = f'{type(e).__name__}: {e}'
    rec.update({'status': status, 'content_type': ctype, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'wall_s': round(time.monotonic() - t0, 3), 'error': err})
    res = {'spec_sha256': hashlib.sha256(SPEC.read_bytes()).hexdigest(), 'request': rec, 'data_files_downloaded': False, 'C_outcomes_accessed': False}
    head = body[:2048].lstrip().lower()
    if body and (head.startswith(b'<!doctype html') or b'<html' in head[:512]):
        res['guard'] = 'HTML instead of CSV; stopped, no bypass'
    elif body and not err:
        rows = list(csv.DictReader(io.StringIO(body.decode('utf-8-sig', errors='replace'))))
        cols = list(rows[0].keys()) if rows else []
        urlish = [c for c in cols if 'url' in c.lower()]
        for r in rows:
            for c in urlish:
                r[c] = pub(r[c] or '')
        buf = io.StringIO(); w = csv.DictWriter(buf, fieldnames=cols); w.writeheader(); w.writerows(rows)
        RAW.mkdir(parents=True, exist_ok=True)
        saved = buf.getvalue().encode()
        (RAW / 'no_captcha_files.csv').write_bytes(saved)
        rcol = next((c for c in cols if c.lower() in ('release', 'release_name')), None)
        fcol = next((c for c in cols if c.lower() in ('filename', 'file_name')), None)
        r26 = [r for r in rows if rcol and '26Q3' in (r.get(rcol) or '')]
        res.update({'columns': cols, 'n_rows': len(rows), 'url_columns_sanitized': urlish,
                    'saved': {'file': 'data/route_probe_26q3_v2/no_captcha_files.csv', 'sha256': hashlib.sha256(saved).hexdigest(), 'note': 'sanitized re-serialization; raw response sha256 in request'},
                    'releases_26Q3': sorted({r[rcol] for r in r26}) if rcol else [],
                    'n_files_26Q3': len(r26),
                    'files_26Q3_selected': [r for r in r26 if fcol and r.get(fcol) in WANT],
                    'filenames_26Q3': sorted({r.get(fcol) for r in r26}) if fcol else [],
                    'nextgen_releases_present': sorted({r[rcol] for r in rows if rcol and 'nextgen' in (r.get(rcol) or '').lower()})})
    res['wall_s'] = round(time.monotonic() - t0, 3)
    OUT.write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res.get(k) for k in ('request', 'guard', 'n_rows', 'releases_26Q3', 'n_files_26Q3')}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
