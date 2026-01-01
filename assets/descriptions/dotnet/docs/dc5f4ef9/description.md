# Reorganize LINQ standard query operators documentation

## Summary

Restructure LINQ standard query operators content to improve organization and consolidate related articles. Move files from `programming-guide/concepts/linq/` to `linq/standard-query-operators/`, merge multiple articles covering similar topics, and remove redundant content.

## Why

- Current structure has LINQ content scattered across multiple sections
- Multiple articles covering joins/groups need consolidation
- Many articles only list API methods without adding conceptual value
- Part of "Everyday C#" content reorganization effort

## Changes Required

### File Moves
- Move standard query operators articles to `docs/csharp/linq/standard-query-operators/`
- Relocate samples to `snippets/standard-query-operators/` folder

### Consolidation
- Merge join-related articles:
  - `perform-inner-joins.md`
  - `perform-left-outer-joins.md`  
  - `perform-grouped-joins.md`
  - `perform-custom-join-operations.md`
  - `join-by-using-composite-keys.md`
  - → Single `join-operations.md`
  
- Merge grouping articles:
  - `group-query-results.md`
  - `create-a-nested-group.md`
  - `perform-a-subquery-on-a-grouping-operation.md`
  - → Single `grouping-data.md`

### Content Updates
- Remove method-listing-only articles (aggregation-operations, concatenation-operations, element-operations, equality-operations, generation-operations, etc.)
- Add pointers to `System.Linq.Enumerable` API reference for comprehensive method lists
- Update index/overview article to remove complex examples
- Provide both query syntax and method syntax examples throughout
- Add notes on available methods pointing to API docs

### Cleanup
- Update all redirects in `.openpublishing.redirection.csharp.json`
- Fix relative links throughout affected articles
- Remove obsolete sample code and tests
- Update cross-references across C# and VB documentation

## Scope

Standard query operators section only - projection, filtering, sorting, set operations, quantifier operations, partitioning, data conversion, grouping, and join operations.