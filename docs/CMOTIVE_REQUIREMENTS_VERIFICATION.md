# CMotive Requirements Verification

This report records the implementation pass against the supplied `CMotive.md`
language requirements.

## Implemented in this iteration

| Requirement area | Status | Updated implementation |
|---|---:|---|
| File extensions `.CMOT`, `.CMTV`, `.HMOT`, `.HMTV`, any case | Implemented | `tools/cmotive.py` accepts source and header extensions in upper/lower case. |
| Capitalized CMotive keywords | Implemented | `src/cmotive/lexer.py` contains the formal CMotive keyword table and compatibility aliases. |
| Formal line-oriented function declarations | Implemented | `src/cmotive/parser.py` parses `ReturnType`, function name, parameter lines, `()`, and body. |
| Old bootstrap `func`/`var` compatibility | Preserved | Parser still accepts legacy tests/examples. |
| Classes, visibility blocks, constructors, destructors | Implemented in bootstrap compiler | Parser accepts `Class`, visibility blocks, constructors/destructors, nested classes, and methods; codegen lowers classes to C structs and methods to package-qualified mangled `Package__Class__Method(this, ...)` functions, using `StartPackage` when no package is declared. |
| Single inheritance | Implemented in bootstrap compiler | Semantic analysis enforces one base, validates that the base exists, detects inheritance cycles, and codegen embeds the base struct as the first field for ABI-compatible upcast layout. |
| Bit member specification | Implemented scaffold | Parser records bit fields; codegen lowers them to C bit-field structs. |
| `Blend`/`Enum` | Parse scaffold | Parser preserves declarations as scaffold metadata without breaking compilation. |
| `Template` and `Type` | Implemented in bootstrap compiler | Parser records template class/function bodies; codegen instantiates concrete class and function templates when `Name<T...>` is used. |
| `Try`/`Catch`/`Catchall`/`Throw` | Implemented in bootstrap compiler | Codegen emits stack-local exception frames with `setjmp`/`longjmp`; caught exceptions continue in matching `Catch`/`Catchall`, uncaught exceptions exit with code 70. |
| Control flow | Implemented | `If`/`Elif`/`Else`, `While`, `Do`/`While`, `For`, raw `Switch`/`Case`/`Default`, `Break`, and `Continue` lower to C. |
| `New`/`Delete` | Implemented in bootstrap compiler/runtime | `New Class(...)` lowers to generated package-qualified `Package__Class__new[_N]` helpers using `CMotive_New` followed by constructor dispatch; `Delete obj` lowers to `Package__Class__delete`, destructor dispatch, and `CMotive_Delete`. |
| Standard operators including `>>>` and `<<<` | Partial implemented | C/C++ operators pass through; rotate shifts lower to helper functions for simple identifiers. |
| `Contains { ... }` strings | Implemented | Lexer folds `Contains` blocks into string tokens. |
| `Package`/`Plugin` | Implemented in preprocessor | `Plugin` resolves real package/header/source files from the source directory, `lib`, and `-I` include paths, materializes them before parsing, and restores the importing file package context afterwards. |
| `Plugswitch`/`Plugcase`/`Plugdefault`/`Plugend` | Implemented scaffold | `src/cmotive/preprocessor.py` selects OS, processor, endian and defined-expression cases. |
| `Replace` | Implemented | Preprocessor handles `Replace` as a CMotive macro definition. |
| Native binary output | Implemented | `tools/cmotive.py` compiles to C, emits `.o`/`.obj` with `-c`, and links executables with platform linker path. |
| Processor targets ARM, ARM64, x86, x86_64 | Implemented CLI scaffold | `--target-arch` accepts `arm`, `arm64`/`aarch64`, `x86`, `x64`/`x86_64`. |
| macOS ARM64 linker flag | Implemented | Darwin builds pass `-arch <target>` for compile and link. |
| Strip-compatible symbols | Implemented scaffold | Native object/executable generation uses normal platform toolchain/debug symbol format. |
| Sys::Stdio | Implemented scaffold | Fluent `cout.expect(...).write(...)` and `cin.expect(...).read(...)` lower to C stdio. |
| Sys::File, Filesystem, Logging, Thread, Net, STL, Exception | Package surfaces updated | Headers and runtime placeholders added/updated under `lib/Sys`; `Sys::STL` template headers now exercise real template instantiation. |

## Known limitations after this iteration

- The native C++ compiler sources are still implementation scaffolds; the Python bootstrap
  compiler path is the executable implementation.
- Userspace threads, sockets, and concrete STL container runtime behavior remain package-stable scaffolds.
- Template instantiation is implemented for concrete type-parameter class/function templates in the bootstrap compiler; advanced constraints/partial specialization are not yet implemented.
- Exception unwinding is implemented with `setjmp`/`longjmp` in generated C; destructor-finalization during unwinding is not yet implemented.
- Multiple inheritance is rejected for this CMotive single-inheritance implementation; one concrete base is validated and lowered.
- Operator overloading with `Operation`, auto `Get`/`Set`/`Getall`/`Setall`, and full
  dynamic struct materialization are not fully implemented.
- RTTI remains intentionally out of scope for this version.

## Verification performed

`make -f Makefile.linux test` passed after the implementation pass.  The tests now
cover legacy bootstrap syntax, formal CMotive line-oriented syntax, class/header parsing, concrete class struct lowering, package-qualified method mangling, constructor/destructor chaining, `New`/`Delete` runtime dispatch, invalid-base diagnostics, control flow, preprocessor selection, concrete template instantiation, caught exception unwinding, real Plugin package loading, object generation, executable generation, emitted C, and preprocessing.
