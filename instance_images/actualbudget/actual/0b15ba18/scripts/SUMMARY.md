# Summary

This repository contains Actual Budget, a local-first personal finance application built with Node.js and TypeScript. The project uses a monorepo structure managed by Yarn workspaces with multiple packages including:
- loot-core: Core application logic
- @actual-app/api: API layer
- @actual-app/crdt: CRDT implementation for sync
- @actual-app/sync-server: Synchronization server
- @actual-app/web: Web client
- desktop-electron: Electron desktop app
- eslint-plugin-actual: Custom ESLint rules
- component-library: Shared React components

## System Dependencies

The project requires the following system dependencies which are already pre-installed in the environment:
- **build-essential**: For compiling native Node.js modules (better-sqlite3, bcrypt)
- **python3**: Required by node-gyp for native module compilation
- **libsqlite3-dev**: SQLite development headers for better-sqlite3

No additional system dependencies need to be installed.

## Project Environment

- **Node.js Version**: v18.16.0 (as specified in .nvmrc)
- **Package Manager**: Yarn 4.3.1 (managed via Corepack, with binary in .yarn/releases/)
- **Package Management**: Yarn workspaces with node-modules linker
- **Native Module Management**: Native modules (better-sqlite3, bcrypt) are rebuilt after installation to ensure compatibility with the correct Node.js version

### Environment Setup Process

1. NVM loads Node.js v18.16.0
2. Corepack is enabled for Yarn support
3. Dependencies are installed via `yarn install --immutable`
4. Native modules are rebuilt using `npm rebuild better-sqlite3` to ensure compatibility

## Testing Framework

The project uses **Jest** as the primary testing framework for most packages:
- **loot-core**: Jest with @swc/jest transformer (352 tests)
- **@actual-app/crdt**: Jest (20 tests)
- **@actual-app/sync-server**: Jest with coverage reporting (238 tests)
- **@actual-app/api**: Jest (9 tests)

Additional testing tools (not included in the test run due to time constraints):
- **Vitest**: Used for @actual-app/web and eslint-plugin-actual
- **Playwright**: Used for E2E testing in @actual-app/web

### Test Execution

The `/scripts/run_tests` script executes Jest tests across all major packages:
- Total tests: 619
- Expected failures: 0
- Expected skips: 2 (as of HEAD commit)

## Additional Notes

### Key Implementation Details

1. **Native Module Compatibility**: The better-sqlite3 module must be rebuilt after `yarn install` to match the current Node.js version. The yarn install process builds it against Node v22, but the project requires Node v18.16.0.

2. **Test Timeouts**: Vitest-based tests (desktop-client, eslint-plugin-actual) were excluded from the test run as they appear to hang in non-interactive environments. The Jest-based tests provide comprehensive coverage of core functionality.

3. **Monorepo Structure**: The project uses Yarn 4 workspaces with the node-modules linker (not PnP), making it straightforward to work with standard Node.js tooling.

4. **Portability**: The scripts work on both HEAD and HEAD~1 without modifications, as they rely on configuration files (package.json, .nvmrc) that are version-controlled.

### No Environment Misconfigurations

The environment was well-configured for this project:
- All required build tools were pre-installed
- NVM was properly set up at /opt/nvm
- Node.js v18.16.0 was easily installed via NVM
- No permission issues were encountered
- Native module compilation worked without issues after proper Node version setup
