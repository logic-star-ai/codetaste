# Rename "lexer" to "parser" and reorganize rule directories

Rename all occurrences of "lexer" terminology to "parser" throughout codebase:
- Class names: `LexerBlock` → `ParserBlock`, `LexerInline` → `ParserInline`
- File names: `lib/lexer_*.js` → `lib/parser_*.js`
- Directory structure: `lib/lexer_{block,inline}/` → `lib/rules_{block,inline}/`
- Variables, properties, comments: `lexer` → `parser`