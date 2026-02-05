# Summary

This document describes the testing setup for the Lettuce Redis Client repository.

## Project Overview

Lettuce is an advanced Java Redis client for synchronous, asynchronous, and reactive usage. The project uses Maven for build management and JUnit 5 for testing.

## System Dependencies

The following system packages are required:
- **Maven 3.8.7**: Java build tool
- **Redis-tools**: Provides redis utilities for development
- **Build-essential**: C compiler and build tools (required for building Redis from source)
- **TCL**: Required for Redis test suite
- **Stunnel4**: SSL tunnel wrapper (required for SSL tests, though not used in unit tests)
- **OpenSSL**: SSL/TLS toolkit

These are installed via `apt-get` in `/scripts/setup_system.sh`.

## PROJECT Environment

### Java Version
- **Java 21** (OpenJDK 21.0.9)
- Note: The project's pom.xml specifies Java 8 as the target, but the build works with Java 21

### Build Tool
- **Maven 3.8.7**

### Redis
- The project requires Redis for integration tests, but **unit tests do not require Redis to be running**
- Redis is built from source (unstable branch) from GitHub during the shell setup
- Redis is built into `/testbed/work/redis-git/src/redis-server`

### Maven Configuration
- **Jacoco code coverage is disabled** (`-Djacoco.skip=true`) due to compatibility issues with Java 21
- The Jacoco version in the project (0.8.4) doesn't support Java 21's class file format (major version 65)

## Testing Framework

### Test Structure
The project uses **JUnit 5 (Jupiter)** as the primary testing framework, along with **JUnit Vintage** for backward compatibility with JUnit 4 tests.

### Test Categories
According to the Maven Surefire plugin configuration in `pom.xml`:

**Unit Tests** (run by `/scripts/run_tests`):
- Include patterns: `**/*UnitTests`, `**/*Tests`
- Exclude patterns: `**/*Test`, `**/*IntegrationTests`
- Do NOT require Redis servers to be running
- Approximately **2060 tests** in the current HEAD

**Integration Tests** (NOT run by `/scripts/run_tests`):
- Include patterns: `**/*IntegrationTests`, `**/*Test`
- Exclude patterns: `**/*UnitTests`
- Require Redis, Sentinel, and Cluster instances to be running
- Can be run using the Makefile: `make start && make test && make stop`

### Test Execution
- Tests are executed using Maven Surefire plugin
- Output format: Final line is JSON with test counts
- Format: `{"passed": int, "failed": int, "skipped": int, "total": int}`

### Test Results
- **HEAD** (418bc1d): 2056 passed, 1 failed, 3 skipped, 2060 total
- **HEAD~1** (9115222): 2061 passed, 1 failed, 3 skipped, 2065 total
- One test consistently fails: `CompressionCodecUnitTests.gzipValueTest` (appears to be a platform-specific GZIP compression issue)

## Additional Notes

### Challenges Encountered
1. **Jacoco Compatibility**: The code coverage tool (Jacoco 0.8.4) is not compatible with Java 21's class file format. This was resolved by disabling Jacoco with `-Djacoco.skip=true` flag.

2. **Redis Build Time**: Building Redis from source takes approximately 1-2 minutes, which adds to the initial setup time.

### Script Behavior
- **`/scripts/setup_system.sh`**: Installs system packages, must be run with sudo
- **`/scripts/setup_shell.sh`**: Sets up the Java environment, builds Redis, compiles the project. Must be sourced (not executed) to set environment variables properly.
- **`/scripts/run_tests`**: Runs unit tests and outputs JSON results. Can be run multiple times without re-running setup.

### Portability
- All scripts work on both HEAD and HEAD~1 commits without modification
- The `work/` and `target/` directories are excluded from version control and are created during build
- Running `git clean -xdff` removes all build artifacts

### Performance
- Full clean build + test run: ~2-3 minutes (including Redis build)
- Test-only run (after setup): ~12-15 seconds
- The scripts are optimized to avoid redundant builds when possible
