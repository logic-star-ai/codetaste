# Title
Split Supports.{cpp,h} into Metal/Wooden and refactor wooden support mappings

# Summary
Split monolithic `Supports.{cpp,h}` (1581 lines) into separate `MetalSupports` and `WoodenSupports` files. Refactor wooden support data structures to use direct array indexing instead of conditional lookups.

# Why
- `Supports.{cpp,h}` mixed metal + wooden support code
- Wooden support type/subtype → image mapping was unclear
- Unnecessary `if` checks when accessing `Byte97B23C` (now `SupportsDescriptors`)

# Changes

**File Split:**
- `paint/Supports.{cpp,h}` → `paint/support/{Metal,Wooden}Supports.{cpp,h}`
- New `paint/support/Generic.h` for shared constants (`SUPPORTS_SLOPE_5`)

**Wooden Supports Refactoring:**
- `WoodenSupportImageIds` → 2D array `[type][subtype]`
- `WoodenCurveSupportImageIds` → 2D array structure
- Add `GetWoodenSupportIds(type, subtype)` helper
- Rename `Byte97B23C` → `SupportsDescriptors`
- Improve struct fields: `AsOrphan`/`BoundingBox` vs `var_6`/`var_7`

**Updates:**
- ~70 files updated to include new headers

# Benefits
- Clearer metal vs wooden separation
- Direct array indexing (eliminates conditionals)
- Better type/subtype → image mapping
- Minor performance gain
- Improved maintainability