# Restructure `frame_support` macro-related exports to `__private` module

Restructure `frame_support`'s public API by moving macro-related reexports to a private `__private` module, forcing explicit imports and clarifying what constitutes public vs internal API surface.