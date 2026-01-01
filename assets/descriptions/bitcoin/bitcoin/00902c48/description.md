# Rename `rpc-tests` directory to `functional`

## Summary
Rename `test/rpc-tests/` directory to `test/functional/` to better reflect the actual scope of the tests contained within.

## Why
The tests in the `rpc-tests` directory test more than just the RPC interface—they cover broader functional/integration testing of Bitcoin Core. The current name is misleading.

## Changes Required

**Directory Structure**
- Move `test/rpc-tests/` → `test/functional/`
- Move all test files and subdirectories accordingly
- Move `test/rpc-tests/test_framework/` → `test/functional/test_framework/`

**Build System Updates**
- Update `Makefile.am`: rename coverage targets (`rpc_test*` → `functional_test*`)
- Update `.travis.yml`: fix path references
- Update `configure.ac`: adjust config file paths
- Update `EXTRA_DIST` paths

**Documentation Updates**
- `README.md`: update test path references
- `test/README.md`: change "rpc-tests" → "functional"
- `doc/developer-notes.md`: update example paths
- `test/pull-tester/rpc-tests.py`: update comments ("RPC tests" → "Functional tests")

**Code References**
- Update all hardcoded paths in scripts (e.g., `tests_dir = src_dir + '/test/functional/'`)
- Update exclude paths in `contrib/devtools/copyright_header.py`
- Update class/variable documentation and comments

**Terminology**
- Replace "RPC test" with "functional test" in comments/error messages where appropriate
- Keep terminology consistent throughout codebase