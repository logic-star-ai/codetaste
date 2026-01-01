# Rename filestate backend to DIY

## Summary

Standardize naming for the self-managed backend throughout the codebase. Replace all references to `filestate`, `local`, and `selfmanaged` with consistent `DIY` terminology.

## Changes

### Package & Types
- Rename `pkg/backend/filestate` → `pkg/backend/diy`
- Rename `localBackend` → `diyBackend`
- Rename `localBackendReference` → `diyBackendReference`
- Rename `localStack` → `diyStack`
- Rename `localStackSummary` → `diyStackSummary`
- Rename `localSnapshotPersister` → `diySnapshotPersister`
- Rename `localQuery` → `diyQuery`
- Update interface: `Backend.local()` → `Backend.diy()`

### Environment Variables
- `SELF_MANAGED_STATE_NO_LEGACY_WARNING` → `DIY_BACKEND_NO_LEGACY_WARNING`
- `SELF_MANAGED_STATE_LEGACY_LAYOUT` → `DIY_BACKEND_LEGACY_LAYOUT`
- `SELF_MANAGED_STATE_GZIP` → `DIY_BACKEND_GZIP`
- `RETAIN_CHECKPOINTS` → `DIY_BACKEND_RETAIN_CHECKPOINTS`
- `DISABLE_CHECKPOINT_BACKUPS` → `DIY_BACKEND_DISABLE_CHECKPOINT_BACKUPS`

### Functions & Methods
- `IsFileStateBackendURL()` → `IsDIYBackendURL()`
- `newLocalBackend()` → `newDIYBackend()`
- `getLocalStacks()` → `getStacks()`
- Update all error messages: "File state backend" → "DIY backend"
- Update all comments: "filestate"/"local" → "DIY"

### Test Files
- Move `tests/integration/backend/filestate/*` → `tests/integration/backend/diy/*`
- Rename test files: `*_filestate_*` → `*_diy_*`
- Update test assertions and error message checks

### Changelog & Config
- Update `changelog/config.yaml`: `backend: [filestate, ...]` → `backend: [diy, ...]`

### Documentation & Comments
- Update all references to "filestate backend" → "DIY backend"
- Update all references to "local backend" → "DIY backend"
- Where "local DIY backend" appears, it refers specifically to DIY backend using `file://` (local filesystem)
- Clarify DIY backend supports: `file://`, `s3://`, `gs://`, `azblob://`

### Compatibility Shim
- Keep deprecated `filestate.IsFileStateBackendURL()` as compat shim for ESC, forwarding to `diy.IsDIYBackendURL()`

## Why

Improve consistency and clarity by using a single, unambiguous term ("DIY") for the self-managed backend across all code, documentation, and user-facing messages.