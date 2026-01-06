# Move RpcModel and utilities to sentry.hybridcloud.rpc

Move `RpcModel`, delegation classes (`DelegatedBySiloMode`, `DelegatedByOpenTransaction`), utility functions (`coerce_id_from`, `extract_id_from`, ...), constants (`IDEMPOTENCY_KEY_LENGTH`, `REGION_NAME_LENGTH`, ...), and related infrastructure from `sentry.services.hybrid_cloud` to `sentry.hybridcloud.rpc`.