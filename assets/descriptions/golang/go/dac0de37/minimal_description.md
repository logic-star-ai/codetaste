# Split typechecking logic into separate `typecheck` package

Refactor compiler to extract all typechecking logic from `gc` package into new `cmd/compile/internal/typecheck` package for better code organization and modularity.