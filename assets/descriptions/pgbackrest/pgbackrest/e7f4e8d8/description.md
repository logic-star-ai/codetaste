# Title

Protocol command multiplexing

# Summary

Refactor protocol layer to support concurrent file operations on the same remote by introducing sessions and asynchronous request/response multiplexing.

# Why

Previously impossible to read/write two files simultaneously on same remote - protocol was entirely taken over by single read/write command. Multiple concurrent reads required for efficient restores when reading bundled files where blocks need to be retrieved from separate files or different parts of same file.

# Changes

**Session Support**
- Add `ProtocolClientSession` to track related commands with shared state
- Support three modes: synchronous, synchronous with session, asynchronous with session
- Sessions have open/process/close lifecycle
- Allow out-of-order response handling for async sessions

**Request/Response Model**
- Break read/write into separate requests instead of streaming all data at once
- Support async read/write requests to keep both client and server busy
- Optimize single-buffer reads to transfer in one command
- Skip explicit close when EOF reached (implicit close)

**Protocol Simplification**
- One response per request (removes `protocolMessageTypeDataEnd`)
- Data sent as request parameters (not separately outside parameters)
- Handler signature: `void handler(PackRead *, ProtocolServer *)` → `ProtocolServerResult *handler(PackRead *)`
- Remove `ProtocolCommand` object - use command ID + `PackWrite` params directly

**Command Types**
- `protocolCommandTypeOpen` - open session
- `protocolCommandTypeProcess` - process command
- `protocolCommandTypeClose` - close session
- `protocolCommandTypeCancel` - cancel session

**Handler Updates**
- `process` - standalone command (no session)
- `open` + `processSession` - session-based commands
- `open` + `processSession` + `close` - session with explicit close handler

**Db Protocol**
- Update to use new session infrastructure
- Remove custom session tracking (previously tracked via `remoteIdx`)

**Files Removed**
- `src/protocol/command.c`
- `src/protocol/command.h`

# Trade-offs

More back-and-forth for read/write operations, mitigated by:
- Async requests keep both endpoints busy
- Single-buffer reads optimized
- Implicit close on EOF
- Overall enables concurrent operations that weren't possible before