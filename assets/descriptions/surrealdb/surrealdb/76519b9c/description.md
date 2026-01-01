# Refactor: Restructure key module and rename Cl→Nd

## Summary
Restructure the key/mod hierarchy to use 2-character root prefixes and rename cluster (Cl) to node (Nd) throughout codebase for consistency.

## Changes

### Key Module Restructuring
- Reorganize flat key structure into logical nested modules:
  - `key/root/*` - root-level keys (all, hb, nd, ns)
  - `key/namespace/*` - namespace keys (all, db, lg, tk)
  - `key/database/*` - database keys (all, az, fc, lg, pa, sc, tb, tk, vs)
  - `key/table/*` - table keys (all, ev, fd, ft, ix, lq)
  - `key/index/*` - index keys (all, bc, bd, bf, bi, bk, bl, bo, bp, bs, bt, bu)
  - `key/scope/*` - scope keys (all, tk)
  - `key/node/*` - node keys (all, lq)
  - `key/change/` - change feed keys
  - `key/graph/` - graph edge keys
  - `key/thing/` - record keys

### Key Prefix System
- Establish 2-character root node entries to reserve critical key paths
- Use consistent prefixes: `!` (database), `+` (index), `±` (scope), `$` (node), `#` (change)
- Prevents collisions and provides clear key space organization

### Cl → Nd Rename
- Rename `dbs/cl.rs` → `dbs/node.rs`
- Update `key/cl.rs` → `key/root/nd.rs`
- Change error variant `ClNotFound` → `NdNotFound`
- Update all references: `cl` → `nd`, `Cl` → `Nd` throughout codebase
- Fix inconsistent naming (cluster vs cl vs node)

### Updated Paths
- All import paths updated to reflect new structure
- Cache keys updated to use new module paths
- Transaction methods updated (`set_cl` → `set_nd`, `get_cl` → `get_nd`, `del_cl` → `del_nd`)

## Why
- Clear reservation of 2-character key paths prevents future collisions
- Nested structure better reflects logical hierarchy
- Consistent Nd (Node) terminology eliminates confusion
- Safer extension with well-defined namespaces