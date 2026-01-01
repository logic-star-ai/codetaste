# Consolidate shape types

## Summary
Consolidate three different representations of shapes into a single parametric type `Shape<T>`, removing the GPI abstraction and utilizing TypeScript's type system more effectively.

## Background
Previously had three different shape representations:
- `GPI<T> = { tag: "GPI", contents: [string, Properties<T>] }`
- `GenericShape<T> = { shapeType: string; properties: Properties<T> }`
- `Shape = Circle | Ellipse | ... | Group`

## Changes

### Type System
- Kept the third representation, made it parametric: `Shape<T> = Circle<T> | Ellipse<T> | ... | Group<T>`
- Each shape type now extends `ShapeCommon<T>` and shape-hierarchy interfaces (`Named<T>`, `Stroke<T>`, `Fill<T>`, `Center<T>`, etc.)
- Removed `GPI` concept entirely; replaced with `ShapeVal<T>` wrapper

### Shape Checker
- Added compilation-time shape checker that validates types and constructs shape objects
- Checks shape parameters against expected types (e.g., `Circle.r` must be `FloatV`)
- Implicit casting support:
  - `ListV` ↔ `VectorV`
  - `MatrixV` ↔ `LListV` ↔ `PtListV`
  - `TupV` → `ListV`/`VectorV` (one-way)

### Passthrough Properties
- Each shape has `passthrough: Map<string, CanPassthrough<T>>` field
- Only `StrV` and `FloatV<T>` types allowed in passthrough
- Populated during compilation with strict type checking

### API Changes
- Constraints/objectives now take shape objects directly (not GPIs)
- Example: `overlappingCircleEllipse(s1: Circle<ad.Num>, s2: Ellipse<ad.Num>)`
- Removed `shapedefs` registry; replaced with `shapeTypes` list and `computeShapeBbox()` function

### Renderer
- Updated all render functions to accept typed shape objects
- Removed `shapeMap` in favor of direct function calls based on shape type

## Benefits
- Type-safe shape access: `circle.r.content`, `circle.name`, etc.
- Better TypeScript inference and autocomplete
- Stricter compile-time guarantees
- Cleaner constraint/objective signatures