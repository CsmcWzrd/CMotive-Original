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
| Templates | Scaffold | Reserved frontend/package area. |
| Exceptions | Scaffold | `CMotive_Throw` boundary. |
| Package/Plugin system | Scaffold | Loader/manager source placeholder. |
| Separate compilation | Implemented scaffold | `-c`, object input link path. |
| Sys::Stdio/File/Filesystem/Logging/Thread | API scaffold | Headers under `lib/Sys`. |
| Sys::Net | Placeholder | Reserved network namespace. |
