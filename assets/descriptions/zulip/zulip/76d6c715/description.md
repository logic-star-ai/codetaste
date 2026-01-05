# Refactor test fixture loading methods

## Summary
Separate webhook and general test fixture loading into distinct methods and standardize fixture data access across test suite.

## Why
- Webhook fixtures (`zerver/webhooks/*/fixtures/`) and general test fixtures (`zerver/tests/fixtures/`) were using the same method, causing confusion
- Many tests were manually constructing file paths and opening files, leading to code duplication
- No clear API contract for loading fixtures

## Changes
1. **Rename existing method**: `fixture_data()` → `webhook_fixture_data()` in `ZulipTestCase` for webhook-specific fixtures
2. **Add new method**: `fixture_data(file_name, type='')` in `ZulipTestCase` for general test fixtures from `zerver/tests/fixtures/`
3. **Update all webhook tests**: Replace `self.fixture_data(...)` → `self.webhook_fixture_data(...)`
4. **Refactor general tests**: Replace manual file path construction + `open()` calls with `self.fixture_data(...)`
5. **Remove constants**: Eliminate `MAILS_DIR`, `FIXTURES_FILE_PATH`, etc.
6. **Update docs**: Modify `webhook-walkthrough.md` to reflect new method name

## Files affected
- `zerver/lib/test_classes.py` (core methods)
- `zerver/webhooks/*/tests.py` (~40 webhook test files)
- `zerver/tests/test_*.py` (decorators, email_mirror, notifications, push_notifications, report, slack_importer)
- `templates/zerver/api/webhook-walkthrough.md`