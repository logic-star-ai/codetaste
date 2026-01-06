# Rename `ConfigSource` and `source` to `RefSource` for better API consistency

Rename the `ConfigSource` field in TaskRun/PipelineRun provenance and the `source` field in ResolutionRequest status to `RefSource` to decouple from SLSA versioning and improve naming clarity.