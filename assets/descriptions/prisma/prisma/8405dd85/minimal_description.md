# Extract `@prisma/dmmf` and `@prisma/generator` packages for better modularity

Create two new packages to extract common types and utilities from `@prisma/generator-helper`:
- `@prisma/dmmf` - DMMF types and utilities
- `@prisma/generator` - Generator configuration types and utilities

`@prisma/generator-helper` remains for backward compatibility with third-party generators using JSON-RPC interface.