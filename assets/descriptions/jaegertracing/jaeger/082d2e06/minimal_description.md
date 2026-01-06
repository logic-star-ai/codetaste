# Refactor: Rename strategy store to sampling strategy provider

Rename `StrategyStore` → `Provider` and related packages/interfaces throughout codebase to better reflect actual behavior. These components provide/return sampling strategies rather than storing them.