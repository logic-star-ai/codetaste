Title
-----
Rename `qa` directory to `test`

Summary
-------
Rename the `qa` directory to `test` throughout the codebase, updating all paths and references accordingly.

Why
---
- Directory should come after `/src` alphabetically for better git diff/PR ordering
- More intuitive naming (tests live in `test/`, source in `src/`)
- Improves project structure consistency

What
----
- Move `qa/*` → `test/*`
- Update path references in:
  - `Makefile.am` (coverage targets, EXTRA_DIST, clean-local, ...)
  - `README.md` (test documentation links)
  - `configure.ac` (AC_CONFIG_FILES, AC_CONFIG_LINKS, sed commands)
  - `contrib/devtools/copyright_header.py` (EXCLUDE paths)
  - `contrib/rpm/bitcoin.spec` (test invocation)
  - `doc/developer-notes.md` (test references)
  - All internal `test/` documentation files

Changes
-------
- `qa/` → `test/`
- `qa/pull-tester/` → `test/pull-tester/`
- `qa/rpc-tests/` → `test/rpc-tests/`
- All script imports/references updated
- Build system paths updated
- Documentation links updated