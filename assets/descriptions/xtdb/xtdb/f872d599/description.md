Title
-----
Unify VectorReader and IVectorReader interfaces with consistent naming

Summary
-------
Refactor to bring `VectorReader` and `IVectorReader` together by having `IVectorReader` implement `VectorReader`, standardizing method names across both interfaces, and converting `IVectorReader` to Kotlin for consistent null-typing.

Why
---
- Allows call-sites to use `VectorReader` when they don't care about implementation differences
- Provides consistent naming convention across the codebase
- Leverages Kotlin's null-safety for more explicit API contracts

Changes
-------

**Method Renames:**
- `keys`/`getKeys` → `keyNames`
- `legs` → `legNames`  
- `keyReader(name)` / `legReader(name)` → unified as `vectorForOrNull(name)`
- Added `vectorFor(name)` for call-sites that know the vector exists
- `listElementReader()` → `listElements` (property)
- `mapKeyReader()` / `mapValueReader()` → `mapKeys` / `mapValues` (properties)
- `elementReader()` → `listElements` (property)
- `valueCount()` → `valueCount` (property in Kotlin) / `getValueCount()` (Java interop)

**API Improvements:**
- Added `get(name)` operator for Kotlin `[]` syntax → calls `vectorFor(name)`
- Added `get(idx)` operator → calls `getObject(idx)`
- Removed duplicate `getPointer(idx)` overload (kept version with reuse parameter)

**Implementation:**
- Converted `IVectorReader` from Java → Kotlin
- `IVectorReader` now implements `VectorReader`
- Updated all call-sites throughout codebase to use new naming