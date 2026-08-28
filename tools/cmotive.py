#!/usr/bin/env python3
import argparse, os, platform, shutil, subprocess, sys, tempfile
from pathlib import Path

def find_root(start):
    for base in [start] + list(start.parents):
        if (base / 'src' / 'cmotive').exists():
            return base
        if base.name == 'bin' and (base.parent.parent / 'src' / 'cmotive').exists():
            return base.parent.parent
    return start.parents[1]
ROOT = find_root(Path(__file__).resolve())
sys.path.insert(0, str(ROOT / 'src'))
from cmotive.compiler import CompilerPipeline

VALID_SRC = {'.CMOT','.CMTV','.HMOT','.HMTV','.cmot','.cmtv','.hmot','.hmtv'}
OBJ_EXTS = {'.o','.obj'}
ARCH_ALIASES = {
    'x86':'x86','i386':'x86','i686':'x86',
    'x64':'x86_64','x86_64':'x86_64','amd64':'x86_64',
    'arm':'arm','armv7':'arm','arm64':'arm64','aarch64':'arm64'
}

def choose_cc():
    if os.environ.get('CMOTIVE_CC'):
        return os.environ['CMOTIVE_CC']
    if platform.system() == 'Windows':
        return shutil.which('clang') or shutil.which('gcc') or shutil.which('cl') or 'cc'
    return shutil.which('cc') or shutil.which('clang') or shutil.which('gcc') or 'cc'

def choose_ld(cc):
    return os.environ.get('CMOTIVE_LD') or cc

def compiler_is_msvc(cc):
    return Path(str(cc).split()[0]).name.lower() in {'cl','cl.exe'}

def run_cmd(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode:
        sys.stderr.write(p.stdout + p.stderr)
    return p.returncode

def compile_c(cc, c_path, obj_path, target_arch=None):
    obj_path.parent.mkdir(parents=True, exist_ok=True)
    if compiler_is_msvc(cc):
        return [cc, '/nologo', '/c', str(c_path), '/Fo' + str(obj_path)]
    cmd = [cc]
    if platform.system() == 'Darwin' and target_arch:
        cmd += ['-arch', target_arch]
    # Strip-compatible native object output.  Debug info is intentionally kept in
    # a normal toolchain format so strip/llvm-strip can operate on the result.
    cmd += ['-g', '-c', str(c_path), '-o', str(obj_path)]
    return cmd

def link_objects(ld, objs, out, libdirs, libs, target_arch=None):
    out.parent.mkdir(parents=True, exist_ok=True)
    if compiler_is_msvc(ld):
        return [ld, '/nologo'] + [str(o) for o in objs] + ['/Fe:' + str(out)]
    cmd = [ld]
    if platform.system() == 'Darwin' and target_arch:
        cmd += ['-arch', target_arch]
    cmd += [str(p) for p in objs]
    cmd += ['-L' + d for d in libdirs] + ['-l' + l for l in libs] + ['-o', str(out)]
    return cmd

def main(argv=None):
    ap = argparse.ArgumentParser(prog='cmotive')
    ap.add_argument('--version', action='store_true')
    ap.add_argument('-c', dest='compile_only', action='store_true')
    ap.add_argument('-o', dest='output')
    ap.add_argument('-I', dest='includes', action='append', default=[])
    ap.add_argument('-L', dest='libdirs', action='append', default=[])
    ap.add_argument('-l', dest='libs', action='append', default=[])
    ap.add_argument('--target-arch', choices=sorted(ARCH_ALIASES.keys()))
    ap.add_argument('--emit-c', action='store_true')
    ap.add_argument('--keep-c', action='store_true')
    ap.add_argument('--print-linker', action='store_true')
    ap.add_argument('inputs', nargs='*')
    ns = ap.parse_args(argv)
    if ns.version:
        print('CMotive compiler 0.2.2-rc1')
        return 0
    cc = choose_cc(); ld = choose_ld(cc)
    if ns.print_linker:
        print(ld)
        return 0
    if not ns.inputs:
        ap.error('no input files')
    srcs = [Path(p) for p in ns.inputs if Path(p).suffix in VALID_SRC]
    objs = [Path(p) for p in ns.inputs if Path(p).suffix.lower() in OBJ_EXTS]
    if not srcs and not objs:
        ap.error('no CMotive source/header or object input files')
    target_arch = ARCH_ALIASES.get(ns.target_arch or '', ns.target_arch) or platform.machine()
    out = Path(ns.output) if ns.output else Path('a.out' if not ns.compile_only else (srcs[0].stem + ('.obj' if platform.system() == 'Windows' else '.o')))
    out.parent.mkdir(parents=True, exist_ok=True)
    pipe = CompilerPipeline(ns.includes, target_arch)
    temp_ctx = tempfile.TemporaryDirectory(prefix='cmotive-')
    with temp_ctx as td_s:
        td = Path(td_s)
        made = []
        for s in srcs:
            unit = pipe.compile_to_c(s)
            c = td / (s.stem + '.c')
            c.write_text(unit.c_source, encoding='utf-8')
            if ns.keep_c:
                keep = out.parent / (s.stem + '.c') if not ns.emit_c else out
                keep.write_text(unit.c_source, encoding='utf-8')
            if ns.emit_c:
                target = out if len(srcs) == 1 else out.parent / (s.stem + '.c')
                target.write_text(unit.c_source, encoding='utf-8')
                continue
            obj = out if ns.compile_only and len(srcs) == 1 else td / (s.stem + ('.obj' if platform.system() == 'Windows' else '.o'))
            rc = run_cmd(compile_c(cc, c, obj, target_arch))
            if rc:
                return rc
            made.append(obj)
        if ns.emit_c or ns.compile_only:
            return 0
        rc = run_cmd(link_objects(ld, made + objs, out, ns.libdirs, ns.libs, target_arch))
        if rc:
            return rc
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
