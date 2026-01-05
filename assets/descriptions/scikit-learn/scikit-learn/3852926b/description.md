# Title
-----
Refactor API reference structure with modular pages and search functionality

# Summary
-------
Refactors the API reference from a single monolithic page (`modules/classes.rst`) to a modular, template-based system with individual module pages and searchable table of all objects.

# Why
---
- Single-page API reference was hard to navigate and maintain
- No search/filter functionality for API objects
- Template fragmentation (10+ templates for classes, functions, etc.)
- Inconsistent module docstrings across codebase

# Architecture Changes
---
- **Remove** `doc/modules/classes.rst` (1900+ lines)
- **Add** `doc/api_reference.py`: Python config defining API structure with modules, sections, descriptions
- **Add** RST templates: `index.rst.template`, `module.rst.template`, `deprecated.rst.template`
- Generate `doc/api/*.rst` at build time from templates + configuration
- Update `.gitignore` to exclude generated `api/*.rst` files

# Search & Navigation
---
- Implement searchable/filterable table on `api/index.html` using DataTables.js
- Add `autoshortsummary` Sphinx extension for inline short summaries
- Custom styling via `api-search.scss` for light/dark theme compatibility

# Template Consolidation
---
- Replace 10+ specific templates (`class.rst`, `function.rst`, `deprecated_*.rst`, etc.) with single `base.rst`
- Add `override_pst_pagetoc.py` extension to customize PyData Sphinx Theme's secondary sidebar for API pages

# Documentation Quality
---
- Refactor docstrings in 30+ modules (`__init__.py` files) for brevity and consistency
- Add cross-references to User/Developer guides in `api_reference.py`
- Structure API reference with titled sections and descriptions per module

# Build System
---
- Update `Makefile` and `make.bat` to clean `api/*.rst` on `make clean`
- Modify `conf.py` to render templates at build time using Jinja2
- Add redirect: `modules/classes` → `api/index`
- Update CI build script path reference

# Styling Improvements
---
- Add `api.scss`: Compact styling for generated API pages (admonitions, docstrings, method lists)
- Add `api-search.scss`: Override DataTables defaults for theme consistency
- Custom JS (`api-search.js`) to initialize search table