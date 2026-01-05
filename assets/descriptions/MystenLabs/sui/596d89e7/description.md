# Refactor ConsensusV2 to use dedicated variant for single-owner

## Summary

Simplify consensus object ownership representation by replacing `Owner::ConsensusV2 { authenticator: Box<Authenticator> }` with `Owner::ConsensusAddressOwner { owner: SuiAddress }` and removing the `Authenticator` type entirely.

## Why

The `Authenticator` abstraction was over-engineered for the current use case:
- Only single-owner authentication is supported
- Nested structure (`Owner` → `Authenticator` → `SingleOwner`) adds unnecessary complexity
- Direct representation in `Owner` enum is clearer and more maintainable

## Changes

- **Type Changes**:
  - Rename `Owner::ConsensusV2` → `Owner::ConsensusAddressOwner`
  - Replace `authenticator: Box<Authenticator>` field with `owner: SuiAddress`
  - Remove `Authenticator` enum entirely

- **API Updates**:
  - GraphQL schema: `ConsensusV2` → `ConsensusAddressOwner`, remove `Authenticator` union
  - OpenRPC spec: update owner type definitions
  - Remove `Owner::authenticator()` method, use direct field access

- **Code Updates**:
  - Update pattern matching across execution, indexing, RPC, and analytics code
  - Simplify owner extraction logic (no more `authenticator.as_single_owner()`)
  - Update comments/TODOs referencing ConsensusV2
  - Fix test snapshots (gas costs changed due to smaller data structure)

## Future Work

If additional authorization modes are needed, add new variants to the `Owner` enum (e.g., `ConsensusMultiSig`, `ConsensusThreshold`, etc.) rather than reintroducing the `Authenticator` abstraction.