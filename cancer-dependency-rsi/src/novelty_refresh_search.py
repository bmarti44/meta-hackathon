"""C1/C6 novelty refresh: bounded Europe PMC REST searches (metadata only: titles/abstract snippets)."""
from __future__ import annotations
import hashlib, json, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ('reviews/novelty_refresh_v3b_pubmed.json' if '--pubmed' in sys.argv else 'reviews/novelty_refresh_v3_search.json')
UA = 'cancer-dependency-rsi-novelty-audit/1.0 (research)'
BASE = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?'
QUERIES = {
    'Q1_format_lability_transfer': '(organoid*) AND (CRISPR) AND ("growth format" OR "culture format" OR dome OR "2D versus 3D" OR "2D vs 3D") AND (dependenc*) AND (transfer* OR concordan* OR displacement OR rank*) AND (PUB_YEAR:[2024 TO 2026])',
    'Q2_minipool_environment': '(minipool OR "mini-pool") AND (CRISPR) AND (organoid* OR "culture condition*" OR serum)',
    'Q3_cellline_to_organoid_dependency_transfer': '("cell line*") AND (organoid*) AND (CRISPR OR "gene dependenc*") AND (transferab* OR "rank transfer" OR "cross-model") AND (PUB_YEAR:[2025 TO 2026])',
    'Q4_S1_citations_proxy': '("next-generation" OR "NextGen") AND ("3D cancer models" OR organoid*) AND ("dependency map" OR DepMap) AND (PUB_YEAR:[2026 TO 2026])',
    'Q5_environment_sensitivity_dependency': '("environmental sensitivity" OR "culture-condition sensitivity" OR "condition-dependent essential*" OR "context-dependent essential*") AND (organoid*) AND (CRISPR) AND (PUB_YEAR:[2024 TO 2026])',
    'Q6_sanger_organoid_crispr_followups': '(Sanger) AND (organoid*) AND ("CRISPR screen*") AND (dependenc*) AND (PUB_YEAR:[2026 TO 2026])',
}


PM_QUERIES = {
    'P1_format_lability_transfer': '(organoid*[tiab]) AND (CRISPR[tiab]) AND ("growth format"[tiab] OR "culture format"[tiab] OR dome[tiab] OR "2D"[tiab]) AND (dependenc*[tiab]) AND (transfer*[tiab] OR concordan*[tiab] OR rank*[tiab]) AND 2024:2026[dp]',
    'P2_minipool_environment': '(minipool[tiab] OR "mini-pool"[tiab]) AND CRISPR[tiab] AND (organoid*[tiab] OR serum[tiab] OR "culture condition*"[tiab])',
    'P3_cellline_to_organoid_transfer': '("cell line*"[tiab]) AND (organoid*[tiab]) AND (CRISPR[tiab] OR "gene dependenc*"[tiab]) AND (transferab*[tiab] OR "cross-model"[tiab] OR translat*[tiab]) AND 2025:2026[dp]',
    'P4_nextgen_depmap': '("next-generation"[tiab] OR NextGen[tiab]) AND (organoid*[tiab] OR "3D"[tiab]) AND ("dependency map"[tiab] OR DepMap[tiab]) AND 2026[dp]',
    'P5_condition_dependent_essentiality': '("context-dependent"[tiab] OR "condition-dependent"[tiab] OR "culture condition*"[tiab] OR "environment*"[tiab]) AND (organoid*[tiab]) AND (CRISPR screen*[tiab]) AND (essential*[tiab] OR dependenc*[tiab]) AND 2024:2026[dp]',
    'P6_sanger_organoid_crispr': '(organoid*[tiab]) AND ("CRISPR screen*"[tiab]) AND (biobank[tiab] OR Sanger[ad]) AND 2026[dp]',
}


def pubmed() -> int:
    E = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    res = {'retrieved_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'source': 'NCBI E-utilities esearch+esummary (official API)', 'queries': {}}
    for k, q in PM_QUERIES.items():
        try:
            u = E + 'esearch.fcgi?' + urllib.parse.urlencode({'db': 'pubmed', 'term': q, 'retmode': 'json', 'retmax': 25, 'sort': 'relevance'})
            with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=30) as r:
                d = json.loads(r.read(2 * 1024 * 1024))
            ids = d['esearchresult'].get('idlist', [])
            hits = []
            if ids:
                time.sleep(0.4)
                u2 = E + 'esummary.fcgi?' + urllib.parse.urlencode({'db': 'pubmed', 'id': ','.join(ids), 'retmode': 'json'})
                with urllib.request.urlopen(urllib.request.Request(u2, headers={'User-Agent': UA}), timeout=30) as r:
                    s2 = json.loads(r.read(4 * 1024 * 1024))
                for i in ids:
                    h = s2['result'].get(i, {})
                    hits.append({'pmid': i, 'title': h.get('title'), 'journal': h.get('source'), 'year': (h.get('pubdate') or '')[:4],
                                 'doi': next((a['value'] for a in h.get('articleids', []) if a.get('idtype') == 'doi'), None)})
            res['queries'][k] = {'query': q, 'hitCount': int(d['esearchresult'].get('count', 0)), 'top': hits}
        except Exception as e:  # noqa: BLE001
            res['queries'][k] = {'query': q, 'error': f'{type(e).__name__}: {e}'}
        time.sleep(0.4)
    OUT.write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v.get('hitCount', v.get('error')) for k, v in res['queries'].items()}))
    return 0


def main() -> int:
    if '--pubmed' in sys.argv:
        if OUT.exists():
            raise SystemExit('immutable output exists')
        return pubmed()
    if OUT.exists():
        raise SystemExit('immutable output exists')
    res = {'retrieved_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'source': 'Europe PMC REST search (official API)', 'queries': {}}
    for k, q in QUERIES.items():
        url = BASE + urllib.parse.urlencode({'query': q, 'format': 'json', 'pageSize': 25, 'resultType': 'lite', 'sort': 'RELEVANCE'})
        t0 = time.monotonic()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=30) as r:
                body = r.read(4 * 1024 * 1024)
            d = json.loads(body)
            hits = [{'id': h.get('id'), 'source': h.get('source'), 'pmid': h.get('pmid'), 'pmcid': h.get('pmcid'), 'doi': h.get('doi'),
                     'title': h.get('title'), 'journal': h.get('journalTitle'), 'year': h.get('pubYear'), 'authors': (h.get('authorString') or '')[:160]}
                    for h in d.get('resultList', {}).get('result', [])]
            res['queries'][k] = {'query': q, 'hitCount': d.get('hitCount'), 'top': hits, 'sha256': hashlib.sha256(body).hexdigest(), 'wall_s': round(time.monotonic() - t0, 3)}
        except Exception as e:  # noqa: BLE001
            res['queries'][k] = {'query': q, 'error': f'{type(e).__name__}: {e}'}
    OUT.write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v.get('hitCount', v.get('error')) for k, v in res['queries'].items()}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
