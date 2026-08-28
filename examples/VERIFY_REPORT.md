# CMotive language examples verification report

PASS for the updated debug-symbol example pass:

- Manifest check: 150 examples present.
- New example `examples/150_debug_symbols_options.CMOT`: compile/link/run PASS.
- `make debug-symbols` equivalent: PASS using `-g3 -O2`, generated `.cmotive.debug.json` and `_cmot_debugsymbols.syms`.
- The generated `.syms` output contains the expected 64-bit offset column, `StartPackage__ExampleDebugSymbol__Add`, and the full CMotive prototype.

The previous 149 examples were retained from the already verified examples archive; only the debug-symbol example and runner target were added in this pass.
