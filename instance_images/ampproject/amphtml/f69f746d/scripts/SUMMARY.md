# Summary

This repository is the AMP HTML project, a JavaScript/Node.js based web framework for building fast-loading web pages. The testing setup has been configured to run a representative subset of the test suite focusing on the fast-running unit tests (ava and jest).

## System Dependencies

- **Operating System**: Ubuntu 24.04
- **Node.js**: Version 10.24.1 (required by package.json engines specification: ^8.0.0 || ^10.0.0)
- **Yarn**: Version 1.10.1 (required by package.json engines specification: ^1.10.1)
- **NVM**: Node Version Manager located at /opt/nvm
- **gulp-cli**: Installed globally via yarn for running build tasks

No system services (databases, Redis, etc.) are required for running tests.

## PROJECT Environment

The project uses:
- **Package Manager**: Yarn (v1.10.1)
- **Build System**: Gulp (task runner)
- **Node Version**: 10.24.1 (managed via NVM)

Environment setup includes:
1. Sourcing NVM from /opt/nvm/nvm.sh
2. Switching to Node.js 10
3. Installing project dependencies with `yarn install --ignore-engines --ignore-optional`
4. Installing gulp-cli globally
5. Adding yarn global bin directory to PATH

The `--ignore-optional` flag is used because the optional native module `iltorb` cannot be built on Ubuntu 24.04 (lacks Python 2), but the project has fallback mechanisms and doesn't require it for basic functionality.

## Testing Framework

The project uses multiple testing frameworks:

1. **AVA** (v0.25.0): Tests located in `build-system/tasks/**/{test,test-*}.js`
   - Runs tests for gulp tasks and build system utilities
   - Outputs in TAP format
   - Current test count: 7 tests

2. **Jest** (v23.6.0): Tests located in `build-system/babel-plugins/[^/]+/test/.+\\.m?js$`
   - Tests Babel plugins used in the build system
   - Uses jest-dot-reporter for output
   - Current test count: 17 tests

3. **Karma + Mocha**: Integration and unit tests (not included in representative subset)
   - Requires building the project first (time-consuming)
   - Runs browser-based tests using Karma test runner
   - Tests located in test/ and extensions/ directories

The `/scripts/run_tests` script runs AVA and Jest tests (24 tests total) as a representative subset that completes in under 1 minute.

## Additional Notes

### Obstacles and Workarounds

1. **Python 2 Unavailability**: Ubuntu 24.04 doesn't include Python 2, which is required by node-gyp for building native modules with Node.js 10. The `iltorb` optional dependency fails to build, but this doesn't affect the test suite as the module is optional and has fallbacks.

2. **Node Version Compatibility**: The project requires Node.js 8 or 10, which is much older than the system default (Node 22). NVM is used to switch to the correct version.

3. **Gulp-cli PATH**: The gulp-cli installed via yarn global needs to be explicitly added to PATH using `$(yarn global bin)`.

4. **Engine Warnings**: The yarn install process shows warnings about outdated Node and Yarn versions, but these are expected given the project's age and don't affect functionality.

### Test Output Format

The `/scripts/run_tests` script outputs a JSON object with test results:
```json
{"passed": 24, "failed": 0, "skipped": 0, "total": 24}
```

This represents:
- 7 AVA tests (gulp task tests)
- 17 Jest tests (Babel plugin tests)
- Total: 24 tests

### Portability

All scripts are designed to work on both HEAD and HEAD~1 without modifications. They handle clean installations and are idempotent (safe to run multiple times).
