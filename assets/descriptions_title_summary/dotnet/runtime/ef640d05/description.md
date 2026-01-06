# Consolidate QueryPerformanceCounter/GetTickCount usages to minipal/time.h

Consolidate duplicated time-related function implementations across CoreCLR, NativeAOT, Mono, and PAL into `minipal/time.h` as single source of truth. Replace scattered calls to `QueryPerformanceCounter`, `QueryPerformanceFrequency`, `GetTickCount`, `GetTickCount64`, and various Unix equivalents with unified minipal API.