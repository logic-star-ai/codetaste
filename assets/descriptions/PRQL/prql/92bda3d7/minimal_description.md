# Rename `prql_compiler::ast` to `prql_compiler::ir`

Rename the `ast` module in `prql_compiler` to `ir` (intermediate representation) to better reflect its purpose now that a dedicated `prql_ast` crate exists for the actual AST.