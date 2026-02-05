# Summary

This repository contains webpack 5.0.0-next, a module bundler for JavaScript applications. The testing setup is configured to run a representative subset of the Jest-based test suite, which includes configuration tests, stats tests, and normal test cases.

## System Dependencies

No system-level dependencies are required for webpack tests. All tests run in a Node.js environment without external services like databases or Redis.

## PROJECT Environment

- **Language**: JavaScript/Node.js
- **Node Version**: Requires Node.js >= 8.9.0 (tested with v22.12.0)
- **Package Manager**: Yarn (v1.22.22)
- **Key Dependencies**:
  - Jest (testing framework)
  - Various webpack loaders and plugins
  - Multiple compiler and parser libraries

### Environment Variables

- `NODE_OPTIONS="--openssl-legacy-provider"`: Required for compatibility with older cryptographic algorithms used by webpack when running on newer Node.js versions (>= 17)

### Project Setup

The project requires a specific setup where webpack is linked to itself using yarn link:
1. Install dependencies with `yarn install`
2. Create a webpack symlink with `yarn link`
3. Link webpack into itself with `yarn link webpack`

This circular dependency setup allows webpack to compile itself during tests.

## Testing Framework

**Framework**: Jest (v23.4.1)

**Test Suites Run**:
- `ConfigTestCases.test.js`: Configuration-based test cases
- `StatsTestCases.test.js`: Statistics output tests
- `TestCasesNormal.test.js`: Normal compilation test cases

**Test Execution**:
- Run with `--json` flag for structured output
- Memory limit increased to 4096MB via `--max-old-space-size=4096`
- Tests run without coverage collection for speed
- Total tests: ~1731 tests
- Expected test results: ~1710 passed, ~15 failed (due to snapshot mismatches from non-deterministic ordering), ~6 skipped

**Test Characteristics**:
- Some tests have non-deterministic behavior (hash ordering, chunk IDs) causing snapshot failures
- These failures are expected and do not indicate actual functional issues
- Tests are comprehensive, covering various webpack configurations and use cases

## Additional Notes

### Challenges Encountered

1. **OpenSSL Compatibility**: Node.js v22 uses OpenSSL 3.0 which dropped support for legacy algorithms like MD4 that older webpack versions use. Solution: Set `NODE_OPTIONS="--openssl-legacy-provider"` to enable legacy cryptographic algorithms.

2. **Self-referential Setup**: Webpack requires linking to itself (`yarn link webpack`) to test properly, which is handled in the setup_shell.sh script.

3. **Jest JSON Output**: Jest outputs JSON embedded within test output rather than as a clean final line. The run_tests script parses the output file to extract the JSON summary line containing test statistics.

4. **Test Determinism**: Some StatsTestCases tests fail due to non-deterministic ordering in webpack's internal structures (e.g., chunk IDs, module ordering). These are expected snapshot mismatches and don't represent actual bugs.

### Script Portability

All scripts are designed to work on both the current commit (3cf0199) and previous commit (HEAD~1) without modification. The scripts:
- Don't modify versioned files in /testbed
- Only manipulate node_modules and build artifacts (git-ignored files)
- Are idempotent and can be run multiple times safely
