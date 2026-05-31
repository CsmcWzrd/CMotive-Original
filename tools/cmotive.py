#!/usr/bin/env python3
import argparse, os, platform, shutil, subprocess, sys, tempfile
from pathlib import Path
HERE=Path(__file__).resolve()
ROOT=None
for cand in [HERE.parent, *HERE.parents]:
    if (cand/'src'/'cmotive').exists():
        ROOT=cand; break
if ROOT is None:
    # installed/copied binary: try current working directory for source-tree execution
    cwd=Path.cwd()
    ROOT=cwd if (cwd/'src'/'cmotive').exists() else HERE.parent
sys.path.insert(0,str(ROOT/'src'))
from cmotive.compiler import CompilerPipeline
VALID_SRC={'.CMOT','.CMTV','.cmot','.cmtv'}
def choose_cc():
    if os.environ.get('CMOTIVE_CC'): return os.environ['CMOTIVE_CC']
    if platform.system()=='Windows': return shutil.which('clang') or shutil.which('gcc') or shutil.which('cl') or 'cc'
    return shutil.which('cc') or shutil.which('clang') or shutil.which('gcc') or 'cc'
def main(argv=None):
    ap=argparse.ArgumentParser(prog='cmotive')
    ap.add_argument('--version',action='store_true'); ap.add_argument('-c',dest='compile_only',action='store_true'); ap.add_argument('-o',dest='output')
    ap.add_argument('-I',dest='includes',action='append',default=[]); ap.add_argument('-L',dest='libdirs',action='append',default=[]); ap.add_argument('-l',dest='libs',action='append',default=[])
    ap.add_argument('--target-arch',choices=['x86_64','arm64','aarch64']); ap.add_argument('--emit-c',action='store_true'); ap.add_argument('--print-linker',action='store_true'); ap.add_argument('inputs',nargs='*')
    ns=ap.parse_args(argv)
    if ns.version: print('CMotive compiler 0.1.0-rc-scaffold'); return 0
    cc=choose_cc()
    if ns.print_linker: print(os.environ.get('CMOTIVE_LD') or cc); return 0
    if not ns.inputs: ap.error('no input files')
    srcs=[Path(p) for p in ns.inputs if Path(p).suffix in VALID_SRC]; objs=[Path(p) for p in ns.inputs if Path(p).suffix.lower() in {'.o','.obj'}]
    if not srcs and not objs: ap.error('no CMotive source or object input files')
    out=Path(ns.output) if ns.output else Path('a.out' if not ns.compile_only else srcs[0].stem+'.o'); out.parent.mkdir(parents=True,exist_ok=True)
    pipe=CompilerPipeline(ns.includes, ns.target_arch or platform.machine())
    with tempfile.TemporaryDirectory(prefix='cmotive-') as td:
        td=Path(td); made=[]
        for s in srcs:
            unit=pipe.compile_to_c(s); c=td/(s.stem+'.c'); c.write_text(unit.c_source,encoding='utf-8')
            if ns.emit_c:
                target=out if len(srcs)==1 else out.parent/(s.stem+'.c'); target.write_text(unit.c_source,encoding='utf-8'); continue
            obj=out if ns.compile_only and len(srcs)==1 else td/(s.stem+('.obj' if platform.system()=='Windows' else '.o'))
            cmd=[cc]
            if platform.system()=='Darwin' and ns.target_arch: cmd+=['-arch',ns.target_arch]
            cmd+=['-c',str(c),'-o',str(obj)]
            r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            if r.returncode: sys.stderr.write(r.stdout+r.stderr); return r.returncode
            made.append(obj)
        if ns.emit_c or ns.compile_only: return 0
        cmd=[os.environ.get('CMOTIVE_LD') or cc]
        if platform.system()=='Darwin' and ns.target_arch: cmd+=['-arch',ns.target_arch]
        cmd += [str(p) for p in made+objs]
        cmd += ['-L'+d for d in ns.libdirs] + ['-l'+l for l in ns.libs] + ['-o',str(out)]
        r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        if r.returncode: sys.stderr.write(r.stdout+r.stderr); return r.returncode
    return 0
if __name__=='__main__': raise SystemExit(main())
