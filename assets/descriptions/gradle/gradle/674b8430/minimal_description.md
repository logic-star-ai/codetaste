# Refactor `ProjectIdentity` to enforce path invariants and remove DM dependencies

Cleanup and refactor `ProjectIdentity` to enforce the relationship between build path, project path, and identity path. Replace `BuildIdentifier` with `Path` to remove dependency on DM types, and introduce restricted factory methods to guarantee invariants for root vs. non-root projects.