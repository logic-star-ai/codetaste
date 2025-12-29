# Title
-----
Move UNet models to dedicated `unets` submodule

# Summary
-------
Reorganize UNet-related models from `models/` to `models/unets/` to improve code organization and mirror the structure used for `autoencoders`.

# Why
---
- Better code organization following established patterns (`autoencoders` module precedent)
- Cleaner separation of concerns within the models directory
- Improved discoverability of UNet variants

# Scope
------
Move the following UNet variants to `models/unets/`:
- `unet_1d.py` → `unets/unet_1d.py`
- `unet_2d.py` → `unets/unet_2d.py`
- `unet_2d_condition.py` → `unets/unet_2d_condition.py`
- `unet_3d_condition.py` → `unets/unet_3d_condition.py`
- `unet_kandinsky3.py` → `unets/unet_kandinsky3.py`
- `unet_motion_model.py` → `unets/unet_motion_model.py`
- `unet_spatio_temporal_condition.py` → `unets/unet_spatio_temporal_condition.py`
- `uvit_2d.py` → `unets/uvit_2d.py`

Also move related modules:
- `unet_*_blocks.py` → `unets/unet_*_blocks.py`
- `unet_2d_condition_flax.py` → `unets/unet_2d_condition_flax.py`

# Implementation
---------------
- Create `models/unets/` submodule with proper `__init__.py`
- Move all UNet model files and blocks to new location
- Update `models/__init__.py` to reference new paths
- Maintain **backward compatibility** via deprecation wrappers in old locations
- Update all internal imports throughout codebase:
  - Pipeline imports
  - Example scripts (community, research_projects)
  - Conversion scripts
  - Test files
  - Documentation autodoc paths
- Fix relative imports within moved files
- Update `# Copied from` comments to reflect new paths

# Backward Compatibility
-----------------------
Old import paths must continue working with deprecation warnings:
```python
from diffusers.models.unet_2d_condition import UNet2DConditionModel  # deprecated but functional
from diffusers.models.unets.unet_2d_condition import UNet2DConditionModel  # new path
```