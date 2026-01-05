# Unify plugin registration API: deprecate `add_plugin`, enhance `add_plugins` to accept tuples

## Summary

Deprecate `App::add_plugin` in favor of a more powerful `App::add_plugins` that accepts single plugins, plugin groups, **and tuples** of plugins/groups.

## Why

- **Consistency**: `add_systems` already accepts tuples, but `add_plugins` didn't
- **Ergonomics**: Multiple `add_plugin` calls create visual noise and make builder chains longer
- **API clarity**: One unified method for all plugin registration scenarios

## Changes

**API Changes:**
- `App::add_plugins` now accepts `impl Plugins<M>` (sealed trait)
- `App::add_plugin` marked `#[deprecated]`, internally calls `add_plugins`

**`Plugins` Trait Implementations:**
- `Plugin` types (single plugin)
- `PluginGroup` types
- Tuples (up to 16 elements) over types implementing `Plugins`

**Codebase Updates:**
- All examples migrated from `add_plugin` → `add_plugins`
- Multiple sequential `add_plugin`/`add_plugins` calls combined into tuple-based calls where appropriate

## Examples

**Before:**
```rust
app.add_plugin(PluginA)
   .add_plugin(PluginB)
   .add_plugins(DefaultPlugins);
```

**After:**
```rust
app.add_plugins((PluginA, PluginB, DefaultPlugins));
```

## Migration

Replace `app.add_plugin(plugin)` with `app.add_plugins(plugin)`.