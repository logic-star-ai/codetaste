# Title
-----
Continue JSX to TSX migration (batch 2)

# Summary
-------
Continue migrating JSX components to TypeScript by converting ~20+ additional files to TSX format with proper type definitions.

# Why
---
- Type safety and better IDE support
- Continuation of #848 migration effort
- ~7 files remaining after this batch

# What
---
Migrate the following components from JSX to TSX:

**Layout & Structure:**
- `AppLayout.tsx`
- `AppMessagePanel.tsx`
- `AppToolbar.tsx`

**UI Components:**
- `Collapse.tsx`
- `Collapser.tsx`
- `LayerEditorGroup.tsx`
- `LayerListGroup.tsx`

**Field Components:**
- `FieldAutocomplete.tsx`
- `FieldCheckbox.tsx`
- `FieldComment.tsx`
- `FieldDynamicArray.tsx`
- `FieldFunction.tsx`
- `FieldSource.tsx`
- `FieldSourceLayer.tsx`
- `_Field*.tsx` (various internal field components)

**Modal Components:**
- `ModalAdd.tsx`
- `ModalDebug.tsx`
- `ModalExport.tsx`
- `ModalSources.tsx`
- `ModalSourcesTypeEditor.tsx`

**Property Components:**
- `PropertyGroup.tsx`
- `_DataProperty.tsx`
- `_ZoomProperty.tsx`
- `_ExpressionProperty.tsx`
- `_SpecProperty.tsx`

**Map Components:**
- `MapOpenLayers.tsx`
- `MapMaplibreGlLayerPopup.tsx`

**Utilities:**
- `util/format.ts`
- `util/spec-helper.ts`
- `libs/accessibility.ts`

# Changes
---
- Replace `PropTypes` with TypeScript type definitions
- Add type annotations to component props and state
- Update function signatures with proper types
- Add missing type packages: `@types/file-saver`, `@types/react-collapse`
- Fix type-related issues (e.g., `onChange` handlers, array types, etc.)
- Update imports to remove PropTypes dependencies

# Notes
---
~7 files remaining for complete migration after this PR merges.