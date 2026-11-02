"""CL-RD-FEASIBILITY-01 stage 1: official documentation of cell-line matrix preprocessing (docs only)."""
from __future__ import annotations
import hashlib, html, json, re, socket, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / 'reviews/prompts/cl_rd_feasibility_stage1_v1.json'
OUT = ROOT / 'reviews/cl_rd_feasibility_stage1_v1.json'
RAW = ROOT / 'data/route_probe_cellline_v1'
UA = 'cancer-dependency-rsi-metadata-probe/1.0 (research; no browser emulation)'
START_URL = 'https://depmap.sanger.ac.uk/documentation/datasets/wg-crispr-knockout/'
MAXREQ, TIMEOUT, CAP = 4, 30, 8 * 1024 * 1024
KEY = re.compile(r'(?i)(combat|batch|quantile|principal component|integrat|achilles|broad|correct)')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def main() -> int:
    if OUT.exists():
        raise SystemExit('immutable output exists')
    socket.setdefaulttimeout(TIMEOUT)
    t0 = time.monotonic(); url = START_URL; reqs = []; body = b''
    while len(reqs) < MAXREQ:
        rec = {'n': len(reqs) + 1, 'url': url}; reqs.append(rec); t1 = time.monotonic()
        try:
            r = urllib.request.build_opener(NoRedirect).open(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=TIMEOUT)
            data = b''
            while len(data) <= CAP and time.monotonic() - t1 < TIMEOUT:
                ch = r.read(min(65536, CAP + 1 - len(data)))
                if not ch:
                    break
                data += ch
            rec.update(status=r.status, content_type=r.headers.get('Content-Type'), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            body = data if len(data) <= CAP else b''
            break
        except urllib.error.HTTPError as e:
            loc = e.headers.get('Location') if e.headers else None
            rec.update(status=e.code, location=loc)
            if 300 <= e.code < 400 and loc:
                nxt = urllib.parse.urljoin(url, loc)
                if not (urllib.parse.urlsplit(nxt).hostname or '').endswith('sanger.ac.uk'):
                    rec['refused'] = 'redirect off sanger.ac.uk'; break
                url = nxt; continue
            break
        except Exception as e:  # noqa: BLE001
            rec['error'] = f'{type(e).__name__}: {e}'; break
        finally:
            rec['wall_s'] = round(time.monotonic() - t1, 3)
    res = {'spec_sha256': hashlib.sha256(SPEC.read_bytes()).hexdigest(), 'requests': reqs, 'dependency_data_requested': False}
    if body:
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / 'wg_crispr_knockout_doc.html').write_bytes(body)
        text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?is)<(script|style).*?</\1>|<[^>]+>', ' ', body.decode('utf-8', 'replace'))))
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if KEY.search(s)]
        res.update(text_chars=len(text), challenge_suspected=bool(re.search(r'(?i)captcha|verify you are human|access denied', text)) and len(text) < 3000,
                   key_sentences=sents[:80], title=re.search(r'(?is)<title>(.*?)</title>', body.decode('utf-8', 'replace')).group(1).strip() if b'<title' in body.lower() else None)
    res['wall_s'] = round(time.monotonic() - t0, 3)
    OUT.write_text(json.dumps(res, indent=1))
    print(json.dumps({'requests': [(r.get('status'), r.get('bytes'), r.get('error')) for r in reqs], 'n_sentences': len(res.get('key_sentences', [])), 'title': res.get('title')}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
