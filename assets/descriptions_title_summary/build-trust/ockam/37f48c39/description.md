# Refactor: Remove lifetime annotations from `Rpc` type

Remove the lifetime parameter from the `Rpc` type, transitioning from `Rpc<'a>` to `Rpc`. Make the type self-contained by owning its data instead of holding references.