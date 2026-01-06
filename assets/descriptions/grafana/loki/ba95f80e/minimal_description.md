# Restructure compactor package hierarchy

Move compactor package from deeply nested storage path (`pkg/storage/stores/shipper/indexshipper/compactor`) to top-level `pkg/compactor`, aligning with other high-level components (querier, distributor, ruler...).