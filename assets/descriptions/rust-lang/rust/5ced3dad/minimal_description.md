# Rename things in new solver and `rustc_type_ir` for clarity

Refactor naming conventions in the trait solver and type infrastructure:
- Rename `interner()` → `cx()` throughout `TypeFolder` and solver
- Rename generic parameter `Infcx` → `D` in solver code  
- Move `infcx.rs` → `delegate.rs` to reflect actual purpose