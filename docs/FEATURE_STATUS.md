# Feature Status

See `docs/CMOTIVE_REQUIREMENTS_VERIFICATION.md` for the detailed requirement-by-requirement verification matrix.

# Feature Status

| Area | Status | Notes |
|---|---:|---|
| Lexer | Implemented scaffold | Tokenization for language constructs. |
| Parser | Implemented scaffold | Classes, functions, control flow. |
| AST | Implemented scaffold | Program/function/class/statements. |
| Semantic analysis | Implemented scaffold | Duplicate and inheritance validation. |
| Native codegen | Implemented scaffold | C lowering plus platform toolchain. |
| ARM64 | Scaffold | `--target-arch arm64/aarch64`; macOS `-arch`. |
| x86_64 | Scaffold | Default native toolchain path. |
| macOS ARM64 linker fixes | Scaffold | clang/cc `-arch arm64` path. |
| Classes/methods | Scaffold | Struct lowering and method mangling. |
| Single inheritance | Scaffold | Base-class validation. |
| Constructors/destructors | Scaffold | Constructor named as class; destructor convention. |
| New/Delete | Runtime scaffold | `CMotive_New`/`CMotive_Delete`. |
| Control flow | Implemented scaffold | `if`, `else`, `while`, `return`. |
| Virtual dispatch | Scaffold | VTable ABI placeholders. |
| Templates | Implemented in bootstrap compiler | Concrete class/function templates instantiate on use, with `Template__Arg` native symbols. |
| Exceptions | Implemented in bootstrap compiler | `Try`/`Catch`/`Catchall`/`Throw` lower to `setjmp`/`longjmp` frames with unhandled-exception exit code 70. |
| Package/Plugin system | Implemented in preprocessor | `Plugin Foo::Bar` resolves and materializes `.HMOT/.HMTV/.CMOT/.CMTV` package files before parsing. |
| Separate compilation | Implemented scaffold | `-c`, object input link path. |
| Sys::Stdio/File/Filesystem/Logging/Thread | API scaffold | Headers under `lib/Sys`. |
| Sys::Net | Placeholder | Reserved network namespace. |
| Sys::Exception | API scaffold | Exception class and throwText package surface. |
