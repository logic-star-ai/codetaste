# Redux Toolkit Migration: modalsSlice

## Summary
Migrate modals state management from legacy Redux patterns to Redux Toolkit, improving type safety and developer experience.

## Changes

### Structure
- Delete `loot-core/client/actions/modals.ts` and `loot-core/client/reducers/modals.ts`
- Create `loot-core/client/modals/modalsSlice.ts` with Redux Toolkit
- Update all modal imports across ~50+ files

### Type Safety
- Consolidate `Modal` type as discriminated union in `modalsSlice`
- Enable autocomplete for `pushModal`, `replaceModal`, etc.
- Reuse modal option types instead of duplicating definitions
- Each modal now has strongly-typed `name` + `options` structure

### API Changes
- Action payloads now consistent object shape:
  ```ts
  // Before
  pushModal('edit-rule', { rule })
  
  // After
  pushModal({ modal: { name: 'edit-rule', options: { rule } } })
  ```
- `collapseModals` now takes `{ rootModalName }` payload
- `openAccountCloseModal` now takes `{ accountId }` payload

### Modal Components
- Update props to extract from `Modal` union type:
  ```ts
  type Props = Extract<Modal, { name: 'foo' }>['options']
  ```
- Split `SingleInputModal` → `NewCategoryModal` + `NewCategoryGroupModal` for better type safety
- Remove intermediate prop spreading (e.g., `autocompleteProps`)

### Validation
- Fix optional params (e.g., `requisitionId`, `syncSource` with defaults)
- Improve error handling in `openAccountCloseModal`
- Clean up unused modal states and definitions

## Why
- Part of Phase 2 Redux Toolkit migration (#4012, #4016, #4018, #4114)
- Better TypeScript autocomplete/IntelliSense
- Single source of truth for modal types
- Consistent action patterns across codebase
- Reduce modal definition duplication