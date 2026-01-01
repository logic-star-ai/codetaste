# Title
-----
Refactor PVF workers into separate crates with inverted dependencies

# Summary
-------
Split the monolithic `polkadot-node-core-pvf-worker` crate into three focused crates: `pvf-common`, `pvf-execute-worker`, and `pvf-prepare-worker`. Invert the dependency relationship so workers no longer depend on the host crate.

# Why
---
- **Separation of concerns**: Execute and prepare workers have distinct responsibilities and should be independently maintainable
- **Correct dependency direction**: Host spawns workers → host should depend on workers, not vice versa
- **Preparation for distribution**: Enables future standalone worker binary distribution
- **Cleaner architecture**: Reduces circular dependencies and improves modularity

# Changes
---------
**New crate structure:**
- `node/core/pvf/common` - shared types, traits, and utilities (`error`, `execute`, `prepare`, `pvf`, `worker`, `executor_intf`)
- `node/core/pvf/execute-worker` - execution worker entrypoint and logic
- `node/core/pvf/prepare-worker` - preparation worker entrypoint and logic

**Dependency updates:**
- Host (`pvf`) now depends on both worker crates + common
- Workers depend only on common
- Updated imports across entire codebase (cli, malus, test-parachains, etc.)

**Code movement:**
- Split `executor_intf.rs` between common (config/params) and workers (prevalidate/prepare/execute)
- Move worker entrypoints to respective crates
- Relocate `decl_worker_main!` macro to common
- Move test utilities to host crate's `testing` module

**Cleanup:**
- Remove `worker/src/lib.rs`
- Update log targets to be worker-specific
- Re-export commonly used types from host crate for convenience

# No Functional Changes
-----------------------
This is a pure refactoring - no behavior changes, only structural improvements.