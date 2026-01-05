# Title
-----
Migrate `turbopack-core` to no-context naming convention

# Summary
-------
Refactor `turbopack-core` to eliminate ambiguous use of the name "context" by renaming to more specific identifiers throughout the crate.

# Why
---
The generic name "context" was overused for different purposes (file paths, asset contexts, chunking contexts, lookup paths), causing naming conflicts and reducing code clarity.

# Changes
---------
**AST Grep Rule Updates:**
- Fix `no-context.yml` to catch `function_item` instead of `function_type`
- Remove `turbopack-core` from ignore list

**Issue Trait Refactoring:**
- Rename `Issue::context()` → `Issue::file_path()`
- Rename `IssueContextExt` → `IssueFilePathExt`
- Rename methods: `attach_context()` → `attach_file_path()`, `issue_context()` → `issue_file_path()`
- Update `PlainIssue.context` → `PlainIssue.file_path`
- Update `IssueProcessingPathItem.context` → `IssueProcessingPathItem.file_path`

**Parameter Naming:**
- `context: Vc<Box<dyn ChunkingContext>>` → `chunking_context`
- `context: Vc<Box<dyn AssetContext>>` → `asset_context`
- `context: Vc<FileSystemPath>` → `lookup_path` / `lookup_dir` / `file_path` (depending on usage)
- `ChunkContentContext.context` → various specific fields
- `ResolveOrigin::context()` → `ResolveOrigin::asset_context()`

**Affected Areas:**
- Chunk processing and evaluation
- Module resolution and path lookups
- Import mapping
- Issue reporting and display
- All implementations across dependent crates (turbopack-*, turbo-tasks-fetch, node-file-trace)