Title
-----
Refactor AbstractInvokable to accept Environment and State in constructor

Summary
-------
Refactor `AbstractInvokable` and remove `StatefulTask` interface to implement RAII pattern for task runtime classes. Tasks now receive all required state via constructor instead of setter methods.

Why
---
- Enable RAII (Resource Acquisition Is Initialization) pattern for cleaner lifecycle management
- Improve immutability by making `environment` field final
- Consolidate checkpointing logic from `StatefulTask` into `AbstractInvokable`
- Eliminate two-phase initialization (construct → set environment → set state)

Changes
-------
**AbstractInvokable:**
- Add constructor accepting `Environment` and optionally `TaskStateSnapshot`
- Remove `setEnvironment()` method
- Make `environment` field final
- Move checkpointing methods (`triggerCheckpoint()`, `triggerCheckpointOnBarrier()`, `abortCheckpointOnBarrier()`, `notifyCheckpointComplete()`) from `StatefulTask` to base class

**StatefulTask interface:**
- Delete entirely
- All functionality merged into `AbstractInvokable`

**Task instantiation:**
- Add `loadAndInstantiateInvokable()` method in `Task.java` using reflection
- Support two constructor patterns: `(Environment, TaskStateSnapshot)` and `(Environment)`
- Fallback to stateless constructor when no initial state provided

**All task implementations:**
- Add constructors accepting `Environment` (required)
- Add constructors accepting `Environment, TaskStateSnapshot` for stateful tasks
- Call `super(environment)` or `super(environment, initialState)`
- Update: `OneInputStreamTask`, `TwoInputStreamTask`, `SourceStreamTask`, `DataSourceTask`, `DataSinkTask`, `BatchTask`, iterative tasks, ...

**Test infrastructure:**
- Refactor test harnesses to use task factory functions instead of instances
- Change from `new OneInputStreamTask<>()` to `OneInputStreamTask::new`
- Update harnesses: `OneInputStreamTaskTestHarness`, `TwoInputStreamTaskTestHarness`, `StreamTaskTestHarness`
- Add `invoke(TaskStateSnapshot)` methods to test harnesses
- Update 100+ test classes...