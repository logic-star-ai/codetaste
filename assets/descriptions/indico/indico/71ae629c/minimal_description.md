# Rename `scalar_exists()` to `has_rows()` and remove `IndicoModel.has_rows()`

Rename the `scalar_exists()` method on `IndicoBaseQuery` to `has_rows()` for better clarity. Remove the `IndicoModel.has_rows()` class method in favor of using `Model.query.has_rows()` directly throughout the codebase.