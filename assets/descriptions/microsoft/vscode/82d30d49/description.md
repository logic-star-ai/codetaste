# Rename Electron Service to Native Host Service

## Summary
Rename `IElectronService` / `ElectronService` to `INativeHostService` / `NativeHostService` across the entire codebase, including file paths, interfaces, implementations, and all references.

## Changes

### File/Folder Renaming
- `vs/platform/electron/*` → `vs/platform/native/*`
- `electronMainService.ts` → `nativeHostMainService.ts`
- `electron.ts` → `native.ts`

### Interface/Class Renaming
- `ICommonElectronService` → `ICommonNativeHostService`
- `IElectronMainService` → `INativeHostMainService`
- `ElectronMainService` → `NativeHostMainService`
- `IElectronService` → `INativeHostService`
- `ElectronService` → `NativeHostService`

### Service Identifiers
- IPC channel: `'electron'` → `'nativeHost'`
- Service ID: `'electronMainService'` → `'nativeHostMainService'`
- Service ID: `'electronService'` → `'nativeHostService'`

### Variable/Property Names
- All instances of `electronService` → `nativeHostService`
- All instances of `electronMainService` → `nativeHostMainService`

### Import Paths
- Update all imports from `vs/platform/electron/*` → `vs/platform/native/*`

### Layer Checker
- Add `ICommonNativeHostService` to `NATIVE_TYPES`
- Add layer checking rule for `vs/platform/native/common/native.ts`

## Scope
- ~100+ files updated
- Electron main process services
- Electron sandbox services
- All service consumers (workbench, extensions, contrib, ...)
- Test files