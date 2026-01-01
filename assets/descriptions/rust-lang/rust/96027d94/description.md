# Rename Generator to Coroutine

## Summary

Rename all occurrences of `Generator`/`generator` terminology to `Coroutine`/`coroutine` throughout the codebase, including:
- Compiler internals (MIR, type system, HIR, traits, etc.)
- Standard library traits (`std::ops::Generator` → `std::ops::Coroutine`, etc.)
- Feature gates (`generators` → `coroutines`, `generator_trait` → `coroutine_trait`, etc.)
- Error messages, diagnostics, and fluent translation files
- Test files and directories
- Documentation and comments

## Why

Implements compiler-team decision #682 to adopt more accurate terminology. The async/yield constructs are more properly described as coroutines in PL theory.

## Scope

**Automated replacements:**
- `Generator` → `Coroutine`
- `generator` → `coroutine`  
- `GeneratorState` → `CoroutineState`
- `GeneratorWitness` → `CoroutineWitness`
- `AsyncGeneratorKind` → `AsyncCoroutineKind`
- File/folder names containing `generator` → `coroutine`

**Manual review required for:**
- "id generators", "code generator", "hash generator" → keep as-is (not the feature being renamed)
- Comments/docs referring to general generators vs the Rust language feature
- Test file contents and expected output

**Feature gates:**
- Rename `generators` feature to `coroutines` (mark old as removed)
- Rename `generator_trait` to `coroutine_trait`
- Rename `generator_clone` to `coroutine_clone`
- Update feature gate documentation

**Files to rename:**
- `tests/ui/generator/**` → `tests/ui/coroutine/**`
- MIR opt test files
- Debuginfo test files
- Any other files with `generator` in name where content refers to the language feature

## Notes

- Mix of automated search/replace + careful manual verification
- Preserve non-Rust-feature uses of "generator" terminology
- Update all error codes, diagnostics, and user-facing messages