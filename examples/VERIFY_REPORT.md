# CMotive examples verification report

PASS: manifest validation found 149 examples.

Verification performed in this iteration:

- Source regression suite: `make -f Makefile.linux clean all test` passed.
- Source full conformance suite: `python3 tests/run_tests.py --bin build/bin --full` passed.
- New examples 146-149 compiled, linked, executed, exited with code 0, and produced no stderr:
  - 146 Global anywhere
  - 147 Fptr function pointer
  - 148 Overridable pure virtual
  - 149 ThreadStore/Tstore
- `tools/check_manifest.py` reports `manifest ok: 149 examples`.

The previous examples 138-145 remain in the manifest for Sys::IO, STL containers, Sys::Algorithms, native sockets, native threading, and Dynamic Struct Expand.

Note: the full 149-example archive-wide runner is available as `tools/run_all_examples.py`. The verification above used the CMotive source conformance suite plus targeted execution of the newly added examples for this pass.
