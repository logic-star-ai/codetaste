# Rename `graph.Value` to `graph.Ref` to reduce naming ambiguity

Rename the `graph.Value` type to `graph.Ref` throughout the codebase. The name `Value` was confusing given the existence of `quad.Value`, and `Ref` more accurately describes its purpose as an opaque reference token.