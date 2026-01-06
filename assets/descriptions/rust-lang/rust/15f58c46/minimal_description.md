# Remove `Nonterminal` and `TokenKind::Interpolated`

Remove the `Nonterminal` enum and `TokenKind::Interpolated` variant from the compiler, eliminating the ability for tokens to contain embedded AST nodes.