# Refactor netstack to use bufferv2

Replace `pkg/buffer` with `pkg/bufferv2` throughout the netstack implementation. The new buffer implementation uses reference counting and pooling to significantly reduce heap allocations and GC pressure.