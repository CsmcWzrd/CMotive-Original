# CMotive language examples verification report

PASS: 137 manifest examples were verified against the updated CMotive compiler/tooling.

Verification performed:

- Manifest validation: 137 examples present.
- Compile/link/run verification in chunks: every manifest example compiled to an executable, executed, exited with code 0, produced no stderr, and printed its per-example verification marker.
- Object generation verification in chunks: every manifest example compiled with `-c` and produced an object file.
- VS2022 package project validation: package project inputs validated, package `.CMOT` files compiled to objects, and `packages.stamp` / `BUILD_OUTPUTS.txt` were generated.
- CMotive source regression check after parser/codegen fixes: `make -f Makefile.linux all test` passed.

Notes:

- The runner checks stdout markers so a source file cannot falsely pass by accidentally lowering to the default empty `main`.
- Some requirements remain represented as compile-safe scaffolds where the current compiler/runtime still marks them as scaffolded: full template instantiation, full exception unwinding, real package loading, userspace scheduler implementation, real sockets, STL containers, auto Get/Set/Getall/Setall materialization, and Operation operator overloading.
