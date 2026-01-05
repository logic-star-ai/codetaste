# Refactor: Move utility modules from `src/utils/` to `src/client/common/utils/`

## Summary
Reorganize codebase by relocating utility modules from `src/utils/` into `src/client/common/utils/` to improve code organization and align utilities with client code structure.

## Why
- Better alignment with project structure where utilities should reside within the client folder
- Improved code organization and maintainability
- Consistent module hierarchy

## Changes

### Files Moved
Move the following utility modules:
- `async.ts`
- `decorators.ts`
- `enum.ts`
- `fs.ts`
- `localize.ts`
- `logging.ts`
- `misc.ts`
- `platform.ts`
- `random.ts`
- `stopWatch.ts`
- `string.ts`
- `sysTypes.ts`
- `text.ts`
- `version.ts`

### Import Updates
Update all import statements across the codebase:
- Activation services
- Common modules (installer, net, platform, process, terminal, variables)
- Debugger
- Formatters
- Interpreter configuration & locators
- Language services
- Linters
- Providers
- Refactoring
- Telemetry
- Unit tests
- All test files

### Test Files
Move corresponding test files from `src/test/utils/` to `src/test/common/utils/`:
- `async.unit.test.ts`
- `platform.unit.test.ts`
- `string.unit.test.ts`
- `text.unit.test.ts`
- `version.unit.test.ts`
- `localize.unit.test.ts`

## Notes
- Pure refactoring - no functional changes
- All imports updated to use `../../client/common/utils/...` or `../common/utils/...` as appropriate