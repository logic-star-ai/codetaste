# Refactor diagnostic system to store salsa IDs and defer message generation

Move diagnostic infrastructure from `hir` to `hir-analysis` crate, refactor diagnostic enums to store salsa IDs instead of pre-computed strings, and consolidate all message formatting in `to_complete()` implementations.