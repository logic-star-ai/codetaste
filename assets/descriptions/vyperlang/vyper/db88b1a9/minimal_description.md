# Merge front-end and codegen type systems

Historically, Vyper maintains two separate type systems: one in `vyper/semantics/types` (front-end) and another in `vyper/codegen/types` (codegen). This creates duplication, complexity, and potential inconsistencies. This refactoring merges both systems into a unified type system.