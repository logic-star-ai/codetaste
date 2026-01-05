# Refactor: Rename strategy store to sampling strategy provider

## Summary
Rename `StrategyStore` → `Provider` and related packages/interfaces throughout codebase to better reflect actual behavior. These components provide/return sampling strategies rather than storing them.

## Why
Original naming caused confusion:
- **"Strategy store"** implied storage, but components only return strategies (don't store)
- **Conflation** between "strategy store" (provider) and "sampling store" (actual storage for adaptive sampling throughputs/calculations)
- Misleading terminology across static & adaptive implementations

## Changes

### Package Renames
- `cmd/collector/app/sampling/strategystore` → `.../samplingstrategy`
- `plugin/sampling/strategystore` → `.../strategyprovider`
- Move `calculationstrategy` package inside `adaptive/` (only used there)

### Interface/Type Renames
- `StrategyStore` → `Provider`
- File: `strategy_store.go` → `provider.go`
- Variables: `strategyStore` → `samplingProvider`, `strategyStoreFactory` → `samplingStrategyFactory`

### Method/Field Renames
- `Factory.CreateStrategyStore()` → `CreateStrategyProvider()`
- `CollectorParams.StrategyStore` → `SamplingProvider`
- `CollectorParams.Aggregator` → `SamplingAggregator`
- `HTTPServerParams.SamplingStore` → `SamplingProvider`
- Similar renames across GRPC handlers, test mocks, etc.

### Scope
- All-in-one & collector main entries
- HTTP/GRPC server params & handlers
- Static & adaptive factory implementations
- Test files & fixtures
- Client config manager

## Testing
- `go run ./cmd/collector` compiles
- `go run ./cmd/all-in-one` compiles
- Existing tests pass