# Refactor EVM ORMs to remove pg dependency

Refactor Headtracker, Forwarder, and Logpoller ORMs to remove dependency on `core/services/pg` and `Q` type. Migrate to using `sqlutil.DB` interface and explicit context propagation.