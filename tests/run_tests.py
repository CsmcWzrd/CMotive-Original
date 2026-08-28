#!/usr/bin/env python3
import argparse, os, subprocess, sys
from pathlib import Path

def run(cmd, allow_stdout=True):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode:
        print('FAILED:', ' '.join(map(str, cmd)))
        if p.stdout: print(p.stdout)
        if p.stderr: print(p.stderr)
    return p.returncode == 0

def run_expect_code(cmd, expected):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != expected:
        print('FAILED:', ' '.join(map(str, cmd)), 'expected', expected, 'got', p.returncode)
        if p.stdout: print(p.stdout)
        if p.stderr: print(p.stderr)
        return False
    if p.stderr:
        print('FAILED: stderr produced by', ' '.join(map(str, cmd)))
        print(p.stderr)
        return False
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--bin', default='build/bin')
    ns = ap.parse_args()
    b = Path(ns.bin)
    exe_suffix = '.exe' if os.name == 'nt' else ''
    ok = True
    ok &= run([str(b/'cmotive'), '--version'])
    ok &= run([str(b/'cmotive'), '-c', 'tests/conformance/basic.CMOT', '-o', 'build/basic.o'])
    ok &= run([str(b/'cmotive'), 'tests/conformance/basic.CMOT', '-o', 'build/basic' + exe_suffix])
    ok &= run_expect_code(['build/basic' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), '--target-arch', 'arm64', '--emit-c', 'tests/abi/platform.CMOT', '-o', 'build/platform.c'])
    ok &= run([str(b/'cmotivepp'), 'tests/conformance/include.CMOT', '-I', 'tests/conformance', '-o', 'build/include.pp.CMOT'])
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_formal_main.CMOT', '-I', 'tests/conformance', '-o', 'build/formal' + exe_suffix])
    ok &= run_expect_code(['build/formal' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_control_flow.CMTV', '-o', 'build/control' + exe_suffix])
    ok &= run_expect_code(['build/control' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_classes_main.CMOT', '-I', 'tests/conformance', '-o', 'build/classes' + exe_suffix])
    ok &= run_expect_code(['build/classes' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_preprocessor.CMOT', '-o', 'build/preprocessor' + exe_suffix])
    ok &= run_expect_code(['build/preprocessor' + exe_suffix], 0)
    print('CMotive tests:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
