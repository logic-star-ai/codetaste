# Title

Migrate internal/test modules to use typed config state objects

# Summary

Refactor config access patterns throughout internal and test modules to use statically-typed state objects instead of dynamic lookups. Replace `config.config._read(...)` with `config._read(...)`, `config.config.flag_name` with `config.flag_name.value`, and `FLAGS.flag_name` with direct config access. Add module-level convenience functions in `config.py` (`_read`, `update`, `define_bool_state`, etc.) that delegate to the global `config` instance.

# Why

Dynamic lookups on `jax.config` are not type checker/IDE friendly. State objects provide static typing and better developer experience.

# Changes

**Core config module (`jax/_src/config.py`)**
- Add module-level aliases: `_read`, `update`, `define_*_state`, `parse_flags_with_absl`
- These delegate to methods on the global `config` instance

**Internal modules (`api.py`, `compiler.py`, `distributed.py`, `maps.py`, `ops/scatter.py`, `tpu_custom_call.py`)**
- Replace `config.config._read(...)` → `config._read(...)`
- Replace `config.config.flag` → `config.flag.value`
- Replace `config.config.update(...)` → `config.update(...)`
- In `maps.py`: convert try/except config definition block to direct assignments, store state objects in module variables (`_SPMD_LOWERING`, `_SPMD_LOWERING_MANUAL`, `_ENSURE_FIXED_SHARDING`)
- In `tpu_custom_call.py`: rename `mosaic_*` flags to `_MOSAIC_*` constants

**Export/jax2tf modules**
- Update imports: `from jax import config` → `from jax._src import config`
- Replace `config.jax_*` → `config.*.value`
- Use config context managers instead of manual save/restore

**Test modules (50+ files)**
- Replace `config.x64_enabled` → `config.enable_x64.value`
- Replace `FLAGS.jax_*` → `config.*.value` or direct access
- Use context managers: `with config.enable_x64(True):` instead of manual update/restore
- Remove `FLAGS = config.FLAGS` assignments
- Update test utilities: remove `set_spmd_lowering_flag`/`restore_spmd_lowering_flag` helpers, use direct config updates

# Details

- All config flag accesses now go through statically-typed state objects
- Enables better IDE autocomplete and type checking
- No functional changes, pure refactoring
- Follows up on #18008