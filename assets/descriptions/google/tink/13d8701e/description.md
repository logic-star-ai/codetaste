# Refactor: Extract registry and keyset packages from tink core

## Summary

Move `registry` and `keyset` functionality out of the `tink` package into their own dedicated packages. This eliminates protobuf dependencies from both `tink` and `subtle` packages.

## Changes

### New Package Structure

**`go/registry/`** - Key manager and KMS client registry
- `KeyManager` interface (was `tink.KeyManager`)
- `PrivateKeyManager` interface (was `tink.PrivateKeyManager`) 
- `KMSClient` interface (was `tink.KMSClient`)
- `RegisterKeyManager()`, `GetKeyManager()`, etc.
- `NewKeyData()`, `NewKey()`, `Primitive()`, etc.

**`go/keyset/`** - Keyset handle and management
- `Handle` type (was `tink.KeysetHandle`)
- `Manager` type (was `tink.KeysetManager`)
- `Reader`/`Writer` interfaces (was `tink.KeysetReader`/`KeysetWriter`)
- `BinaryReader`/`BinaryWriter` (was `tink.BinaryKeysetReader`/`BinaryKeysetWriter`)
- `MemReaderWriter` (was `tink.MemKeyset`)
- `Primitives()`, `PrimitivesWithKeyManager()` moved to `Handle` methods

**`go/insecurecleartextkeyset/`** (renamed from `go/insecure/`)
- `Read()` (was `NewKeysetHandleFromReader()`)
- `Write()` (was `WriteUnencryptedKeysetHandle()`)

**`go/testkeyset/`** (renamed from `go/testkeysethandle/`)
- `NewHandle()` (was `KeysetHandle()`)
- `Read()`, `Write()` test helpers

### Type & Function Renames

**Keyset operations:**
- `tink.NewKeysetHandle()` → `keyset.NewHandle()`
- `tink.NewKeysetHandleFromReader()` → `keyset.Read()`
- `tink.NewKeysetHandleFromReaderWithNoSecrets()` → `keyset.ReadWithNoSecrets()`
- `tink.KeysetHandleWithNoSecret()` → `keyset.NewHandleWithNoSecrets()`
- `tink.NewKeysetManager()` → `keyset.NewManager()`
- `tink.FromKeysetHandle()` → `keyset.NewManagerFromHandle()`
- `KeysetManager.KeysetHandle()` → `Manager.Handle()`

**Registry operations:**
- `tink.RegisterKeyManager()` → `registry.RegisterKeyManager()`
- `tink.GetKeyManager()` → `registry.GetKeyManager()`
- `tink.NewKeyData()` → `registry.NewKeyData()`
- `tink.NewKey()` → `registry.NewKey()`
- `tink.Primitive()` → `registry.Primitive()`
- `tink.RegisterKMSClient()` → `registry.RegisterKMSClient()`
- `tink.GetKMSClient()` → `registry.GetKMSClient()`

### Updated Imports

All packages importing keyset/registry functionality updated:
- `aead/*`, `daead/*`, `mac/*`, `signature/*` → import `keyset` and `registry`
- Factory functions now accept `keyset.Handle` and `registry.KeyManager`

## Why

- **Separation of concerns**: Registry management and keyset handling are distinct responsibilities
- **Reduced dependencies**: Core `tink` package no longer depends on protobuf
- **Cleaner API surface**: Each package has focused, cohesive functionality
- **Better testability**: Separate packages for insecure/test utilities