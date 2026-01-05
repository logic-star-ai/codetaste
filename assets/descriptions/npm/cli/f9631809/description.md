# Refactor: Use `process.chdir()` in mockNpm instead of mocking `process.cwd()`

## Summary
Change `mockNpm` test helper to use actual `process.chdir()` for directory changes instead of mocking the `process.cwd()` getter.

## Why
- More realistic test behavior that mirrors actual npm usage
- Cleaner test code - eliminates need for mocking global `process.cwd`
- Simplifies test fixture setup and teardown

## Changes
- Add `changeDir()` helper that:
  - Calls `process.chdir(dir)` to change working directory
  - Returns teardown function to restore original cwd
- Add `chdir` option to `mockNpm` config (defaults to `prefix`)
- Remove `process.cwd` from mocked globals
- Update tests using `globals: { 'process.cwd': ... }` → `chdir: ...` option

## Implementation
```javascript
// New helper
const changeDir = (dir) => {
  const cwd = process.cwd()
  process.chdir(dir)
  return () => process.chdir(cwd)
}

// Usage in setupMockNpm
const teardownDir = changeDir(withDirs(chdir))
t.teardown(teardownDir)
```

## Test Updates
Replace patterns like:
```javascript
globals: ({ prefix }) => ({
  'process.cwd': () => join(prefix, 'some', 'path')
})
```

With:
```javascript
chdir: ({ prefix }) => join(prefix, 'some', 'path')
```