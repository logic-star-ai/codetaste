# Refactor: Use `process.chdir()` in mockNpm instead of mocking `process.cwd()`

Change `mockNpm` test helper to use actual `process.chdir()` for directory changes instead of mocking the `process.cwd()` getter.