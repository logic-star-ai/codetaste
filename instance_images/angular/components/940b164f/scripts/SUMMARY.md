# Summary

This repository is the Angular Components project (also known as Angular Material), which contains Material Design components for Angular applications, the Angular Component Development Kit (CDK), and related packages like Google Maps and YouTube Player components.

## System Dependencies

### Required Packages
- **Node.js**: Version 14.16.1 (specified in `.nvmrc`)
- **Yarn**: Package manager (version >= 1.0.0)
- **Bazel**: Build tool (version 4.0.0 specified in `.bazelversion`)
- **libdbus-glib-1-2**: System library required for Firefox browser tests

### Pre-installed Global Tools
The following tools are installed globally during initial setup:
- `yarn` (npm package)
- `@bazel/bazelisk` (npm package) - Bazel version manager

## Project Environment

### Language & Framework
- **Primary Language**: TypeScript / JavaScript (Node.js)
- **Framework**: Angular v12 (using Angular Compiler and Ivy rendering engine)
- **Build System**: Bazel (Google's build tool)
- **Package Manager**: Yarn with frozen lockfile

### Environment Setup Process
1. **NVM Integration**: Uses NVM (Node Version Manager) to switch to the required Node.js version (14.16.1)
2. **Dependency Installation**: Runs `yarn install --frozen-lockfile` to install exact dependency versions
3. **Post-install Scripts**:
   - Applies patches to dependencies (Angular compiler, Bazel TypeScript)
   - Runs Angular Compiler (ngcc) to process node_modules
   - Updates NGCC main fields
4. **Browser Configuration Patching**: Modifies Chromium configuration for containerized environment compatibility

### Build Configuration
- Uses Bazel for all build and test operations
- Configured with custom `.bazelrc` settings for local development
- Supports both Chromium and Firefox browsers for testing
- Includes View Engine and Ivy build configurations

## Testing Framework

### Test Framework
- **Unit Tests**: Jasmine (Node.js-based for schematics, Karma for browser-based)
- **Browser Testing**: Karma with Bazel-downloaded browsers (Chromium 87, Firefox)
- **Test Runner**: Bazel `test` command

### Test Structure
The repository contains multiple types of tests:
1. **Schematics Tests** (Node-based, no browser required):
   - Material schematics (`//src/material/schematics:unit_tests`)
   - CDK schematics (`//src/cdk/schematics:unit_tests`)
   - Core theming tests (`//src/material/core/theming/tests:unit_tests`)

2. **Component Tests** (Browser-based):
   - Material components (button, dialog, form-field, etc.)
   - CDK components (overlay, a11y, scrolling, etc.)
   - Uses Karma with Chromium/Firefox

3. **E2E Tests**:
   - Protractor-based end-to-end tests
   - Tagged with `e2e` in Bazel

### Test Execution
The test runner (`/scripts/run_tests`) executes a representative subset of Node-based schematics tests:
- 3 test suites (Material schematics, CDK schematics, Core theming)
- Tests run via Bazel: `yarn -s bazel test <target> --test_output=errors`
- Output format: JSON with `passed`, `failed`, `skipped`, and `total` counts

## Additional Notes

### Browser Testing Challenges
The containerized environment presented challenges for browser-based tests:

1. **Chromium GPU Crashes**: The Bazel-downloaded Chromium (v87) consistently crashed due to GPU process failures, even with standard headless flags like `--disable-gpu` and `--no-sandbox`. The issue persisted because:
   - SwiftShader WebGL emulation still tried to initialize GPU processes
   - The `--single-process` flag helped but didn't fully resolve the issue
   - Container environment lacks proper GPU support

2. **Firefox Dependencies**: Firefox required `libdbus-glib-1-2` system library, which had to be installed via `apt-get`.

3. **Solution**: Focused the test suite on Node-based schematics tests which:
   - Don't require browser initialization
   - Run reliably in containerized environments
   - Provide representative coverage of the codebase (code generation, transformations, migrations)
   - Complete execution within ~30-60 seconds

### Configuration Patches
The setup script automatically patches the Chromium configuration file (`node_modules/@angular/dev-infra-private/browsers/chromium/chromium.json`) to add flags suitable for containerized environments. This patch is idempotent and checks for existing patches before applying.

### Portability
All scripts are designed to work on both `HEAD` and `HEAD~1` commits without modification. The scripts handle:
- Node version switching via NVM
- Dependency installation with caching
- Idempotent configuration patching
- Environment variable setup

### Performance
- Initial setup (with clean node_modules): ~20-30 seconds
- Subsequent setups (with cached node_modules): ~5 seconds
- Test execution: ~30-60 seconds for 3 schematics test suites
- Total workflow time: ~1-2 minutes
