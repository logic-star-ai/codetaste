# Title

Remove `.Type()` and `.Route()` from all message types

# Summary

Refactor to eliminate deprecated `.Type()` and `.Route()` methods from all message implementations across the SDK, simplifying the `legacytx.LegacyMsg` interface.

# Why

These methods are legacy artifacts that add unnecessary boilerplate:
- Their functionality is now provided by `sdk.MsgTypeURL()`
- Simplifies the `legacytx.LegacyMsg` interface to only what's essential (`GetSignBytes()`)
- Reduces code duplication across all message types

# Changes

**Message Types** (x/auth, x/bank, x/staking, x/gov, x/distribution, x/slashing, x/authz, x/feegrant, x/group, x/upgrade, x/crisis, x/mint, x/consensus, x/vesting, x/evidence):
- Remove `Type()` method from all msg implementations
- Remove `Route()` method from all msg implementations
- Retain `legacytx.LegacyMsg` interface implementation where needed (for `GetSignBytes()` only)

**Interface**:
- Simplify `legacytx.LegacyMsg` interface to only require `GetSignBytes()`

**Simulation**:
- Replace `msg.Type()` calls with `sdk.MsgTypeURL(msg)` throughout
- Remove `MsgType` field from `simulation.OperationInput` struct
- Update all simulation operations to use `sdk.MsgTypeURL()` for message identification
- Update `NoOpMsg()` and `NewOperationMsg()` calls with correct module names

**Helpers**:
- Add `GetModuleNameFromTypeURL()` utility to extract module name from type URL (e.g., `cosmos.bank.v1beta1.MsgSend` → `bank`)

**Tests**:
- Update all test assertions to use `sdk.MsgTypeURL()` for message type comparisons

# Breaking Changes

- **API**: `legacytx.LegacyMsg` interface signature changed
- **Simulation**: `OperationInput` struct no longer contains `MsgType` field