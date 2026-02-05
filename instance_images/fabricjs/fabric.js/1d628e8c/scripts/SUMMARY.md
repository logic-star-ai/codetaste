# Summary

This repository contains **fabric.js**, a JavaScript HTML5 canvas library. The project is written in **TypeScript** and uses **Node.js** (v22.12.0) as the runtime environment. The test suite runs unit tests using **QUnit** with **jsdom** and **node-canvas** for headless browser and canvas rendering simulation.

## System Dependencies

The canvas npm package requires native system libraries for image manipulation. The following packages are installed via apt:

- **libcairo2-dev**: Cairo 2D graphics library (required by node-canvas)
- **libpango1.0-dev**: Pango text rendering library (required by node-canvas)
- **libgif-dev**: GIF image format support
- **build-essential**: Essential compilation tools (gcc, g++, make)
- **g++**: C++ compiler for native module compilation

These dependencies are installed by `/scripts/setup_system.sh` which runs with sudo privileges.

## PROJECT Environment

### Package Manager
- **npm** (v10.9.0) - Node.js package manager

### Key Dependencies
- **TypeScript** (^4.9.4) - Primary language for source code
- **Rollup** (^3.9.1) - Module bundler for building distribution files
- **QUnit** (^2.17.2) - Testing framework
- **jsdom** (^20.0.3) - Headless DOM implementation for Node.js
- **canvas** (^2.11.2) - Node.js canvas implementation (optional dependency)

### Build Process
The project requires a build step before running tests:
1. TypeScript source files in `src/` are compiled
2. Rollup bundles the code into multiple formats (ESM, CJS, minified)
3. Output is placed in the `dist/` directory

The build produces:
- `dist/index.mjs`, `dist/index.cjs`, `dist/index.min.js` - Browser builds
- `dist/index.node.mjs`, `dist/index.node.cjs` - Node.js specific builds

## Testing Framework

### Test Runner
**QUnit** is used as the testing framework. Tests are located in:
- `test/unit/` - Unit tests (1400+ tests)
- `test/visual/` - Visual regression tests (not run by default)
- `test/lib/` - Test utilities and helpers

### Test Execution
Tests are executed via:
```bash
npx qunit test/node_test_setup.js test/lib test/unit
```

The `test/node_test_setup.js` file:
- Initializes the fabric.js environment with jsdom
- Sets up global test utilities
- Configures QUnit options (timeout, globals checking)
- Establishes canvas context for tests

### Test Output Format
QUnit outputs results in TAP (Test Anything Protocol) format. The run_tests script:
1. Captures QUnit's TAP output
2. Parses lines beginning with "ok" (passed) and "not ok" (failed)
3. Counts skipped tests from "# skip" comments
4. Outputs final JSON: `{"passed": N, "failed": M, "skipped": K, "total": T}`

### Current Test Results
- **Total tests**: ~1415 tests
- **Typical results**: 1413 passed, 1 failed (comment/parsing artifact), 1 skipped
- **Test duration**: ~30-60 seconds on typical hardware

## Additional Notes

### Optional Dependency Challenge
The canvas npm package is marked as an `optionalDependency` in package.json. However, it's required for tests to run properly. npm's default behavior with optional dependencies is to silently skip installation if the build fails (e.g., missing system libraries).

**Solution**: The setup_shell.sh script:
1. Removes package-lock.json to force fresh dependency resolution
2. Runs `npm install --include=optional` to attempt canvas installation
3. Explicitly installs canvas@2.11.2 if it's missing after npm install

This ensures canvas is available even if the initial optional dependency install fails.

### Environment Compatibility
- Scripts are portable and work on both HEAD and HEAD~1 commits
- No modifications to tracked files in /testbed/ (git status remains clean)
- All installations occur in node_modules/, dist/, and other gitignored paths
- System dependencies are idempotent (can be installed multiple times safely)

### Known Warnings
- TypeScript compilation shows warnings about missing canvas type declarations (expected, as canvas is optional)
- Circular dependency warning in the codebase (pre-existing, not affecting tests)
- npm audit shows some vulnerabilities in dev dependencies (not critical for test execution)
