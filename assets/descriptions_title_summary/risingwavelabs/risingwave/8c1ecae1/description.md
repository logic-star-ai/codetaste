# refactor(stream): refactor `trait Executor` to get rid of `info()`

Refactor the `Executor` trait to cleanly separate executor metadata (`ExecutorInfo`) from execution logic, eliminating unnecessary code duplication and preventing info consistency issues.