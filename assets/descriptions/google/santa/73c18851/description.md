# Title
-----
Simplify namespace hierarchy for endpoint security logging components

# Summary
-------
Flatten deeply nested C++ namespaces in endpoint security logging code. Convert `santa::santad::logs::endpoint_security::*` namespaces to top-level `santa` namespace, following Google C++ style guide recommendations.

# Why
---
- Current namespace nesting (`santa::santad::logs::endpoint_security::serializers::Utilities`) is excessively deep
- Style guide recommends single top-level namespace per project unless necessary
- Reduces verbosity in code and improves readability
- Minimizes exposure to naming collisions

# Scope
------
Convert the following namespaces to `santa::`:

- `santa::santad::logs::endpoint_security::serializers::Utilities`
- `santa::santad::logs::endpoint_security::writers`
- `santa::santad::logs::endpoint_security::serializers`  
- `santa::santad::logs::endpoint_security`

Additional changes:
- Convert `santatest` to anonymous namespace in test files
- Rename type aliases to avoid conflicts (e.g., `PathList` → `PathAndTypeVec`, `ProcessList` → `PolicyProcessVec`)
- Update all using declarations, forward declarations, and references

# Components Affected
-------------------
- Logger and MockLogger
- Serializers: BasicString, Empty, Protobuf, SanitizableString, Utilities
- Writers: File, Null, Spool, Syslog
- All test files for above components
- Integration points: SNTCompilerController, SNTDaemonControlController, Santad, SantadDeps, EndpointSecurity event providers