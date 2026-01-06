# Decouple pure replication state from storage

Refactor replication components to separate pure replication concerns from storage-specific implementation. Establishes cleaner architecture where replication state (epoch, role, durability) is independent of storage, with a handler layer coordinating between them.