# Title
-----
Remove RegisterState parameter from IRQ handlers

# Summary
-------
Refactor all interrupt/IRQ handlers to no longer receive `RegisterState const&` as a parameter. This affects:

- `GenericInterruptHandler::handle_interrupt()` 
- `IRQHandler::handle_irq()`
- `HardwareTimer` callback signatures (`Function<void(RegisterState const&)>` → `Function<void()>`)
- All device driver IRQ handlers (USB, Audio, Storage, Network, ...)
- Timer tick functions in `Scheduler` and `TimeManagement`
- All CPU architectures (x86_64, aarch64, riscv64)

# Why
---
Most interrupt handlers never use the register state anywhere - it's just being passed around for no reason. This simplifies the API and eliminates unnecessary parameter passing overhead.

The one consumer that actually needs register state (`PerformanceManager`) now accesses it via `current_thread->current_trap()->regs` instead.

# Changes
---------
- **Interrupt handlers**: Remove `RegisterState const& regs` parameter from all `handle_interrupt()` and `handle_irq()` methods
- **Hardware timers**: Change callback type from `Function<void(RegisterState const&)>` to `Function<void()>`
- **Scheduler**: `Scheduler::timer_tick()` no longer receives register state
- **PerformanceManager**: Access register state via trap frame instead of parameter
- Update all implementations across all architectures and device drivers

# Precedent
-----------
Linux made an identical change 18 years ago for similar reasons - https://github.com/torvalds/linux/commit/7d12e78