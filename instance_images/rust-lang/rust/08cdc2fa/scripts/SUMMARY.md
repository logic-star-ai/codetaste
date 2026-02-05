# Summary

This repository contains the Rust programming language compiler and standard library. The testing setup has been configured to run the tidy test suite, which validates code quality, style, formatting, license headers, and other checks that are always run in CI.

## System Dependencies

The following system dependencies are required:
- **Python 3**: Required for the bootstrap build system (x.py)
- **Git**: Required for repository management and submodule handling
- **C/C++ compiler**: build-essential package (gcc, g++)
- **pkg-config**: Required for library configuration
- **libssl-dev**: Required for SSL/TLS support in Cargo
- **curl**: Used for downloading bootstrap components

The system already has all necessary dependencies installed. Ninja is NOT required for tidy tests as LLVM is not built.

## Project Environment

- **Language**: Rust (self-hosted compiler)
- **Build System**: Custom Python-based bootstrap system (x.py)
- **Package Manager**: Cargo (included with Rust)
- **Runtime**: The project uses the system-installed Rust (rustc 1.92.0) for bootstrapping
- **Configuration**: A minimal `config.toml` is automatically created that:
  - Disables LLVM download (not needed for tidy tests)
  - Sets the change-id to avoid warnings
  - Configures the build for "dev" channel
  - Disables extended build

### Git Branch Handling

The Rust bootstrap system requires a valid git branch (not detached HEAD). The setup script automatically creates a temporary branch if the repository is in detached HEAD state, ensuring the build system functions correctly.

### Submodules

The repository uses git submodules for:
- `library/stdarch`: Architecture-specific intrinsics
- `library/backtrace`: Backtrace support library
- `src/doc/book`: The Rust Programming Language book

These are initialized on first run with `--depth 1` to minimize download time.

## Testing Framework

The test suite uses the Rust compiler's built-in testing framework via `x.py test tidy --stage 0`.

### Tidy Tests

Tidy tests are fast (< 1 minute) validation checks that run before any compilation:
- **Format checking**: Verifies Rust code follows rustfmt style guidelines
- **License validation**: Checks for proper license headers on all source files
- **Feature gate checks**: Validates unstable feature documentation
- **Error code documentation**: Ensures all error codes are documented
- **Code quality checks**: Various linting and style rules

### Test Results

The test runner outputs a JSON line with the following format:
```json
{"passed": 1, "failed": 0, "skipped": 0, "total": 1}
```

Since tidy is an all-or-nothing test suite (either all checks pass or the suite fails), the counts are:
- `passed`: 1 if all tidy checks pass, 0 otherwise
- `failed`: 0 if all tidy checks pass, 1 otherwise
- `skipped`: Always 0
- `total`: Always 1

## Additional Notes

### Bootstrap Process

The first run will download stage0 bootstrap components (~50MB) from https://static.rust-lang.org/. These are cached in `/testbed/build/cache/` and reused on subsequent runs.

### Why Tidy Tests?

Tidy tests were chosen because they:
1. Run quickly (< 1 minute after first bootstrap)
2. Don't require building LLVM or the compiler
3. Are deterministic and stable
4. Are always run in the Rust CI pipeline
5. Provide meaningful validation of code quality

### Portability

The scripts work correctly on both HEAD and HEAD~1 commits without modification, as required. The configuration is minimal and doesn't assume specific compiler versions or features.
