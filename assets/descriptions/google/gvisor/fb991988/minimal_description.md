# Decouple memory allocation from platform abstraction

Refactor memory management by moving `platform/filemem` to `pgalloc` and removing the `Memory` interface from the `Platform` abstraction. The `Kernel` now directly owns a `MemoryFile` instance instead of accessing it through the platform.