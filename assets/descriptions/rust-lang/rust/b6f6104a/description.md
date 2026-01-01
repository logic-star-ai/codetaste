# Refactor unwind in MIR

## Summary

Replace `Option<BasicBlock>` representation of unwinding with explicit `UnwindAction` enum to improve type safety and semantic clarity.

## Changes

Transform unwinding representation from `Option<BasicBlock>` into:

```rust
enum UnwindAction {
    Continue,           // No cleanup, continue unwinding
    Cleanup(BasicBlock), // Execute cleanup in block
    Unreachable,        // UB if unwind occurs
    Terminate,          // Abort execution if unwind occurs
}
```

## Implementation Details

### MIR Representation
- Replace `cleanup: Option<BasicBlock>` fields with `unwind: UnwindAction` in:
  - `TerminatorKind::Call`
  - `TerminatorKind::Assert`
  - `TerminatorKind::Drop`
  - `TerminatorKind::InlineAsm`
  - `TerminatorKind::FalseUnwind`
- Rename `TerminatorKind::Abort` → `TerminatorKind::Terminate`

### Interpreter/Const Eval
- Remove `StackPopUnwind` enum, use `UnwindAction` directly
- Update `Machine` trait methods to accept `UnwindAction`
- Update panic/unwind handling to use new representation

### Codegen
- Update unwind block generation logic
- Handle `Terminate` with platform-specific termination (SEH catch-all on MSVC, cleanup landing pad elsewhere)
- Replace `double_unwind_guard` → `terminate_block`
- Update funclet generation for cleanup blocks

### MIR Transforms
- Update all visitors/passes handling terminators
- `AbortUnwindingCalls`: use `UnwindAction::Terminate` directly instead of inserting abort blocks
- Elaborate drops: map between `Unwind` and `UnwindAction`
- Inlining: handle `UnwindAction` mapping

### Tests
- Update ~100+ mir-opt tests with new syntax
- Tests now show `-> [return: bb, unwind: action]` format
- Update coverage tests referencing terminology

## Benefits

- **Type safety**: Explicit variants vs. `Some`/`None`
- **Clarity**: Intent clear from variant name
- **Consistency**: Single representation across interpreter and codegen
- **POF semantics**: `Continue` vs `Cleanup(_)` distinction makes POF (panic-on-unwind) frames explicit

cc @JakobDegen @RalfJung @Amanieu