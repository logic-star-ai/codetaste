# Title
Remove regex engine singleton and pass explicitly as dependency

# Summary
Refactor regex engine usage to eliminate singleton pattern and use explicit dependency injection instead. All `parseRegex()` calls and regex-related components now require an explicit `Engine&` parameter.

# Why
- Singleton creates hidden dependencies and global state
- Makes testing harder (requires `ScopedInjectableLoader` workarounds)
- Unclear ownership and lifecycle
- Potential thread safety concerns

# Changes

## Core Infrastructure
- Remove `EngineSingleton` typedef and `InjectableSingleton<Engine>` usage from `regex.h`
- Remove `parseRegex()` overload that relied on singleton lookup
- Update all `parseRegex()` calls to accept explicit `Engine&` parameter
- Remove `EngineSingleton::initialize()` call from `server/regex_engine.cc`

## Updated Components
- `HeaderHashMethod`, `HashPolicyImpl` - accept `regex_engine` in constructor
- `HeaderUtility::HeaderData` - get engine from `factory_context`
- `NullRouteImpl`, `RouteEntryImpl` - pass engine through
- `ImmediateMutationChecker` - moved from static local to `FilterConfig` member
- Various filter configs: `header_to_metadata`, `json_to_metadata`, `payload_to_metadata`, etc.
- `Checker` (mutation rules) - accept engine in constructor

## Tests
- Remove `ScopedInjectableLoader<Regex::Engine>` from ~20+ test files
- Add `regex_engine_` member where needed for explicit passing
- Update integration tests to use `test_server_->server().regexEngine()`

# Risk
Low - purely mechanical refactoring, no behavior changes