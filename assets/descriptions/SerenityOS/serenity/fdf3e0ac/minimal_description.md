# Remove RegisterState parameter from IRQ handlers

Refactor all interrupt/IRQ handlers to no longer receive `RegisterState const&` as a parameter. This affects:

- `GenericInterruptHandler::handle_interrupt()` 
- `IRQHandler::handle_irq()`
- `HardwareTimer` callback signatures (`Function<void(RegisterState const&)>` → `Function<void()>`)
- All device driver IRQ handlers (USB, Audio, Storage, Network, ...)
- Timer tick functions in `Scheduler` and `TimeManagement`
- All CPU architectures (x86_64, aarch64, riscv64)