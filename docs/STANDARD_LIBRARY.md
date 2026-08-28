# CMotive Standard Library

The standard library package surface is stored under `lib/Sys` and uses CMotive
header syntax (`.HMOT`).  This iteration updates the package declarations for:

- `Sys::Stdio` — `cout.expect(...).write(...)`, `cin.expect(...).read(...)`, `print`, `println`.
- `Sys::File` — `File` class and open/close method surface.
- `Sys::Filesystem` — exists/mkdir/remove surface.
- `Sys::Logging` — info/error surface and runtime helper mapping.
- `Sys::Thread` — userspace-thread package scaffold and `Tstore` example surface.
- `Sys::Net` — TCP/UDP/IP/raw socket package scaffold.
- `Sys::STL` — initial `Vector<T>` template package scaffold.

The bootstrap compiler lowers the common Stdio fluent calls directly to C stdio
so conformance tests can compile, link, and execute.  File, Filesystem, Logging,
Thread, Net, and STL are package-stable scaffolds with native runtime placeholders
in `lib/Sys/runtime.c`.
