Title
-----
Refactor: Remove "cricontainerd" from all variable, type, and function names

Summary
-------
Systematic rename of all variables, types, functions, and comments to remove the "cricontainerd" naming convention across the codebase.

Why
---
- Simplifies naming by removing redundant "containerd" reference in CRI plugin context
- Makes codebase more maintainable with clearer, shorter identifiers
- Aligns naming with actual component purpose (CRI plugin vs cri-containerd)

Changes
-------

**Types & Interfaces:**
- `criContainerdService` → `criService`
- `CRIContainerdService` → `CRIService`
- `CRIContainerdServiceClient` → `CRIPluginServiceClient`
- `CRIContainerdServiceServer` → `CRIPluginServiceServer`

**Functions:**
- `NewCRIContainerdService()` → `NewCRIService()`
- `NewCRIContainerdClient()` → `NewCRIPluginClient()`
- `newTestCRIContainerdService()` → `newTestCRIService()`
- ...all receiver methods updated...

**Variables:**
- `criContainerdClient` → `criPluginClient`
- `criContainerdEndpoint` → `criEndpoint`
- `criContainerdRoot` → `criRoot`

**Proto Definitions:**
- Service `CRIContainerdService` → `CRIPluginService`
- Comments: "cri-containerd" → "cri plugin"

**Documentation:**
- Update comments/docs referencing "cri-containerd" to "CRI plugin" or "CRI service"

Scope
-----
- `cli/`, `pkg/server/`, `pkg/client/`, `pkg/api/`, `integration/`
- Proto definitions & generated code
- Test files & utilities