# Title
Refactor: Move topo cell map into topo package, introduce Conn interface

## Summary
Major architectural refactoring of topology server implementation. Moves cell management from individual backend implementations into the central `topo` package. Backends now only provide connection objects (`Conn`) and factory methods instead of managing cells themselves.

## Changes

### Core Architecture
- Rename `topo.Backend` → `topo.Conn` interface
- Remove `cell` parameter from all `Conn` methods (connection is now cell-specific)
  - `ListDir(ctx, cell, dirPath)` → `ListDir(ctx, dirPath)`
  - `Create(ctx, cell, filePath, ...)` → `Create(ctx, filePath, ...)`
  - Similar for `Update`, `Get`, `Delete`, `Watch`, `Lock`
- Add `topo.Server.ConnForCell(ctx, cell)` to obtain cell-specific connections
- Store global cell connection directly in `Server.globalCell`
- Update `Factory.Create(serverAddr, root)` → `Factory.Create(cell, serverAddr, root)`

### Implementation Changes
**consultopo/etcd2topo/zk2topo:**
- Remove cell map and `cellClient`/`instance` types
- Remove `clientForCell()` / `connForCell()` methods  
- `Server` struct now directly implements `Conn` interface
- Cell creation/lookup handled by parent `topo.Server`

**memorytopo:**
- Introduce `Factory` struct (holds single data tree for all cells)
- Introduce `Conn` struct (cell-specific view into factory data)
- Each `Conn` operates on subtree for its cell

**helpers (Tee):**
- Create `TeeFactory` implementing `topo.Factory`
- Create `TeeConn` implementing `topo.Conn`
- Remove cell management logic from Tee implementation

### Usage Changes
- High-level code: `ts.globalCell.Method()` instead of `ts.Impl.Method(ctx, GlobalCell, ...)`
- Cell-specific ops: Get `Conn` via `ts.ConnForCell(ctx, cell)` first, then call methods
- Lock/Watch/Election operations work on `Conn` not `Server+cell`

## Why
- **Simplifies backend implementations**: No need to duplicate cell management logic
- **Cleaner separation**: Backend = connection to topo server, not cell manager
- **Easier to implement new backends**: Just implement `Conn` + `Factory`
- **More consistent API**: Cell-specific connection → cell-specific operations
- **Reduces duplication**: Cell map logic was duplicated across all implementations