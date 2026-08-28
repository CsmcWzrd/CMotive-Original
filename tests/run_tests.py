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

def run_expect_failure(cmd):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode == 0:
        print('FAILED:', ' '.join(map(str, cmd)), 'expected failure but got success')
        if p.stdout: print(p.stdout)
        if p.stderr: print(p.stderr)
        return False
    return True

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

    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_template_instantiation.CMOT', '-o', 'build/template' + exe_suffix])
    ok &= run_expect_code(['build/template' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_exception_unwinding.CMOT', '-o', 'build/exception' + exe_suffix])
    ok &= run_expect_code(['build/exception' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_package_loading.CMOT', '-I', 'tests/conformance', '-o', 'build/package' + exe_suffix])
    ok &= run_expect_code(['build/package' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_sys_stl_template.CMOT', '-o', 'build/sys_stl_template' + exe_suffix])
    ok &= run_expect_code(['build/sys_stl_template' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_class_lifecycle.CMOT', '-o', 'build/class_lifecycle' + exe_suffix])
    ok &= run_expect_code(['build/class_lifecycle' + exe_suffix], 0)

    ok &= run([str(b/'cmotive'), '--emit-c', 'tests/conformance/cmotive_package_method_mangling.CMOT', '-o', 'build/package_method_mangling.c'])
    if ok:
        sym_c = Path('build/package_method_mangling.c').read_text(encoding='utf-8')
        needed = ['StartPackage__DefaultMangle__Ping', 'CustomPkg__CustomMangle__Ping']
        if not all(x in sym_c for x in needed):
            print('FAILED: package-qualified method symbols missing from generated C')
            ok = False
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_package_method_mangling.CMOT', '-o', 'build/package_method_mangling' + exe_suffix])
    ok &= run_expect_code(['build/package_method_mangling' + exe_suffix], 0)

    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_keyword_synonyms.CMOT', '-o', 'build/keyword_synonyms' + exe_suffix])
    ok &= run_expect_code(['build/keyword_synonyms' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_virtual_dispatch.CMOT', '-o', 'build/virtual_dispatch' + exe_suffix])
    ok &= run_expect_code(['build/virtual_dispatch' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_exception_destructor_unwind.CMOT', '-o', 'build/exception_destructor_unwind' + exe_suffix])
    ok &= run_expect_code(['build/exception_destructor_unwind' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_constructor_type_overload.CMOT', '-o', 'build/constructor_type_overload' + exe_suffix])
    ok &= run_expect_code(['build/constructor_type_overload' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), '--target-arch', 'x86_64', '--emit-c', 'tests/abi/platform.CMOT', '-o', 'build/platform_x86_64.c'])
    if ok and 'target-arch: x86_64' not in Path('build/platform_x86_64.c').read_text(encoding='utf-8'):
        print('FAILED: x86_64 target marker missing from generated C')
        ok = False


    ok &= run([str(b/'cmotive'), '--emit-c', 'tests/conformance/cmotive_target_hit_direct.CMOT', '-o', 'build/target_hit_direct.c'])
    if ok:
        ctext = Path('build/target_hit_direct.c').read_text(encoding='utf-8')
        if 'StartPackage__PrintTarget(1, 2);' not in ctext:
            print('FAILED: Target/Hit direct dispatch call missing from generated C')
            ok = False
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_target_hit_direct.CMOT', '-o', 'build/target_hit_direct' + exe_suffix])
    ok &= run_expect_code(['build/target_hit_direct' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), '--emit-c', 'tests/conformance/cmotive_target_hit_object.CMOT', '-o', 'build/target_hit_object.c'])
    if ok:
        ctext = Path('build/target_hit_object.c').read_text(encoding='utf-8')
        needed_target = ['StartPackage__TargetReceiver__Add(&obj1, 3, 4);', 'StartPackage__TargetReceiver__AddSender(&obj1, 5, 6);']
        if not all(x in ctext for x in needed_target):
            print('FAILED: Target/Hit object dispatch calls missing from generated C')
            ok = False
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_target_hit_object.CMOT', '-o', 'build/target_hit_object' + exe_suffix])
    ok &= run_expect_code(['build/target_hit_object' + exe_suffix], 0)
    ok &= run([str(b/'cmotive'), '--emit-c', 'tests/conformance/cmotive_target_hit_sender.CMOT', '-o', 'build/target_hit_sender.c'])
    if ok:
        ctext = Path('build/target_hit_sender.c').read_text(encoding='utf-8')
        if 'StartPackage__SenderTarget(8);' not in ctext:
            print('FAILED: Target/Hit sender-qualified dispatch call missing from generated C')
            ok = False
    ok &= run([str(b/'cmotive'), 'tests/conformance/cmotive_target_hit_sender.CMOT', '-o', 'build/target_hit_sender' + exe_suffix])
    ok &= run_expect_code(['build/target_hit_sender' + exe_suffix], 0)

    ok &= run_expect_failure([str(b/'cmotive'), 'tests/conformance/cmotive_invalid_base.CMOT', '-o', 'build/invalid_base' + exe_suffix])
    print('CMotive tests:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1

if __name__ == '__main__':
    raise SystemExit(main())
