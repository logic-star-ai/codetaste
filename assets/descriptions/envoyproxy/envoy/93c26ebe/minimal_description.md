# Consolidate listener info into `ListenerInfo` interface and expose in factory contexts

Refactor listener-related information (`direction`, `metadata`, `typedMetadata`, `isQuic`) from scattered context methods into a dedicated `ListenerInfo` interface, making it accessible across wider contexts including access loggers.