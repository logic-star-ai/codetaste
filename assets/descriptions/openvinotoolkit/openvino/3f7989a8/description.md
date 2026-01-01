# [CPU] Migrate CPU Plugin to Plugin API 2.0

## Summary
Migrate Intel CPU plugin from legacy plugin API 1.0 (InferenceEngine) to modern plugin API 2.0 (OpenVINO Runtime), replacing blob-based interfaces with tensor-based ones and updating all plugin components to use new API contracts.

## Why
- Modernize plugin architecture to align with OpenVINO 2.0
- Replace legacy blob-based API with tensor-based API
- Improve type safety and consistency across plugin interfaces
- Enable better support for dynamic shapes and modern features

## Changes

### Core Classes Renamed/Refactored
- `ExecNetwork` → `CompiledModel` (implements `ov::ICompiledModel`)
- `InferRequestBase/InferRequest/LegacyInferRequest` → `SyncInferRequest` (implements `ov::ISyncInferRequest`)
- `AsyncInferRequest` updated to use `ov::IAsyncInferRequest`
- `Engine` updated to implement `ov::IPlugin`

### API Method Changes
- `LoadExeNetworkImpl()` → `compile_model()`
- `ImportNetwork()` → `import_model()`
- `Export()` → `export_model()`
- `QueryNetwork()` → `query_model()`
- `GetBlob()/SetBlob()` → `get_tensor()/set_tensor()`
- `GetConfig()/SetConfig()` → `get_property()/set_property()`
- `GetMetric()` → `get_ro_property()`
- `InferImpl()` → `infer()`
- `GetPerformanceCounts()` → `get_profiling_info()`
- `QueryState()` → `query_state()`

### Data Handling
- Replace `InferenceEngine::Blob::Ptr` with `ov::SoPtr<ITensor>`
- Replace `BlobMap` with `std::unordered_map<std::string, ov::SoPtr<ITensor>>`
- Replace `CNNNetwork` with `ov::Model`
- Update all blob operations to tensor operations
- Remove legacy mean image preprocessing

### Precision Support
- Add support for U16/I16/U32/I64/U64/FP64 precisions
- Improve precision conversion handling
- Fix float→bool conversion with abs+ceil insertion
- Better precision mismatch error messages

### Serialization
- `CNNNetworkSerializer` → `ModelSerializer`
- `CNNNetworkDeserializer` → `ModelDeserializer`
- Update cache format to store model metadata

### Configuration/Properties
- Migrate all config keys to new property API
- Update streams calculation for new API
- Handle performance hints in new property format
- Support `ov::loaded_from_cache` property

### Memory Management
- Update memory state handling for new API
- Remove mean image blob caching
- Update external pointer management
- Fix ROI tensor stride handling

### Testing
- Skip legacy API tests incompatible with 2.0 behavior
- Update test expectations for new precision handling
- Fix python binding tests
- Update accuracy thresholds where needed

## Affected Components
- Plugin core (engine, compiled model, infer request)
- Graph execution
- Memory/state management
- Serialization/deserialization
- Configuration system
- All node implementations
- Test infrastructure
- Python bindings

## Notes
- Maintains backward compatibility mode via `isLegacyApi` flag
- Some transformations adjusted for new precision handling
- Reorder executor improved to support any precision
- Several edge cases fixed (dynamic shapes, empty tensors, etc.)