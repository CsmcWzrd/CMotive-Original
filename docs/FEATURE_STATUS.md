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
| Classes/methods | Implemented in bootstrap compiler | Classes lower to concrete C structs; methods lower to `Package__Class__Method(this, ...)` symbols with `StartPackage` as the default package; object and pointer method calls are rewritten to mangled calls. |
| Single inheritance | Implemented in bootstrap compiler | Semantic analysis validates one base class, verifies the base exists, detects cycles, and codegen embeds the base struct as the first member. |
| Constructors/destructors | Implemented in bootstrap compiler | Constructors named as the class and `~Class` destructors lower to `Package__Class__ctor[_N]` and `Package__Class__dtor`; derived constructors/destructors chain to the base. |
| New/Delete | Implemented in bootstrap compiler/runtime | `New Class(...)` routes through package-qualified `Package__Class__new[_N]` helpers backed by `CMotive_New`; `Delete obj` routes through package-qualified delete helpers backed by `CMotive_Delete`. |
| Control flow | Implemented scaffold | `if`, `else`, `while`, `return`. |
| Virtual dispatch | Scaffold | VTable ABI placeholders. |
| Templates | Implemented in bootstrap compiler | Concrete class/function templates instantiate on use, with `Template__Arg` native symbols. |
| Exceptions | Implemented in bootstrap compiler | `Try`/`Catch`/`Catchall`/`Throw` lower to `setjmp`/`longjmp` frames with unhandled-exception exit code 70. |
| Package/Plugin system | Implemented in preprocessor | `Plugin Foo::Bar` resolves and materializes `.HMOT/.HMTV/.CMOT/.CMTV` package files before parsing. |
| Separate compilation | Implemented scaffold | `-c`, object input link path. |
| Sys::Stdio/File/Filesystem/Logging/Thread | API scaffold | Headers under `lib/Sys`. |
| Sys::Net | Placeholder | Reserved network namespace. |
| Sys::Exception | API scaffold | Exception class and throwText package surface. |
