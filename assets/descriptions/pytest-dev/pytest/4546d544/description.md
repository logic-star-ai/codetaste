# Title
Consolidate linting and formatting tools by migrating to ruff

# Summary
Replace multiple Python code quality tools (`autoflake`, `black`, `isort`, `pyupgrade`, `flake8`, `pydocstyle`) with a single unified tool: `ruff`.

# Why
- Running 6+ separate tools for linting/formatting adds complexity and overhead
- `ruff` provides equivalent functionality with significantly better performance
- Single tool → simpler configuration, faster CI, easier maintenance

# Changes
**Pre-commit hooks:**
- Remove: `black`, `autoflake`, `flake8`, `isort`, `pyupgrade`
- Add: `ruff` (with `--fix`) and `ruff-format`
- Keep: `blacken-docs` (ruff doesn't support this yet)

**Configuration:**
- Add `[tool.ruff]` section to `pyproject.toml` with:
  - Import sorting rules (equivalent to previous `isort` config)
  - Code style rules (E, F, W, D, UP)
  - Ignored rules (match previous `flake8`/`pydocstyle` exceptions)
  - Line length = 88, docstring formatting enabled
- Remove `[flake8]` and `[isort]` sections from `tox.ini`

**Codebase:**
- Apply ruff auto-formatting across all `.py` files
  - Import reordering (two blank lines after imports)
  - Minor formatting adjustments
  - f-string conversions where applicable
- Update `.git-blame-ignore-revs` to skip this formatting commit in blame

**Documentation:**
- Remove black badge from `README.rst`

# Notes
- Some churn expected due to different formatting opinions between tools
- Configuration aims to maintain existing code style as much as possible
- Follow-up to #11896