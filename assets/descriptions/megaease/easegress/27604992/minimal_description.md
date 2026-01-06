# Refactor: Remove duplicated code in proxy implementations

Consolidate duplicated load balancing, request matching, and server pool management code between HTTP and gRPC proxy filters into a unified `proxies` package with shared interfaces and implementations.