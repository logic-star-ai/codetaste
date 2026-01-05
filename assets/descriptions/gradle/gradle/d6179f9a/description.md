# Title

Rename "conventions" to "model defaults" across DSL components

# Summary

Comprehensive terminology update from "conventions" → "model defaults" throughout the declarative DSL infrastructure to better reflect the actual purpose of these constructs.

# Changes

**Core Concepts**
- `Conventions` interface → `SharedModelDefaults`
- `conventions { }` DSL block → `defaults { }`
- Convention-related classes/interfaces → ModelDefault equivalents

**Resolution Results**
- `conventionAssignments/Additions/NestedObjectAccess` → `assignmentsFromDefaults/...`
- `ConventionApplication` feature → `ApplyModelDefaults`
- `ConventionDefinition` feature → `DefineModelDefaults`

**Handlers & Processors**
- `ConventionApplicationHandler` → `ApplyModelDefaultsHandler`
- `ConventionDefinitionCollector` → `ModelDefaultsDefinitionCollector`
- `SoftwareTypeConventionApplicator` → `ModelDefaultsApplicator`
- ...and related infrastructure classes

**Package Restructuring**
- `.evaluator.conventions` → `.evaluator.defaults`
- Files moved/renamed accordingly

**Schema & Configuration**
- `ConventionsTopLevelReceiver` → `DefaultsTopLevelReceiver`
- `ConventionsConfiguringBlock` → `DefaultsConfiguringBlock`
- `buildConventions` → `modelDefaults` in schemas

**Settings & API**
- `Settings.getConventions()` → `Settings.getDefaults()`
- `Settings.conventions(Action)` → `Settings.defaults(Action)`

# Scope

- All internal declarative DSL modules
- Kotlin DSL accessor generation
- Plugin infrastructure
- Tests and integration tests
- Documentation references