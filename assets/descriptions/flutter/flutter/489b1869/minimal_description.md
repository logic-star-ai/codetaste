# Move nested DisplayList canvas enums to separate translation unit with Dl prefix

Extract `ClipOp`, `PointMode`, and `SrcRectConstraint` from `DlCanvas` class into standalone enums in new `dl_types.h`/`dl_types.cc` files. Rename them to `DlClipOp`, `DlPointMode`, and `DlSrcRectConstraint` respectively.