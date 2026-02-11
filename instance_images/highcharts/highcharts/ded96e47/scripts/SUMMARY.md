# Summary

This repository contains **Highcharts**, a JavaScript charting library written in TypeScript. The testing infrastructure is configured to run Node.js-based unit tests using Node's built-in test runner with TAP (Test Anything Protocol) output format.

## System Dependencies

**No system-level dependencies are required** for running the Highcharts test suite. The tests do not require any external services such as:
- Databases (PostgreSQL, MySQL, Redis, etc.)
- Message queues
- Web services
- Browser automation tools (for the ts-node-unit-tests)

All testing is performed using Node.js runtime environment with JavaScript/TypeScript modules.

## Project Environment

### Runtime & Package Manager
- **Node.js**: v22.12.0 (pre-installed in environment)
- **npm**: v10.9.0 (pre-installed in environment)
- **Package Manager**: npm (uses package-lock.json for reproducible builds)

### Build System
- **Build Tool**: Gulp (task runner)
- **TypeScript**: ~5.4.5
- **Test Runner**: Node's built-in test runner (`node:test`)

### Dependencies Installation
The `setup_shell.sh` script:
1. Installs all npm dependencies via `npm install`
2. Runs post-install hooks that:
   - Execute `gulp update-vendor` to copy vendor files
   - Execute `gulp patch-ink-docstrap` for documentation patches
   - Initialize Husky git hooks
   - Run `gulp clean` and `gulp update-vendor` via prepare script
3. Sets environment variables (`CI=true`, `NODE_ENV=test`)
4. Implements idempotency by checking for existing `node_modules` and comparing `package-lock.json`

## Testing Framework

### Test Suite: ts-node-unit-tests
The test suite runs TypeScript unit tests that verify:
- Module loading (Highmaps, Highstock, Highcharts)
- Series types availability
- Product names and configurations
- Utility functions
- Language modules
- Global DOM utilities

### Test Execution
Tests are executed via:
```bash
npm run test-node
```

This command:
1. Runs `tsx ./test/ts-node-unit-tests/index.ts`
2. Builds required scripts via `gulp scripts`
3. Discovers test files matching `test/ts-node-unit-tests/tests/**/*.test.ts`
4. Executes tests using Node's test runner
5. Outputs results in TAP format (when `CI=true`)

### Test Output Format
The `run_tests` script parses TAP output and generates JSON:
```json
{"passed": 70, "failed": 0, "skipped": 0, "total": 70}
```

### Test Results
- **HEAD commit (09f0d36)**: 70 passed, 0 failed, 0 skipped
- **HEAD~1 commit (ded96e4)**: 70 passed, 0 failed, 0 skipped
- Tests are deterministic and reproducible

## Additional Notes

### Portability
All three scripts (`setup_system.sh`, `setup_shell.sh`, `run_tests`) work correctly on both HEAD and HEAD~1 commits without any modifications, meeting the portability requirement.

### Git Status Verification
The scripts do not modify any version-controlled files. Only the following are created/modified:
- `node_modules/` (git-ignored)
- `code/`, `js/`, `build/`, `vendor/` (git-ignored build artifacts)
- `.husky/_/` (git-ignored)

Running `git status` after script execution shows no changes to tracked files.

### Warnings Encountered
During `npm install`, several deprecation warnings appear for dependencies:
- Deprecated packages: rimraf@3, request, q, lolex, inflight, istanbul, babel-eslint, glob@7, eslint@8
- These are transitive dependencies and do not affect test execution
- 46 vulnerabilities reported (11 low, 16 moderate, 13 high, 6 critical) - typical for legacy frontend projects with deep dependency trees

### Test Scope
The configured test suite focuses on **ts-node-unit-tests** (70 tests), which provides fast, representative coverage of core functionality. The full test suite includes additional Karma-based browser tests that would take significantly longer to run.

### Performance
- Clean setup (including npm install): ~30-40 seconds
- Test execution: ~20-30 seconds
- Total time from clean state to results: ~1 minute
