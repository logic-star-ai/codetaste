# Unify VectorReader and IVectorReader interfaces with consistent naming

Refactor to bring `VectorReader` and `IVectorReader` together by having `IVectorReader` implement `VectorReader`, standardizing method names across both interfaces, and converting `IVectorReader` to Kotlin for consistent null-typing.