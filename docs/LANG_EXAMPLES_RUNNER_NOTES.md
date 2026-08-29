# Runner notes

`tools/example_build.py` is the source of truth for verification. It reads `manifests/examples.jsonl`, compiles each example with the CMotive compiler, executes it, requires the expected exit code, rejects stderr, and checks that stdout contains the per-example verification marker.

This prevents a false pass where a parser might accidentally lower a source file to the default empty `main`.

Current manifest count: 137 examples.


- `examples/150_debug_symbols_options.CMOT`: exercises source-level debug symbol metadata with `-g3 -O2` through the CMotive source test suite and can be used manually with `CMotiveSymsToDebugFile`.
