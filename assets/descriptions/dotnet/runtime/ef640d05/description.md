# Consolidate QueryPerformanceCounter/GetTickCount usages to minipal/time.h

## Summary
Consolidate duplicated time-related function implementations across CoreCLR, NativeAOT, Mono, and PAL into `minipal/time.h` as single source of truth. Replace scattered calls to `QueryPerformanceCounter`, `QueryPerformanceFrequency`, `GetTickCount`, `GetTickCount64`, and various Unix equivalents with unified minipal API.

## Why
- Multiple duplicate implementations existed across VM, JIT, PAL, GC, NativeAOT, Mono
- Each implementation handled platform differences independently (Windows vs Unix, `clock_gettime`, `mach_absolute_time`, etc.)
- Maintenance burden with scattered `#ifdef` logic
- Inconsistent behavior and configuration across components

## Changes

### New Unified API in minipal/time.h
- `minipal_hires_ticks()` → replaces `QueryPerformanceCounter`, `clock_gettime(CLOCK_MONOTONIC)`, `mach_absolute_time`
- `minipal_hires_tick_frequency()` → replaces `QueryPerformanceFrequency` and various frequency calculations
- `minipal_lowres_ticks()` → replaces `GetTickCount`, `GetTickCount64`, millisecond timer implementations

### Removed Implementations
- CoreCLR: `SystemNative::GetTickCount/GetTickCount64` (ecalls)
- PAL: `GetTickCount`, `GetTickCount64`, `QueryPerformanceCounter`, `QueryPerformanceFrequency`
- NativeAOT: `PalGetTickCount64`, `PalQueryPerformanceCounter/Frequency`, `RhpGetTickCount64`
- Mono: `ves_icall_System_Environment_get_TickCount/64`, `mono_msec_boottime`
- GC: Duplicate time query logic
- EventPipe: Platform-specific performance counter code

### Updated Components
- JIT compiler timing (compiler.cpp, utils.cpp)
- GC timing (gcenv.unix.cpp)
- Stress log timestamps (stresslog.cpp)
- Thread suspension timeouts (threads.cpp, threadsuspend.cpp)
- Performance measurements (CycleTimer, PerfCounter, SimpleTimer)
- ILAsm timing (main.cpp, writer.cpp)
- Profiler detach timing (profdetach.cpp)
- Background JIT work scheduling (tieredcompilation.cpp)
- Test suites (palsuite/...)

### Cleanup
- Removed CMake checks: `HAVE_CLOCK_MONOTONIC_COARSE`, `HAVE_CLOCK_GETTIME_NSEC_NP` (moved to minipal)
- Removed test cases: `GetTickCount/test1`, `queryperformancecounter/test1`, `queryperformancefrequency/test1`
- Consolidated configuration to `minipal/configure.cmake`

### Not Changed
- Debug-only `#ifdef`'d instances for local debugging

## Notes
- All time APIs now consistently return `int64_t` instead of mixed types
- Platform abstraction fully handled in minipal layer
- Existing behavior preserved, no functional changes to timing semantics