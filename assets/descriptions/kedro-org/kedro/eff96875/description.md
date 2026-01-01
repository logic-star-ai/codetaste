# Title
Rename `KedroDataCatalog` to `DataCatalog`

# Summary
Rename the experimental `KedroDataCatalog` class to `DataCatalog` across the entire codebase, including core implementation, tests, documentation, and examples.

# Why
The experimental `KedroDataCatalog` is being promoted as the default catalog implementation. The naming should reflect this by removing the "Kedro" prefix and making it the standard `DataCatalog` class.

# Changes Required

## Core Implementation
- Rename `kedro/io/kedro_data_catalog.py` → `kedro/io/data_catalog.py`
- Rename class `KedroDataCatalog` → `DataCatalog` in implementation
- Update all imports from `kedro.io.KedroDataCatalog` to `kedro.io.DataCatalog`
- Update `__init__.py` exports
- Update default `DATA_CATALOG_CLASS` in project settings

## Tests
- Rename `tests/io/test_kedro_data_catalog.py` → `tests/io/test_data_catalog.py`
- Update all test class names from `TestKedroDataCatalog` → `TestDataCatalog`
- Update all instantiations in test files

## Documentation
- Remove experimental feature page `docs/pages/catalog-data/kedro_data_catalog.md`
- Update all references in docs from `KedroDataCatalog` to `DataCatalog`
- Update code examples in tutorials and guides
- Update docstrings and error messages
- Update settings templates

## Other Files
- Update benchmark files
- Update example notebooks
- Update starter templates
- Update `.secrets.baseline`
- Update `mkdocs.yml` navigation

# Scope
This is a pure refactoring task focused on renaming. No functional changes to the catalog implementation itself.