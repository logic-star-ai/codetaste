# Refactor: Migrate to new driver adapter interface

Refactor SQL driver adapters to use a simplified interface with factory pattern for instantiation. Removes `TransactionContext` abstraction and consolidates transaction lifecycle management.