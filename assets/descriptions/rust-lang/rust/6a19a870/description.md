Title
-----
Rename `FulfillmentErrorCode` and `ObligationCauseCode` variants to reduce redundancy

Summary
-------
Refactor `FulfillmentErrorCode` and `ObligationCauseCode` enums to have shorter, less redundant variant names. Remove glob imports and consistently use fully qualified paths with `ObligationCauseCode::` prefix.

Changes
-------
**FulfillmentErrorCode variants:**
- `SelectionError` → `Select`
- `ProjectionError` → `Project`
- `SubtypeError` → `Subtype`
- `ConstEquateError` → `ConstEquate`

**ObligationCauseCode variants:**
- `MiscObligation` → `Misc`
- `ItemObligation` → `WhereClause`
- `BindingObligation` → `SpannedWhereClause`
- `ExprItemObligation` → `WhereClauseInExpr`
- `ExprBindingObligation` → `SpannedWhereClauseInExpr`
- `BuiltinDerivedObligation` → `BuiltinDerived`
- `ImplDerivedObligation` → `ImplDerived`
- `WellFormedDerivedObligation` → `WellFormedDerived`
- `FunctionArgumentObligation` → `FunctionArg`
- `CompareImplItemObligation` → `CompareImplItem`

**Supporting types:**
- `ImplDerivedObligationCause` → `ImplDerivedCause`
- `DerivedObligationCause` → `DerivedCause`

Why
---
- Variant names were repetitive (e.g., `FulfillmentErrorCode::SelectionError`, `ObligationCauseCode::MiscObligation`)
- Glob imports (`use ...::*`) obscured where variants came from
- Shorter names improve readability when fully qualified paths are used

Implementation
--------------
- Replace glob imports with explicit `ObligationCauseCode` usage throughout codebase
- Update all pattern matches, constructors, and references to use new names
- Adjust error reporting and diagnostic code accordingly