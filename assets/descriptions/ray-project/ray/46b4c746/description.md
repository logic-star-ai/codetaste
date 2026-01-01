# Rename Ray SGD v2 to Ray Train

## Summary
Rebrand the Ray SGD v2 library to Ray Train to reduce confusion and better reflect its purpose as a general distributed deep learning library on Ray.

## Why
The "Ray SGD" name has led to confusion. "Ray Train" better communicates that this is a library for distributed training on Ray, not limited to SGD optimization.

## Changes

### Code Structure
- Create new `ray.train` module, move all code from `ray.util.sgd.v2`
- `ray.util.sgd.v2` imports from `ray.train` with deprecation warning
- `ray.sgd` raises `DeprecationWarning`

### Renamed Entities
- Classes:
  - `SGDIterator` → `TrainingIterator`
  - `SGDWorkerGroup` → `TrainWorkerGroup`  
  - `SGDCallback` → `TrainingCallback`
  - `SGDBackendError` → `TrainBackendError`
- Log directories: `sgd_<datetime>` → `train_<datetime>`
- Environment variables:
  - `SGD_RESULT_ENABLE_DETAILED_AUTOFILLED_METRICS` → `TRAIN_RESULT_ENABLE_DETAILED_AUTOFILLED_METRICS`
  - `SGD_ENABLE_SHARE_CUDA_VISIBLE_DEVICES` → `TRAIN_ENABLE_SHARE_CUDA_VISIBLE_DEVICES`

### Tests & CI
- Move tests/examples from `ray/util/sgd/v2` to `ray/train`
- Update buildkite pipelines with Train steps (🚂 emoji)
- Add `RAY_CI_TRAIN_AFFECTED` flag

### Documentation
- Move docs from `doc/source/raysgd/v2` to `doc/source/train`
- Replace all "Ray SGD v2" references with "Ray Train"
- Update API references, user guides, examples

### Backwards Compatibility
- `ray.util.sgd.v2.*` continues to work with deprecation warnings
- Maintains import compatibility for smooth migration