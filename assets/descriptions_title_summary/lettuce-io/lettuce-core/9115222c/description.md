# Consolidate Future utilities and remove PromiseAggregator

Consolidate future utility methods into `internal.Futures` and simplify promise aggregation by using standard `CompletableFuture.allOf()` instead of custom implementation.