Consolidate tf.data options implementation into single module

Summary
-------
Move all tf.data options-related classes from scattered experimental modules into a single `tensorflow/python/data/ops/options.py` module.

Why
---
Options classes (`Options`, `OptimizationOptions`, `DistributeOptions`, `ThreadingOptions`) and enums (`AutoShardPolicy`, `ExternalStatePolicy`) are currently scattered across multiple experimental modules, creating maintenance burden and unclear code organization.

Changes
-------
- Create new `tensorflow/python/data/ops/options.py` containing:
  - `Options` (moved from `dataset_ops.py`)
  - `OptimizationOptions` (from `experimental/ops/optimization_options.py`)
  - `DistributeOptions` (from `experimental/ops/distribute_options.py`)
  - `ThreadingOptions` (from `experimental/ops/threading_options.py`)
  - `AutoShardPolicy` enum
  - `ExternalStatePolicy` enum

- Delete obsolete files:
  - `experimental/ops/optimization_options.py`
  - `experimental/ops/distribute_options.py`
  - `experimental/ops/threading_options.py`

- Update imports across:
  - All benchmark files
  - All test files
  - Production code (distribute, keras, etc.)
  - From `dataset_ops.Options` → `options_lib.Options`
  - From `experimental.ops.*_options` → `ops.options`

- Update BUILD dependencies accordingly

Impact
------
Internal refactoring only. Public API surface remains unchanged via `tf_export` decorators. All existing tests should continue passing.