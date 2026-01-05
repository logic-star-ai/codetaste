# Title
Rename `key` to `keyRing` throughout codebase

## Summary
Follow-up refactoring to align naming conventions after `lib/client.Key` was renamed to `lib/client.KeyRing`. Update all related functions, variables, struct fields, and types to use `keyRing` terminology consistently.

## Changes
**Type renames:**
- `KeyIndex` → `KeyRingIndex`

**Function/method renames:**
- `AddKey()` → `AddKeyRing()`
- `GetKey()` → `GetKeyRing()`
- `DeleteKey()` → `DeleteKeyRing()`
- `LoadKey()` → `LoadKeyRing()`
- `UnloadKey()` → `UnloadKeyRing()`
- `activateKey()` → `activateKeyRing()`
- `GenerateRSAKey()` → `GenerateRSAKeyRing()`
- `AddDatabaseKey()` → `AddDatabaseKeyRing()`
- `AddKubeKey()` → `AddKubeKeyRing()`
- `AddAppKey()` → `AddAppKeyRing()`
- `GetCoreKey()` → `GetCoreKeyRing()`
- `LoadKeyForCluster()` → `LoadKeyRingForCluster()`
- `MustCreateUserKey()` → `MustCreateUserKeyRing()`
- ... and similar helpers

**Struct field renames:**
- `User.Key` → `User.KeyRing`
- `UserCreds.Key` → `UserCreds.KeyRing`
- `WriteConfig.Key` → `WriteConfig.KeyRing`
- `KeyRing.KeyIndex` → `KeyRing.KeyRingIndex`

**Variable renames:**
- `key` → `keyRing` across hundreds of call sites

## Scope
Purely cosmetic refactoring - no functional changes. Affects:
- `lib/client/*`
- `lib/tbot/*`
- `integration/*`
- `tool/tsh/*`
- `tool/tctl/*`
- `lib/kube/*`
- `lib/teleterm/*`