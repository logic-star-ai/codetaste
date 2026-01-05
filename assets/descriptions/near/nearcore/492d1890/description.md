# Title

Update borsh dependency to v1.0.0

# Summary

Upgrade borsh serialization library from v0.10.2 to v1.0.0 across the entire codebase.

# Why

Borsh-rs 1.0.0 is a major milestone release with breaking changes requiring migration throughout nearcore.

# Changes Required

**Cargo.toml**
- Update `borsh = "0.10.2"` → `borsh = "1.0.0"` with `features = ["derive", "rc"]`

**Serialization API**
- Replace `.try_to_vec()` → `borsh::to_vec()`
- Use `borsh::object_length()` for size calculations without serialization
- Replace `borsh::to_writer()` for file writing

**Attribute Syntax**
- `#[borsh_init(init)]` → `#[borsh(init=init)]`
- `#[borsh_skip]` → `#[borsh(skip)]`
- Add `#[borsh(use_discriminant = false)]` for enums where needed

**Import Changes**
- Remove explicit `BorshSerialize` trait imports in many places
- Change `use borsh::{BorshDeserialize, BorshSerialize}` → `use borsh::BorshDeserialize`
- Add `use borsh` or specific function imports where needed

**Namespace Updates**
- `borsh::maybestd::collections::*` → `std::collections::*`
- `borsh::maybestd::sync::Arc` → `std::sync::Arc`
- `borsh::maybestd::io::Error` → `std::io::Error`
- `borsh::maybestd::io::Read` → `std::io::Read`

**Error Handling**
- Update error kind: `ErrorKind::InvalidInput` → `ErrorKind::InvalidData` (for empty buffer deserialization)
- Parse error types now use `std::io::Error`

**Custom Deserializers**
- Update `deserialize_reader<R: borsh::maybestd::io::Read>` → `deserialize_reader<R: Read>`

# Files Affected

- ~200+ files across chain, core, integration-tests, nearcore, runtime, and tools
- All crates using borsh serialization/deserialization

# Migration Guide

Reference: https://github.com/near/borsh-rs/blob/borsh-v1.0.0/docs/migration_guides/v0.10.2_to_v1.0.0_nearcore.md