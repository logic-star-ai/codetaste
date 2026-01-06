# Refactor: Break circular dependencies in `@angular/core` by extracting symbols to dedicated files

Clean up circular dependencies in the core package by extracting symbols into separate, focused files. This reduces ~8 circular dependency chains tracked in the golden file.