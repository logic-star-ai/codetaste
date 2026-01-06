# Introduce ChunkGraph to decouple chunk-module relationships

Extract chunk↔module relationship management into dedicated `ChunkGraph` class, removing direct coupling between `Chunk` and `Module` objects.