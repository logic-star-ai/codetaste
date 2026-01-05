# Refactor geom2 internal representation from sides to outlines

## Summary

Change geom2 data structure from storing `sides` (edge pairs) to storing `outlines` (ordered point arrays). This eliminates the need for graph traversal when producing outlines, improving performance and reducing memory allocations.

## Why

Operations like booleans, extrusions, and expansions require outlines as input. Previous implementation stored edges as disconnected side pairs `[[p0, p1], [p1, p2], ...]`, requiring depth-first search to reconstruct outlines. New structure stores data as already-connected outlines `[[p0, p1, p2, ...]]`.

## Changes

**Data Structure:**
- `geom2.sides` → `geom2.outlines`
- Sides: `Array<[Vec2, Vec2]>` → Outlines: `Array<Array<Vec2>>`

**API Changes:**
- `create(sides)` → `create(outlines)` 
- `fromOutlines()` → merged into `create()`
- `toOutlines()` → simplified (direct property access)
- New `fromSides()` function (old toOutlines logic moved here)

**Internal Updates:**
- Refactored compact binary serialization format
- Updated `applyTransforms()` to map over outlines
- Updated `reverse()`, `toPoints()`, `toSides()` implementations
- Fixed `validate()` to check outline constraints

**Dependencies:**
- Updated boolean operations (martinez integration)
- Updated expansion operations (`expand...`, `offset...`)
- Updated extrusion operations (`extrudeLinear`, `extrudeRotate`, etc.)
- Updated `snap()`, `project()`, `measureBoundingSphere()`
- Updated primitives (`polygon`)
- Fixed martinez bug #155 (colinear edge handling)

**Tests:**
- Updated all geom2 tests for new structure
- Updated test expectations for point ordering differences
- Fixed martinez-specific edge cases

## Breaking Changes

⚠️ This is a **breaking change** affecting:
- Direct access to `geom2.sides` 
- `geom2.create()` signature
- `geom2.fromOutlines()` removed