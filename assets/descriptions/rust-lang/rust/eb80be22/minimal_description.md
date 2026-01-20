# Rename `astconv::AstConv` and related items

Large-scale refactoring renaming `astconv::AstConv` trait to `HirTyLowerer` and updating related module, function, and variable names throughout the compiler to reflect that this is HIR type lowering, not AST conversion.