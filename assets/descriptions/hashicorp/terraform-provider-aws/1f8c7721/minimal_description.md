# Lazy-load all AWS API clients

Refactored AWS SDK client initialization to use lazy loading instead of eagerly creating all 300+ service clients during provider configuration. Clients are now created on-demand and cached in maps, reducing memory footprint and initialization time.