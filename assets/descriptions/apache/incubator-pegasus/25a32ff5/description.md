# Title
Refactor: Extract task module from runtime

## Summary
Move `task` module from `runtime/task/` to standalone `task/` directory to reduce library size and dependencies.

## Why
- Reduce coupling between task and runtime modules
- Smaller, more focused libraries
- Clearer dependency boundaries

## What Changed
**Directory Structure**
- Move `src/runtime/task/*` → `src/task/*`
- Create `src/task/tests/` with dedicated test suite

**Files Moved**
- `async_calls.h`, `future_types.h`, `task.{h,cpp}`, `task_code.{h,cpp}`
- `task_engine.{h,cpp}`, `task_engine.sim.{h,cpp}`
- `task_queue.{h,cpp}`, `task_spec.{h,cpp}`, `task_tracker.{h,cpp}`
- `task_worker.{h,cpp}`, `timer_service.h`
- `hpc_task_queue.{h,cpp}`, `simple_task_queue.{h,cpp}`

**Include Path Updates**
- `runtime/task/...` → `task/...` throughout codebase
  - ~200+ files updated across `aio/`, `block_service/`, `client/`, `meta/`, `replica/`, `rpc/`, `server/`, etc.

**Build System**
- New `src/task/CMakeLists.txt` for `dsn_task` library
- New `src/task/tests/CMakeLists.txt` for `dsn_task_tests`
- Update `dsn_runtime` to link `dsn_task`
- Add `dsn_task_tests` to CI workflows

**Tests**
- Create dedicated test suite: `dsn_task_tests`
- Move tests: `async_call_test.cpp`, `lpc_test.cpp`, `task_engine_test.cpp`
- Add test configs: `config-test.ini`, `config-test-sim.ini`

**Cleanup**
- Remove duplicate comments from various `CMakeLists.txt`
- Update `.licenserc.yaml` paths

## Notes
- Pure refactor, no functional changes
- All tests passing
- No API changes for consumers