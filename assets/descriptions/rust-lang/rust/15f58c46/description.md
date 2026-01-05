# Remove `Nonterminal` and `TokenKind::Interpolated`

## Summary

Remove the `Nonterminal` enum and `TokenKind::Interpolated` variant from the compiler, eliminating the ability for tokens to contain embedded AST nodes.

## Why

The `Interpolated` token kind was conceptually problematic and costly:
- **Conceptually strange**: Tokens containing AST nodes is like words containing sentences
- **Special handling**: Required custom code paths throughout the parser
- **Prevented `Copy`**: Made `Token` and `TokenKind` unable to implement `Copy`
- **Performance overhead**: Added complexity and required token cloning
- **Recursion depth**: Forced ~20 crates to increase `recursion_limit` to 256

## Changes

### Core Token Types
- Remove `Nonterminal` enum (`NtBlock` variant)
- Remove `TokenKind::Interpolated` variant
- Make `Token` and `TokenKind` implement `Copy`
- Remove `InvisibleOrigin::FlattenToken` variant
- Simplify `ParseNtResult` enum (remove `Nt` variant, add `Block` variant)

### Token Stream Handling
- Remove `TokenStream::flattened()` and related flattening logic
- Remove `TokenStream::flatten_token()` and `flatten_token_tree()`
- Remove `TokenStream::from_nonterminal_ast()`
- Simplify `LazyAttrTokenStream` implementation

### Parser Updates
- Replace interpolated token checks with metavariable checks
- Change `is_whole_block()` → `is_metavar_block()`
- Update `token_uninterpolated_span()` / `prev_token_uninterpolated_span()`
- Remove special handling for `Interpolated` in `visit_token()`
- Remove `visit_nonterminal()` visitor function
- Eliminate `maybe_whole!` macro pattern for `NtBlock`

### Nonterminal Parsing
- Update `parse_nonterminal()` to return specific `ParseNtResult` variants
- Add direct handling for `Block` metavariables
- Remove `Nt` wrapper around parsed nonterminals

### Cleanup
- Remove `recursion_limit = "256"` from ~20 crates
- Remove `HasTokens` impl for `Nonterminal`
- Remove `nonterminal_to_string()` from pretty printer
- Update tests (interpolated blocks → metavar blocks)

### Attribute Handling
- Update `DelimArgs` construction to use tokens directly
- Remove flattening in `cfg_eval` and attribute parsing
- Simplify `AttrTokenStream` processing