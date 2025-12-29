Title
-----
Simplify Node API: Better defaults for ChoiceParam and numeric range parameters

Summary
-------
Refactor node parameter API to use more intuitive defaults, reducing boilerplate in node descriptions.

Changes
-------
- `ChoiceParam`: `exclusive` now defaults to `True` (previously required explicit specification)
- `IntParam`/`FloatParam`: `range` now defaults to `None` (previously required)
- Remove `exclusive=True` from all node definitions across codebase (~100+ occurrences)

Why
---
Most `ChoiceParam` attributes are exclusive (single selection), making `exclusive=True` the overwhelming majority case. Setting it as default eliminates repetitive boilerplate.

For numeric params, not all attributes need range constraints/sliders. Making `range` optional allows text field fallback when slider constraints are unnecessary.

Technical Details
-----------------
- `desc.py`: Updated param constructors with new defaults
- All AliceVision nodes: Stripped redundant `exclusive=True` declarations
- Blender nodes: Same cleanup applied
- No behavior changes for existing nodes (purely simplification)
- UI behavior: `range=None` → text field instead of slider
- Validation: Still enforced when range is specified

Impact
------
- Cleaner, more readable node descriptions
- Easier to write new nodes (less required boilerplate)
- Backward compatible (existing behavior preserved)