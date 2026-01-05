# Title
-----
Move `IsDebuggerPresent` to minipal, convert debugger methods to QCall

# Summary
-------
Consolidate native debugger detection across CoreCLR, Mono, and NativeAOT into a shared `minipal` component and convert managed debugger APIs to use QCalls.

# Why
---
- **Code duplication**: Platform-specific debugger detection logic was scattered across PAL, NativeAOT, and Mono implementations
- **Inconsistent APIs**: Different implementations and calling conventions for similar functionality
- **Unnecessary interop**: Libraries layer had direct kernel32 dependency for `IsDebuggerPresent`

# What Changed
---
**New minipal component**:
- Added `minipal_is_native_debugger_present()` in `src/native/minipal/debugger.{c,h}`
- Consolidated platform-specific detection for Windows, Linux, macOS, FreeBSD, NetBSD, Solaris, AIX, etc.

**Replaced PAL implementation**:
- Removed `PAL_IsDebuggerPresent()` from `pal.h` / `pal.cpp`
- Updated all `IsDebuggerPresent()` / `PAL_IsDebuggerPresent()` call sites to use `minipal_is_native_debugger_present()`

**Converted to QCall**:
- `Debugger.IsAttached` → `DebugDebugger_IsManagedDebuggerAttached` (QCall)
- `Debugger.IsLogging()` → `DebugDebugger_IsLoggingHelper` (QCall)
- Added `DebugDebugger_IsNativeDebuggerAttached` for NativeAOT

**Removed**:
- `Interop.Windows.Kernel32.IsDebuggerPresent.cs` from libraries
- `mono-utils-debug.{c,h}` (replaced by minipal)
- InternalCall implementations for debugger methods

**Updated**:
- CMakeLists.txt files across CoreCLR, Mono, NativeAOT to include `debugger.c`
- Calling code in debugger, exception handling, JIT, utilities, etc.

# Impact
---
- Single source of truth for native debugger detection
- Consistent behavior across all runtimes
- Cleaner managed/native boundary (QCall vs InternalCall)
- Reduced platform interop dependencies