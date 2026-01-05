# Title

Remove `TLShapeDef` and simplify shape configuration

# Summary

Removes `TLShapeDef` abstraction and simplifies how shapes are configured in the editor. Instead of defining shapes through a definition object, shapes are now configured by directly providing util classes, validators, and migrations.

# Why

The `TLShapeDef` abstraction layer was overly complex and made customization harder. Loosening the configuration system better supports custom shapes and third-party extensions.

# What Changed

**Removed:**
- `TLShapeDef` interface & `defineShape()` function
- `App.getShapeUtilByType()` method
- Shape definition exports (`TLArrowShapeDef`, `TLGeoShapeDef`, etc.)
- `allowUnknownShapes` option

**Modified:**
- `App.getShapeUtil()` now accepts shape types, shapes, or util classes directly
- `TldrawEditorConfig` now takes `shapes` as `{ [type]: { util, validator?, migrations? } }`
- `createTLSchema()` params changed to `{ shapeValidators, shapeMigrations, ... }`
- Shape validators now optional in `createRecordType`

**Added:**
- `App.isShapeOfType<T>(shape, Util)` type guard helper
- `TLShapeUtil.type` static property
- `UtilsForShapes`, `ValidatorsForShapes`, `MigrationsForShapes` types

# Breaking Changes

```diff
- import { TLArrowShapeDef, defineShape } from '@tldraw/editor'
+ import { TLArrowUtil } from '@tldraw/editor'

- const util = app.getShapeUtilByDef(TLArrowShapeDef)
+ const util = app.getShapeUtil(TLArrowUtil)

- if (TLArrowShapeDef.is(shape)) { }
+ if (app.isShapeOfType(shape, TLArrowUtil)) { }

  const config = new TldrawEditorConfig({
-   shapes: [CardShape],
-   allowUnknownShapes: true,
+   shapes: {
+     card: { util: CardUtil }
+   }
  })
```