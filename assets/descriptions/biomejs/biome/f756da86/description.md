# Title
Remove `NeedsParentheses::needs_parentheses_with_parent` method

# Summary
Remove `NeedsParentheses::needs_parentheses_with_parent` from the trait and all implementations. Consolidate parentheses logic into the single `needs_parentheses()` method.

# Why
- **Indirection**: The `needs_parentheses_with_parent` method created unnecessary indirection without reducing code complexity
- **Confusion**: Inconsistent usage across the codebase—some call sites used `needs_parentheses()`, others used `needs_parentheses_with_parent()`
- **Duplication**: Led to code duplication in `Any*` enum implementations that had to delegate to the appropriate method

# What Changed
- Removed `needs_parentheses_with_parent(&self, parent: JsSyntaxNode)` from `NeedsParentheses` trait
- Updated all implementations to use only `needs_parentheses(&self)` 
- Implementations that need parent now call `self.syntax().parent()` internally instead of receiving it as parameter
- Cleaned up unused `JsSyntaxNode` imports across the codebase

# Implementation Details
**Pattern changes:**
```rust
// Before
fn needs_parentheses_with_parent(&self, parent: JsSyntaxNode) -> bool {
    matches!(parent.kind(), ...)
}

// After  
fn needs_parentheses(&self) -> bool {
    let Some(parent) = self.syntax().parent() else {
        return false;
    };
    matches!(parent.kind(), ...)
}
```

**Affected types:**
- All `AnyJs*Expression`, `AnyJs*Assignment`, `AnyTsType` implementations
- Helper functions like `needs_binary_like_parentheses`, `unary_like_expression_needs_parentheses`, etc.
- Utility functions in `parentheses.rs` module