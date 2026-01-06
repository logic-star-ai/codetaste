# Replace Context lock guards with closure-based API to prevent deadlocks

Refactor `Context` (and `Ui`) accessor methods to use closures instead of returning `RwLockReadGuard`/`RwLockWriteGuard`. This prevents accidental double-locking deadlocks.