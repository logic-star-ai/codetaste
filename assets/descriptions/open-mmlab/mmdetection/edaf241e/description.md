# Refactor: Restructure Unit Test File Organization

## Summary
Reorganize unit test files from flat structure into hierarchical directory layout by component type, splitting large test files into smaller focused modules.

## Why
- Large monolithic test files difficult to navigate/maintain
- Flat structure made test discovery challenging
- Memory usage issues during test execution
- Poor separation of concerns

## Changes

### Test Data/Datasets
- Split `test_dataset.py` → `test_datasets/*.py`:
  - `test_common.py` - general dataset tests
  - `test_custom_dataset.py` - custom class overrides
  - `test_dataset_wrapper.py` - ConcatDataset/RepeatDataset/...
  - `test_xml_dataset.py` - XML dataset specific

### Pipelines
- Moved `test_*.py` → `test_pipelines/*.py`:
  - `test_formatting.py`, `test_loading.py`, `test_sampler.py`
  - Transforms → `test_pipelines/test_transform/*.py`

### Models
- `test_backbones.py` → `test_backbones/*.py` (per architecture):
  - `test_resnet.py`, `test_resnext.py`, `test_res2net.py`, ...
  - Shared utils in `test_backbones/utils.py`

- `test_heads.py` → split by head type:
  - `test_dense_heads/*.py` - anchor/FCOS/corner/transformer/...
  - `test_roi_heads/*.py` - bbox/mask/SABL/...

- `test_losses.py` → `test_metrics/test_losses.py`
- `test_iou2d_calculator.py` → `test_metrics/test_box_overlap.py`
- Position encoding/transformer → `test_utils/*.py`

### Runtime
- Runtime tests → `test_runtime/`:
  - `test_config.py`, `test_async.py`, `test_eval_hook.py`
  - `async_benchmark.py`
  - Added `test_fp16.py`

### Utils
- Core utils → `test_utils/`:
  - `test_anchor.py`, `test_assigner.py`, `test_coder.py`
  - `test_masks.py`, `test_visualization.py`, ...

## Benefits
- Easier test discovery/navigation
- Reduced memory per test module
- Better separation of concerns
- Improved maintainability
- Clearer test organization by component