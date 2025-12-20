# Title
Remove Python 2/3 compatibility flags from tests

# Summary
Remove `compat.PY2` and `compat.PY3` flags from test suite after dropping Python 2 support.

# Why
After dropping Python 2 support (#25725), the PY2/PY3 compatibility flags in tests are no longer needed and add unnecessary complexity.

# What Changed
- Removed `@pytest.mark.skipif(PY2, ...)` and `@pytest.mark.skipif(not PY3, ...)` decorators
- Removed conditional `if PY2:` / `if PY3:` branches, keeping only Python 3 code paths
- Removed `from pandas.compat import PY2, PY3` imports
- Simplified test assertions that had different expectations for Python 2 vs 3
- Removed Python 2-specific test cases and error handling

# Files Affected
- `tests/arithmetic/...`
- `tests/arrays/...`
- `tests/computation/...`
- `tests/dtypes/...`
- `tests/extension/...`
- `tests/frame/...`
- `tests/generic/...`
- `tests/groupby/...`
- `tests/indexes/...`
- `tests/indexing/...`
- `tests/io/...`
- `tests/plotting/...`
- `tests/reductions/...`
- `tests/reshape/...`
- `tests/scalar/...`
- `tests/series/...`
- `tests/sparse/...`
- `tests/test_*.py`

# Examples
- Removed truediv vs div distinction for division operators
- Unified unicode/string handling (always unicode in PY3)
- Removed encoding-related conditional logic
- Simplified regex matching in pytest.raises (works differently in PY2)