Title
-----
Remove `mock` dependency and migrate to `unittest.mock`

Summary
-------
Replace external `mock` package with Python's built-in `unittest.mock` module across entire test suite.

Why
---
Python 3.3+ includes `unittest.mock` in stdlib, making external `mock` package unnecessary. This reduces dependencies and simplifies project requirements.

Changes
-------
- Remove `mock==1.3.0` from `requirements-test.txt`
- Update `awscli/testutils.py` to import from `unittest.mock` instead of attempting standalone `mock` import
- Replace all `import mock` / `from mock import ...` statements with `from unittest import mock` across test files
- Update imports in `tests/functional/...` test modules
- Update imports in `tests/unit/...` test modules  
- Update imports in `tests/integration/...` test modules
- Adjust mock-related imports to use `awscli.testutils.mock` or `tests.mock` where appropriate

Scope
-----
All test files under:
- `tests/functional/...`
- `tests/unit/...`
- `tests/integration/...`
- `awscli/testutils.py`

No functional changes to test behavior or logic.