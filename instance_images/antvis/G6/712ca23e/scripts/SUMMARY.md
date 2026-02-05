# Summary

G6 is a TypeScript/JavaScript graph visualization framework developed using a pnpm monorepo structure. The project consists of multiple packages, with the main `@antv/g6` package located in `packages/g6`. The testing setup uses Jest with ts-jest for TypeScript support and jsdom for browser environment simulation.

## System Dependencies

No system-level dependencies are required. G6 is a frontend library that runs entirely in a simulated browser environment (jsdom) for testing. All dependencies are JavaScript/TypeScript packages managed through pnpm.

- **Node.js**: v22.12.0 (pre-installed in environment)
- **pnpm**: Installed globally via npm during setup
- **Package Manager**: pnpm (workspace-based monorepo)

## Project Environment

### Structure
- **Language**: TypeScript/JavaScript
- **Build Tool**: TypeScript compiler (tsc) + Rollup for UMD builds
- **Package Count**: ~4550 packages across the monorepo
- **Monorepo Tool**: pnpm workspaces
- **Main Package**: `packages/g6`

### Dependencies Installation
Dependencies are installed using `pnpm install` at the repository root. The installation:
- Installs dependencies for all 5 workspace packages
- Sets up git hooks via husky
- Prepares documentation with dumi for some packages
- Takes approximately 20-25 seconds on cached installations

### Build Process
The project has TypeScript compilation errors on the current commit (HEAD) but tests still run successfully because:
1. Jest uses ts-jest which compiles TypeScript on-the-fly during test execution
2. The errors are in type definitions rather than runtime code
3. The build errors are isolated to specific type mismatches in 3 files

## Testing Framework

### Framework Details
- **Test Runner**: Jest 29.7.0
- **TypeScript Support**: ts-jest 29.4.6
- **Environment**: jsdom (simulates browser DOM)
- **Test Configuration**: `packages/g6/jest.config.js`

### Test Structure
- **Test Location**: `packages/g6/__tests__/`
- **Test Types**:
  - Unit tests: `__tests__/unit/` (runtime, utils, spec, registry tests)
  - Integration tests: `__tests__/integration/` (animation, static, default tests)
- **Test Count**:
  - HEAD: 166 tests in 39 test suites
  - HEAD~1: 163 tests in 39 test suites

### Test Execution
Tests are run from the `packages/g6` directory using:
```bash
npm test
```

This internally calls:
```bash
npm run jest:base __tests__
```

Which executes:
```bash
node --expose-gc --max-old-space-size=4096 --unhandled-rejections=strict --experimental-vm-modules ../../node_modules/jest/bin/jest --coverage --logHeapUsage --detectOpenHandles __tests__
```

### Test Performance
- **Execution Time**: ~33-35 seconds for full test suite
- **Coverage**: 94.51% statement coverage, 80.98% branch coverage
- **Memory**: Uses up to ~400MB heap size during test execution

### Test Output Format
Jest outputs a summary line in the format:
```
Tests:       X passed, Y total
```

This is parsed by the `/scripts/run_tests` script to generate the required JSON output.

## Additional Notes

### Observations
1. **Build vs Test Separation**: While the project has TypeScript build errors, the test suite runs successfully because Jest compiles TypeScript independently using ts-jest
2. **No Build Required for Testing**: The `/scripts/setup_shell.sh` intentionally skips the build step to avoid the TypeScript errors while still allowing tests to run
3. **Monorepo Complexity**: The project uses pnpm workspaces with 5 packages, but tests are only run for the main `g6` package
4. **Peer Dependency Warnings**: The installation shows many peer dependency warnings (primarily React version mismatches) but these don't affect test execution
5. **Version Consistency**: The test suite produces deterministic results across commits (166 tests on HEAD, 163 tests on HEAD~1)

### Known Issues
- TypeScript compilation errors exist in 3 files related to type mismatches with `IndexedCollection` vs `Point` types
- These errors don't prevent tests from running due to Jest's independent compilation
- The errors are in: `src/elements/edges/base-edge.ts`, `src/utils/edge.ts`, and `src/utils/element.ts`

### Script Portability
All scripts (`setup_system.sh`, `setup_shell.sh`, `run_tests`) are designed to work on both HEAD and HEAD~1 commits without modification. They handle:
- Missing lockfile (pnpm-lock.yaml is gitignored)
- Fresh installations from clean state
- Idempotent operations (safe to run multiple times)
