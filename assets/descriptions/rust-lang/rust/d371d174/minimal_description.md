# Refactor TLS implementation to improve maintainability and modularity

Consolidate platform-specific TLS (Thread-Local Storage) code into a unified, modular structure under `sys/thread_local/` to simplify future porting efforts and reduce code duplication.