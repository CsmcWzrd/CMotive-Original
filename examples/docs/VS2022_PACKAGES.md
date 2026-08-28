# VS2022 package project

Open `vs2022/CMotive.LangExamples.Packages.sln` from Visual Studio 2022. It is an NMake-style project and calls `tools/vs2022_build_packages.py`.

Expected output after Build Solution:

```text
Lang-Examples/build/vs2022/packages/<Configuration>-<Platform>/
  BUILD_OUTPUTS.txt
  packages.stamp
  obj/
  manifests/
```

The project avoids generated or absolute `FULLPath` entries. All project items are relative to the `.vcxproj` file.
