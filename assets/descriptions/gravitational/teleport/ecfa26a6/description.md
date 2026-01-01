# Title
-----
Refactor `client.Key` → `client.KeyRing` and un-embed `PrivateKey`

# Summary
-------
Rename `client.Key` to `client.KeyRing` and convert the embedded `keys.PrivateKey` to an explicit field. This prepares the codebase for RFD 136, which will introduce unique private keys per certificate.

# Why
---
Currently, `client.Key` embeds `keys.PrivateKey`, allowing direct method calls like `key.MarshalSSHPublicKey()`. Under RFD 136, each certificate will have its own unique key rather than sharing a single private key. 

By un-embedding and making `PrivateKey` explicit, all current usage sites become easier to identify and migrate.

# Changes
-------
- Rename `client.Key` → `client.KeyRing` throughout codebase
- Change `PrivateKey` from embedded anonymous field to explicit struct field
- Update all call sites: `key.Method()` → `key.PrivateKey.Method()`
- Update function signatures, return types, variables, etc.

# Scope
-----
- `lib/client/...`
- `lib/tbot/...`
- `tool/tsh/...`
- `integration/...`
- Test files

# Notes
-----
No functional changes. Pure refactoring to make future migration clearer.