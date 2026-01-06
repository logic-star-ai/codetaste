# Rename csslayout to yoga across codebase

Rename all references from `csslayout`/`CSSLayout` to `yoga`/`Yoga`:
- `CSSLayout/` → `yoga/` directory
- `com.facebook.csslayout` → `com.facebook.yoga` package
- `CSSLAYOUT_ROOT` → `YOGA_ROOT` 
- `csslayout_dep()` → `yoga_dep()`
- `#include <CSSLayout/...>` → `#include <yoga/...>`
- Function parameters: `cssMalloc` → `ygmalloc`, `cssCalloc` → `yccalloc`, etc.
- Build targets: `//:CSSLayout` → `//:yoga`
- C# targets: `csslibnet*` → `yogalibnet*`
- Variable names and compiler flag constants