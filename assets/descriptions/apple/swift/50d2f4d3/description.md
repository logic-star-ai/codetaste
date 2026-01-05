# Title
[NFC] Make llvm namespace explicit for Optional and None to prepare for std::optional migration

## Summary
Phase-1 preparation for migrating from `llvm::Optional` to `std::optional`. Makes the `llvm` namespace explicit for all uses of `Optional` and `None` throughout the Swift compiler codebase.

## Why
- `llvm::Optional` was removed from upstream LLVM
- Need to migrate to `std::optional` before next rebranch
- On Darwin, `std::optional` and `llvm::Optional` have same layout (minimal ABI impact)
- Making namespace explicit now enables mechanical replacement later:
  - `llvm::Optional` → `std::optional`
  - `llvm::None` → `std::nullopt`
- Incremental approach allows cherry-picking to release/5.9 branch with minimal disruption

## Changes
- Remove `using llvm::Optional` and `using llvm::None` declarations
- Replace all `Optional<T>` → `llvm::Optional<T>`
- Replace all `None` → `llvm::None`
- Add explicit `#include "llvm/ADT/Optional.h"` where needed

## Affected Areas
- AST headers and implementations (Decl.h, Expr.h, Type.h, Attr.h, ...)
- Type system (TypeCheckRequests.h, TypeCheckType.cpp, ...)
- Serialization/deserialization (ModuleFile.*, Deserialization.cpp, ...)
- SIL generation and optimization
- SourceKit integration
- Symbol graph generation
- Test utilities and fixtures

This is purely mechanical namespace qualification—no functional changes (NFC).