Title
-----
Refactor: Extract physical expressions into standalone `polars-expr` crate

Summary
-------
Move physical expression evaluation logic from `polars-lazy` to a new `polars-expr` crate to enable reuse across different execution engines without requiring dependency on `polars-lazy`.

Why
---
Currently, physical expressions are tightly coupled with `polars-lazy`, making it difficult for alternative execution engines to leverage the same expression evaluation infrastructure without pulling in unnecessary dependencies.

Changes
-------

**New Crate Structure**
- Create `polars-expr` crate
- Move physical expressions from `polars-lazy/src/physical_plan/expressions/*` → `polars-expr/src/expressions/*`
- Move execution state from `polars-lazy/src/physical_plan/state.rs` → `polars-expr/src/state/execution_state.rs`
- Move node timer from `polars-lazy/src/physical_plan/node_timer.rs` → `polars-expr/src/state/node_timer.rs`
- Move expression planner from `polars-lazy/src/physical_plan/planner/expr.rs` → `polars-expr/src/planner.rs`

**Expressions Moved**
- `aggregation.rs`, `alias.rs`, `apply.rs`, `binary.rs`, `cast.rs`, `column.rs`, `count.rs`, `filter.rs`, `group_iter.rs`, `literal.rs`, `rolling.rs`, `slice.rs`, `sort.rs`, `sortby.rs`, `take.rs`, `ternary.rs`, `window.rs`

**Dependencies**
- Add `polars-expr` dependency to `polars-lazy` and `polars-pipe`
- Propagate feature flags (`dtype-*`, `temporal`, `streaming`, `parquet`, etc.) from `polars-lazy` → `polars-expr`

**API Improvements**
- Rename `AAggExpr` → `IRAggExpr` for clarity (IR = Intermediate Representation)
- Add `Clone` impl to `Scalar`
- Add `Scalar::dtype()` and `Scalar::update()` methods
- Add `TotalEq` impl for `AnyValue`
- Simplify `PhysicalPipedExpr::evaluate()` to take `&ExecutionState` directly instead of `&dyn Any`
- Remove `SExecutionContext` trait in favor of direct `ExecutionState` usage in streaming pipeline

**Module Updates**
- Update imports across `polars-lazy`, `polars-pipe`, `py-polars`
- Update `Makefile` to include `polars-expr` in publish order
- Make `ExecutionState` fields and methods `pub` for cross-crate access
- Expose `AggState`, `AggregationContext`, `PhysicalExpr`, etc. through `polars-expr::prelude`