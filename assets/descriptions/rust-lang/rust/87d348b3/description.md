# Title
Introduce `TypingMode` to unify `intercrate`, `reveal`, and `defining_opaque_types`

# Summary
Introduce `TypingMode` enum to replace the separate `intercrate` boolean, `Reveal` mode, and `defining_opaque_types` list in `InferCtxt`. This unifies three related concepts into a single, more explicit typing mode parameter.

# Why
The previous design split typing mode across multiple parameters (`InferCtxt::intercrate`, `ParamEnv::reveal`, `InferCtxt::defining_opaque_types`), making it unclear which combination of settings should be used in different contexts. This refactoring:
- Makes the typing mode explicit and self-documenting
- Prevents invalid combinations of settings
- Simplifies trait solver logic by removing mode-specific checks
- Enables cache unification between coherence/non-coherence modes in the new solver
- Prepares for removing `Reveal` from `ParamEnv` (tracked separately)

# Changes
- Add `TypingMode<I>` enum with variants:
  - `Coherence`: During overlap/coherence checking, must be complete
  - `Analysis { defining_opaque_types }`: During HIR typeck, can define specific opaques
  - `PostAnalysis`: During codegen/MIR optimization, all opaques revealed
  
- Replace `InferCtxt` fields:
  - Remove `intercrate: bool` → use `typing_mode`
  - Remove `defining_opaque_types` → use `typing_mode`
  
- Thread `TypingMode` through:
  - `InferCtxtBuilder::build()` now takes explicit `TypingMode`
  - Add to `CanonicalQueryInput` as query input
  - Add `InferCtxt::typing_mode()` accessor with debug assertions
  
- Merge caches:
  - Unify coherence/non-coherence caches for new trait solver
  - Clear local cache when forking with different `TypingMode`
  
- Update all `InferCtxt` construction sites to pass appropriate mode

# Compatibility Notes
- Temporary: `InferCtxt::typing_mode()` asserts agreement with `ParamEnv::reveal` until future cleanup
- Uses `TypingMode::from_param_env()` in places where analysis should eventually use body-specific mode
- Many uses should eventually reveal only body-defined opaques instead of `UserFacing` mode

# Future Work
See #132279 and inline FIXMEs for:
- Remove `Reveal` from `ParamEnv` entirely
- Use analysis mode with proper opaque revelation in more places
- Clean up `from_param_env()` usage patterns