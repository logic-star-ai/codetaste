# Title
Consolidate Future utilities and remove PromiseAggregator

# Summary
Consolidate future utility methods into `internal.Futures` and simplify promise aggregation by using standard `CompletableFuture.allOf()` instead of custom implementation.

# Why
- Reduces duplication of future handling logic across codebase
- Simplifies promise aggregation using JDK standard APIs
- Improves separation between public API and internal implementation
- Clarifies responsibilities with better naming (`PromiseAdapter` vs generic `Futures`)

# Changes

**Consolidation**
- Move `awaitAll()`, `awaitOrCancel()` implementations from `LettuceFutures` → `internal.Futures`
- Add `await()`, `toCompletionStage()`, `adapt()` to `internal.Futures`
- Let `LettuceFutures` delegate to `internal.Futures`

**Simplification**
- Remove custom `PromiseAggregator` implementation
- Replace aggregator usage with `CompletableFuture.allOf()`
- Update `allOf()` to accept `CompletionStage<?>` collection

**Renaming**
- Rename `resource.Futures` → `PromiseAdapter` (Netty-specific Promise adaptation)
- Rename test utility `Futures` → `TestFutures` (avoid naming conflicts)

**Updates**
- Update `DefaultClientResources.shutdown()` to use `Futures.allOf()` with `CompletionStage` list
- Update `DefaultEventLoopGroupProvider.shutdown()` similarly
- Replace `toBooleanPromise()` references throughout codebase