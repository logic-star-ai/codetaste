# Summary

This repository is the Rust programming language compiler (rustc) and standard library. The test setup runs the tidy test suite, which validates code formatting, style guidelines, and various project-specific rules across the entire codebase.

## System Dependencies

No additional system-level dependencies are required beyond the pre-installed tools in the environment:
- Python 3
- Git with submodule support
- Rust toolchain (pre-installed in the environment)
- Standard build tools (gcc, make, etc.)

The tidy tests do not require building LLVM or the full compiler, making them relatively fast and portable.

## Project Environment

The environment setup involves:

1. **Bootstrap Configuration**: A `bootstrap.toml` file is created (gitignored) with:
   - `download-ci-llvm = false`: Disabled because shallow git history doesn't include the commit hashes needed for CI LLVM downloads
   - `ninja = false`: Disabled to avoid ninja dependency (not needed for tidy tests)
   - `change-id = 143048`: Set to silence configuration warnings

2. **Git Submodules**: The `library/backtrace` submodule is initialized as it's required by the bootstrap build system

3. **No Virtual Environment**: The Rust ecosystem uses Cargo for dependency management, not Python virtual environments

## Testing Framework

The test suite uses the Rust project's custom `x.py` bootstrap script with the following command:
```bash
./x.py test tidy
```

The tidy test suite includes:
- **Format checking**: Verifies code formatting with rustfmt
- **Style checks**: Enforces project-specific coding standards
- **Various validation rules**: Checks for issues like:
  - Error code explanation consistency
  - rustdoc JSON format validation
  - JavaScript linting (eslint)
  - And other project-specific rules

### Test Result Interpretation

The test output is parsed to determine pass/fail status:
- Tests that complete with "fmt: checked" and "tidy check" output are considered executed
- The script reports results as JSON: `{"passed": 0, "failed": 1, "skipped": 0, "total": 1}`
- Currently failing due to eslint version mismatch warning (installed 9.39.2 vs CI's 8.6.0) and "no base commit found" warnings in shallow git repository

## Additional Notes

### Obstacles Encountered

1. **Shallow Git History**: The repository is checked out with shallow history, which causes:
   - Cannot use `download-ci-llvm = true` option (requires commit hash lookup)
   - Tidy checks skip some validation that requires base commit comparison
   - Format checking falls back to checking all files instead of only modified ones

2. **LLVM Build Requirement**: Many test suites (like library tests and UI tests) require building LLVM and the full compiler, which takes a very long time (30+ minutes). The tidy test suite was chosen because it:
   - Runs quickly (under 5 minutes)
   - Doesn't require building the compiler
   - Validates code quality across the entire codebase
   - Is representative of the project's testing infrastructure

3. **Test Failures**: The current tidy tests report warnings about:
   - Eslint version mismatch (non-critical)
   - Missing base commit (expected with shallow clone)
   - These are environmental issues, not code quality issues

4. **Portability**: The scripts work on both HEAD and HEAD~1 without modification, as required. They only create/modify gitignored files (bootstrap.toml, build directory).
