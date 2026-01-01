Title
-----
Refactor CLI clients to reduce duplication and improve code organization

Summary
-------
Consolidate overlapping code between `kcadm` and `kcreg` CLI tools by extracting common functionality into shared packages and base classes. Reorganize package structure to clearly delineate code roles and responsibilities.

Why
---
- Significant code duplication exists between `admin-cli` and `client-registration-cli` modules
- Unclear separation between shared and tool-specific code
- Duplicate shading configuration between the two clients
- Difficult to maintain consistency across both CLI tools

What Changed
------------
**Package Restructuring:**
- Created `org.keycloak.client.cli.common.*` for shared command logic
- Created `org.keycloak.client.cli.config.*` for shared configuration classes
- Created `org.keycloak.client.cli.util.*` for shared utilities
- Moved tool-specific code to respective `kcadm`/`kcreg` packages

**Deduplicated Classes:**
- `AttributeKey`, `AttributeOperation` → `client.cli.common`
- `ConfigData`, `RealmConfigData`, `ConfigHandler`, `FileConfigHandler`, `InMemoryConfigHandler` → `client.cli.config`
- `IoUtil`, `HttpUtil`, `ConfigUtil`, `AuthUtil`, `OsUtil`, `ParseUtil` → `client.cli.util`
- `CmdStdinContext` → moved to tool-specific packages but with common base logic

**Introduced Base Classes:**
- `BaseAuthOptionsCmd` - common auth options handling
- `BaseConfigCredentialsCmd` - common credentials configuration
- `BaseConfigTruststoreCmd` - common truststore configuration  
- `BaseGlobalOptionsCmd` - common global options

**New Abstractions:**
- `CommandState` interface - abstracts command-specific constants (CMD, DEFAULT_CONFIG_FILE_PATH, etc.)
- `GlobalOptionsCmdHelper` interface - common helper methods for commands

**Removed Duplication:**
- Eliminated duplicate `AbstractGlobalOptionsCmd` implementations
- Consolidated utility class functionality (AuthUtil, ConfigUtil, etc.)
- Unified parsing and reflection utilities

Impact
------
- Easier maintenance - changes to common functionality only need to be made once
- Clearer code organization - shared vs. tool-specific code is obvious from package structure
- Foundation for future work - prepares for consolidating both tools into single module
- Reduced distribution size - less duplicate shading required

Testing
-------
- All existing CLI tests updated with new import paths
- Test behavior remains unchanged - pure refactoring