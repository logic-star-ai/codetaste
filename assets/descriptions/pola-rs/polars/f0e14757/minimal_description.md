# Refactor: Introduce `UnifiedScanArgs` to consolidate scan arguments

Replace `FileScanOptions` with `UnifiedScanArgs` to contain arguments common to all scan types. This centralizes scan configuration and simplifies adding features across different file formats.