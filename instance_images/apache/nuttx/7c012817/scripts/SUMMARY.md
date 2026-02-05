# Summary

This testing setup provides code quality and validation checks for Apache NuttX, a real-time operating system (RTOS). The testing framework validates code style compliance, Python tool quality, repository structure, and basic C compilation capabilities.

## System Dependencies

The testing environment requires minimal system-level dependencies:
- **GCC Compiler**: Standard GNU C compiler for building test tools
- **Git**: Version control system (already present in repository)
- **Python 3**: For running code quality tools and pytest-based tests

No additional system services or daemons are required. The `setup_system.sh` script is a no-op that exits successfully.

## Project Environment

The project uses a Python virtual environment for dependency isolation:

### Build Tools
- **nxstyle**: Custom NuttX code style checker (compiled from `tools/nxstyle.c`)
  - Located in: `${NUTTXTOOLS}/bin/nxstyle`
  - Validates C code against NuttX coding standards

### Python Environment
- **Virtual Environment**: Created at `${NUTTXTOOLS}/venv`
- **Location**: `${NUTTXTOOLS}` defaults to `${HOME}/.nuttx-tools`

### Python Dependencies
The following Python packages are installed for code quality checks:
- **codespell**: Spell checker for source code
- **cmake-format**: CMake file formatter
- **black**: Python code formatter
- **isort**: Python import sorter
- **flake8**: Python linting tool
- **cvt2utf**: Character encoding converter

Additional pytest dependencies for runtime testing (from `tools/ci/testrun/env/requirements.txt`):
- **pexpect**: Process interaction library
- **pytest**: Testing framework
- **pytest-repeat**: Test repetition plugin
- **pytest-json**: JSON output plugin
- **pytest-ordering**: Test execution order control
- **pyserial**: Serial port communication

### Environment Variables
- `TESTBED_ROOT`: Set to `/testbed`
- `NUTTXTOOLS`: Set to `${HOME}/.nuttx-tools`
- `PATH`: Extended to include `${NUTTXTOOLS}/bin`

## Testing Framework

The test suite runs the following categories of tests:

### 1. Code Style Tests
- Validates C source files using `nxstyle` tool
- Tests files from recent git commits or a sample set
- Ensures compliance with NuttX coding standards

### 2. Python Linting Tests
- **black**: Checks Python code formatting
- **flake8**: Performs Python linting with relaxed line length limits
- Validates Python tools in `tools/ci/testrun/script/`

### 3. Spell Checking
- **codespell**: Checks for common spelling errors in documentation

### 4. Repository Structure Tests
- Validates presence of critical directories (`arch/`, `drivers/`, `sched/`)
- Checks for essential build files (`Makefile`, `Kconfig`, `CMakeLists.txt`)

### 5. Git Repository Tests
- Verifies git repository integrity
- Ensures git log is accessible

### 6. C Compilation Tests
- Compiles sample C tools to verify compiler functionality
- Tests include `nxstyle.c` and `cfgdefine.c`

## Test Execution

Tests are executed using:
```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

### Output Format
The test runner outputs results in JSON format:
```json
{"passed": N, "failed": M, "skipped": K, "total": T}
```

### Test Results
- Typical run produces 30-35 tests
- All tests should pass on a clean checkout
- Tests are deterministic and repeatable

## Additional Notes

### Idempotency
- The `setup_shell.sh` script is idempotent - safe to run multiple times
- Only creates/installs dependencies if they don't already exist
- Virtual environment is reused across runs

### Portability
- Scripts work on both HEAD and HEAD~1 commits
- No modifications to versioned files in `/testbed/`
- All build artifacts are created outside the repository or in git-ignored locations

### Limitations
This test setup focuses on code quality and static analysis rather than runtime testing because:
1. **No Cross Compilers**: Full NuttX builds require architecture-specific toolchains (ARM, RISC-V, etc.)
2. **No Hardware/Simulators**: Runtime tests require either physical boards or QEMU simulators
3. **Build Configuration**: NuttX requires board-specific configuration before building

The tests validate:
- Code style compliance (critical for NuttX contributions)
- Python tool quality
- Repository structure integrity
- Basic C compilation capability

### Performance
- Setup time: ~30-60 seconds (first run with venv creation)
- Test execution time: ~5-10 seconds
- Subsequent runs: ~5-10 seconds (setup already cached)

### Test Coverage
The current test suite provides a representative sample of NuttX quality checks:
- Code style validation (mirrors NuttX CI check workflow)
- Python tool validation (used in CI infrastructure)
- Repository integrity checks
- Compiler smoke tests

For comprehensive testing, the full NuttX CI pipeline includes:
- Multi-architecture builds (ARM, RISC-V, x86_64, etc.)
- Board-specific configurations (hundreds of targets)
- Simulator-based runtime tests
- Hardware-in-the-loop testing
