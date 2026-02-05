# Summary

This document describes the testing setup for the Modern.js monorepo, a Progressive React Framework for modern web development.

## System Dependencies

**No system-level dependencies are required** for running the test suite. The `/scripts/setup_system.sh` script exists to satisfy the requirements but performs no operations (exits 0).

All dependencies are JavaScript/Node.js-based and are installed at the project level through pnpm.

## Project Environment

### Runtime
- **Node.js**: Version >=14.17.6 (project supports any modern Node version; tested with v22.12.0)
- **Package Manager**: pnpm v8.6.1 (specified in `packageManager` field)
- **Monorepo Tool**: Turbo v1.10.2 for build orchestration

### Setup Process
The `/scripts/setup_shell.sh` script performs the following:

1. **Dependency Installation**: Runs `pnpm install --frozen-lockfile` to install all workspace dependencies
   - The monorepo includes 250+ workspace projects
   - ~3222 packages are installed from pnpm store
   - Includes Playwright browsers and Puppeteer (Chromium)

2. **Package Building**: Executes `turbo run build` to build internal packages
   - Builds ~107 packages in the workspace
   - Uses turbo cache for faster subsequent builds
   - Skips husky git hooks during build (HUSKY=0)

3. **Environment Variables**: Sets `NODE_ENV=test` and `CI=true`

The setup script is idempotent and skips steps when artifacts already exist.

### Key Technologies
- **Monorepo Structure**: pnpm workspaces with multiple packages
- **Build Tools**:
  - Turbo (build orchestration)
  - Modern-lib (internal build tool)
  - esbuild v0.17.19
- **Compilers**:
  - @swc/jest for test transformation
  - Babel (babel-preset-app, babel-preset-base)
  - TypeScript v5

## Testing Framework

The project uses a hybrid testing approach with two main frameworks:

### 1. Jest (Primary Unit Tests)
- **Location**: `/testbed/tests/` directory
- **Configuration**: `jest-ut.config.js`
- **Command**: `pnpm run test:ut` (runs in tests directory)
- **Key Features**:
  - Uses @swc/jest for fast TypeScript transformation
  - Custom test environment (`jest.env.js`)
  - Custom resolver (`jest.resolver.js`)
  - Puppeteer integration for browser tests (preset: jest-puppeteer)
  - Coverage collection enabled
  - 30-second timeout per test

- **Test Patterns**:
  - `<rootDir>/packages/**/src/**/*.test.[jt]s?(x)`
  - `<rootDir>/packages/**/tests/**/*.test.[jt]s?(x)`

- **Excludes**: builder packages, e2e toolkit, libuild packages

### 2. Vitest (Package-Level Tests)
- **Location**: Individual packages with `vitest.config.ts` files
- **Configuration**: Per-package vitest configs
- **Key Features**:
  - Modern, fast test runner
  - Native ESM support
  - Used in newer packages (builder-shared, toolkit packages, etc.)

### Test Execution
The `/scripts/run_tests` script executes:
- **Jest unit tests** from the tests directory
- Parses test results from Jest output format
- Reports final counts in JSON format: `{"passed": N, "failed": N, "skipped": N, "total": N}`

### Test Coverage
- Jest collects coverage for most packages under `packages/**/src/**/*.ts`
- Excludes generators, create tools, upgrade tools, and temporarily builder packages
- Coverage reports are generated in `tests/coverage/`

## Example Test Results

A typical successful test run produces:
```
Test Suites: 2 skipped, 215 passed, 215 of 217 total
Tests:       86 skipped, 978 passed, 1064 total
Snapshots:   72 passed, 72 total
Time:        ~50-60 seconds
```

Output JSON:
```json
{"passed": 978, "failed": 0, "skipped": 86, "total": 1064}
```

## Additional Notes

### Working with the Scripts

**Full clean test run:**
```bash
git clean -xdff && sudo /scripts/setup_system.sh && source /scripts/setup_shell.sh && /scripts/run_tests
```

**After initial setup:**
```bash
source /scripts/setup_shell.sh && /scripts/run_tests
```

### Compatibility
- Scripts work on both current commit (HEAD) and previous commit (HEAD~1)
- No modifications needed when checking out different commits
- Build artifacts and node_modules are in .gitignore

### Performance Considerations
- Initial `pnpm install` downloads ~3200 packages (3-5 minutes on fast connection)
- Turbo build caches significantly speed up repeated builds
- Tests run in parallel with maxWorkers=2 for Jest
- Total test time: ~1-2 minutes after setup

### Known Warnings
- Turbo may show warnings about lockfile operations for certain doc packages (non-fatal)
- Some napi-rs/image-linux-x64-musl installation may fail (non-critical, does not affect tests)
- pnpm may suggest updating to newer version (8.6.1 is specified version)

### Project Structure
- `/packages/` - Main source packages (CLI, toolkit, builder, server, etc.)
- `/tests/` - Integration and unit tests
- `/scripts/` - Build and utility scripts
- Root is a pnpm workspace with 250+ projects
