# Title
Rename NDirect → PInvoke throughout codebase

## Summary
Rename legacy "NDirect" terminology to "PInvoke" for consistency across the runtime.

## Why
- "NDirect" is an outdated internal term for P/Invoke (Platform Invoke)
- "PInvoke" is the standard, user-facing terminology used in .NET
- Improves code clarity and reduces confusion for contributors
- Aligns internal implementation with public API naming

## Changes

**Classes & Types:**
- `NDirectMethodDesc` → `PInvokeMethodDesc`
- `NDirectStubLinker` → `PInvokeStubLinker`
- `NDirectImportThunkGlue` → `PInvokeImportThunkGlue`
- `NDirectImportPrecode` → `PInvokeImportPrecode`
- ...

**Functions:**
- `NDirectImportWorker()` → `PInvokeImportWorker()`
- `NDirectImportThunk()` → `PInvokeImportThunk()`
- `PopulateNDirectMethodDesc()` → `PopulatePInvokeMethodDesc()`
- `GetNDirectTarget()` → `GetPInvokeTarget()`
- ...

**Flags & Constants:**
- `NDIRECTSTUB_FL_*` → `PINVOKESTUB_FL_*`
- `HAS_NDIRECT_IMPORT_PRECODE` → `HAS_PINVOKE_IMPORT_PRECODE`
- `kNDirectPopulated` → `kPInvokePopulated`
- ...

**Fields:**
- `m_pNDirectTarget` → `m_pPInvokeTarget`
- `m_wFlags` → `m_wPInvokeFlags`
- `pNDirectILStub` → `pPInvokeILStub`
- ...

**Scope:**
- C++ runtime code (vm/*, jit/*, debug/*)
- Platform-specific assembly (x86, x64, ARM, ARM64, LoongArch64, RISC-V)
- Documentation (docs/design/coreclr/botr/*)
- Resource strings & error messages
- Managed data contracts

**Notes:**
- Pure terminology refactoring, no functional changes
- "N/Direct" comments updated to "PInvoke"
- Error message: `Arg_NDirectBadObject` → `Arg_PInvokeBadObject`