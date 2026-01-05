# Consolidate project definition into `pyproject.toml`

## Summary

Migrate project metadata, dependencies, and build configuration from `setup.cfg` and `setup.py` to `pyproject.toml` following modern Python packaging standards (PEP 621).

## Why

- `pyproject.toml` is the new preferred way for Python project definition
- Future distributions should use a single source of truth
- Simplifies multi-distribution project management
- Reduces configuration fragmentation

## Changes

**Core refactoring:**
- Remove `setup.cfg` and `setup.py` entirely
- Migrate all metadata, dependencies, and options to `pyproject.toml`
- Update all file references (`setup.cfg` → `pyproject.toml`) across...
  - `Dockerfile` / `Dockerfile.s3`
  - `Makefile`
  - `bin/release-helper.sh`
  - Documentation and dev tools

**Dependency management:**
- Replace `%(extra)s` syntax with recursive package references (e.g., `"localstack-ext[runtime]"`)
- Mark package itself as unsafe for pinning
- Upgrade all pinned dependencies
- Add `build` package as new dependency

**Build process:**
- Use `python -m build` instead of `setup.py sdist bdist_wheel`
- Use `plux` for entrypoint generation

**Pre-commit hooks:**
- Update to support `pyproject.toml` in pinned dependency checker
- Align black version with pinned version
- Black now properly detects Python 3.8 target from `pyproject.toml` → reformat generated AWS APIs

**Files modified:**
- `.pre-commit-config.yaml`
- All `requirements-*.txt` files
- All generated AWS API files (`localstack/aws/api/*/__init__.py`)
- Various utility files referencing setup configs