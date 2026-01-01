Title
-----
Remove Writable wire protocol types and translators to complete Protocol Buffers transition

Summary
-------
Complete migration from Writable-based RPC protocols to Protocol Buffers by removing legacy R23-compatible wire protocol implementations and translator classes.

Why
---
Legacy Writable-based protocol infrastructure is no longer needed after Protocol Buffers migration is complete. Maintaining both implementations adds code complexity and maintenance burden.

What Changed
------------
**Removed R23-compatible protocol classes:**
- `ClientNamenodeWireProtocol`, `DatanodeWireProtocol`, `InterDatanodeWireProtocol`, `ClientDatanodeWireProtocol`
- Server-side translators: `*ServerSideTranslatorR23`
- Client-side translators: `*TranslatorR23`

**Removed Writable wrapper types:**
- `BlockWritable`, `DatanodeInfoWritable`, `LocatedBlockWritable`, `ExtendedBlockWritable`
- `ContentSummaryWritable`, `DirectoryListingWritable`, `HdfsFileStatusWritable`
- `CheckpointSignatureWritable`, `UpgradeStatusReportWritable`, `StorageInfoWritable`
- `DatanodeRegistrationWritable`, `ReceivedDeletedBlockInfoWritable`, `RecoveringBlockWritable`
- Command types: `DatanodeCommandWritable`, `BlockCommandWritable`, `BalancerBandwidthCommandWritable`, etc.

**Updated protocol documentation:**
- Changed comments in `ClientProtocol`, `DatanodeProtocol`, `InterDatanodeProtocol`, `JournalProtocol`, `NamenodeProtocol`, `ClientDatanodeProtocol`
- Now reference Protocol Buffer `.proto` definitions in `.../protocolPB/` instead of removed R23Compatible classes

**Code cleanup:**
- Removed unused imports from `ClientNamenodeProtocolTranslatorPB`, `DatanodeProtocolClientSideTranslatorPB`
- Fixed socket factory reference in `DatanodeProtocolClientSideTranslatorPB` to use `DatanodeProtocolPB.class`
- Removed `setRpcEngine()` helper method from `MiniDFSCluster`

Impact
------
Breaking change for any external code still using R23-compatible wire protocol classes. All RPC communication now uses Protocol Buffers exclusively.