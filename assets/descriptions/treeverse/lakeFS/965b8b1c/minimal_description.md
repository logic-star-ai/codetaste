# Simplify config package structure by embedding template

Refactor config package to eliminate indirection layer by embedding template structure directly into `Config` struct, allowing direct field access instead of getter methods.