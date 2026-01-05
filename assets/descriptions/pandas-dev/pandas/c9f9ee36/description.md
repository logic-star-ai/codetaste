Title
-----
CLN: De-privatize core.common functions, remove unused utilities

Summary
-------
Clean up `pandas.core.common` module by:
- Removing underscore prefix from internal functions (de-privatizing)
- Moving console detection functions to `io.formats.console`
- Removing functions only used in tests or not used at all

Why
---
- Functions like `asarray_tuplesafe`, `values_from_object`, `get_callable_name`, etc. were marked private with `_` prefix but are widely used internally
- Console-related functions (`in_interactive_session`, `in_qtconsole`, `in_ipnb`, `in_ipython_frontend`) belong in `io.formats.console` module, not `core.common`
- Several utility functions (`_mut_exclusive`, `iterpairs`, `split_ranges`, `_long_prod`, custom `groupby`, `map_indices_py`, `union`, `difference`, `intersection`) were never used outside tests or are dead code

Changes
-------
**De-privatize (remove underscore prefix):**
- `_asarray_tuplesafe` → `asarray_tuplesafe`
- `_values_from_object` → `values_from_object`
- `_get_callable_name` → `get_callable_name`
- `_apply_if_callable` → `apply_if_callable`
- `_dict_compat` → `dict_compat`
- `_maybe_box_datetimelike` → `maybe_box_datetimelike`
- `_maybe_box` → `maybe_box`
- `_get_info_slice` → `get_info_slice`
- `_consensus_name_attr` → `consensus_name_attr`
- `_count_not_none` → `count_not_none`
- `_try_sort` → `try_sort`
- `_dict_keys_to_ordered_list` → `dict_keys_to_ordered_list`
- `_index_labels_to_array` → `index_labels_to_array`
- `_maybe_make_list` → `maybe_make_list`
- `_random_state` → `random_state`
- `_get_distinct_objs` → `get_distinct_objs`

**Move to `io.formats.console`:**
- `in_interactive_session`
- `in_qtconsole`
- `in_ipnb`
- `in_ipython_frontend`

**Remove entirely:**
- `_mut_exclusive`
- `iterpairs`
- `split_ranges`
- `_long_prod`
- `groupby` (custom implementation)
- `map_indices_py`
- `union`
- `difference`
- `intersection`

**Update all references** throughout codebase to use new names/locations

Notes
-----
- Left `_any_not_none`, `_all_not_none`, `_not_none` as-is (candidates for future removal in favor of Python builtins)
- Added whatsnew entry for removed functions
- `pandas.core.common` is not part of public API