# Refactor remaining `ImmutableOpenMap` usage to `java.util.Map` and remove class

Replace all remaining occurrences of HPPC-backed `ImmutableOpenMap<K, V>` with standard `java.util.Map<K, V>` and completely remove the `ImmutableOpenMap` class from the codebase.