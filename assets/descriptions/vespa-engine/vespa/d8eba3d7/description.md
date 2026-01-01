# Title
-----
Rename disk/memory usage notification classes to generic resource usage naming

# Summary
-------
Refactor resource monitoring infrastructure by renaming classes, interfaces, methods, and files from `DiskMemUsage*` naming convention to more generic `ResourceUsage*` naming.

# Why
---
- Improve semantic clarity by using more generic "resource" terminology
- Better align naming with broader resource management concepts
- Make the API more extensible for additional resource types beyond disk/memory

# Changes
---------
**Classes/Interfaces renamed:**
- `DiskMemUsageNotifier` → `ResourceUsageNotifier`
- `DiskMemUsageState` → `ResourceUsageState`
- `IDiskMemUsageListener` → `IResourceUsageListener`
- `IDiskMemUsageNotifier` → `IResourceUsageNotifier`
- `DiskMemUsageForwarder` → `ResourceUsageForwarder`

**Methods renamed:**
- `notifyDiskMemUsage()` → `notify_resource_usage()`
- `addDiskMemUsageListener()` → `add_resource_usage_listener()`
- `removeDiskMemUsageListener()` → `remove_resource_usage_listener()`
- `diskMemUsageListener()` → `resource_usage_forwarder()`

**Files renamed:**
- `disk_mem_usage_{notifier,forwarder}.*` → `resource_usage_{notifier,forwarder}.*`
- `i_disk_mem_usage_{listener,notifier}.h` → `i_resource_usage_{listener,notifier}.h`
- `disk_mem_usage_state.h` → `resource_usage_state.h`

**Scope:**
- `searchcore/proton/server/...`
- `searchcore/proton/persistenceengine/...`
- `searchcore/proton/test/...`
- Test files and applications

# Notes
-------
Pure refactoring - no functional changes, only naming improvements for consistency and clarity.