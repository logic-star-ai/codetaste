# Rename "lexer" to "parser" and reorganize rule directories

## Summary
Rename all occurrences of "lexer" terminology to "parser" throughout codebase:
- Class names: `LexerBlock` → `ParserBlock`, `LexerInline` → `ParserInline`
- File names: `lib/lexer_*.js` → `lib/parser_*.js`
- Directory structure: `lib/lexer_{block,inline}/` → `lib/rules_{block,inline}/`
- Variables, properties, comments: `lexer` → `parser`

## Why
Correct terminology usage - the components are performing parsing operations, not lexical analysis. The rule implementations should reside in `rules_*` directories rather than `lexer_*` to better reflect their purpose.

## Changes Required

**Class Renames:**
- `LexerBlock` → `ParserBlock`
- `LexerInline` → `ParserInline`

**File Renames:**
- `lib/lexer_block.js` → `lib/parser_block.js`
- `lib/lexer_inline.js` → `lib/parser_inline.js`  
- `lib/parse_ref.js` → `lib/parser_ref.js`

**Directory Restructure:**
- `lib/lexer_block/*` → `lib/rules_block/*`
- `lib/lexer_inline/*` → `lib/rules_inline/*`

**Code Updates:**
- All `state.lexer` references → `state.parser`
- All `this.lexer` references → `this.parser`
- Function parameter names: `lexer` → `parser`
- Error messages: "Lexer rule not found" → "Parser rule not found"
- Comments: "lexer" → "parser" where applicable