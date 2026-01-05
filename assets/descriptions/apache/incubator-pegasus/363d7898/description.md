# Title
Refactor: Extract security module from runtime into standalone component

## Summary
Move the security module from `src/runtime/security/` to `src/security/` to establish it as an independent component with reduced dependencies. Create dedicated test suite `dsn_security_tests` separate from `dsn_runtime_tests`.

## Changes

### Directory Structure
- Move `src/runtime/security/*` → `src/security/*`
- Move security tests from `src/runtime/test/*` → `src/security/test/*`

### Build System
- Add `src/security/` as top-level subdirectory in main CMakeLists
- Convert `dsn.security` object library to `dsn_security` standalone library
- Update `dsn_runtime` to link against `dsn_security` instead of embedding object files
- Create new test target `dsn_security_tests` with dedicated config & run script

### Include Paths
Update all imports across codebase:
- `#include "runtime/security/*.h"` → `#include "security/*.h"`
- Affected files in:
  - `src/meta/...`
  - `src/replica/...`
  - `src/runtime/service_api_c.cpp`
  - All security source/test files

### CI/CD
- Add `dsn_security_tests` to GitHub workflow matrices (Ubuntu/macOS test jobs)

## Why
- Reduce coupling between runtime and security components
- Decrease library size and dependency footprint
- Enable independent testing and development of security features
- Improve build modularity