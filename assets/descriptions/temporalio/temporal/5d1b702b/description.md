# Title
-----
Split MutableState interface from implementation

# Summary
-------
Move `MutableState` interface + related types to `service/history/interfaces` package, separating interface from implementation to reduce code entanglement and dependency graph bloat.

# Why
---
Currently, interface and implementation reside in same file → bloats dependency graph → encourages bad practices when dealing with module cyclic dependencies.

Part of larger effort to split interfaces for:
* Engine
* MutableState ✓
* Shard Context
* Workflow Context

# What Changed
-------------
* **Moved to `interfaces` package:**
  - `MutableState` interface
  - `WorkflowTaskInfo` struct
  - `WorkflowTaskCompletionLimits` struct
  - `QueryRegistry` interface
  - `QueryCompletionState` struct
  - `TransactionPolicy` type
  
* **Updated imports:** All references now use `historyi "go.temporal.io/server/service/history/interfaces"`

* **Implementation stays:** `MutableStateImpl` remains in `workflow` package

* **Mock updates:** Generated mocks moved to interfaces package

# Files Affected
--------------
* Interface definitions: `service/history/interfaces/*`
* Implementation: `service/history/workflow/mutable_state_impl.go`
* ~100+ files updated with new import paths across:
  - API handlers
  - NDC components
  - Task executors
  - Queue processors
  - Tests

# Testing
--------
Existing tests pass (no functional changes)