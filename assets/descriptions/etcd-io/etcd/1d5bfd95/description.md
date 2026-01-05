Title
-----
Rename `storage` package to `mvcc`

Summary
-------
Rename the `storage` package and all related sub-packages to `mvcc` to better reflect their purpose (Multi-Version Concurrency Control).

Why
---
The name `storage` is too generic. The package implements MVCC functionality, so naming it `mvcc` provides better clarity about its purpose and scope.

Changes
-------
**Package Renames:**
- `storage` → `mvcc`
- `storage/backend` → `mvcc/backend`
- `storage/storagepb` → `mvcc/storagepb` → `mvcc/mvccpb`

**Updates Required:**
- All import paths: `github.com/coreos/etcd/storage/*` → `github.com/coreos/etcd/mvcc/*`
- Package declarations in all `.go` files
- Error messages: `"storage:"` → `"mvcc:"`
- Documentation references and URLs
- Protobuf package names and generated code
- Test/benchmark files
- Tool commands: `storage-*` → `mvcc-*`

**Files Affected:**
- `etcdserver/`, `etcdctl/`, `clientv3/`, `integration/`, `compactor/`, `alarm/`, `auth/`, `lease/`, `contrib/recipes/`
- Documentation: `api_v3.md`, `api_reference_v3.md`, `interacting_v3.md`, `maintenance.md`, `v3api.md`
- Build scripts: `genproto.sh`, `test`

Scope
-----
- ~40+ files with import path updates
- All package files moved from `storage/*` to `mvcc/*`
- Protobuf regeneration required
- All references in documentation, comments, error messages updated