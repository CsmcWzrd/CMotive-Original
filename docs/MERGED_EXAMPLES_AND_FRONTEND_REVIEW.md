# Merged examples and frontend review

This package merges the former standalone CMotive language examples into the main CMotive source tree under `examples/`.

## Layout

```text
CMotive/
  examples/
    001_hello_world.CMOT
    ...
    158_object_wide_strings.CMOT
    frontend_hello.CMOT
    frontend_classes.CMOT
    frontend_control_flow.CMTV
    headers/
    packages/
    manifests/examples.jsonl
    MANIFEST.txt
  makefile.examples.linux
  makefile.examples.mac
  makefile.examples.windows
```

## Source cleanup

All `.CMOT`, `.CMTV`, `.HMOT`, and `.HMTV` files in the package were scanned for `var`-prefixed declarations. Stale declarations were converted to CMotive typed declarations such as:

```text
value : I32 = 0;
slot : I32 = 0;
```

The examples were also refreshed to avoid stale `Virtual` / `virtual` and `operator` keyword usage in source files. CMotive source now uses `Overridable` and `Operation` where those constructs are represented.

## Verification performed

The following checks were run from the main source tree:

```sh
python3 -m py_compile src/cmotive/*.py tools/*.py tests/run_tests.py
make -f Makefile.linux clean all test
python3 tests/run_tests.py --bin build/bin --full
python3 tools/verify_cmotive_files.py --jobs 4 --timeout 80
make -f makefile.examples.linux check TIMEOUT=10
make -f makefile.examples.linux debug-symbols
```

Results:

- `CMotive tests: PASS`
- Full conformance suite: `PASS`
- All-source verification: `228` CMotive files preprocessed and compiled to native objects with no compiler stderr.
- Merged example verification: `161` examples preprocessed, object-built, compiled, linked, executed, exited with expected status, and produced no stderr.
- Debug symbol example: `PASS`.

## Makefiles for examples

The root example makefiles are:

- `makefile.examples.linux`
- `makefile.examples.mac`
- `makefile.examples.windows`

Primary targets:

```sh
make -f makefile.examples.linux check
make -f makefile.examples.linux preprocess
make -f makefile.examples.linux objects
make -f makefile.examples.linux run
make -f makefile.examples.linux verify-all
make -f makefile.examples.linux debug-symbols
```

`verify-all` checks every `.CMOT`, `.CMTV`, `.HMOT`, and `.HMTV` file in the package. `check` compiles and runs all examples listed in `examples/manifests/examples.jsonl`.
