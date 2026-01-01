# Refactor SMP pause mechanism: rename xxxx_pause.c → xxxx_smpcall.c

## Summary
Rename `*_cpupause.c` files to `*_smpcall.c` across all architectures and update associated function/IRQ handler names to reflect actual SMP semantics.

## Why
- Current naming (`pause`, `async_pause`) doesn't accurately represent the SMP call/scheduling mechanism
- Misleading names cause confusion about what these handlers actually do
- Need clearer distinction between SMP scheduling requests and general SMP calls

## Changes

### File Renames
```
*_cpupause.c → *_smpcall.c
```
Affected: armv7-a, armv7-r, armv8-r, arm64, cxd56xx, lc823450, rp2040, sam34, risc-v, sim, s698pm, x86_64, xtensa

### Function Renames
- `*_pause_async_handler()` → `*_smp_sched_handler()`
- `*_pause_handler()` → `*_smp_call_handler()`  
- `up_cpu_pause_async()` → `up_send_smp_sched()`

### IRQ Definition Renames
- `GIC_SMP_CPUPAUSE_ASYNC` → `GIC_SMP_SCHED`
- `GIC_SMP_CPUCALL` → `GIC_SMP_CALL`
- `*_IRQ_SW_INT` → `*_IRQ_SMP_CALL` (cxd56xx)
- `*_SIO_IRQ_PROC*` → `*_SMP_CALL_PROC*` (rp2040)
- `*_IRQ_IPC*` → `*_IRQ_SMP_CALL*` (sam4cm)
- `SMP_IPI_*_IRQ` renaming (x86_64)
- ...

## Impact
All SMP-enabled architectures (ARM, RISC-V, SPARC, x86_64, Xtensa)

## Notes
Pure refactoring—no functional changes, just naming clarity