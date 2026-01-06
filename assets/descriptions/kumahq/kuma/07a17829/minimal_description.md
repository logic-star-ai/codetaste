# Refactor: Replace `*kri.Identifier` with value-based `kri.Identifier` in policy logic

Replace pointer-based `*kri.Identifier` with value-based `kri.Identifier` throughout policy handling code to simplify the API, eliminate unnecessary pointer handling, and improve code consistency.