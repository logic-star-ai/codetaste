# Refactor JSON config parsing architecture

Massive refactoring of JSON configuration parsing across all proxy types. Consolidates JSON parsing logic, eliminates unnecessary interface abstractions, and introduces build-tag-based conditional compilation for JSON support.