# Refactor Series Tests into Organized Directory Structure

## Summary
Reorganize `test_series.py` into a structured directory hierarchy to improve test organization and maintainability.

## Structure
Split monolithic test file into:
- `test/series/indexing/*` - Tests for loc/iloc/`__getitem__`/`__setitem__`
- `test/series/methods/*` - Tests for `Series.<method>` (e.g., `fillna`, `drop`, `round`, etc.)
- `test/series/test_constructors.py` - Series construction tests
- `test/series/test_binops.py` - Binary operations tests
- `test/reshape/test_concat.py` - Concat-related tests

## Changes
- Extract method-specific tests into individual files under `series/methods/`:
  - `test_add_prefix_suffix.py`, `test_astype.py`, `test_autocorr.py`, `test_between.py`, `test_contains.py`, `test_count.py`, `test_describe.py`, `test_diff.py`, `test_digitize.py`, `test_drop.py`, `test_duplicated.py`, `test_equals.py`, `test_explode.py`, `test_factorize.py`, `test_fillna.py`, `test_hash_values.py`, `test_isin.py`, `test_isna_notnull.py`, `test_memory_usage.py`, `test_mode.py`, `test_nans_to_nulls.py`, `test_nlargest_nsmallest.py`, `test_nunique.py`, `test_pipe.py`, `test_reindex.py`, `test_rename.py`, `test_reset_index.py`, `test_round.py`, `test_sort_index.py`, `test_squeeze.py`, `test_to_*.py`, `test_transpose.py`, `test_truncate.py`, `test_update.py`, `test_value_counts.py`, `test_where.py`
- Extract indexing tests into `series/indexing/test_setitem.py`
- Move constructor tests to `test_constructors.py`
- Move binary operations to `test_binops.py`
- Add shared fixtures to `conftest.py`:
  - `numeric_and_bool_types_as_str`, `datetime_types_as_str`, `timedelta_types_as_str`, `temporal_types_as_str`
  - `dropna`, `nan_as_null`, `inplace`, `ignore_index`, `ascending`
- Remove empty stub files: `test_accessors.py`, `test_binary_operations.py`, `test_categorial.py`, `test_combining.py`, `test_computation.py`, `test_function_application.py`, `test_indexing.py`, `test_io_serialization.py`, `test_missing.py`, `test_reshaping.py`, `test_selecting.py`, `test_sorting.py`, `test_timeseries.py`
- Update existing files with minimal changes (copyright year, imports)

## Benefits
- Easier navigation and discovery of tests
- Better separation of concerns
- Improved test maintainability
- Consistent structure across test suite