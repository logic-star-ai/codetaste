# Title
Rename `trax.math` package to `trax.fastmath`

# Summary
Refactor the `trax.math` package to `trax.fastmath` to better reflect its purpose (accelerated NumPy-style math operations) and improve code consistency across the codebase.

# Changes Required

## Package Renaming
- Rename directory: `trax/math/` → `trax/fastmath/`
- Update module docstring to: `"Trax fast math -- NumPy-style math on accelerators"`
- Update all package imports: `from trax import math` → `from trax import fastmath`
- Update internal imports: `trax.math.*` → `trax.fastmath.*`

## Code Cleanup
- Change fastmath.numpy alias from `np` to `jnp` throughout codebase
- Remove Python 2 compatibility imports (`from __future__ import ...`)
- Fix minor docstring typos encountered during refactoring

## Documentation Updates
- Update `README.md` link: `math/` → `fastmath/`
- Update Sphinx docs: `trax.math.rst` → `trax.fastmath.rst`
- Update Jupyter notebooks with new import paths
- Update test scripts and CI configurations

## Affected Areas
- `trax/__init__.py`
- `trax/layers/...`
- `trax/models/...`
- `trax/optimizers/...`
- `trax/rl/...`
- `trax/supervised/...`
- Tests and examples