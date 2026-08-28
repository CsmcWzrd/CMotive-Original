# CMotive Programming Language Source Archive

CMotive is a production-oriented native language source tree scaffold. It includes `cmotivepp`, `cmotive`, and `cmotive++`, root-only platform Makefiles, native object/executable generation via `-c` and `-o`, platform linker routing, strip-compatible native artifacts, docs, tests, release packaging, and provenance metadata.

## Extensions

- Source: `.CMOT`, `.CMTV`
- Header: `.HMOT`, `.HMTV`

## Build

```sh
make -f Makefile.linux all
make -f Makefile.linux test
./build/bin/cmotive -c examples/hello.CMOT -o build/hello.o
./build/bin/cmotive examples/hello.CMOT -o build/hello
```

Use `Makefile.mac` on macOS and `Makefile.windows` for a Windows-oriented POSIX/MinGW or clang shell. No `build.sh` is included.

## Status

This is a production-oriented compiler source scaffold with a working Python bootstrap compiler driver. The native backend currently lowers CMotive to C and invokes the platform toolchain; the repository also contains C/C++ implementation scaffolds for lexer, parser, AST, semantic analysis, native codegen, ARM64, x86_64, ABI/platform work, templates, exceptions, package/plugin loading, and separate compilation.

See `docs/FEATURE_STATUS.md` for the full matrix.

## Current object-symbol ABI note

Class methods, constructors, destructors, and `New`/`Delete` helpers now use package-qualified C symbols. If no `Package` declaration is active, the default package prefix is `StartPackage`, for example `StartPackage__ClassName__MethodName`.


## VS2022 package project

Open `vs2022/CMotive.Packages.sln` to build the package-system scaffold with Visual Studio 2022. See `docs/VS2022_PACKAGES.md`.
