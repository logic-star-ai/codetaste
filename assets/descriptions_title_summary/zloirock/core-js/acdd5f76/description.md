# Refactor Typed Arrays: Extract `ArrayBuffer` Methods & Move to Separate Namespace

Refactor typed arrays module structure by:
- Extracting `ArrayBuffer` methods (`constructor`, `isView`, `slice`) into separate modules
- Moving `ArrayBuffer` and `DataView` out of typed arrays namespace
- Reorganizing entry points and file structure for better granularity