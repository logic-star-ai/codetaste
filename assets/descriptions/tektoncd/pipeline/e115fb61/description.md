# Title
Rename `ConfigSource` and `source` to `RefSource` for better API consistency

# Summary
Rename the `ConfigSource` field in TaskRun/PipelineRun provenance and the `source` field in ResolutionRequest status to `RefSource` to decouple from SLSA versioning and improve naming clarity.

# Why
- **Leaky abstraction**: `ConfigSource` is tied to SLSA v0.2 spec, naming fields after external specs couples us to their versioning
- **Non-Tekton concept**: "config" isn't a concept that exists in Tekton
- **Too generic**: The name `source` in ResolutionRequest status is ambiguous

# Changes
- Rename `ConfigSource` struct → `RefSource` in v1 API
- Rename `configSource` field → `refSource` in `Provenance` struct
- Rename `source` field → `refSource` in `ResolutionRequest.Status`
- Update resolver interface method `Source()` → `RefSource()`
- Update all internal references and documentation

# Backward Compatibility
- Deprecate old fields (`configSource`, `source`) but keep them in v1beta1
- Populate both old and new fields during transition period
- Old fields will be removed in future release