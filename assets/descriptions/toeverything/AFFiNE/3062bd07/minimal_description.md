# Remove global types from edgeless implementation

Refactor edgeless block types from global `BlockSuite.*` namespace declarations to explicit type imports and exports. Eliminates ambient type declarations across surface elements, blocks, and related utilities.