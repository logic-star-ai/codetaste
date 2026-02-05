# Summary

This document describes the testing setup for the JointJS project, a JavaScript/TypeScript diagramming library.

## System Dependencies

No special system-level dependencies or services are required. The project runs entirely within the Node.js ecosystem with the following pre-installed tools:

- **Node.js**: v22.12.0 (project specifies v18.18.2 via Volta, but tests work with v22)
- **Yarn**: v3.4.1 (managed via corepack)
- **Chromium**: Provided by Puppeteer for browser-based tests

## PROJECT Environment

### Project Structure
- **Primary Language**: JavaScript/TypeScript
- **Build System**: Grunt task runner
- **Module Bundler**: Rollup
- **Package Manager**: Yarn v3 (workspaces enabled)
- **Monorepo**: Multiple packages under `packages/` directory

### Key Packages
1. `packages/joint-core` - Main JointJS library
2. `packages/joint-decorators` - Decorators package
3. `packages/joint-shapes-general` - General shapes
4. `packages/joint-shapes-general-tools` - Tools for shapes

### Build Process
The project requires building before tests can run:
1. Install dependencies: `yarn install`
2. Build project: `yarn run build`
   - Runs rollup to bundle source files
   - Generates UMD modules
   - Minifies JavaScript and CSS
   - Compiles documentation

## Testing Framework

### Test Types

1. **Server-Side Tests (Mocha)**
   - Location: `packages/joint-core/test/jointjs-nodejs/`
   - Framework: Mocha
   - Tests: Node.js environment tests (~12 tests)
   - Command: `yarn run test-server`

2. **Client-Side Tests (Karma + QUnit)**
   - Location: `packages/joint-core/test/`
   - Framework: Karma with QUnit
   - Browser: ChromeHeadless (via Puppeteer)
   - Tests: Browser-based tests for geometry, vectorizer, and joint modules
   - Total: ~2264 tests across three test suites:
     - `karma:geometry` - Geometry utilities (~346 tests)
     - `karma:vectorizer` - SVG manipulation (~443 tests)
     - `karma:joint` - Main JointJS library (~1476 tests)

3. **TypeScript Tests**
   - Location: `packages/joint-core/test/ts/`
   - Framework: TypeScript compiler validation
   - Purpose: Ensures type definitions are correct
   - Counted as 1 successful compilation check

### Test Execution

The full test suite is run via: `yarn run test`

This executes:
1. `shell:rollup-test-bundle` - Builds test bundles
2. `test:server` - Runs Mocha tests
3. `test:client` - Runs Karma tests (geometry, vectorizer, joint)
4. `ts:test` - Validates TypeScript definitions

### Test Results Format

The `/scripts/run_tests` script parses test output and generates JSON:
```json
{"passed": 2276, "failed": 1, "skipped": 0, "total": 2277}
```

Note: There is currently 1 known failing test related to international character handling in `util.breakText`.

## Additional Notes

### Script Portability
All three scripts (`setup_system.sh`, `setup_shell.sh`, and `run_tests`) are designed to work on both HEAD and HEAD~1 commits without modification. They handle:
- Fresh installations (no node_modules)
- Incremental builds (cached dependencies)
- Idempotent operations (safe to run multiple times)

### Build Artifacts
The following directories are created during setup and testing:
- `node_modules/` - Installed dependencies
- `packages/*/node_modules/` - Workspace-specific modules
- `packages/joint-core/build/` - Built source files
- `.yarn/cache/` - Yarn package cache

These are all git-ignored and cleaned by `git clean -xdff`.

### Test Stability
Tests are deterministic and produce consistent results across runs. The single failing test (international character handling) is a known issue in the current codebase.

### Performance
- Full dependency installation: ~1-2 minutes (first time)
- Build process: ~15-20 seconds
- Test execution: ~15-20 seconds
- Total time (clean state): ~2-3 minutes
