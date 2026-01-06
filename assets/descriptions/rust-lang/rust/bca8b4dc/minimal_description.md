# Remove `HirId -> LocalDefId` map from HIR data structure

Remove the `local_id_to_def_id: SortedMap<ItemLocalId, LocalDefId>` field from `OwnerNodes` in HIR, along with associated lookup methods like `local_def_id(HirId)` and `opt_local_def_id(HirId)`.