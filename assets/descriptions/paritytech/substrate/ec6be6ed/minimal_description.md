# Simplify state backend by fixing transaction type to `PrefixedMemoryDB`

Remove `Backend::Transaction` associated type and fix it to `PrefixedMemoryDB<H>`, eliminating unnecessary generics throughout the codebase.