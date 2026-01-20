# Rename statistics classes to improve naming clarity

Refactor statistics-related classes to use clearer, more concise naming conventions by:
- Removing `ShardingSphere` prefix from internal statistics classes
- Explicitly using `Statistics` suffix instead of `Data`
- Updating all related methods, fields, and accessors