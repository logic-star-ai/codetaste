# Title
-----
Refactor ShenYu-Infra module to centralize infrastructure dependencies

# Summary
-------
Reorganize infrastructure modules (Redis, Nacos, Etcd) to eliminate duplicate code, centralize configuration, and improve maintainability. Creates dedicated infra modules with auto-configuration support and consolidates scattered infrastructure client implementations.

# Why
---
- Duplicate infrastructure client code (Redis, Etcd) exists across multiple modules
- Configuration properties scattered throughout codebase
- No centralized location for infrastructure dependencies
- Inconsistent patterns for infrastructure integration
- Hard to maintain and reuse infrastructure components

# What Changed
---
**Module Structure:**
- Created `shenyu-infra-common` for shared infrastructure code
- Consolidated `shenyu-infra-redis`, `shenyu-infra-nacos`, `shenyu-infra-etcd` modules
- Added auto-configuration support with conditional annotations

**Code Consolidation:**
- Moved `RedisConfigProperties`, `RedisConnectionFactory`, serializers → `shenyu-infra-redis`
- Moved `EtcdClient` from admin-listener/sync-data/registry → `shenyu-infra-etcd`
- Moved Nacos config classes → `shenyu-infra-nacos`
- Removed duplicate implementations across modules

**Configuration:**
- Created `InfraParentProperties` base class with standard prefix `shenyu.sync.*`
- Added `@ConditionOnSyncEtcd`, `@ConditionOnSyncNacos` conditional annotations
- Implemented builder pattern for config classes (`EtcdConfig`, `NacosConfig`, `NacosACMConfig`)
- Added Spring Boot auto-configuration files

**Constants:**
- Added `ShenyuModuleConstants`, `InfraConstants` for module naming
- Updated property prefix resolution using constants

**Dependency Updates:**
- Updated ~20+ modules to use new infra dependencies
- Removed redundant dependency declarations
- Updated imports across codebase

**Benefits:**
- Single source of truth for infrastructure clients
- Reduced code duplication by ~1000+ lines
- Easier testing and mocking
- Consistent configuration patterns
- Better separation of concerns