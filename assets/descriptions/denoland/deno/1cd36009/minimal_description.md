# Refactor CLI to use `std::fs` via `sys_traits` instead of `deno_fs::FileSystem`

Replace `deno_fs::FileSystem` usage throughout the CLI with direct `std::fs` operations via the `sys_traits` abstraction layer.