# Refactor to non-global file systems

Eliminate global file system state throughout Hugo by moving to instance-based file systems passed through a dependency structure. This involves creating a new `deps` package to hold shared dependencies and refactoring all file system access to use `*hugofs.Fs` instances instead of global functions.