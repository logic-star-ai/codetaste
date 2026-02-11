# Summary

This repository is **TanStack Router**, a type-safe router for React applications with built-in caching and state management. The project is a monorepo using **pnpm workspaces** and **Nx** for build orchestration, containing multiple packages for the router core, React integration, plugins, and the TanStack Start framework.

## System Dependencies

- **Node.js**: v20.17.0 (specified in `.nvmrc`)
- **pnpm**: v9.15.4 (package manager, specified in `package.json`)
- **No external services required**: No databases, Redis, or other system services need to be running

## PROJECT Environment

### Runtime & Package Manager
- **Language**: TypeScript/JavaScript
- **Package Manager**: pnpm v9.15.4 (workspace mode)
- **Build Tool**: Nx v20.3.3 for task orchestration
- **Node Version**: v22.12.0 (pre-installed, compatible with required v20.17.0)

### Key Dependencies
- **Testing Framework**: Vitest v2.1.8 (unit tests)
- **E2E Testing**: Playwright v1.50.0 (not run in test suite)
- **Linting**: ESLint v9.19.0
- **Build**: Vite v6.0.11
- **TypeScript**: v5.7.3 (with compatibility testing for v5.2-5.6)

### Workspace Structure
The monorepo contains 98+ workspace projects including:
- Core packages: `@tanstack/router-core`, `@tanstack/history`, `@tanstack/react-router`
- Plugin packages: `@tanstack/router-plugin`, `@tanstack/router-vite-plugin`
- Start framework: `@tanstack/start` and related server/client packages
- Adapters: Zod, Valibot, Arktype schema adapters
- Developer tools: Router devtools, CLI, generator
- E2E test projects and examples

## Testing Framework

### Test Approach
The test suite runs **unit tests only** using Vitest across all packages that contain tests. The test runner is configured with:
- **Single-threaded execution**: `--pool=threads --poolOptions.threads.singleThread` to avoid resource exhaustion issues (EAGAIN errors)
- **JSON reporter**: For structured test result output
- **Type checking**: Vitest includes experimental type checking with TypeScript

### Test Execution
- Tests are discovered automatically from all packages with `tests/` directories
- Approximately **366-425 tests** execute (varies based on which packages have tests)
- Test files include: `router-core`, `history`, `react-router`, `router-generator`, `router-plugin`, `server-functions-plugin`, `start-plugin`, and adapter packages
- Tests complete in under 2 minutes

### Test Results Format
The `/scripts/run_tests` script outputs a JSON line with the format:
```json
{"passed": <int>, "failed": <int>, "skipped": <int>, "total": <int>}
```

## Additional Notes

### Challenges Encountered
1. **Binary Permissions**: After `pnpm install`, binaries in `node_modules/.pnpm/*/bin/` lack execute permissions. Fixed by recursively adding execute permissions in `setup_shell.sh`.

2. **Resource Constraints**: Initial test runs with default Vitest configuration (parallel execution) caused EAGAIN errors due to excessive process spawning. Resolved by using single-threaded pool execution.

3. **Git Branch Reference**: The repository is in a detached HEAD state with no `main` branch locally, so Nx's `affected` commands fail. Using `test:ci` or direct vitest execution avoids this issue.

4. **JSON Output Parsing**: Vitest JSON reporter outputs warnings to stderr which get mixed with the JSON output. Fixed by grepping for the JSON line starting with `{"numTotalTestSuites"`.

5. **Test Determinism**: Some tests may fail intermittently (observed 6 failures in some runs), but the test suite generally produces consistent results across runs.

### Not Included in Test Suite
- **Build tests** (`test:build`): Package validation with publint/attw - these encounter EAGAIN errors
- **Type tests** (`test:types`): TypeScript compilation across multiple TS versions - too resource intensive
- **ESLint tests** (`test:eslint`): Linting checks - not run to focus on unit tests
- **E2E tests** (`test:e2e`): Playwright browser tests - would require significant additional time
- **Examples**: Example projects are excluded from the test run

### Script Portability
All scripts in `/scripts/` are designed to work on both HEAD and HEAD~1 commits without modification. They handle:
- Fresh installations after `git clean -xdff`
- Idempotent dependency installation (skip if already present)
- Environment variable setup for CI mode
