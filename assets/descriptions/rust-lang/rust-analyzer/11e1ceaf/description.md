# Title
------
Refactor TokenMap to SpanMap for macro expansion tracking

# Summary
---------
Replace token ID-based tracking with span-based tracking in macro expansions. Move from dual maps (expansion + arguments) to single `SpanMap` per expansion by associating subtrees with their source text ranges.

# Why
-----
- **Better incrementality**: Text ranges are made relative to anchors, avoiding recomputation on every file change
- **Simplified architecture**: Single map instead of separate expansion/argument maps
- **Improved hygiene**: Proper syntax context tracking with `SyntaxContextId`

# Changes
---------

**Core Token Tree (`tt` crate)**
- Make `Subtree`, `Leaf`, `TokenTree` etc. generic over span type `S: Span`
- Replace `TokenId` with generic `SpanData<Anchor, Ctx>` containing:
  - `range: TextRange` - relative to anchor
  - `anchor: SpanAnchor` - file + AST ID for incrementality  
  - `ctx: SyntaxContextId` - for hygiene

**Macro Expansion (`mbe`, `hir-expand`)**
- Replace `TokenMap` with `SpanMap` tracking `(TextSize, SpanData)` pairs
- `syntax_node_to_token_tree()` now takes `SpanMap` instead of returning `TokenMap`
- Remove token ID allocation, directly assign spans during conversion
- Update `Hygiene` → `SpanMap` throughout macro expansion

**Proc Macros (`proc-macro-api`, `proc-macro-srv`)**
- Thread `def_site`, `call_site`, `mixed_site` spans through expansion
- Update `FlatTree` serialization to handle `SpanData` via `IndexSet`
- `TokenId` remains as indexing type for proc macro bridge

**HIR Layer (`hir-def`)**
- Update `Expander`, `LowerCtx` to use `SpanMap` instead of `Hygiene`
- Fix `$crate` hygiene by properly resolving syntax contexts
- Thread call site contexts through derive/attr macro invocations

**Tests**
- Update all macro expansion tests to show spans with `+spans+syntaxctxt`
- Add regression tests for macro hygiene issues (#10300, #15685)

# Implementation Notes
----------------------
- `SpanAnchor::DUMMY` / `SyntaxContextId::ROOT` for backwards compatibility
- `Delimiter` now stores open/close spans separately
- Invisible delimiters use `DUMMY_INVISIBLE` constant
- Doc comment conversion updated to handle spans properly