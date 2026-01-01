# Title

Rename `NextChunk` to `Next` across codebase

# Summary

Simplify method name from `NextChunk()` to `Next()` for chunk-based data retrieval interfaces.

# Why

The method already takes a `*chunk.Chunk` parameter, making the "Chunk" suffix redundant. Shortening to `Next()` improves API clarity and conciseness while maintaining semantic meaning.

# Changes

**Interface Updates:**
- `ast.RecordSet.NextChunk()` → `Next()`
- `Executor.NextChunk()` → `Next()` 
- `distsql.SelectResult.NextChunk()` → `Next()`
- `server.ResultSet.NextChunk()` → `Next()`

**Implementation Updates:**
- All executor implementations (`executor/*`)
- DistSQL components (`distsql/*`)
- Session layer (`session/*`)
- Server drivers (`server/*`)
- Statistics collectors (`statistics/*`)
- Storage layer (`store/*`)
- Table operations (`table/*`)
- Test files (`*_test.go`)

**Documentation:**
- Update method comments
- Update inline documentation

# Scope

~100+ files affected across:
- `ast/`, `executor/`, `distsql/`, `session/`, `server/`, `statistics/`, `store/`, `table/`, `cmd/`, `ddl/`, `privilege/`