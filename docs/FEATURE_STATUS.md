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
| x86_64 | Implemented scaffold | Canonical `x86_64` target alias, emitted target marker, and `-m64`/Darwin `-arch x86_64` native toolchain path. |
| macOS ARM64 linker fixes | Scaffold | clang/cc `-arch arm64` path. |
| Classes/methods | Implemented in bootstrap compiler | Classes lower to concrete C structs; methods lower to `Package__Class__Method(this, ...)` symbols with `StartPackage` as the default package; object and pointer method calls are rewritten to mangled calls. |
| Single inheritance | Implemented in bootstrap compiler | Semantic analysis validates one base class, verifies the base exists, detects cycles, and codegen embeds the base struct as the first member. |
| Constructors/destructors | Implemented in bootstrap compiler | Constructors named as the class and `~Class` destructors lower to `Package__Class__ctor__<Type...>` and `Package__Class__dtor`; derived constructors/destructors chain to the base and constructor overloads resolve by inferred argument type. |
| New/Delete | Implemented in bootstrap compiler/runtime | `New Class(...)` routes through package-qualified typed `Package__Class__new__<Type...>` helpers backed by `CMotive_New`; `Delete obj` routes through package-qualified delete helpers backed by `CMotive_Delete`. |
| Control flow | Implemented scaffold | `if`, `else`, `while`, `return`. |
| Virtual dispatch | Implemented in bootstrap compiler | `Overridable` methods populate vtable slots; receiver method calls through base pointers lower to runtime vtable dispatch. |
| Templates | Implemented in bootstrap compiler | Concrete class/function templates instantiate on use, with `Template__Arg` native symbols. |
| Exceptions | Implemented in bootstrap compiler | `Try`/`Catch`/`Catchall`/`Throw` lower to `setjmp`/`longjmp`; protected stack objects register destructor cleanup frames that run during unwinding. |
| Package/Plugin system | Implemented in preprocessor | `Plugin Foo::Bar` resolves and materializes `.HMOT/.HMTV/.CMOT/.CMTV` package files before parsing. |
| Separate compilation | Implemented scaffold | `-c`, object input link path. |
| Sys::Stdio/File/Filesystem/Logging/Thread | Expanded runtime-backed API surface | Headers under `lib/Sys`; generated C embeds helper implementations and `runtime.c` mirrors them. |
| Sys::Net | Reserved runtime-backed placeholder | TCP/UDP/raw socket API surface exists with deterministic placeholder helpers. |
| Sys::Exception | Expanded API surface | `Exception`, `throwText`, `throwCode`, and `lastCode`; integrates with compiler exception lowering. |

| Keyword/type synonyms | Implemented | `Int16`, `Int32`, `Int`, `Uint16`, `Uint32`, and `Uint` are accepted as aliases for `I16`, `I32`, `I64`, `U16`, `U32`, and `U64`. |


| Sys::Locks | Implemented runtime-backed surface | Mutex, recursive mutex, RW lock, spin-lock facade, condition variable, semaphore, and free wrapper APIs. |
| Sys::Math | Implemented runtime-backed surface | Broad Linux/libm-style math package backed by generated C helpers and `-lm`. |
| Sys::String | Implemented runtime-backed surface | String/memory/conversion/case helpers plus `str_parse` table parser. |
| Sys::Wide | Implemented runtime-backed surface | Char16/Char32 length/compare/copy/concat/find helpers. |

| Target/Hit dispatch | Implemented in bootstrap compiler | `Hit Sender:Id` registers a function/method handler and `Target Sender:Object:args:Id` lowers to deterministic direct dispatch, with unresolved routes failing through `CMotive_UnresolvedTarget`. |
