# Introduce `TypingMode` to unify `intercrate`, `reveal`, and `defining_opaque_types`

Introduce `TypingMode` enum to replace the separate `intercrate` boolean, `Reveal` mode, and `defining_opaque_types` list in `InferCtxt`. This unifies three related concepts into a single, more explicit typing mode parameter.