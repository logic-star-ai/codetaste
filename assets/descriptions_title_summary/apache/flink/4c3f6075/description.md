# Refactor AbstractInvokable to accept Environment and State in constructor

Refactor `AbstractInvokable` and remove `StatefulTask` interface to implement RAII pattern for task runtime classes. Tasks now receive all required state via constructor instead of setter methods.