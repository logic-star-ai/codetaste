Title
-----
Consolidate CPU architecture information into `cmd/internal/sys` package

Summary
-------
Introduce new `cmd/internal/sys` package to centralize architecture metadata (name, family, byte order, pointer/register sizes) that was previously scattered redundantly across the source tree.

Replace old char-based architecture identifiers ('6', '5', '8', '7', '9', '0', 'z') with named constants (`sys.AMD64`, `sys.ARM`, `sys.I386`, `sys.ARM64`, `sys.PPC64`, `sys.MIPS64`, `sys.S390X`) throughout codebase.

Why
---
Architecture information was redundantly defined across multiple packages and files, leading to:
- Code duplication
- Maintenance burden
- Unclear architecture identification via single-char constants
- Scattered initialization of arch-specific values (Widthptr, Widthint, Widthreg, etc.)

Changes
-------
**New Package**: `cmd/internal/sys/arch.go`
- `ArchFamily` type for architecture families
- `Arch` struct with Name, Family, ByteOrder, IntSize, PtrSize, RegSize, MinLC
- `InFamily()` method for cleaner multi-arch checks
- Pre-defined arch constants: `Arch386`, `ArchAMD64`, `ArchARM`, `ArchARM64`, `ArchMIPS64`, `ArchPPC64`, `ArchS390X`

**Replacements**:
- `Thechar` → `Family` (e.g., `'6'` → `sys.AMD64`)
- `Thestring` → `Name`
- `Thelinkarch` → `LinkArch.Arch`
- `Widthptr/Widthint/Widthreg` initialization moved to use `SysArch.{PtrSize,IntSize,RegSize}`

**Scope**:
- cmd/asm/internal/... 
- cmd/compile/internal/...
- cmd/internal/obj/...
- cmd/link/internal/...

**Exceptions**:
- Error messages referencing old toolchain names (intentionally kept)
- `reltype` function in cmd/link (intentionally kept)