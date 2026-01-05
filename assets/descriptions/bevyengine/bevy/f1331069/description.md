# Refactor: Consolidate schedule configuration traits using generics

## Summary
Eliminate code duplication between `IntoSystemConfigs` and `IntoSystemSetConfigs` by introducing a generic trait-based approach. Replace both traits with a single `IntoScheduleConfigs<T, M>` trait parameterized over `Schedulable` types.

## Why
- Significant code duplication between system and system set configuration implementations
- Both traits implemented nearly identical methods with only type differences
- Opens door for additional node types (e.g., #14195)
- Improves maintainability by reducing parallel implementations

## Changes

**New traits:**
- `Schedulable` trait with associated types `Metadata` and `GroupMetadata`
- `ProcessScheduleConfig` trait (replaces `ProcessNodeConfig`)

**Renamed/consolidated:**
- `IntoSystemConfigs<M>` + `IntoSystemSetConfigs` → `IntoScheduleConfigs<T: Schedulable, M>`
- `SystemConfigs` → `ScheduleConfigs<ScheduleSystem>`
- `SystemSetConfigs` → `ScheduleConfigs<InternedSystemSet>`
- `SystemConfig` → `ScheduleConfig<ScheduleSystem>`
- `SystemSetConfig` → `ScheduleConfig<InternedSystemSet>`
- `NodeConfigs<T>` → `ScheduleConfigs<T>`
- `NodeConfig<T>` → `ScheduleConfig<T>`

**Implementations:**
- `ScheduleSystem` and `InternedSystemSet` now implement `Schedulable`
- Single generic implementation of all configuration methods
- `GraphInfo` made public to support trait bounds

## Migration Guide
```rust
// Before
IntoSystemConfigs<M> → IntoScheduleConfigs<ScheduleSystem, M>
IntoSystemSetConfigs → IntoScheduleConfigs<InternedSystemSet, M>
SystemConfigs → ScheduleConfigs<ScheduleSystem>  // or NodeConfigs<ScheduleSystem>
SystemSetConfigs → ScheduleConfigs<InternedSystemSet>  // or NodeConfigs<InternedSystemSet>
```

## Notes
- All existing API usage patterns remain compatible through trait bounds
- No functional behavior changes
- Enables future extensibility for custom schedulable node types