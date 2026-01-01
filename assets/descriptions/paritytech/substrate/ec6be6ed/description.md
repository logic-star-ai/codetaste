Title
-----
Simplify state backend by fixing transaction type to `PrefixedMemoryDB`

Summary
-------
Remove `Backend::Transaction` associated type and fix it to `PrefixedMemoryDB<H>`, eliminating unnecessary generics throughout the codebase.

Why
---
`PrefixedMemoryDB` was always the transaction type used in Substrate. The generic parameter added complexity without providing actual flexibility.

Changes
-------
- Remove `Backend::Transaction` associated type
- Introduce `BackendTransaction<H>` type alias for `PrefixedMemoryDB<H>`
- Move storage transaction cache into `OverlayedChanges`
- `BlockImportParams<Block, Transaction>` → `BlockImportParams<Block>`
- `DefaultImportQueue<Block, Client>` → `DefaultImportQueue<Block>`
- Remove `Transaction` generic from `BlockImport`, `Proposer`, `Environment` traits
- Remove `TransactionFor`, `TransactionForSB`, `StateBackendFor` type aliases
- Update `StorageChanges<Transaction, H>` → `StorageChanges<H>`
- Remove `storage_transaction_cache` parameter from `CallExecutor::contextual_call`
- Simplify `ApiExt::into_storage_changes` to take backend generically

Downstream Impact
-----------------
- Remove `TransactionFor<...>` / `StateBackend::Transaction` from where bounds
- Update `BlockImportParams` usage to single generic parameter
- Update `DefaultImportQueue` usage to single generic parameter
- Remove transaction-related generic parameters from implementations