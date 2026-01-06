# Refactor application lifecycle management with SPI-based `ApplicationLifecycle` interface

Introduce `ApplicationLifecycle` SPI to distribute lifecycle management across modules, replacing centralized logic in `DefaultApplicationDeployer` with modular, ordered implementations.