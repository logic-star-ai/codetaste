# Summary

This testing setup configures the Rust compiler repository for running tidy checks, which validate code formatting, style guidelines, and other linting rules. The setup avoids building the full compiler or LLVM, making it fast and portable.

## System Dependencies

The following system-level dependencies are pre-installed in the environment:
- **Python 3** (3.12.3+) - Required for the x.py build system
- **GCC/G++** (13.x) - C/C++ compiler
- **CMake** (3.28.3+) - Build system (not used by tidy but part of standard dev environment)
- **Git** - Version control
- **OpenSSL development libraries** - Required for building Rust tools
- **pkg-config** - Build configuration helper

No additional system services (databases, Redis, etc.) are required for running the tidy tests.

## Project Environment

The project uses the Rust compiler's bootstrap build system (`x.py`) with the following configuration:

- **Build System**: Python-based x.py bootstrap script
- **Stage0 Compiler**: Downloaded from rust-lang.org (beta/nightly versions)
- **LLVM**: Disabled (not needed for tidy checks)
- **Configuration**: Minimal `config.toml` created by `setup_shell.sh`:
  - `download-ci-llvm = false` - Avoids 404 errors on older commits
  - `ninja = false` - Disables ninja requirement
  - `download-rustc = false` - Uses bootstrap compiler

### Key Directories

- `/testbed` - The Rust compiler source repository
- `/testbed/build` - Build artifacts (created during setup, ignored by git)
- `/testbed/src/tools/tidy` - The tidy tool source code
- `/testbed/config.toml` - Build configuration (created by setup, ignored by git)

## Testing Framework

**Test Suite**: Tidy Checks

The tidy tool (`src/tools/tidy`) performs three main checks:

1. **fmt check** - Validates code formatting using rustfmt
2. **tidy check** - Performs various linting rules (line lengths, file conventions, etc.)
3. **x.py completions check** - Validates shell completion scripts

**Execution**: `python3 x.py test tidy`

**Output Format**: The test script parses tidy's output and reports:
- **Passed**: Number of checks that succeeded (3 when all pass)
- **Failed**: Number of checks that failed (0 when all pass)
- **Skipped**: Always 0 (tidy doesn't skip checks)
- **Total**: Total number of checks performed

**Typical Runtime**: 20-40 seconds after initial setup (includes compiling tidy tool)

## Additional Notes

### Design Decisions

1. **Tidy vs Compiler Tests**: We use tidy checks instead of full compiler tests because:
   - They don't require building LLVM (saves hours of build time)
   - They don't require a full stage0/stage1 compiler build
   - They complete in under a minute
   - They provide meaningful validation of code quality
   - They work consistently across different commits

2. **LLVM Download Disabled**: The `download-ci-llvm` feature is disabled because:
   - Older commits may have 404 errors when trying to download CI artifacts
   - Tidy checks don't need LLVM at all
   - This makes the setup portable across different commit ages

3. **Portability**: The scripts work on both HEAD and HEAD~1 because:
   - The x.py build system is stable across commits
   - Tidy tool interface hasn't changed significantly
   - Config options used are long-standing and stable

### Potential Issues

- **Submodule Updates**: The first run downloads Git submodules (cargo, backtrace). This is expected and handled automatically.
- **Stage0 Compiler**: The bootstrap process downloads ~100MB of stage0 compiler artifacts on first run.
- **Build Cache**: The `/testbed/build/` directory is created and used for caching. It's properly ignored by git.

### Alternative Test Suites

If more comprehensive testing is needed in the future, consider:
- `python3 x.py test library/std --stage 0` - Standard library tests (requires building stage0 compiler)
- `python3 x.py test tests/ui/parser --stage 0` - Parser tests (~745 tests, needs compiler)
- `python3 x.py test tests/codegen-units --stage 0` - Codegen tests (~52 tests, needs LLVM)

However, these require significant build time (30+ minutes for first run) and are less portable across commits.
