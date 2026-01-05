# Refactor Java generator into separate packages and targets

## Summary
Reorganize Java code generator into distinct packages for immutable and lite implementations, improving modularity and maintainability.

## Changes

### Directory Structure
- Created `src/google/protobuf/compiler/java/immutable/` for immutable generator implementations
- Created `src/google/protobuf/compiler/java/lite/` for lite generator implementations
- Kept common code at top level (`helpers.h`, `context.h`, etc.)

### Code Reorganization
- **Split `field.h`/`field.cc`**:
  - Common field utilities → `field_common.h`/`field_common.cc`
  - Generator interfaces → `generator_common.h`
  - Immutable field generators → `immutable/field_generator.h` + concrete implementations
  - Lite field generators → `lite/field_generator.h` + concrete implementations

- **Moved generators by type**:
  - Immutable: `enum.cc`, `message.cc`, `message_builder.cc`, `extension.cc`, `service.cc`, `*_field.cc` → `immutable/`
  - Lite: `enum_lite.cc`, `message_lite.cc`, `message_builder_lite.cc`, `extension_lite.cc`, `*_field_lite.cc` → `lite/`

- **Factory pattern**:
  - Extracted factory implementations into `immutable/generator_factory.cc` and `lite/generator_factory.cc`
  - Defined common `GeneratorFactory` interface in `generator_factory.h`
  - Added `MakeImmutableGeneratorFactory()` and `MakeImmutableLiteGeneratorFactory()`

- **Field generator creation**:
  - Added `make_field_generators.cc` in both `immutable/` and `lite/` directories
  - Encapsulates field generator instantiation logic

### Build Configuration
- Updated `BUILD.bazel` files with new target structure
- Added `:kotlin` target visibility
- Organized dependencies to reflect new package hierarchy
- Used abbreviated target names in immutable/BUILD.bazel to work around Bazel limitations

### API Changes
- `FieldGeneratorMap<T>` constructor no longer creates generators internally
- Field generators created via `MakeImmutable*Generators()` functions
- `GeneratorFactory` returns `std::unique_ptr<>` instead of raw pointers
- Service/Enum/Extension generators now inherit from common base classes

## Benefits
- **Clearer separation** between immutable and lite implementations
- **Better encapsulation** of generator creation logic
- **Improved maintainability** with smaller, focused files
- **Cleaner dependencies** between components
- **Easier testing** with isolated packages