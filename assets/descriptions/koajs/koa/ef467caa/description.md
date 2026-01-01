# Modularize Application Tests

## Summary
Split monolithic `test/application.js` into focused test modules under `test/application/` directory. Reorganize test helpers into dedicated `test/helpers/` directory.

## Changes

**Test File Split**
- `test/application.js` → multiple files:
  - `test/application/index.js` - core app behavior
  - `test/application/toJSON.js` - serialization tests
  - `test/application/inspect.js` - inspection tests  
  - `test/application/use.js` - middleware composition
  - `test/application/onerror.js` - error handling
  - `test/application/respond.js` - response handling
  - `test/application/context.js` - context customization
  - `test/application/request.js` - request customization
  - `test/application/response.js` - response customization

**Helper Organization**
- `test/context.js` → `test/helpers/context.js`
- Update all imports across `test/{context,request,response}/*` files

**Build Configuration**
- Update Makefile: `test/application` → `test/application/*`
- Fix relative import paths (`..` → `../..`)

## Why
- Improve test discoverability and maintainability
- Enable faster, focused test execution
- Separate test utilities from actual tests
- Better organize ~1000 LOC file into logical modules

Closes #517