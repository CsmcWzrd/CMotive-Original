# CMotive Language Examples

This archive contains 137 runnable CMotive examples plus header and package/VS2022 scaffolds.

Expected layout after extraction:

```text
CMotive/
  tools/cmotive.py
  tools/cmotivepp.py
  Lang-Examples/
    Makefile
    examples/
    headers/
    packages/
    vs2022/
```

Build and verify from `CMotive/Lang-Examples`:

```sh
make check
```

Useful targets:

```sh
make compile     # compile every manifest example into build/bin
make objects     # compile every manifest example with -c into build/obj
make run         # compile and execute every manifest example
make preprocess  # preprocess every manifest example into build/pp
make clean
```

The examples are aligned with the formal CMotive requirements: capitalized keywords, `.CMOT/.CMTV/.HMOT/.HMTV` extensions, line-oriented functions, classes, inheritance, constructors/destructors, `New`/`Delete`, control flow, templates/blend/enum scaffolds, exceptions scaffolds, Package/Plugin syntax, standard-library package usage, and platform/ABI-oriented source shapes.
