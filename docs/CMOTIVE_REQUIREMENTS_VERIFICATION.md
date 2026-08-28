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
| Classes, visibility blocks, constructors, destructors | Implemented scaffold | Parser accepts `Class`, `Public`/`Private`/`Protected`, constructors, destructors, nested classes, and methods. |
| Single inheritance | Implemented scaffold | Parser records `Inherits`; codegen reserves a single-inheritance layout comment and object header. |
| Bit member specification | Implemented scaffold | Parser records bit fields; codegen lowers them to C bit-field structs. |
| `Blend`/`Enum` | Parse scaffold | Parser preserves declarations as scaffold metadata without breaking compilation. |
| `Template` and `Type` | Parse scaffold | Parser accepts formal template headers and preserves scaffold metadata. |
| `Try`/`Catch`/`Catchall`/`Throw` | Compile scaffold | `Throw` lowers to runtime helper; `Try`/`Catch` parse and keep a native-unwinding scaffold. |
| Control flow | Implemented | `If`/`Elif`/`Else`, `While`, `Do`/`While`, `For`, raw `Switch`/`Case`/`Default`, `Break`, and `Continue` lower to C. |
| `New`/`Delete` | Implemented scaffold | Codegen lowers allocation/free to `CMotive_New`/`CMotive_Delete`. |
| Standard operators including `>>>` and `<<<` | Partial implemented | C/C++ operators pass through; rotate shifts lower to helper functions for simple identifiers. |
| `Contains { ... }` strings | Implemented | Lexer folds `Contains` blocks into string tokens. |
| `Package`/`Plugin` | Parse scaffold | Parser accepts package/import declarations; package manager C++ scaffold updated. |
| `Plugswitch`/`Plugcase`/`Plugdefault`/`Plugend` | Implemented scaffold | `src/cmotive/preprocessor.py` selects OS, processor, endian and defined-expression cases. |
| `Replace` | Implemented | Preprocessor handles `Replace` as a CMotive macro definition. |
| Native binary output | Implemented | `tools/cmotive.py` compiles to C, emits `.o`/`.obj` with `-c`, and links executables with platform linker path. |
| Processor targets ARM, ARM64, x86, x86_64 | Implemented CLI scaffold | `--target-arch` accepts `arm`, `arm64`/`aarch64`, `x86`, `x64`/`x86_64`. |
| macOS ARM64 linker flag | Implemented | Darwin builds pass `-arch <target>` for compile and link. |
| Strip-compatible symbols | Implemented scaffold | Native object/executable generation uses normal platform toolchain/debug symbol format. |
| Sys::Stdio | Implemented scaffold | Fluent `cout.expect(...).write(...)` and `cin.expect(...).read(...)` lower to C stdio. |
| Sys::File, Filesystem, Logging, Thread, Net, STL | Package scaffolds updated | Headers and runtime placeholders added/updated under `lib/Sys`. |

## Known limitations after this iteration

- The native C++ compiler sources are still implementation scaffolds; the Python bootstrap
  compiler path is the executable implementation.
- Templates, exceptions, package loading, userspace threads, sockets, and STL containers
  are parsed/package-stable scaffolds, not full runtime implementations yet.
- Multiple inheritance syntax is accepted as metadata, but only the first base is reserved
  for the current single-inheritance layout.
- Operator overloading with `Operation`, auto `Get`/`Set`/`Getall`/`Setall`, and full
  dynamic struct materialization are not fully implemented.
- RTTI remains intentionally out of scope for this version.

## Verification performed

`make -f Makefile.linux test` passed after the implementation pass.  The tests now
cover legacy bootstrap syntax, formal CMotive line-oriented syntax, class/header parsing,
control flow, preprocessor selection, object generation, executable generation, emitted C,
and preprocessing.
