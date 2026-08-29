#!/usr/bin/env python3
from __future__ import annotations
import argparse, concurrent.futures, json, os, subprocess, sys
from pathlib import Path

VALID_EXTS = {'.cmot','.cmtv','.hmot','.hmtv'}
EXCLUDE_DIRS = {'build','dist','.git','__pycache__'}


def root_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def source_files(root: Path) -> list[Path]:
    files = []
    for p in root.rglob('*'):
        if not p.is_file() or p.suffix.lower() not in VALID_EXTS:
            continue
        parts = set(p.relative_to(root).parts)
        if parts & EXCLUDE_DIRS:
            continue
        files.append(p)
    return sorted(files, key=lambda x: str(x).lower())


def cmd_prefix(tool: Path) -> list[str]:
    return [sys.executable, str(tool)] if tool.suffix == '.py' else [str(tool)]


def include_args(root: Path) -> list[str]:
    return ['-I', str(root/'lib'), '-I', str(root/'examples'), '-I', str(root/'examples'/'headers'), '-I', str(root/'examples'/'packages'), '-I', str(root/'tests'/'conformance')]


def run(cmd: list[str], timeout: int):
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout)


def verify_one(root: Path, rel: str, timeout: int) -> dict:
    pp = root/'tools'/'cmotivepp.py'
    cc = root/'tools'/'cmotive.py'
    src = root/rel
    out_base = root/'build'/'verify_all_cmot'/'out'/rel
    pp_out = out_base.with_suffix(out_base.suffix + '.pp')
    obj_out = (root/'build'/'verify_all_cmot'/'obj'/rel).with_suffix('.obj' if os.name == 'nt' else '.o')
    pp_out.parent.mkdir(parents=True, exist_ok=True)
    obj_out.parent.mkdir(parents=True, exist_ok=True)
    args = include_args(root)
    result = {'file': rel, 'preprocess': 'not-run', 'compile': 'not-run'}
    try:
        p = run(cmd_prefix(pp) + args + [str(src), '-o', str(pp_out)], timeout)
        if p.returncode != 0 or p.stderr:
            result.update({'preprocess': 'fail', 'phase': 'preprocess', 'code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
            return result
        result['preprocess'] = 'pass'
        p = run(cmd_prefix(cc) + args + ['-c', str(src), '-o', str(obj_out)], timeout)
        if p.returncode != 0 or p.stderr:
            result.update({'compile': 'fail', 'phase': 'compile', 'code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
            return result
        result['compile'] = 'pass'
        return result
    except subprocess.TimeoutExpired:
        result.update({'phase': 'timeout', 'code': 'timeout', 'stdout': '', 'stderr': ''})
        return result


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=max(1, min(4, (os.cpu_count() or 2))))
    ap.add_argument('--timeout', type=int, default=60)
    ap.add_argument('--report', default='VERIFY_ALL_CMOTIVE_FILES.md')
    ns = ap.parse_args(argv)
    root = root_dir()
    files = [str(p.relative_to(root)) for p in source_files(root)]
    failures = []
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=ns.jobs) as ex:
        futs = {ex.submit(verify_one, root, rel, ns.timeout): rel for rel in files}
        done = 0
        for fut in concurrent.futures.as_completed(futs):
            res = fut.result()
            results.append(res)
            done += 1
            if res.get('preprocess') != 'pass' or res.get('compile') != 'pass':
                failures.append(res)
            if done % 25 == 0 or done == len(files):
                print(f'verified: {done}/{len(files)}')
    results.sort(key=lambda r: r['file'].lower())
    failures.sort(key=lambda r: r['file'].lower())
    report = root/ns.report
    if failures:
        report.write_text('# CMotive all source verification\n\nFAILED\n\n' + f'- Files checked: {len(files)}\n- Failures: {len(failures)}\n\n```json\n' + json.dumps(failures, indent=2) + '\n```\n', encoding='utf-8')
        print(f'FAILED: {len(failures)} of {len(files)} files. See {report}', file=sys.stderr)
        return 1
    report.write_text('# CMotive all source verification\n\nPASS\n\n' + f'- Files checked: {len(files)}\n- Every `.CMOT`, `.CMTV`, `.HMOT`, and `.HMTV` file was preprocessed with `cmotivepp` and compiled to an object with `cmotive -c`.\n- No compiler stderr was produced.\n', encoding='utf-8')
    print(f'PASS: {len(files)} CMotive files preprocessed and compiled')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
