"""Guarded single-execution external evaluation (scientific-only track; Lock-S / Lock2).

Execution contract:
- Only via src/run_external_eval.py (run_bounded: reserve-before-dispatch, RSS watchdog,
  timeout, reconciliation). main() refuses unless an outstanding ledger reservation named
  JOB_NAME exists for this script (no silent bypass through direct invocation).
- Refuses unless lock_s/LOCK2_COMMIT.json exists and every committed file hash matches.
- Single execution: atomic O_EXCL start record (fsynced) BEFORE the exposure record and any
  Table-6 decoding; results committed atomically with no-overwrite links. A start record
  without a result refuses further runs (documented adjudication required).

Primary (decision): confirmatory207 / mean_abs_delta / base_strength via
confirmatory_estimand.donor_bootstrap (5000 donor-cluster reps, seed 20261028).
Secondary Holm family (FWER 0.05; H0 rho=0, two-sided): S1 null-calibrated displacement;
S2 TMOD1-alias 208 genes; S3 v1_1 library for dual-library models; S4 unadjusted.
Invalid analyses keep their family slot with p=None (treated as 1 in Holm) and never reject.
Bootstrap p over ALL B replicates; failed replicates count against rejection in both tails.
Stability (never decision) is isolated: any failure is recorded, never blocks persistence.
"""
from __future__ import annotations

import csv
import io
import json
import os
import sys
import time
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import confirmatory_estimand as ce  # noqa: E402
import donor_kernel as dk  # noqa: E402
import estimators  # noqa: E402
from ledger import append_record, read_records, sha256_file  # noqa: E402

T6 = 'supplementary_table_6_revision.csv'
JOB_NAME = 'external_eval_lock2_v1'
REPS, SEED, STAB_REPS = 5000, 20261028, 2000
MAX_MODEL_EXCLUSION_FRACTION = 0.05
REQUIRED = {
    'src/external_eval.py', 'src/run_external_eval.py', 'src/confirmatory_estimand.py', 'src/donor_kernel.py',
    'src/estimators.py', 'src/ledger.py', 'src/budget.py', 'src/cli.py', 'src/lock_s_prep.py',
    'lock_s/covariates.csv', 'lock_s/cohort.csv', 'lock_s/presence.json', 'lock_s/scientific_protocol_v1.json',
    'data/raw/sanger_figshare/S2_Supplementary_Tables.zip', 'data/broad_stability_groupings.json',
    'data/raw/broad_figshare/minipool_screen_metadata.csv', 'data/raw/broad_figshare/minipool_chronos_gene_effects.csv',
    'data/raw/broad_figshare/organoids_vs_2d_gene_dependency_tests_full.csv',
    'data/raw/broad_figshare/minipool_library_composition.csv',
    'data/split_manifest.json', 'data/gene_scopes.json', 'data/confirmatory_gene_candidates.json',
    'data/crosswalk_sanger_screened.csv', 'data/provenance_v3_addendum.md', 'contract.json',
    'config/resources.json', 'config/allocations.json', 'pyproject.toml', 'uv.lock', 'requirements-lock.txt'}


class LockError(RuntimeError):
    pass


def verify_lock(root: Path = ROOT) -> dict:
    commit = root / 'lock_s' / 'LOCK2_COMMIT.json'
    if not commit.is_file():
        raise LockError('REFUSED: Lock2 not committed (lock_s/LOCK2_COMMIT.json missing)')
    c = json.loads(commit.read_text())
    if c.get('state') != 'COMMITTED' or not c.get('files'):
        raise LockError('REFUSED: Lock2 commit incomplete')
    missing = REQUIRED - set(c['files'])
    if missing:
        raise LockError(f'REFUSED: Lock2 commit lacks required files {sorted(missing)}')
    for rel, digest in c['files'].items():
        p = root / rel
        if not p.is_file() or sha256_file(p) != digest:
            raise LockError(f'REFUSED: hash mismatch for {rel}')
    return c


NONCE_ENV = 'CDRSI_EXTERNAL_EVAL_NONCE'
MAX_RESERVATION_AGE_S = 120


def require_bounded(root: Path) -> dict:
    """Bind execution to the launcher's own live reservation and supervised child.

    The launcher (src/run_external_eval.py) generates a one-time nonce, records only its
    sha256 and its own PID in the run_bounded reservation, and passes the nonce to the child
    via the environment. The child must (a) hold the nonce, (b) find exactly one outstanding
    reservation for JOB_NAME with that nonce hash, (c) be a direct child of the recorded
    launcher PID, and (d) start within MAX_RESERVATION_AGE_S of the reservation. Stale
    reservations and direct/unsupervised invocations are refused.
    """
    import calendar
    import hashlib
    nonce = os.environ.get(NONCE_ENV)
    if not nonce:
        raise LockError('REFUSED: must run via src/run_external_eval.py (no launcher nonce)')
    digest = hashlib.sha256(nonce.encode()).hexdigest()
    recs = read_records(root / 'ledger' / 'resources.jsonl')
    done = {r.get('reservation_id') for r in recs if r.get('kind') == 'reconcile'}
    active = [r for r in recs if r.get('kind') == 'reserve' and r['record_id'] not in done
              and r['job'].get('name') == JOB_NAME and r['job'].get('cpu_heavy')
              and r['job'].get('launch_nonce_sha256') == digest
              and any(str(a).endswith('external_eval.py') for a in r['job'].get('argv', []))]
    if len(active) != 1:
        raise LockError('REFUSED: must run via src/run_external_eval.py (no matching live bounded reservation)')
    job = active[0]['job']
    if job.get('launcher_pid') != os.getppid():
        raise LockError('REFUSED: process is not the supervised child of the reserving launcher')
    age = time.time() - calendar.timegm(time.strptime(active[0]['ts_utc'], '%Y-%m-%dT%H:%M:%SZ'))
    if not -5 <= age <= MAX_RESERVATION_AGE_S:
        raise LockError('REFUSED: stale bounded reservation')
    return active[0]


def start_parent_watchdog(launcher_pid: int, interval: float = 0.25):
    """Child-side guard: if the supervising launcher dies (even by SIGKILL), kill this job's process group."""
    import signal
    import threading

    def watch():
        while True:
            if os.getppid() != launcher_pid:
                try:
                    os.killpg(os.getpgid(0), signal.SIGKILL)
                finally:
                    os._exit(137)
            time.sleep(interval)
    threading.Thread(target=watch, daemon=True, name='launcher-watchdog').start()


def _fsync_dir(d: Path):
    fd = os.open(d, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def acquire_start(path: Path, payload: dict):
    created = not path.parent.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    if created:
        _fsync_dir(path.parent.parent)  # durable directory entry for the results directory
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o444)
    except FileExistsError:
        raise LockError('REFUSED: a previous execution started; result exists or documented adjudication required (no silent rerun)') from None
    with os.fdopen(fd, 'w') as fh:
        fh.write(json.dumps(payload)); fh.flush(); os.fsync(fh.fileno())
    _fsync_dir(path.parent)


def commit_bytes(path: Path, data: bytes):
    """Durable, no-overwrite commit: write temp, fsync, hard-link to final name (fails if exists)."""
    tmp = path.with_name(path.name + f'.tmp{os.getpid()}')
    with open(tmp, 'xb') as fh:
        fh.write(data); fh.flush(); os.fsync(fh.fileno())
    try:
        os.link(tmp, path)
    finally:
        os.unlink(tmp)
    _fsync_dir(path.parent)


def read_inputs(root: Path):
    cov = list(csv.DictReader(open(root / 'lock_s/covariates.csv')))
    coh = list(csv.DictReader(open(root / 'lock_s/cohort.csv')))
    return cov, coh


def stream_lfc(zip_path: Path, member: str, samples: set, genes: set) -> dict:
    """Return {(sample, library, gene): float}; only cohort/panel cells are converted."""
    out = {}
    with zipfile.ZipFile(zip_path) as z, z.open(member) as raw:
        rd = csv.reader(io.TextIOWrapper(raw, encoding='utf-8'), delimiter=' ')
        h = next(rd)
        i_s, i_g, i_l, i_v = h.index('sample_ID'), h.index('gene'), h.index('library'), h.index('LFC')
        for row in rd:
            if row[i_s] in samples and row[i_g] in genes:
                key = (row[i_s], row[i_l], row[i_g])
                if key in out:
                    raise ValueError(f'duplicate Table-6 cell {key}')
                try:
                    out[key] = float(row[i_v])
                except ValueError:
                    out[key] = float('nan')
    return out


def build_matrix(lfc, coh, genes_sanger, use_alternate=False):
    """genes x models under the library rule; models with any nonfinite/missing cell excluded."""
    cols, sids, dids, excluded = [], [], [], []
    for c in coh:
        lib = c['library_alternate'] if (use_alternate and c['library_alternate']) else c['library_primary']
        v = np.array([lfc.get((c['sample_ID'], lib, g), np.nan) for g in genes_sanger], dtype=float)
        if not np.isfinite(v).all():
            excluded.append({'sample_ID': c['sample_ID'], 'library': lib, 'n_nonfinite_or_missing': int((~np.isfinite(v)).sum())})
            continue
        cols.append(v); sids.append(c['sample_ID']); dids.append(c['donor_ID'])
    return (np.column_stack(cols) if cols else np.zeros((len(genes_sanger), 0))), sids, dids, excluded


def boot_p(values, total=None) -> float | None:
    """Two-sided bootstrap p over all B replicates; failed (nonfinite) replicates count against rejection."""
    v = np.asarray(values, dtype=float)
    B = int(total if total is not None else len(v))
    fin = v[np.isfinite(v)]
    if B == 0 or not len(fin):
        return None
    F = B - len(fin)
    lo = (np.sum(fin <= 0) + F + 1) / (B + 1)
    hi = (np.sum(fin >= 0) + F + 1) / (B + 1)
    return float(min(1.0, 2 * min(lo, hi)))


def holm(pvals: dict) -> dict:
    items = sorted(((p if p is not None else 1.0), k) for k, p in pvals.items())
    m, out, running = len(items), {}, 0.0
    for i, (p, k) in enumerate(items):
        running = max(running, min(1.0, (m - i) * p))
        out[k] = running
    return out


def finalize_family(sec: dict) -> dict:
    """Holm over all 4 slots; invalid members keep their slot (p treated as 1) and never reject."""
    def ok(v):
        return bool(v.get('point_valid') and v.get('interval_valid') and v.get('bootstrap_p_two_sided_rho0') is not None)
    hp = holm({k: (v.get('bootstrap_p_two_sided_rho0') if ok(v) else None) for k, v in sec.items()})
    for k, v in sec.items():
        v['holm_adjusted_p'] = hp[k] if ok(v) else None
        v['holm_reject_rho0_at_0.05'] = bool(ok(v) and hp[k] <= 0.05)
    return sec


def invalid(reason: str, **extra) -> dict:
    return {'point_valid': False, 'interval_valid': False, 'estimate': None, 'ci95_donor_percentile': None,
            'decision': 'INCONCLUSIVE', 'invalid_reasons': [reason], 'bootstrap_p_two_sided_rho0': None, **extra}


def analysis(scores, reference, L, base, sids, dids, excluded, n_cohort, null_calibrated=False):
    """Structured result for one frozen analysis; never raises on data degeneracy."""
    meta = {'n_models_analyzed': len(sids), 'n_donors_analyzed': len(set(dids)), 'model_exclusions': excluded}
    if len(excluded) > MAX_MODEL_EXCLUSION_FRACTION * n_cohort or len(set(dids)) < 2:
        return invalid('model exclusions exceed 5% of cohort or <2 donors', **meta), None
    try:
        res = ce.donor_bootstrap(scores, reference, L, base, sids, dids, reps=REPS, seed=SEED, null_calibrated=null_calibrated)
    except ValueError as exc:
        return invalid(f'extraction/kernel invalid: {exc}', **meta), None
    res.update(meta)
    if not (res.get('point_valid') and res.get('interval_valid')):
        res['bootstrap_p_two_sided_rho0'] = None
        res['decision'] = 'INCONCLUSIVE'
        return res, None
    profiles, donors, rank0, den = ce._profiles(scores, reference, sids, dids, integer=True)
    n = profiles.shape[1]
    draws = np.random.default_rng(SEED).integers(0, n, size=(REPS, n))
    counts = np.zeros((REPS, n), dtype=np.int64)
    np.add.at(counts, (np.repeat(np.arange(REPS), n), draws.ravel()), 1)
    r0 = rank0 if null_calibrated else None
    vals = dk.rank_correlations(dk.means_from_sums(counts @ profiles.T, n, den, r0), L, base)
    point = dk.means_from_sums(profiles.sum(axis=1), n, den, r0)
    fin = vals[np.isfinite(vals)]
    ci2 = np.percentile(fin, [2.5, 97.5]).tolist()
    if not np.allclose(ci2, res['ci95_donor_percentile'], rtol=0, atol=1e-12) or int((~np.isfinite(vals)).sum()) != res['failed_replicates']:
        raise RuntimeError('replicate reconstruction disagrees with production kernel')
    res['bootstrap_p_two_sided_rho0'] = boot_p(vals, REPS)
    return res, point


def _safe(fn):
    try:
        return fn()
    except Exception as exc:  # noqa: BLE001 - stability never blocks persistence
        return {'failed': f'{type(exc).__name__}: {exc}'}


def stability(D, deltas, genes_broad, base, groupings, classes, rng_seed=SEED):
    """Broad-side composition stability; D fixed at its point value. Never decision."""
    rng = np.random.default_rng(rng_seed)
    models = sorted({c.split('|')[0] for c in deltas.columns})

    def rho(Lv, idx=None):
        if idx is None:
            return estimators.partial_spearman(D, Lv, base)
        return estimators.partial_spearman(D[idx], Lv[idx], base[idx])

    def lab(draw=None):
        return estimators.lability(deltas, draw).loc[genes_broad].to_numpy()

    def boot(make):
        vv = []
        for _ in range(STAB_REPS):
            try:
                vv.append(make())
            except ValueError:
                vv.append(np.nan)
        vv = np.array(vv); ff = vv[np.isfinite(vv)]
        return {'reps': STAB_REPS, 'failed': int((~np.isfinite(vv)).sum()), 'pct95': np.percentile(ff, [2.5, 97.5]).tolist() if len(ff) else None}

    out = {'point_rho': _safe(lambda: rho(lab()))}
    out['model_cluster_bootstrap'] = _safe(lambda: boot(lambda: rho(lab(list(rng.choice(models, size=len(models), replace=True))))))
    out['leave_one_model_out'] = {m: _safe(lambda m=m: rho(lab([x for x in models if x != m]))) for m in models}
    lin = {}
    for name, mapping in groupings.items():
        clusters = sorted(set(mapping.values()))
        members = {k: [m for m in models if mapping[m] == k] for k in clusters}
        lin[name] = _safe(lambda clusters=clusters, members=members: {'n_clusters': len(clusters), **boot(
            lambda: rho(lab([m for k in rng.choice(clusters, size=len(clusters), replace=True) for m in members[k]])))})
    out['lineage_cluster_bootstrap'] = lin
    cls_names = sorted(set(classes.values()))
    mem = {k: np.array([i for i, g in enumerate(genes_broad) if classes[g] == k]) for k in cls_names}
    Lfull = _safe(lab)
    if isinstance(Lfull, dict):
        out['pathway_block_bootstrap'] = Lfull
    else:
        out['pathway_block_bootstrap'] = _safe(lambda: {'n_blocks': len(cls_names), **boot(
            lambda: rho(Lfull, np.concatenate([mem[k] for k in rng.choice(cls_names, size=len(cls_names), replace=True)])))})
    out['interpretation'] = 'stability/composition sensitivity conditional on measured Broad models; never governs SIGNAL/BOUND/NEGATIVE'
    return out


def primary_class(genes_broad, root: Path):
    comp = list(csv.DictReader(open(root / 'data/raw/broad_figshare/minipool_library_composition.csv', encoding='utf-8-sig')))
    order = [c for c in comp[0].keys() if c not in ('Gene', 'All test genes')]
    by = {r['Gene']: r for r in comp}
    return {g: (next((c for c in order if by[g][c] == 'True'), 'Other') if g in by else 'Other') for g in genes_broad}


def _json(o):
    return o.tolist() if hasattr(o, 'tolist') else str(o)


def main(root: Path = ROOT) -> int:
    commit = verify_lock(root)
    reservation = require_bounded(root)
    start_parent_watchdog(reservation['job']['launcher_pid'])
    res_dir = root / 'lock_s' / 'results'
    RESULT, DGTABLE, STARTED = res_dir / 'external_v1.json', res_dir / 'external_v1_gene_displacement.csv', res_dir / 'external_v1.started.json'
    ZIP = root / 'data/raw/sanger_figshare/S2_Supplementary_Tables.zip'
    if RESULT.exists():
        raise LockError('REFUSED: immutable external result already exists; single execution only')
    acquire_start(STARTED, {'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                            'lock2_commit': commit.get('commit_id'), 'reservation_id': reservation['record_id'],
                            'pid': os.getpid()})
    t0 = time.monotonic()
    cov, coh = read_inputs(root)
    g207 = [r for r in cov if r['in_207'] == 'True']
    g208 = [r for r in cov if r['in_208'] == 'True']
    samples = {c['sample_ID'] for c in coh}
    append_record(root / 'data/exposure_log.jsonl', {
        'actor': 'external_eval.py', 'operation': 'LOCK2_external_outcome_decode', 'partition': 'C',
        'path': f'data/raw/sanger_figshare/S2_Supplementary_Tables.zip::{T6}', 'outcome_values_decoded': True,
        'scope': '148 cohort samples x 208 panel genes (primary+alternate libraries)',
        'lock2_commit_sha256': sha256_file(root / 'lock_s/LOCK2_COMMIT.json'), 'reservation_id': reservation['record_id'],
        'consequence': 'C consumed; any later use of C is exploratory'})
    lfc = stream_lfc(ZIP, T6, samples, {r['gene_sanger'] for r in g208})

    def arrays(rows):
        return (np.array([float(r['AdherentMean']) for r in rows]), np.array([float(r['L']) for r in rows]),
                np.array([float(r['base_strength']) for r in rows]), [r['gene_sanger'] for r in rows], [r['gene_broad'] for r in rows])

    n = len(coh)
    ref7, L7, b7, gs7, gb7 = arrays(g207)
    S, sids, dids, excl = build_matrix(lfc, coh, gs7)
    prim, Dpoint = analysis(S, ref7, L7, b7, sids, dids, excl, n)
    res = {'lock2_commit': commit.get('commit_id'), 'protocol': 'lock_s/scientific_protocol_v1.json', 'C_consumed': True,
           'primary': prim}
    sec = {}
    sec['S1_null_calibrated'], _ = analysis(S, ref7, L7, b7, sids, dids, excl, n, null_calibrated=True)
    ref8, L8, b8, gs8, gb8 = arrays(g208)
    S8, s8, d8, e8 = build_matrix(lfc, coh, gs8)
    sec['S2_tmod1_alias208'], _ = analysis(S8, ref8, L8, b8, s8, d8, e8, n)
    Sv, sv, dv, ev = build_matrix(lfc, coh, gs7, use_alternate=True)
    sec['S3_v1_1_dual_library'], _ = analysis(Sv, ref7, L7, b7, sv, dv, ev, n)
    sec['S4_unadjusted'], _ = analysis(S, ref7, L7, np.zeros_like(b7), sids, dids, excl, n)
    res['secondary_holm_family'] = finalize_family(sec)
    if Dpoint is not None:
        def run_stab():
            meta, eff, _t = estimators.load_dev()
            deltas = estimators.format_pairs(meta, eff)
            gr = json.loads((root / 'data/broad_stability_groupings.json').read_text())
            groupings = dict(gr['groupings'])
            groupings.update({f'lineage_if_ACH-003052={k}': v for k, v in gr['unknown_lineage_scenarios'].items()})
            return stability(np.asarray(Dpoint, dtype=float), deltas, gb7, b7, groupings, primary_class(gb7, root))
        res['stability_not_decision'] = _safe(run_stab)
        buf = io.StringIO(); w = csv.writer(buf)
        w.writerow(['gene_broad', 'gene_sanger', 'D_g', 'L_g', 'AdherentMean', 'base_strength'])
        for i in range(len(gb7)):
            w.writerow([gb7[i], gs7[i], repr(float(Dpoint[i])), repr(float(L7[i])), repr(float(ref7[i])), repr(float(b7[i]))])
        commit_bytes(DGTABLE, buf.getvalue().encode())
    else:
        res['stability_not_decision'] = {'skipped': 'primary invalid; no point displacement profile'}
    res['decision'] = prim.get('decision', 'INCONCLUSIVE')
    res['claim_language'] = json.loads((root / 'lock_s/scientific_protocol_v1.json').read_text())['decision_claim_map'][res['decision']]
    res['wall_s'] = time.monotonic() - t0
    commit_bytes(RESULT, json.dumps(res, indent=1, default=_json).encode())
    print(json.dumps({'decision': res['decision'], 'estimate': prim.get('estimate'), 'ci': prim.get('ci95_donor_percentile')}))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except LockError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(3)
