# Refactor: Remove trie → triedb dependency via interface abstraction

Inverts the dependency between `trie` and `triedb` packages by introducing interface abstractions, moving database implementations to top-level `triedb/` package, and making trie operations depend on interfaces rather than concrete database types.