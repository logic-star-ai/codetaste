Title
-----
Refactor Zig imports and file structure (part 1)

Summary
-------
Standardize Bun's file structure and import style to be more consistent and closer to Zig standard library conventions.

Changes
-------
### Import Style
- Prefer `bun.foo.Bar` over `@import("../../foo/Bar.zig")`
- Nested namespaces in `foo/Bar.zig` → `foo/Bar/*.zig`
- Namespaces use `snake_case`

### Breaking Changes
- **`bun.JSC` → `bun.jsc`** (deprecated alias removed)
- **String type aliases removed**:
  - `string` → `[]const u8`
  - `stringZ` → `[:0]const u8`
  - `stringMutable` → `[]u8`

### Major Renames
- `js_ast.zig` → `ast.zig` (available as `bun.ast`)
- `bun_js.zig` → `bun.js.zig`
- Allocators: `*_allocator.zig` → `PascalCase.zig`

### New Namespaces
- `bun.collections`: `BabyList`, `BitSet`, `HiveArray`, `MultiArrayList`
- `bun.interchange`: `json`, `toml`
- `bun.string.immutable`: `paths`, `unicode`, `visible`, `grapheme`, `escapeHTML`, ...
- `bun.analytics`: consolidated analytics modules

Why
---
- Reduce deep relative import chains
- Improve code discoverability
- Align with Zig stdlib patterns
- Group related functionality

Notes
-----
**Part 1** of refactoring. Merging incrementally to reduce conflicts.

Tracking: STAB-842, STAB-843, STAB-844, STAB-845, STAB-846, STAB-847, STAB-848