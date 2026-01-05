Title
-----
Unify scheduler context switch calls with `nxsched_switch_context` across architectures

Summary
-------
Replace all separate `nxsched_suspend_scheduler`/`nxsched_resume_scheduler` calls with unified `nxsched_switch_context(prev, next)` across all architecture implementations.

Why
---
- Simplifies arch↔sched layer interaction
- Provides single unified entry point for context switches
- Completes missing scheduling metadata updates in architectures where context switching occurs in both `up_switch_context` **and** IRQ handlers

Changes
-------
**In `up_switch_context` functions:**
- Remove separate `nxsched_suspend_scheduler(rtcb)` + `nxsched_resume_scheduler(tcb)` calls
- Replace with single `nxsched_switch_context(rtcb, tcb)` call

**In IRQ handlers (`*_doirq` functions):**
- Add missing `nxsched_switch_context(*running_task, tcb)` calls where context switches can occur during interrupt handling
- Store `this_task()` in local `tcb` variable before updating `*running_task` for consistency

Affected Architectures
----------------------
avr, avr32, ceva, hc, mips32, misoc (lm32/minerva), or1k, renesas, risc-v, sim, sparc_v8, tricore, x86, x86_64, xtensa, z16, z80

Impact
------
- No behavior change expected
- Purely refactoring to standardize scheduler interaction pattern
- Critical for architectures where context switching happens in both normal and IRQ paths