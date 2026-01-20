# Remove parser dependency from `ruff-python-ast`

Break circular dependency between `ruff-python-ast` and `rustpython-parser` by extracting and reorganizing code into new crates. This is a pure refactoring with no logical changes - only code movement between crates.