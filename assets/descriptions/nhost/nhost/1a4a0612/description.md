# Refactor Dialog and Drawer API

## Summary

Simplify dialog/drawer management by removing hardcoded form types and passing components directly. Replace enum-based API with type-safe component-based API.

## Problem

Current API requires:
- Importing all forms in `DialogProvider`
- Adding forms to global `<Drawer />` with conditional rendering
- Passing props through multiple layers (`payload`, `props`, `dialogProps`)
- No type safety when calling `openDialog(type, config)`
- Location (`drawer`/`dialog`) hardcoded per component

Example:
```tsx
// DialogProvider - hardcoded imports + conditionals
{activeDialogType === 'CREATE_TABLE' && <CreateTableForm {...sharedDrawerProps} {...drawerProps.payload} />}

// Usage - no type safety
openDrawer('CREATE_TABLE', { payload: { onSubmit, onCancel, ... } })
```

## Changes

**New API:**
```tsx
openDrawer({
  title: 'Create Table',
  component: <CreateTableForm onSubmit={...} onCancel={...} />,
  props: { ... }
})
```

**Implementation:**
- Remove `DialogType` enum (21 hardcoded types)
- Change `openDialog/openDrawer` to accept `OpenDialogOptions` with `component` prop
- Use `cloneElement` to inject `location`, `onSubmit`, `onCancel` automatically
- Add `DialogFormProps` interface with `location?: 'drawer' | 'dialog'`
- Move form imports to usage sites with dynamic imports
- Extract `FormActivityIndicator` for loading states

**Benefits:**
- ✅ Type-safe component props
- ✅ Co-located form usage with business logic
- ✅ Forms work in both drawers and dialogs
- ✅ No need to modify `DialogProvider` for new forms
- ✅ Cleaner, more intuitive API

## Technical Details

- `DialogProvider` now renders `activeDialog` directly via `cloneElement`
- Reducers store `ReactElement` instead of `type` + `payload`
- All base forms extend `DialogFormProps` for `location` prop
- Dirty state tracking uses injected `location` prop
- Dynamic imports prevent unnecessary bundle loading