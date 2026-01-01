# Consolidate Bridging Modules: Merge CBasicBridging + CASTBridging into BasicBridging + ASTBridging

## Summary
Merge `CASTBridging` and `CBasicBridging` modules with their respective parent modules (`ASTBridging` and `BasicBridging`) to enable C++ interop in ASTGen and unify bridging code between ASTGen and SwiftCompilerSources.

## Why
- Eliminate duplication between C-only and C++ bridging modules
- Enable ASTGen to use C++ interoperability features
- Share bridging code between ASTGen and SwiftCompilerSources
- Simplify module structure and reduce maintenance burden

## Changes

### Module Structure
- Remove separate `CASTBridging` and `CBasicBridging` modules
- Consolidate all bridging code into `ASTBridging` and `BasicBridging`
- Add `PURE_BRIDGING_MODE` flag to conditionally compile C++ code
- Introduce `ASTBridgingImpl.h` / `BasicBridgingImpl.h` for inline C++-dependent functions

### Bridging Types
- Update wrapper types (e.g., `BridgedDiagEngine` → `BridgedDiagnosticEngine`)
- Standardize pointer wrapper pattern using `BRIDGING_WRAPPER_*` macros
- Change from C-style structs to C++ classes with explicit conversions
- Add `.raw` accessors and `init(raw:)` initializers for Swift interop
- Mark old-style accessors as `SWIFT_UNAVAILABLE`

### API Changes
- Rename types: `BridgedString` → `BridgedStringRef`, `BridgedOptionalDiagnosticEngine` → `BridgedNullableDiagnosticEngine`, etc.
- Update struct fields: `data`/`length` → standardized naming, `numElements` → `count`
- Add methods to bridging types (e.g., `BridgedDiagnosticEngine.diagnose(...)`)
- Move C++ implementations to separate header (included when not in PURE mode)

### Build System
- Add C++ interop flags: `-cxx-interoperability-mode=default` (5.9+) or `-enable-experimental-cxx-interop` (5.8)
- Add `-DCOMPILED_WITH_SWIFT` and `-DPURE_BRIDGING_MODE` defines
- Configure include paths for LLVM/Clang headers
- Add workaround for pre-5.8 Swift compiler crash with C++ interop
- Update Package.swift files with C++ language standard and macOS deployment target

### Code Updates
- Update all imports: `CASTBridging` → `ASTBridging`, `CBasicBridging` → `BasicBridging`
- Update all call sites to use new type names and APIs
- Fix pointer access patterns (e.g., `.raw` → `.getOpaquePointerValue()`)

### File Removals
- Delete `include/swift/AST/CASTBridging.h`
- Delete `include/swift/Basic/CBasicBridging.h`
- Delete `lib/AST/CASTBridging.cpp`
- Delete `lib/Basic/CBasicBridging.cpp`
- Update `include/module.modulemap`

## Notes
- Future work: Further improve bridging (e.g., potentially remove `bridged`/`unbridged` functions in ASTBridging.cpp)
- Requires Swift 5.8+ for C++ interop support
- PURE_BRIDGING_MODE allows compilation without full C++ headers