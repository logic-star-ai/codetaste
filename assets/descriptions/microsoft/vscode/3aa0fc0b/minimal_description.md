# Refactor smoke UI automation into separate package

Split `smoke` project into two packages: `test/smoke` (test cases + test runner) and `test/automation` (UI automation driver + component automation modules). Smoke tests now depend on automation package via local filesystem reference.