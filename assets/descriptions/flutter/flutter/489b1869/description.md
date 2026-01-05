Title
-----
Move nested DisplayList canvas enums to separate translation unit with Dl prefix

Summary
-------
Extract `ClipOp`, `PointMode`, and `SrcRectConstraint` from `DlCanvas` class into standalone enums in new `dl_types.h`/`dl_types.cc` files. Rename them to `DlClipOp`, `DlPointMode`, and `DlSrcRectConstraint` respectively.

Why
---
Nested enums cause ambiguous compiler reference errors on some GCC versions. While newer clang resolves this by checking type identity, the errors are technically correct. Moving these types to their own translation unit and adding the `Dl` prefix improves clarity and compatibility.

Changes
-------
- Create `display_list/dl_types.h` and `display_list/dl_types.cc`
- Move enums from `DlCanvas` class:
  - `DlCanvas::ClipOp` → `DlClipOp`
  - `DlCanvas::PointMode` → `DlPointMode`
  - `DlCanvas::SrcRectConstraint` → `DlSrcRectConstraint`
- Update all references across:
  - `display_list/...`
  - `flow/...`
  - `impeller/...`
  - `shell/...`
  - `testing/...`
  - `lib/ui/...`
- Remove now-unnecessary typedefs in `DlOpReceiver`
- Update BUILD.gn and licenses_golden

Impact
------
No functional changes. Pure refactoring/renaming.