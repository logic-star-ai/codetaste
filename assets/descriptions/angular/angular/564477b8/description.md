# Title
Rename View and Template concepts for clarity

# Summary
Rename core annotations and properties to better reflect their purpose and reduce ambiguity between the `@Template` annotation and the internal `View` class.

# Why
- Naming collision: The `@Template` annotation and internal `View` class names were ambiguous
- Semantic clarity: `properties` better describes directive property bindings than `bind`
- Consistency: `hostListeners` more accurately describes DOM event listeners
- Alignment: `injectables` is more precise than `services` for dependency injection configuration

# What
**Annotation Renames:**
- `@Template` → `@View`
- File: `template.js` → `view.js`

**Property Renames:**
- `bind` → `properties` (directive property bindings)
- `events` → `hostListeners` (DOM event handlers)  
- `services` → `injectables` (DI configuration)
- `inline` → `template` (inline template string)
- `url` → `templateUrl` (external template URL)

**Internal Class Renames:**
- `View` → `AppView` (to disambiguate from `@View` annotation)
- `ProtoView` → `AppProtoView`

**Affected Areas:**
- Core annotations & compiler
- All directives (`For`, `If`, `Switch`, etc.)
- Form directives
- Documentation
- Examples & benchmarks
- Test infrastructure
- Dart transformer

# References
Fixes #1244