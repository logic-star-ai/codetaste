# Rename "delegation" terminology to "stake" throughout framework

## Summary

Perform large-scale rename of "delegation/delegate" terminology to "stake/staking" across Move framework, Rust, and TypeScript. This improves clarity and consistency by using staking terminology that better reflects the actual functionality.

## Scope

### Move Framework

**Entry functions renamed** (sui_system.move):
- `request_add_delegation*` → `request_add_stake*` (4 variants)
- `request_withdraw_delegation` → `request_withdraw_stake`

**Object fields**:
- `StakingPool::pending_delegation` → `pending_stake`
- `StakedSui::delegation_activation_epoch` → `stake_activation_epoch`

**Internal functions**:
- `process_pending_delegations_and_withdraws` → `process_pending_stakes_and_withdraws`
- `deposit_delegation_rewards` → `deposit_stake_rewards`
- Similar renames in staking_pool, validator, validator_set modules

### Rust

**Type renames**:
- `DelegatedStake` → `Stake`
- `DelegationStatus` → `StakeStatus`

**Constants**:
- `ADD_DELEGATION_*_FUN_NAME` → `ADD_STAKE_*_FUN_NAME`
- `WITHDRAW_DELEGATION_FUN_NAME` → `WITHDRAW_STAKE_FUN_NAME`

**API methods** (TransactionBuilder):
- `request_add_delegation()` → `request_add_stake()`
- `request_withdraw_delegation()` → `request_withdraw_stake()`

### TypeScript SDK

**Methods**:
- `newRequestAddDelegationTxn()` → `newRequestAddStakeTxn()`
- `newRequestWithdrawlDelegationTxn()` → `newRequestWithdrawlStakeTxn()`

**RPC endpoints**:
- `sui_requestAddDelegation` → `sui_requestAddStake`
- `sui_requestWithdrawDelegation` → `sui_requestWithdrawStake`

### Additional Changes

- Test files: `delegation_tests.move` → `stake_tests.move`
- Variable/parameter names: `delegator` → `staker`, `delegate_amount` → `stake_amount`, etc.
- Comments/documentation throughout
- Event: `DelegationRequestEvent` → `StakingRequestEvent`

## Why

Current "delegation" terminology is misleading - users are staking SUI with validators, not delegating authority. "Stake" terminology is more accurate and intuitive.

## Breaking Changes

- ⚠️ **Move**: All entry function names changed
- ⚠️ **Move**: Object field names changed (on-chain data)
- ⚠️ **Rust**: Public API method names changed
- ⚠️ **TypeScript**: SDK method names and RPC endpoints changed
- ⚠️ All clients must update to use new function/method names

## Notes

- TypeScript keeps `DelegatedStake` type (existing `Stake` type had different meaning)
- No functional changes - pure rename
- Affects validators, FNs, and all client SDKs