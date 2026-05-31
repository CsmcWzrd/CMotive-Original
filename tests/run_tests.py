#!/usr/bin/env python3
import argparse, subprocess
from pathlib import Path
def run(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode: print('FAILED:', ' '.join(map(str,cmd)), p.stdout, p.stderr)
    return p.returncode==0
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--bin',default='build/bin'); ns=ap.parse_args(); b=Path(ns.bin); ok=True
    ok &= run([str(b/'cmotive'),'--version'])
    ok &= run([str(b/'cmotive'),'-c','tests/conformance/basic.CMOT','-o','build/basic.o'])
    ok &= run([str(b/'cmotive'),'tests/conformance/basic.CMOT','-o','build/basic'])
    ok &= run([str(b/'cmotive'),'--target-arch','arm64','--emit-c','tests/abi/platform.CMOT','-o','build/platform.c'])
    ok &= run([str(b/'cmotivepp'),'tests/conformance/include.CMOT','-I','tests/conformance','-o','build/include.pp.CMOT'])
    print('CMotive tests:', 'PASS' if ok else 'FAIL'); return 0 if ok else 1
if __name__=='__main__': raise SystemExit(main())
