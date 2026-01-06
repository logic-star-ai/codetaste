# Refactor: Consolidate schedule configuration traits using generics

Eliminate code duplication between `IntoSystemConfigs` and `IntoSystemSetConfigs` by introducing a generic trait-based approach. Replace both traits with a single `IntoScheduleConfigs<T, M>` trait parameterized over `Schedulable` types.