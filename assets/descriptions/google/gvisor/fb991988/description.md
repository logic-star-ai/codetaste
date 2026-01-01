# Title

Decouple memory allocation from platform abstraction

# Summary

Refactor memory management by moving `platform/filemem` to `pgalloc` and removing the `Memory` interface from the `Platform` abstraction. The `Kernel` now directly owns a `MemoryFile` instance instead of accessing it through the platform.

# Why

Improved page cache reclaim requires tighter integration between the page cache and page allocator. The current design couples memory allocation to the platform abstraction, which creates unnecessary indirection and prevents direct interaction between these subsystems.

# What Changed

- **Package reorganization**
  - `pkg/sentry/platform/filemem` → `pkg/sentry/pgalloc`
  - `FileMem` → `MemoryFile`

- **Platform interface**
  - Removed `Memory()` method from `Platform` interface
  - Removed `platform.Memory` interface entirely
  - Platform no longer responsible for memory allocation

- **Kernel changes**
  - `Kernel` now holds `mfp` (`MemoryFileProvider`) field
  - Added `SetMemoryFile()` and `MemoryFile()` methods
  - `Kernel` implements `MemoryFileProvider` interface

- **Context propagation**
  - Added `CtxMemoryFile` and `CtxMemoryFileProvider` context keys
  - All context implementations updated to provide memory file access

- **Callsite updates**
  - All `platform.FromContext(ctx).Memory()` → `pgalloc.MemoryFileProviderFromContext(ctx).MemoryFile()`
  - Memory file creation now explicit during initialization
  - ~30+ files updated across filesystems, mm, kernel, etc.

# Implementation Details

- `MemoryFileProvider` interface added for S/R compatibility (allows `Kernel` to be dependency-injected without circular deps)
- Memory file backed by memfd, created during kernel initialization
- All memory allocation operations (`Allocate`, `DecRef`, `IncRef`, `MapInternal`, etc.) now go through `MemoryFile` directly
- Documentation updated to reflect new architecture