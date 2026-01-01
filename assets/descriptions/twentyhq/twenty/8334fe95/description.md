# Title
Refactor Modal System to Imperative API and Fix Hotkey Scope Race Conditions

# Summary
Refactor modal system from effect-based to imperative approach to eliminate race conditions in hotkey scope management when modals close.

# Why
Effect-based hotkey scope management caused race conditions during modal closing:
- Modal closes → effect tries to restore previous scope → but command menu already restored scope
- Result: wrong hotkey scope persists (e.g., `command-menu-focus` instead of `table-focus`)
- Users unable to use keyboard shortcuts after actions like deleting records

# Changes

**New Modal API**
- Introduce `useModal` hook with imperative methods: `openModal()`, `closeModal()`, `toggleModal()`
- Similar pattern to existing dropdown API

**Modal Identification**
- Add required `modalId` prop to `Modal` and `ConfirmationModal` components
- Create modal ID constants: `FavoriteFolderDeleteModalId`, `RecordIndexRemoveSortingModalId`, `AuthModalId`, etc.

**State Management**
- Introduce `isModalOpenedComponentState` (component-scoped)
- Remove individual boolean state atoms (e.g., `isRemoveSortingModalOpenState`)
- Add `ModalComponentInstanceContext` for component-state tracking

**Hotkey Scope Handling**
- Move from effect-based to imperative hotkey scope management
- Set scope on `openModal()`, restore on `closeModal()`
- Eliminates race conditions

**Mount Effects**
- Create `AuthModalMountEffect` and similar components
- Handle auto-opening modals on mount where needed

# Components Updated
- `Modal`, `ConfirmationModal` → accept `modalId` prop
- `ActionModal`, `AttachmentList` → use `useModal` hook
- Auth modal, favorite folder delete, record sorting removal
- Settings modals: billing, workspace members, API keys, webhooks, domains, ...
- Spreadsheet import modal

# Benefits
- ✓ Fixes hotkey scope race conditions
- ✓ Consistent API (modal + dropdown alignment)
- ✓ Better modal lifecycle control
- ✓ Improved DX