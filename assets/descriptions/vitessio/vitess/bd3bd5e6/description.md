# Title
-----
Refactor flags from underscore to dash notation (Part 4)

# Summary
-------
Migrate 273 command-line flags from underscore (`_`) to dash (`-`) naming convention across vtbackup, vtcombo, vtctld, vtgate, vttablet, mysqlctl, mysqlctld, and related components. Update all flag definitions, documentation, examples, and tests to use the new dashed format while maintaining backward compatibility.

# Why
---
Standardize flag naming conventions across Vitess to follow industry best practices and improve consistency. Dash-separated flags are more idiomatic in modern CLI tools.

# Flags Migrated
---
**Backup & Storage** (31 flags):
- `--azblob-backup-*` (account-key-file, account-name, buffer-size, container-name, parallelism, storage-root)
- `--backup-engine-implementation`, `--backup-storage-*` (block-size, compress, implementation, number-blocks)
- `--builtinbackup-*` (mysqld-timeout, progress)
- `--gcs-backup-storage-*` (bucket, root)
- `--s3-backup-*` (aws-endpoint, aws-min-partsize, aws-region, aws-retries, force-path-style, log-level, server-side-encryption, storage-bucket, storage-root, tls-skip-verify-cert)
- `--xtrabackup-*` (backup-flags, prepare-flags, root-path, stream-mode, stripe-block-size, stripes, user)

**MySQL Configuration** (21 flags):
- `--mycnf-*` (bin-log-path, data-dir, error-log-path, general-log-path, innodb-data-home-dir, innodb-log-group-home-dir, master-info-file, mysql-port, pid-file, relay-log-index-path, relay-log-info-path, relay-log-path, secure-file-priv, server-id, slow-log-path, socket-file, tmp-dir)
- `--mysql-port`, `--mysql-server-port`, `--mysql-socket`, `--mysql-auth-server-impl`

**Tablet Configuration** (16 flags):
- `--init-*` (db-name-override, keyspace, shard, tablet-type, tags)
- `--tablet-*` (grpc-ca, grpc-cert, grpc-crl, grpc-key, grpc-server-name, hostname, protocol, refresh-interval, refresh-known-tablets, types-to-wait, uid, url-template)

**Topology & Heartbeat** (7 flags):
- `--srv-topo-*` (cache-refresh, cache-ttl, timeout)
- `--heartbeat-enable`, `--heartbeat-interval`
- `--replication-connect-retry`
- `--remote-operation-timeout`

**Other** (3 flags):
- `--consul-auth-static-file`
- `--initialize-with-random-data`
- `--emit-stats`
- `--pool-hostname-resolve-interval`

# Implementation Details
---
- Use new `utils.SetFlag*Var()` helpers to register both dashed and underscored variants
- Update flag definitions across: vtbackup, vtcombo, vtctld, vtgate, vttablet, mysqlctl, mysqlctld
- Maintain backward compatibility by supporting both variants until v25
- Add TODOs for cleanup: `//TODO: Remove underscore(_) flags in v25, replace them with dashed(-) notation`
- Update all documentation, examples, docker-compose files, and shell scripts
- Modify test utilities to use dashed variants via `GetFlagVariantForTests()`

# Files Modified
---
- **Core flag definitions**: `go/vt/{mysqlctl,vtgate,vttablet,discovery,srvtopo,topo}/**/*.go`
- **CLI commands**: `go/cmd/{mysqlctl,mysqlctld,vtbackup,vtcombo,vtctld,vtgate,vttablet,vttestserver}/cli/**/*.go`
- **Documentation**: `go/flags/endtoend/*.txt`, `config/tablet/default.yaml`
- **Examples & Scripts**: `examples/**/*.{sh,yml}`, `go/test/endtoend/**/*_test.go`
- **Test utilities**: `go/vt/utils/flags.go`

# Testing
---
- Verify backward compatibility for underscored flags
- Update ~50 test files to use dashed variants
- Ensure flag help text shows dashed format
- Confirm both variants work until deprecation in v25

# Migration Path
---
**Now (v24)**: Both `--flag_name` and `--flag-name` work  
**v25**: Remove underscore support, enforce dashed-only