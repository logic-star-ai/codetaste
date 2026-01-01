Title
-----
Remove commons-logging dependency and migrate to SLF4J

Summary
-------
Remove all references to Apache Commons Logging and migrate to SLF4J-based logging throughout the Hadoop codebase. Restrict future usage through Maven Enforcer rules.

Why
---
- Part of Log4j1 to Log4j2 migration effort (HADOOP-16206)
- Commons-logging is an outdated logging facade
- SLF4J provides better logging abstraction and is already used in parts of the codebase
- Need consistent logging approach across all modules

Changes
-------
**Dependency Removal:**
- Remove `commons-logging:commons-logging:1.1.3` from LICENSE-binary
- Remove commons-logging dependency from hadoop-common, hadoop-nfs, hadoop-hdfs modules, hadoop-mapreduce-client, hadoop-archive-logs, and test dependencies

**Code Migration:**
- Replace `org.apache.commons.logging.Log` with `org.slf4j.Logger` across codebase
- Replace `LogFactory.getLog()` with `LoggerFactory.getLogger()`
- Update DataNode, FSNamesystem, NameNode metrics logging to use logger names instead of Log objects
- Update MetricsLoggerTask constructor to accept String logger name

**API Changes:**
- Deprecate `IOUtils.cleanup(Log, Closeable...)` 
- Deprecate `ServiceOperations.stopQuietly(Log, Service)`
- Deprecate `ReflectionUtils.logThreadInfo(Log, ...)`
- Remove `LogAdapter` utility class entirely
- Simplify LogLevel servlet to work directly with Log4j Logger
- Update SignalLogger to accept slf4j Logger

**Test Infrastructure:**
- Update GenericTestUtils.LogCapturer to work with slf4j/log4j
- Remove commons-logging based test helper methods
- Update test classes to use slf4j Logger

**Enforcement:**
- Add Maven Enforcer `restrictImports` rule to ban `org.apache.commons.logging.**` imports
- Apply to both main and test code

Affected Components
-------------------
- hadoop-common
- hadoop-hdfs (datanode, namenode, rbf)
- hadoop-nfs
- hadoop-mapreduce
- hadoop-yarn (appcatalog, resourcemanager, nodemanager)
- hadoop-azure tools
- Test utilities and infrastructure