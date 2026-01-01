Title
-----
Remove deprecated APIs from 0.14 release cycle

Summary
-------
Remove all deprecated APIs from the 0.14 cycle that have direct replacements or are no longer used.

Why
---
These deprecations have replacements and can be safely removed. Keeping deprecated APIs increases maintenance burden and cognitive load.

Changes
-------
**Build System**
- Remove `addSharedLibrary`/`addStaticLibrary` → use `addLibrary` with `.linkage` field
- Remove `addAssembly` → use `addObject` with `Module.addAssemblyFile`
- Remove deprecated `ExecutableOptions`/`ObjectOptions`/`TestOptions` fields → use `root_module` instead
- Remove `addExecutable(...).filter` → use `.filters` array
- Remove `TranslateC.addExecutable` → use `createModule`/`addModule`

**Calling Conventions**
- Remove `CallingConvention.*` uppercase aliases (`.Unspecified`, `.C`, `.Stdcall`, etc.) → lowercase variants
- Remove `windows.WINAPI` → use `std.builtin.CallingConvention`

**Standard Library**
- Remove `std.ascii.isASCII` → `isAscii`
- Remove `std.time.sleep` → `std.Thread.sleep`
- Remove `std.zig.fatal` → `std.process.fatal`
- Remove `std.atomic.Value.fence` → use other atomics
- Remove `std.builtin.Mode` → `OptimizeMode`
- Remove `std.builtin.PanicFn` → use `Panic` namespace
- Remove `std.crypto.utils.*` → `std.crypto.*` direct functions
- Remove `std.crypto.kem.ml_kem_01` → `ml_kem`
- Remove `std.fs.MAX_PATH_BYTES` → `max_path_bytes`
- Remove `std.fs.atomicSymLink` → `cwd().atomicSymLink()`
- Remove `std.hash.uint32` → `std.hash.int`
- Remove `std.hash.crc.Polynomial` enum → use `Crc` with algorithm
- Remove `std.leb.{readULEB128,writeULEB128,readILEB128,writeILEB128}` → lowercase variants
- Remove `std.math.big.int.{to,Const.to}` → `toInt`
- Remove `std.mem.{tokenize,split,splitBackwards}` → use specific variants (`*Sequence`, `*Any`, `*Scalar`)
- Remove `std.meta.FieldType` → `@FieldType`
- Remove `std.net.Address.ListenOptions.reuse_port` → merged into `reuse_address`
- Remove `std.unicode.{utf16leToUtf8*,utf8ToUtf16LeWithNull,fmtUtf16le}` → lowercase variants
- Remove `std.valgrind.nonSIMDCall*` → `nonSimdCall*`
- Remove `std.zig.CrossTarget` → `std.Target.Query`

**Config Headers**
- Remove `ConfigHeader.Style.autoconf` → `autoconf_undef`

Notable Exclusions
------------------
Not removed (require separate cleanup):
- `std.ArrayHashMap` (too much fallout)
- `std.debug.runtime_safety` (too much fallout)  
- `std.heap.GeneralPurposeAllocator` (many refs, not 1:1 with "debug allocator")
- `std.io.Reader` (being reworked)
- `std.unicode.utf8Decode()` (needs new API first)
- Manifest backwards compat options (breaks TestFetchBuilder)
- Panic handler as namespace (many tests still use function)