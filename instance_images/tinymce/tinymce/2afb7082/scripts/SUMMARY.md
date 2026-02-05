# Summary

This repository contains the TinyMCE monorepo, which includes the TinyMCE rich text editor and its related libraries. The project uses Yarn workspaces with Lerna for managing multiple packages, TypeScript for compilation, and Bedrock for testing.

## System Dependencies

The following system packages are required and are installed during the setup process:

- **Google Chrome Stable**: Required for running browser-based tests with ChromeDriver
- **ChromeDriver**: WebDriver for Chrome, version must match Chrome version (144.0.7559.96)
- Standard build tools (already available in base image)

These dependencies are installed outside of /testbed and persist across sessions.

## PROJECT Environment

### Runtime Version
- **Node.js**: v16.20.2 (via NVM)
  - Node 16 is required due to compatibility issues between the `esm` module used by Gulp and Node 22
  - The oxide-icons and oxide build steps use Gulp with the esm module, which has an assertion failure on Node 22

### Package Manager
- **Yarn**: v1.22.22 (via Corepack)
  - The project enforces Yarn usage and will fail if npm is used
  - Uses Yarn workspaces for monorepo management

### Build Process
The setup shell script performs the following steps:
1. Switches to Node 16 using NVM
2. Enables Corepack for Yarn
3. Installs dependencies with `yarn install --frozen-lockfile`
4. Builds oxide-icons-default (icon package)
5. Builds oxide (default skin/theme)
6. Compiles TypeScript for all modules

### Project Structure
The repository is a monorepo with 23 packages in the `modules/` directory, including:
- Various utility libraries (@ephox/katamari, @ephox/boss, @ephox/boulder, etc.)
- UI component libraries (@ephox/alloy, @ephox/agar)
- The main tinymce editor package
- Theme packages (@tinymce/oxide, @tinymce/oxide-icons-default)

## Testing Framework

### Bedrock Test Runner
The project uses **@ephox/bedrock v4.3.3** as its test framework, which:
- Compiles TypeScript test files using Webpack
- Runs tests in a real browser environment (Chrome headless)
- Provides real-time test execution feedback with dots (.) for passing tests
- Supports both PhantomJS and browser-based testing (only browser tests are configured here)

### Test Organization
Tests are organized by type within each module:
- `atomic/` - Unit tests that don't require DOM
- `browser/` - Tests that require a browser environment
- `phantom/` - Tests designed for PhantomJS (not used in our setup)
- `webdriver/` - Tests using WebDriver API

### Test Execution
The test runner (`/scripts/run_tests`) executes tests for a representative subset of 8 modules:
- @ephox/katamari (data structures and utilities)
- @ephox/boss (DOM operations)
- @ephox/boulder (data validation)
- @ephox/dragster (drag and drop)
- @ephox/jax (AJAX utilities)
- @ephox/polaris (search functionality)
- @ephox/robin (text operations)
- @ephox/echo (data structures)

This subset completes within the 15-minute time limit while providing good test coverage across different library types.

### Test Output
The test runner outputs a JSON line in the format:
```json
{"passed": N, "failed": N, "skipped": N, "total": N}
```

Test counts are derived by:
- Counting dots (.) in the output for passed tests
- Parsing error messages for failed tests
- Setting skipped to 0 (Bedrock doesn't skip tests by default)

## Additional Notes

### Compatibility Issues Encountered
1. **Node 22 + Gulp + ESM**: The oxide-icons-default and oxide packages use Gulp with the `esm` module loader, which has an assertion failure on Node 22. This was resolved by using Node 16.

2. **ChromeDriver Installation**: The Ubuntu package for chromium-browser is a snap stub that doesn't actually install the browser. We had to:
   - Install Google Chrome Stable from the official repository
   - Download a matching ChromeDriver binary from the Chrome for Testing repository

3. **PhantomJS**: PhantomJS is not available and tests requiring it are not run. The project has enough browser-based tests to validate functionality.

### Test Suite Scope
The full test suite (all 23 packages) would take approximately 63 minutes to complete. To meet the 15-minute constraint, the test runner executes a representative subset covering:
- Core utility libraries (katamari, echo, jax)
- DOM manipulation (boss)
- Data validation (boulder)
- UI interactions (dragster)
- Text processing (robin, polaris)

This provides adequate coverage for detecting regressions while staying within time limits.

### Git Status Preservation
All setup scripts are designed to not modify versioned files. Build artifacts (lib/, dist/, node_modules/) are in .gitignore and don't affect git status.
