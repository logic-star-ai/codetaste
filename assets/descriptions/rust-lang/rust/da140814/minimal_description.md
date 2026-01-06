# Remove redundant `u32` indices from `BrAnon` and `BoundTyKind::Anon`, store `BoundVar` in `Placeholder` types

Refactor internal representation of anonymous bound regions and types by removing duplicate index information and consolidating bound variable data into `Placeholder` types.