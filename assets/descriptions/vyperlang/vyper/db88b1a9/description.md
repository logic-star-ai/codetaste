# Merge front-end and codegen type systems

## Summary
Historically, Vyper maintains two separate type systems: one in `vyper/semantics/types` (front-end) and another in `vyper/codegen/types` (codegen). This creates duplication, complexity, and potential inconsistencies. This refactoring merges both systems into a unified type system.

## Why
- Eliminates duplicate type definitions and logic
- Reduces maintenance burden
- Ensures type consistency between compilation phases
- Simplifies type parsing and handling
- Improves code architecture and clarity

## What Changed

### Type System Unification
- **Removed** `vyper/codegen/types/types.py` and `vyper/codegen/types/convert.py`
- **Unified** all type definitions under `vyper/semantics/types`
- **Added** API compatibility properties to new types (e.g., `maxlen`, `subtype`, `name`)
- **Moved** helper functions like `is_numeric_type()`, `is_integer_type()`, etc. to `vyper/codegen/core.py`

### Type API Enhancements
- Added `memory_bytes_required`, `storage_size_in_words`, `int_bounds`, `ast_bounds` properties
- Enhanced numeric types (`IntegerT`, `DecimalT`) with better bounds checking
- Improved `BytesM_T`, `BytesT`, `StringT` with consistent APIs
- Unified `TupleT` and `StructT` with `tuple_items()`, `tuple_keys()`, `tuple_members()` methods

### Code Organization
- **Renamed** `ModuleNodeVisitor` → `ModuleAnalyzer`
- **Moved** `VariableRecord` from `vyper/ast/signatures/function_signature.py` → `vyper/codegen/context.py`
- **Simplified** `GlobalContext.parse_type()` to use semantic analysis directly
- **Attached** namespace to module metadata for downstream use

### Test Updates
- Updated ~10+ test files to use new type system
- Changed imports from `vyper.codegen.types` → `vyper.semantics.types`
- Adapted assertions/comparisons for new type APIs

## Implementation Details
- Types now have `_is_prim_word`, `_is_array_type`, `_is_bytestring` flags
- Integer/decimal types expose `bits`, `is_signed`, `divisor`, `epsilon` properties  
- Array types unified with `value_type`, `count`/`length` properties
- Structs/tuples share common iteration patterns via `tuple_*()` methods
- Backwards compatibility maintained via property aliases (e.g., `maxlen`, `subtype`)

## Known Issues
- Some kludges introduced to integrate new types into existing codegen machinery
- Follow-up work needed on `GlobalContext` and `FunctionSignature` refactoring