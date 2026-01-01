# Rename `hir::Map::{get_,find_}parent_node` methods and add convenience helpers

## Summary

Rename `hir::Map::get_parent_node` → `parent_id` and `find_parent_node` → `opt_parent_id`. Add new `get_parent` and `find_parent` methods that return `Node` directly.

## Why

The current `get_parent_node` / `find_parent_node` methods are **confusing** because:
- Despite their names suggesting they return a `Node`, they actually return a `HirId`
- This naming mismatch makes the API less intuitive

## Changes

**Renames:**
- `hir::Map::get_parent_node(hir_id)` → `hir::Map::parent_id(hir_id)` 
- `hir::Map::find_parent_node(hir_id)` → `hir::Map::opt_parent_id(hir_id)`

**New methods:**
- `hir::Map::get_parent(hir_id)` - returns `Node<'hir>` directly
- `hir::Map::find_parent(hir_id)` - returns `Option<Node<'hir>>` directly

## Benefits

- **Clearer naming**: `parent_id` clearly indicates it returns an ID, not a Node
- **Less boilerplate**: Replace `hir.get(hir.get_parent_node(id))` with `hir.get_parent(id)`
- **Better ergonomics**: Common pattern becomes single method call

## Migration

```rust
// Before
let parent_id = hir.get_parent_node(hir_id);
let parent_node = hir.get(parent_id);

// After  
let parent_id = hir.parent_id(hir_id);
let parent_node = hir.get_parent(hir_id);
```

```rust
// Before
if let Some(parent_id) = hir.find_parent_node(hir_id) { ... }

// After
if let Some(parent_id) = hir.opt_parent_id(hir_id) { ... }
```