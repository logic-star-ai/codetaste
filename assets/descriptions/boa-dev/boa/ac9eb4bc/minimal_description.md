# Refactor registers to use the stack

Refactor VM execution to store registers directly on the stack instead of maintaining a separate `Registers` data structure. Consolidate stack and register management into a single `Stack` type with improved API and readability.