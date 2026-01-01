Title
-----
Rename `Generics::params` to `Generics::own_params`

Summary
-------
Rename the `params` field in `ty::Generics` to `own_params` to clarify that it only contains generic parameters directly defined on the item, not inherited from parent scopes.

Why
---
The name `params` is ambiguous when dealing with nested items (associated types, trait methods, impl items, etc.). It's unclear whether it includes parent generics or only the item's own parameters.

The new name `own_params` makes it explicit that:
- These are only the parameters defined directly on this item
- Parent parameters must be accessed separately via `parent` / `parent_count`
- When considering all parameters for nested items, both sources must be combined

Changes
-------
- Rename `Generics::params` → `Generics::own_params` throughout compiler
- Update all usages across:
  - `rustc_middle::ty::generics`
  - HIR analysis (check, collect, wfcheck, ...)
  - Borrowck diagnostics
  - Codegen (LLVM debuginfo)
  - Privacy checking
  - Trait selection
  - Type utilities
  - Clippy lints
  - Rustdoc

Note
----
No audit of usage patterns performed - this is purely a mechanical rename to improve clarity at call sites.