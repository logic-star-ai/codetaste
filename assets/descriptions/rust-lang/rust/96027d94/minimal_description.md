# Rename Generator to Coroutine

Rename all occurrences of `Generator`/`generator` terminology to `Coroutine`/`coroutine` throughout the codebase, including:
- Compiler internals (MIR, type system, HIR, traits, etc.)
- Standard library traits (`std::ops::Generator` → `std::ops::Coroutine`, etc.)
- Feature gates (`generators` → `coroutines`, `generator_trait` → `coroutine_trait`, etc.)
- Error messages, diagnostics, and fluent translation files
- Test files and directories
- Documentation and comments