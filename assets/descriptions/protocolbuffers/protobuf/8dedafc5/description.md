# Title
Refactor Java generator: Reorganize into `immutable/` and `lite/` subdirectories

# Summary
Major refactoring of Java code generator structure to better separate immutable API from lite API implementations, preventing ODR violations and improving code organization.

# Changes

## Directory Reorganization
- Split Java generator code into `src/google/protobuf/compiler/java/{immutable,lite}/` subdirectories
- Moved immutable-specific implementations → `immutable/`
  - `enum.cc`, `message.cc`, `message_builder.cc`, `extension.cc`, `service.cc`, field generators...
- Moved lite-specific implementations → `lite/`
  - `enum_lite.cc` → `enum.cc`, `message_lite.cc` → `message.cc`, lite field generators...

## Code Split & Extraction
- Deleted monolithic `field.cc/h` 
- Created focused modules:
  - `field_common.{cc,h}`: Common field utilities (`SetCommonFieldVariables`, `PrintExtraFieldInfo`...)
  - `generator_common.h`: Shared interfaces (`FieldGenerator`, `FieldGeneratorMap`...)
  - `internal_helpers.{cc,h}`: Internal utilities (`GetExperimentalJavaFieldType`, `SupportUnknownEnumValue`, `CheckUtf8`...)
- Split `generator_factory.cc` into separate `immutable/generator_factory.cc` and `lite/generator_factory.cc`

## Factory Pattern Changes
- Created `make_field_generators.{cc,h}` in both `immutable/` and `lite/` 
- Replaced template-based `FieldGeneratorMap` construction with explicit factories
- `MakeImmutableFieldGenerators()` and `MakeImmutableFieldLiteGenerators()` functions
- Switched from raw pointers to `std::unique_ptr<>` in factory returns

## Interface Refinements
- Split `ImmutableFieldGenerator` → `immutable/field_generator.h`
- Split `ImmutableFieldLiteGenerator` → `lite/field_generator.h`
- Made `EnumGenerator`, `ExtensionGenerator`, `ServiceGenerator` abstract base classes in `generator_factory.h`
- Created `EnumNonLiteGenerator` (for immutable) and `EnumLiteGenerator` separately

## Build System Updates
- New `BUILD.bazel` files for `immutable/` and `lite/` packages
- Updated `file_lists.cmake` with new file paths
- Added `:kotlin` target dependency

## Why
- **Prevent ODR violations** from `java_features.proto` bootstrap
- **Clearer separation** between immutable and lite code paths
- **Reduced coupling** via smaller, focused modules
- **Improved maintainability** with explicit factory implementations
- **Better type safety** using `unique_ptr` over raw pointers