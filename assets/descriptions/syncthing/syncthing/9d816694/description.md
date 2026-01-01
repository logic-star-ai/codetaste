# Title
Rename core terminology: Repository → Folder, Node → Device

## Summary
Comprehensive refactoring to replace terminology throughout the entire codebase:
- `Repository` → `Folder`
- `Node` → `Device`

This affects all layers: internal packages, protocol definitions, configuration files, GUI, documentation, and tests.

## Why
The original terminology was unintuitive and potentially confusing:
- "Repository" suggests version control semantics, while we're actually synchronizing directories
- "Node" is too abstract; "Device" more clearly represents the physical/logical entity (computer, phone, server, etc.)

More intuitive naming improves:
- User understanding
- Developer onboarding
- Documentation clarity
- API comprehension

## Changes

### Code (Go)
- All internal packages: `model`, `config`, `protocol`, `stats`, `versioner`, ...
- Type renames: `NodeID` → `DeviceID`, `NodeConfiguration` → `DeviceConfiguration`, `RepositoryConfiguration` → `FolderConfiguration`, etc.
- Variable/field renames: `node*` → `device*`, `repo*` → `folder*`
- Function signatures updated throughout

### Protocol
- Wire format structures: `Repository` → `Folder`, `Node` → `Device`
- Message field names in XDR definitions
- Documentation updates in `PROTOCOL.md` and `DISCOVERY.md`

### Configuration
- XML elements: `<repository>` → `<folder>`, `<node>` → `<device>`
- All test configuration files updated

### GUI
- JavaScript: variables, functions, API endpoints
- HTML: templates, labels, IDs
- REST API paths: `/rest/nodeid` → `/rest/deviceid`, query params `repo=` → `folder=`, etc.

### Documentation
- README, CONTRIBUTING, protocol specs
- All references updated for consistency

### Breaking Changes
- **Configuration format** (XML schema)
- **REST API** endpoints and parameters
- **Database keys** (internal)

## Impact
- ✅ More intuitive terminology
- ✅ Better alignment with user mental models
- ⚠️ Breaking changes require migration/upgrade logic