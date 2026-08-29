# CMotive language examples verification report

PASS for the updated debug-symbol example pass:

- Manifest check: 150 examples present.
- New example `examples/150_debug_symbols_options.CMOT`: compile/link/run PASS.
- `make debug-symbols` equivalent: PASS using `-g3 -O2`, generated `.cmotive.debug.json` and `_cmot_debugsymbols.syms`.
- The generated `.syms` output contains the expected 64-bit offset column, `StartPackage__ExampleDebugSymbol__Add`, and the full CMotive prototype.

The previous 149 examples were retained from the already verified examples archive; only the debug-symbol example and runner target were added in this pass.


Object standard library refresh: added examples 151-153 and verified object-method APIs for STL containers, algorithms, and IO streams.

## Object standard library revalidation

Examples 151-153 compile/link/run successfully against the refreshed object-oriented `Sys::STL`, `Sys::Algorithms`, and `Sys::IO` APIs.

Result: PASS.


Added examples 154-158 for Sys::Filesystem, Sys::Net, Sys::Thread MicroSleep/NanoSleep, Sys::String, and Sys::Wide object/class standard library APIs. Manifest now includes 158 examples.
