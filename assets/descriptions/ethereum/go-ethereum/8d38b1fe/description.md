# Refactor metrics package: split interfaces, clarify concurrency model

## Summary
Major refactoring of the metrics package to improve API clarity and performance by splitting interfaces into read/write components and clarifying the concurrency model.

## Changes

### Interface Separation (Read/Write)
- Split all meter interfaces into:
  - **Write interface** (`Counter`, `Gauge`, `Meter`, `Timer`, etc.) - for updates
  - **Read interface** (`CounterSnapshot`, `GaugeSnapshot`, `MeterSnapshot`, `TimerSnapshot`, etc.) - for reading
- `Snapshot()` method is the gateway from write to read
- Example:
  ```go
  type Counter interface {
    Clear()
    Dec(int64)
    Inc(int64)
    Snapshot() CounterSnapshot
  }
  
  type CounterSnapshot interface {
    Count() int64
  }
  ```

### Concurrency Model Clarification
- **Meters** (write interfaces):
  - Accessible via registry
  - All methods must be concurrency-safe (multiple goroutines can update)
  - `Snapshot()` must also be concurrency-safe
- **Snapshots** (read interfaces):
  - Not guaranteed to be concurrency-safe
  - Designed for single-threaded access by exporters
  - Simple snapshots are immutable (thread-safe)
  - Complex snapshots with lazy calculations (e.g., `Variance()`, `Mean()`) are not thread-safe

### Sample Performance Improvements
- `Sample` types now calculate `Mean()`, `Sum()`, `Min()`, `Max()` once during snapshot creation
- Previously recalculated on every method call
- Same optimization applied to `runtimeHistogram`

### ResettingTimer API Standardization
- `Percentiles()` now uses `0.5` for 50% (was `50`)
- Returns `[]float64` with interpolation (was `[]int64`)
- Removed internal value exposure
- Added `Max()`, `Min()`, `Mean()` getters

### Type Visibility
- Unexported types that don't need public visibility
- Examples: `CounterSnapshot` → `counterSnapshot`, `MeterSnapshot` → `meterSnapshot`, etc.

### Additional Changes
- Added `UpdateIfGt()` to `Gauge` for atomic conditional updates
- Added `CalculatePercentiles()` helper with interpolation
- Improved EWMA implementation with better atomic operations
- Standardized nil/empty implementations

## Why
- **Clearer semantics**: Separation of concerns between reading and writing
- **Performance**: Reduce redundant calculations in samples
- **Consistency**: Standardized percentile calculations across all types
- **Safety**: Explicit concurrency guarantees prevent misuse
- **Maintainability**: Cleaner API surface, unexported internals