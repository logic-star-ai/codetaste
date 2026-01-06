# Simplify WASI internal implementations by removing generic wrapper types

Refactor WASIp2 implementation to remove generic wrapper types (`WasiImpl<T>`, `IoImpl<T>`, `WasiHttpImpl<T>`) and implement Host traits directly for concrete view types instead.