# Complete `RegionKind` renaming: `ReEarlyBound` → `ReEarlyParam`, `ReFree` → `ReLateParam`

Rename region kinds and related types to use more descriptive terminology:
- `ReEarlyBound` → `ReEarlyParam`
- `ReFree` → `ReLateParam`
- `EarlyBoundRegion` → `EarlyParamRegion`
- `FreeRegion` → `LateParamRegion`
- `RegionNameSource::NamedEarlyBoundRegion` → `NamedEarlyParamRegion`
- `RegionNameSource::NamedFreeRegion` → `NamedLateParamRegion`
- `infer::EarlyBoundRegion` → `RegionParameterDefinition`

Update `CheckRegions` enum:
- `OnlyEarlyBound` → `OnlyParam`
- `Bound` → `FromFunction`

Rename methods:
- `lub_free_regions` → `lub_param_regions`
- `is_free_or_static` → `is_free` (with updated semantics)