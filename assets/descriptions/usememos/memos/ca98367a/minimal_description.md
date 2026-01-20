# Refactor: Move migration and seed code into Driver layer

Consolidate database migration and seed logic from `store/db` package into the `store/sqlite` driver implementation. Eliminate the `store/db.DB` abstraction by merging its responsibilities directly into `Driver`.