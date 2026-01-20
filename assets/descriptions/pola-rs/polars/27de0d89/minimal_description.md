# Refactor: Extract physical expressions into standalone `polars-expr` crate

Move physical expression evaluation logic from `polars-lazy` to a new `polars-expr` crate to enable reuse across different execution engines without requiring dependency on `polars-lazy`.