# Reorganize non-constant global statics into structs

Refactor scattered mutable and immutable static global variables throughout the NumPy C codebase into organized structs exposed via `multiarraymodule.h`.