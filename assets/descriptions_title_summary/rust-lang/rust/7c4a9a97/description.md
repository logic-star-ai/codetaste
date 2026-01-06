# Migrate `rustc_incremental` diagnostics to translatable structs

Migrate diagnostics in `rustc_incremental` crate from string-based errors to translatable diagnostic structs. Apply diagnostic migration lints to additional `Session` methods and add `IntoDiagnosticArg` implementations for common types.