Title
-----
Rename "chill mode" to "safe mode" across HDDS/Ozone codebase

Summary
-------
Comprehensive terminology change replacing all occurrences of "chill mode" with "safe mode" throughout the codebase.

Why
---
Align with standard distributed systems terminology and improve clarity.

Changes
-------
**Class & Package Renaming:**
- `SCMChillModeManager` → `SCMSafeModeManager`
- `ChillModeHandler` → `SafeModeHandler`
- `*ChillModeRule` classes → `*SafeModeRule` classes
- `ChillModePrecheck` → `SafeModePrecheck`
- Package: `org.apache.hadoop.hdds.scm.chillmode` → `org.apache.hadoop.hdds.scm.safemode`

**Method Renaming:**
- `inChillMode()` → `inSafeMode()`
- `forceExitChillMode()` → `forceExitSafeMode()`
- `setChillModeStatus()` → `setSafeModeStatus()`
- `getChillModeStatus()` → `getSafeModeStatus()`
- ... and related methods

**Configuration Keys:**
- `hdds.scm.chillmode.*` → `hdds.scm.safemode.*`
- `HDDS_SCM_CHILLMODE_*` → `HDDS_SCM_SAFEMODE_*`

**Protocol Changes:**
- Protobuf message renaming: `InChillModeRequest/Response` → `InSafeModeRequest/Response`
- `ForceExitChillModeRequest/Response` → `ForceExitSafeModeRequest/Response`
- RPC service methods updated
- SCM action enums: `IN_CHILL_MODE` → `IN_SAFE_MODE`, `FORCE_EXIT_CHILL_MODE` → `FORCE_EXIT_SAFE_MODE`

**CLI Tools:**
- `ChillModeCommands` → `SafeModeCommands`
- Command: `ozone scm chillmode` → `ozone scm safemode`
- Subcommands: `ChillModeCheckSubcommand`, `ChillModeExitSubcommand` → `SafeModeCheck/ExitSubcommand`

**Event & Exception Handling:**
- Event: `CHILL_MODE_STATUS` → `SAFE_MODE_STATUS`
- Exception code: `CHILL_MODE_EXCEPTION` → `SAFE_MODE_EXCEPTION`
- Delete result: `chillMode` → `safeMode`

**Test & Documentation Updates:**
- All test classes renamed (`TestSCMChillModeManager` → `TestSCMSafeModeManager`, etc.)
- Comments, log messages, and documentation updated
- Web UI labels updated
- Configuration file documentation (`ozone-default.xml`)

Scope
-----
Affects:
- `hadoop-hdds/client`
- `hadoop-hdds/common`
- `hadoop-hdds/server-scm`
- `hadoop-hdds/tools`
- `hadoop-ozone/integration-test`
- `hadoop-ozone/ozone-manager`
- `hadoop-ozone/tools`