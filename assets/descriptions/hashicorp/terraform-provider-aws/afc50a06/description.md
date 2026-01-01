# Title
-----
Remove AWS SDK for Go v1 support from `internal/generate/tags` generator

# Summary
-------
Clean up `internal/generate/tags` generator by removing AWS SDK for Go v1 support, simplifying the codebase to only support AWS SDK for Go v2.

# Why
---
- Provider has migrated to AWS SDK for Go v2
- Maintaining dual SDK version support in the generator adds unnecessary complexity
- V1-specific code paths, templates, and flags are no longer needed
- Simplifies maintenance and reduces cognitive overhead for contributors

# Changes
---

## Generator Simplification
- Remove `sdkVersion` flag and related version selection logic
- Remove `sdkV1` and `sdkV2` constants
- Eliminate v1/v2 template switching in `newTemplateBody()`
- Consolidate template function map to include `Snake` helper

## Template Restructuring
- Move templates from `internal/generate/tags/templates/v2/` to `internal/generate/tags/templates/`
- Remove entire `internal/generate/tags/templates/v1/` directory
- Update template package name from `v2` to `templates`
- Simplify header template to always import AWS SDK v2 packages
- Remove conditional imports (ConnsPkg, FmtPkg, HelperSchemaPkg, etc.)

## Flag Cleanup
- Convert string-based boolean flags to actual booleans:
  - `ListTagsInIDNeedValueSlice`
  - `TagInIDNeedValueSlice`
  - `UntagInNeedTagKeyType`
  - `UntagInNeedTagType`
- Remove unused flags:
  - `skipAWSImp`
  - `skipNamesImp`
  - `skipServiceImp`
  - `skipTypesImp`
- Simplify `TagOpBatchSize` to int type

## namevaluesfilters Package
- Move from `internal/namevaluesfilters/v2/` to `internal/namevaluesfilters/`
- Update all service imports to use consolidated package
- Remove wrapper types and simplify API

## Documentation
- Remove AWS SDK version selection documentation from `docs/resource-tagging.md`
- Delete legacy README files: `README_keyvaluetags.md`, `README_listtags.md`, `README_servicetags.md`, `README_updatetags.md`
- Update remaining README with consolidated flag documentation table

## Service Package Updates
- Remove `-SkipTypesImp`, `-SkipAWSImp`, `-SkipServiceImp`, `-SkipNamesImp` flags from all `generate.go` directives across ~80+ service packages
- Update flag usage to boolean syntax (e.g., `-ListTagsInIDNeedValueSlice` instead of `-ListTagsInIDNeedValueSlice=yes`)

## Code Cleanup
- Move `ToSnakeCase()` from `internal/tags/key_value_tags.go` to `names/snake.go` for better organization
- Add comprehensive tests for snake case conversion
- Simplify client type generation to only support v2 format

# Testing
---
```console
% make testacc TESTARGS='-run=TestAccSecretsManagerSecretsDataSource_' PKG=secretsmanager
...
--- PASS: TestAccSecretsManagerSecretsDataSource_filter (47.22s)
PASS
```