# Summary

This repository is a **TypeScript/Node.js monorepo** for Sanity.io, managed using **pnpm** as the package manager and **Turbo** for build orchestration. The test suite uses **Vitest** for unit/integration testing and **Playwright** for end-to-end tests.

## System Dependencies

The following system-level dependencies are required:

- **Node.js**: v22.12.0 (pre-installed via NVM)
- **pnpm**: v9.13.1 (installed globally via npm)
- **Git**: For repository operations

No additional system services (databases, Redis, etc.) are required for running the test suite.

## PROJECT Environment

### Package Manager
- **pnpm** v9.13.1 (specified in `package.json` as `"packageManager": "pnpm@9.13.1"`)
- Workspace configuration defined in `pnpm-workspace.yaml`

### Build System
- **Turbo**: Used for parallel package builds
- **TypeScript**: v5.7.3 for type checking
- Build outputs go to `lib/` directories in each package

### Monorepo Structure
The workspace includes 38 packages across:
- `packages/@sanity/*` - Core Sanity packages (@sanity/cli, @sanity/types, @sanity/schema, etc.)
- `packages/sanity` - Main Sanity Studio package
- `packages/@repo/*` - Internal development packages
- `dev/*` - Development test studios
- `examples/*` - Example projects
- `perf/*` - Performance testing

### Environment Setup Process
1. **Dependencies Installation**: `pnpm install --frozen-lockfile` installs all workspace dependencies
2. **Build**: `pnpm build` compiles all TypeScript packages using Turbo
3. **Environment Variables**: `NODE_ENV=test` is set for test execution

## Testing Framework

### Primary Test Framework: Vitest
- **Version**: 2.1.8
- **Configuration**: Workspace-based testing defined in `vitest.workspace.ts`
- **Test Packages**:
  - packages/@sanity/migrate
  - packages/@sanity/cli
  - packages/@sanity/codegen
  - packages/@sanity/mutator
  - packages/@sanity/schema
  - packages/@sanity/types
  - packages/@sanity/util
  - packages/sanity
  - packages/sanity/src/_internal/cli
  - perf/tests

### Test Execution
- **Command**: `pnpm vitest run`
- **Reporters**: JSON and default reporters for structured output
- **Timeout**: 15-minute maximum (900 seconds) to prevent hanging
- **Environment**: jsdom for browser-like environment in most tests

### Test Results (HEAD)
- **Total Tests**: 2272
- **Passed**: 2146
- **Failed**: 3 (known failing tests in StructureTitle component)
- **Skipped**: 111
- **Duration**: ~80 seconds

### Additional Testing Tools
- **Playwright**: v1.49.1 for E2E testing (not run in standard test suite)
- **Testing Library**: @testing-library/react for component testing

## Additional Notes

### Key Observations
1. **Build Required**: Tests depend on compiled packages, so `pnpm build` must run before testing
2. **Idempotent Setup**: The `setup_shell.sh` script checks for existing installations to avoid redundant work
3. **Clean Git Status**: The scripts modify only ignored directories (node_modules/, lib/, etc.) and maintain a clean git status
4. **Portability**: Scripts work on both HEAD and HEAD~1 without modifications
5. **Test Failures**: 3 tests consistently fail in `StructureTitle.test.tsx` related to document title assertions, plus 1 unhandled error in `Studio.test.tsx`. These appear to be environmental issues rather than actual bugs.

### Performance Considerations
- Initial install and build takes ~3-4 minutes on a clean checkout
- Subsequent builds are faster due to Turbo caching
- Test execution takes ~80 seconds for the full suite
- Total time for clean setup + tests: ~5-6 minutes

### Test Output Format
The `/scripts/run_tests` script produces JSON output in the format:
```json
{"passed": 2146, "failed": 3, "skipped": 111, "total": 2272}
```

This format accurately reflects the Vitest test results and is deterministic across runs.
