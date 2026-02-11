# Summary

This repository is Strapi, a headless CMS built with Node.js/TypeScript. The project uses Jest for unit testing across a monorepo structure with multiple packages.

## System Dependencies

No additional system-level services (databases, Redis, etc.) are required for running unit tests.

## Project Environment

- **Language**: TypeScript/JavaScript (Node.js)
- **Package Manager**: Yarn 3.6.1 (Berry)
- **Node Version**: Requires Node 16-20 (tested with Node 18.20.8)
- **Build System**: Nx workspace with multiple packages
- **Dependencies**: Installed via `yarn install`

## Testing Framework

- **Framework**: Jest 29.6.0
- **Configuration**: `jest.config.js` with multiple project-specific configs
- **Test Types Available**:
  - `test:unit` - Unit tests across all packages
  - `test:front` - Frontend tests
  - `test:api` - API integration tests
  - `test:e2e` - End-to-end tests

## Additional Notes

### Native Module Compatibility Issue

There is a significant blocker preventing successful dependency installation and test execution:

**Issue**: The `better-sqlite3` package (v8.6.0) fails to compile with Node.js 20+ due to V8 API changes. The package attempts to use deprecated V8 APIs that were removed in Node 22 and have compilation issues even with Node 18-20.

**Error**: `v8::ObjectTemplate::SetAccessor` signature mismatch - the native addon uses an old API signature that's incompatible with modern Node.js versions.

**Impact**: Yarn's strict mode causes the entire `yarn install` to fail when better-sqlite3 fails to build, preventing installation of any dependencies including Jest and other test infrastructure.

**Attempted Solutions**:
1. Tried Node 18, 19, 20 - all fail with similar V8 API errors
2. Attempted `--mode=skip-build` and `--ignore-optional` flags - Yarn still enforces build success
3. Cleared node-gyp cache to ensure correct Node headers - didn't resolve the API mismatch
4. better-sqlite3 v8.6.0 appears to need updating for Node 18+ compatibility

**Workaround Needed**: The repository maintainers would need to either:
- Update better-sqlite3 to a newer version that supports Node 18+
- Make better-sqlite3 an optional dependency
- Provide prebuilt binaries for the target Node versions
- Use a different SQL library that's compatible with modern Node.js

Due to this blocker, the test scripts created are non-functional placeholders. The scripts document the intended setup process, but cannot successfully execute until the native module compatibility issue is resolved.
