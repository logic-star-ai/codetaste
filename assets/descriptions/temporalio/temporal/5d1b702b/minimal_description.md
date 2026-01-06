# Split MutableState interface from implementation

Move `MutableState` interface + related types to `service/history/interfaces` package, separating interface from implementation to reduce code entanglement and dependency graph bloat.