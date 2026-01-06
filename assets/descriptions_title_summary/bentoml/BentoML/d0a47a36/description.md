# Refactor: Move legacy APIs to `bentoml.legacy` module

Move deprecated APIs (`Service`, `Runner`, `Runnable`, `Strategy`, `Resource`, `HTTPServer`, `GrpcServer`) from top-level `bentoml` namespace to new `bentoml.legacy` module to avoid naming conflicts with new SDK.