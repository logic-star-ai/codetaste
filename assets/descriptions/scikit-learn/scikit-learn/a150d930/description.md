# Refactor: Drop SciPy < 0.13 support and remove backport code

## Summary
Remove backport implementations for SciPy < 0.13 compatibility and replace with direct SciPy imports throughout the codebase.

## Why
- Reduce code duplication and maintenance burden
- Simplify codebase by removing ~2000 lines of backport code
- SciPy 0.13+ is now minimum supported version
- Use optimized SciPy implementations directly

## Changes

### Removed backports from `utils.fixes`
- `expit` → use `scipy.special.expit`

### Deprecated backports in `utils.extmath`
- `logsumexp` → `scipy.misc.logsumexp`
- `norm` → `scipy.linalg.norm`
- `pinvh` → `scipy.linalg.pinvh`

### Deprecated entire `utils.arpack` module
- `eigs` → `scipy.sparse.linalg.eigs`
- `eigsh` → `scipy.sparse.linalg.eigsh`
- `svds` → `scipy.sparse.linalg.svds`

### Deprecated `utils.stats.rankdata`
- `rankdata` → `scipy.stats.rankdata`

### Deprecated `utils.sparsetools.connected_components`
- `connected_components` → `scipy.sparse.csgraph.connected_components`
- Remove graph traversal Cython implementations (`_traversal.pyx`, `_graph_tools.pyx`)

### Updated imports across modules
- cluster, covariance, cross_decomposition, decomposition, ensemble, feature_extraction, feature_selection, linear_model, manifold, metrics, mixture, model_selection, naive_bayes, neighbors, neural_network
- Examples updated to handle SciPy API differences

### Cleanup
- Remove SciPy version checks for < 0.13
- Update documentation (remove backport references from utilities guide)
- Add deprecation warnings with scheduled removal in 0.21