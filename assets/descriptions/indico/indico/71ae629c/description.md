# Rename `scalar_exists()` to `has_rows()` and remove `IndicoModel.has_rows()`

## Summary
Rename the `scalar_exists()` method on `IndicoBaseQuery` to `has_rows()` for better clarity. Remove the `IndicoModel.has_rows()` class method in favor of using `Model.query.has_rows()` directly throughout the codebase.

## Why
- `has_rows()` is more descriptive and intuitive than `scalar_exists()`
- Having both `Model.has_rows()` and `Model.query.has_rows()` creates unnecessary API duplication
- Using `Model.query.has_rows()` makes it explicit that a query operation is being performed
- More consistent with the rest of the query API

## Changes

### Core Changes
- Rename `IndicoBaseQuery.scalar_exists()` → `IndicoBaseQuery.has_rows()`
- Remove `IndicoModel.has_rows()` class method (lines 136-143 in `models.py`)

### Code Updates
- Replace all `*.scalar_exists()` calls with `*.has_rows()` throughout:
  - `indico/modules/...` (categories, events, registration, reminders, sessions, surveys, tracks, vc, bootstrap, etc.)
  - `indico_zodbimport/modules/...` (all importer modules)
  
- Replace all `Model.has_rows()` calls with `Model.query.has_rows()`:
  - `User.has_rows()` → `User.query.has_rows()`
  - `Category.has_rows()` → `Category.query.has_rows()`
  - `AttachmentFolder.has_rows()` → `AttachmentFolder.query.has_rows()`
  - `Attachment.has_rows()` → `Attachment.query.has_rows()`
  - ... (all model classes)