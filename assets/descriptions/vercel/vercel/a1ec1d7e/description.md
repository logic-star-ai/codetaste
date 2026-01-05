# Refactor: Decouple `Output` from `Client` for improved testability

## Summary

Refactor the `Output` class usage to be a managed singleton instead of being directly coupled to the `Client` instance. This enables better testability of the CLI entrypoint and allows the output configuration to be modified as the program flows.

## Why

- The CLI entrypoint is difficult to unit test due to tight coupling between `Output` and `Client`
- Direct system dependencies make it hard to mock and control output behavior
- The current architecture requires passing `client.output` through many function layers
- Need to decouple output handling from client instance lifecycle

## Changes

### Core

- Create `output-manager.ts` singleton wrapping `Output` class
- Remove `output: Output` property from `Client` class
- Add `initialize()` method to allow runtime configuration of output settings

### Usage Pattern

**Before:**
```ts
client.output.debug('some message');
client.output.error('error message');
```

**After:**
```ts
import output from './output-manager';
output.debug('some message');
output.error('error message');
```

### Affected Areas

- Remove `output` parameter from ~100+ function signatures across:
  - `util/alias/*`
  - `util/certs/*`
  - `util/deploy/*`
  - `util/domains/*`
  - `util/env/*`
  - `commands/*` (all commands)
- Update all call sites to use singleton import
- Update test setup to initialize output globally
- Update mocks to work with singleton pattern

### Test Infrastructure

- Add `vitest.config.mts` and `vitest.setup.mts` for CLI-specific test setup
- Initialize output singleton in test setup with disabled colors/hyperlinks
- Update test snapshots (colors removed from output)
- Loosen regex in integration tests to accommodate line breaks

## Benefits

- Enables future refactoring of CLI entrypoint for unit testing
- Reduces function signature complexity (one less parameter everywhere)
- Centralizes output configuration management
- Makes output behavior easier to control in tests