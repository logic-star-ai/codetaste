Title
-----
Rename response flag types: `ResponseFlag` → `CoreResponseFlag`, `ExtendedResponseFlag` → `ResponseFlag`

Summary
-------
Refactor stream info response flag types to improve API clarity. Rename the core `ResponseFlag` enum to `CoreResponseFlag` and rename `ExtendedResponseFlag` class to `ResponseFlag`.

Why
---
- Current naming with `ExtendedResponseFlag` is confusing and not intuitive
- The `ResponseFlag` enum should be called `CoreResponseFlag` to clarify it represents core/built-in flags
- The extendable `ExtendedResponseFlag` class should become the primary `ResponseFlag` type

Changes
-------
1. **Type Renames**:
   - `ResponseFlag` enum → `CoreResponseFlag` enum
   - `ExtendedResponseFlag` class → `ResponseFlag` class

2. **Macro Updates**:
   - Update `REGISTER_CUSTOM_RESPONSE_FLAG` macro parameters: `short` → `short_flag_string`, `long` → `long_flag_string`
   - Update `CUSTOM_RESPONSE_FLAG` macro accordingly

3. **Flag Metadata Structure**:
   - Update `CORE_RESPONSE_FLAGS` array from `std::pair<FlagStrings, ResponseFlag>` → `FlagStrings{...}` with flag included
   - Add `flag_` field to `FlagStrings` struct

4. **Test Updates**:
   - Add `LegacyResponseFlagTest` to ensure `legacyResponseFlags()` method works correctly with backward compatibility
   - Update existing tests to use new type names

5. **API Updates**:
   - Update all `setResponseFlag()` / `hasResponseFlag()` call sites across codebase
   - Update `streamResetReasonToResponseFlag()` return type
   - Update response flag utility methods

Scope
-----
- `envoy/stream_info/stream_info.h` - Core interface definitions
- `source/common/stream_info/` - Implementation files
- `source/common/http/` - HTTP connection manager, codec, router
- `source/common/router/` - Router filter
- `source/extensions/` - All filters using response flags
- `test/` - All corresponding test files
- `contrib/` - Contrib filters

Risk
----
Low - No functional changes, pure refactoring with mechanical renames