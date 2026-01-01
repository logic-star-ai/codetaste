# refactor(stream): refactor `trait Executor` to get rid of `info()`

## Summary

Refactor the `Executor` trait to cleanly separate executor metadata (`ExecutorInfo`) from execution logic, eliminating unnecessary code duplication and preventing info consistency issues.

## Why

Most executor implementations contained an `info: ExecutorInfo` field that was never actually used by the executor itself—only returned via `info()` method for downstream consumers. This led to:

- Duplicated boilerplate: `info` field + trait method implementations in every executor
- Risk of inconsistency: executors could accidentally construct info that differs from frontend-derived metadata
- Unnecessary coupling: executors aware of metadata they don't need

## What Changed

**Core trait refactoring:**
- Renamed `Executor` trait → `Execute` trait (now only contains `execute()` methods)
- Removed `info()`, `schema()`, `pk_indices()`, `identity()` methods from trait
- Introduced `Executor` struct: combines `ExecutorInfo` + `Box<dyn Execute>`

**Executor implementations:**
- Removed unused `info` fields from most executors (except HashAgg, HashJoin, SimpleAgg, Sink, TemporalJoin)
- Executors now receive `input: Executor` instead of `input: BoxedExecutor`
- Simplified executor construction—no longer need to pass/store info they don't use

**Type changes:**
- `BoxedExecutor` remains but now refers to `Executor` struct (not `Box<dyn Executor>`)
- Executor builders return `Executor` struct wrapping both info and execute impl
- Pattern: `(ExecutorInfo, Box<dyn Execute>).into()` → `Executor`

## Benefits

- **Cleaner implementations**: Executors only store data they actually need
- **Safer construction**: Harder to create inconsistent executor info
- **Less boilerplate**: No more repeated `impl Executor { fn schema(&self) -> &Schema { &self.info.schema } }`
- **Better separation of concerns**: Static metadata vs. runtime execution logic