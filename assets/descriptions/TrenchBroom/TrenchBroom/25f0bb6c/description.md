# Refactor entity definition modeling to use `std::variant`

## Summary

Replace inheritance-based entity and property definition model with simpler `std::variant`-based model.

## Why

Simplify codebase by eliminating class hierarchies for entity and property definitions.

## Changes

**Property Definitions:**
- Flatten `PropertyDefinition` class hierarchy into single struct
- Use `PropertyValueType` (std::variant) containing `String`, `Integer`, `Float`, `Boolean`, `Choice`, `Flags`, `TargetSource`, `TargetDestination`, `Unknown`
- Remove derived classes: `StringPropertyDefinition`, `IntegerPropertyDefinition`, `FloatPropertyDefinition`, `BooleanPropertyDefinition`, `ChoicePropertyDefinition`, `FlagsPropertyDefinition`
- Change from `definition->key()` to `definition.key` (direct member access)

**Entity Definitions:**
- Flatten `EntityDefinition` hierarchy (remove `PointEntityDefinition`/`BrushEntityDefinition` subclasses)
- Use `std::optional<PointEntityDefinition>` to distinguish point/brush entities
- Add utility functions: `getType()`, `getPointEntityDefinition()`, `getShortName()`, `getGroupName()`
- Remove virtual methods, use pattern matching on variant types

**Ownership & Memory:**
- Replace `std::unique_ptr<EntityDefinition>` with value semantics
- Store definitions in `std::vector<EntityDefinition>` instead of `std::vector<std::unique_ptr<...>>`
- Remove pointer-based caching
- Use `const EntityDefinition*` for references (non-owning)

**API Changes:**
- `parseDefinitions()` returns `Result<std::vector<EntityDefinition>>`
- Parser methods return `PropertyDefinition` or `std::optional<PropertyDefinition>` instead of `std::unique_ptr`
- `EntityDefinition::definition()` returns `const EntityDefinition*`
- Remove `EntityDefinitionType` enum values: `PointEntity`→`Point`, `BrushEntity`→`Brush`

**Files:**
- Add `mdl/EntityDefinitionUtils.h`
- Simplify parsers (DefParser, EntParser, FgdParser)
- Update all consumers of entity definitions