# Refactor integration tests to use `BeforeTest(t)` pattern

Replace `defer AfterTest(t)` calls with `BeforeTest(t)` in integration tests. The new `BeforeTest(t)` method handles both test initialization and cleanup registration via `t.Cleanup(func)`.