# Refactor integration tests to use `BeforeTest(t)` pattern

## Summary

Replace `defer AfterTest(t)` calls with `BeforeTest(t)` in integration tests. The new `BeforeTest(t)` method handles both test initialization and cleanup registration via `t.Cleanup(func)`.

## Why

- **Single entry point**: One method handles setup + cleanup registration
- **Idiomatic Go**: Leverages native `t.Cleanup(func)` instead of manual `defer`
- **Cleaner test structure**: Remove `defer` statements from test functions
- **Consistency**: Uniform pattern across all integration tests

## Changes

- Add `BeforeTest(testing.TB)` in `pkg/testutil/leak.go`
  - Registers `AfterTest(t)` via `t.Cleanup(func)`
- Replace `defer testutil.AfterTest(t)` → `testutil.BeforeTest(t)` across:
  - `client/v3/*_test.go`
  - `tests/integration/**/*_test.go`
  - `tests/e2e/*_test.go`
- Update `AfterTest` signature: `*testing.T` → `testing.TB`
- Add e2e-specific `BeforeTestV2(t)` wrapper for v2 API tests

## Example

```go
// Before
func TestExample(t *testing.T) {
    defer testutil.AfterTest(t)
    // ... test code
}

// After
func TestExample(t *testing.T) {
    testutil.BeforeTest(t)
    // ... test code
}
```