Title
-----
Refactor CLI to use `std::fs` via `sys_traits` instead of `deno_fs::FileSystem`

Summary
-------
Replace `deno_fs::FileSystem` usage throughout the CLI with direct `std::fs` operations via the `sys_traits` abstraction layer.

Why
---
- **Easier extraction**: Removes `deno_fs` dependency, making it easier to extract code from the CLI crate
- **Better performance**: Eliminates the extra abstraction layer that does unnecessary work for stats, directory reads, etc.

Changes
-------
- Introduce `CliSys` type wrapping either `RealSys` or `DenoCompileFileSystem`
- Replace `FsSysTraitsAdapter` with `CliSys` across the codebase
- Update method signatures: `CliOptions::from_flags()`, `DenoDirProvider::new()`, `DiskCache::new()`, `CliLockfile::discover()`, etc.
- Remove `FsSysTraitsAdapter` and `InMemoryFs` from `ext/fs`
- Upgrade `sys_traits` 0.1.1 → 0.1.4 with additional features (`getrandom`, `filetime`, `strip_unc`, etc.)
- Update node resolution types: `CliNodeResolver`, `CliPackageJsonResolver`
- Refactor standalone binary filesystem to implement `sys_traits` directly
- Add clippy rule to disallow `sys_traits::impls::RealSys` (use `CliSys` instead)

Implementation Details
---------------------
- `CliSys` delegates to underlying implementation (real or compile FS)
- All file operations go through `sys_traits` traits instead of `FileSystem` trait
- Test code updated to use memory-based sys where needed
- Permission descriptor parser now generic over sys type