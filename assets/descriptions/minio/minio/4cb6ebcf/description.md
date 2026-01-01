# Refactor: Reorganize bucket-related packages into hierarchical structure

## Summary
Reorganize `pkg/{tagging,lifecycle,objectlock,policy}` packages into `pkg/bucket/*` subdirectory for better hierarchy and grouping of bucket-related features.

## Why
- Current flat structure under `pkg/` lacks clear organization
- Bucket-related features scattered across multiple top-level packages
- Need proper hierarchical structure to accommodate future bucket features
- Better code organization and discoverability

## Changes

**Package Moves:**
- `pkg/tagging` → `pkg/bucket/object/tagging`
- `pkg/lifecycle` → `pkg/bucket/lifecycle`  
- `pkg/objectlock` → `pkg/bucket/object/lock`
- `pkg/policy` → `pkg/bucket/policy`

**Import Path Updates:**
- Update all imports across `cmd/*`, `cmd/gateway/*`, `pkg/iam/policy/*`
- Update go.mod dependencies
- No functional code changes

## Scope
- [ ] Move package directories to new locations
- [ ] Update import paths throughout codebase (cmd/, gateway/, iam/, ...)
- [ ] Verify all tests pass with new structure
- [ ] Ensure no breaking changes to public APIs