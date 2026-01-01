# Refactor Statistics with Precision Estimates (`Exact`, `Inexact`, `Absent`)

## Summary

Introduce `Precision<T>` enum to track exactness of statistics throughout query planning and execution, replacing the coarse-grained `is_exact` boolean and ambiguous optional fields.

## Why

- Current `FilterExec::statistics()` creates and discards `DataFusionError`s, causing planning inefficiency
- Single `is_exact` boolean provides insufficient granularity for tracking statistics accuracy
- `Option<T>` fields conflate "unknown", "not computed", and "absent" semantics
- No way to distinguish exact vs. inexact estimates at field level

## Changes

**Core Type System:**
- Add `Precision<T>` enum: `Exact(T)`, `Inexact(T)`, `Absent`
- Refactor `Statistics` fields:
  - `num_rows: Option<usize>` → `Precision<usize>`
  - `total_byte_size: Option<usize>` → `Precision<usize>`
  - `column_statistics: Option<Vec<...>>` → `Vec<...>` (always present, use `Absent` for unknown)
  - Remove `is_exact: bool` (redundant with per-field precision)
- Update `ColumnStatistics`: `null_count`, `max_value`, `min_value`, `distinct_count` → `Precision<...>`

**API Changes:**
- `ExecutionPlan::statistics()` → returns `Result<Statistics>` for proper error handling
- Add helpers: `Statistics::new_unknown()`, `Statistics::into_inexact()`, `Precision::add()`, `Precision::max()`, etc.

**Optimization Improvements:**
- Aggregate statistics optimizations consider per-field exactness
- Join cardinality estimation uses precision-aware calculations
- Filter statistics properly handle and propagate precision information

## Benefits

- Fine-grained statistics exactness tracking per field
- Eliminates error creation/disposal overhead in statistics calculations
- Clearer semantics: absent vs. unknown vs. inexact
- More accurate query optimization decisions
- Enhanced aggregate pushdown capabilities