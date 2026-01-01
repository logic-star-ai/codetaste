# Standardize BigTreeTech Board Naming Convention

## Summary

Rename all BigTreeTech board identifiers to use consistent `BTT_*` prefix and introduce MCU-based naming for SKR 2 variants.

## Why

- Current naming inconsistent (`BIGTREE_*` vs `BTT_*`)
- SKR 2 boards have multiple MCU variants but share same env name
- Need MCU-specific env names to distinguish F407VG vs F429VG variants
- Align with naming standard used for other multi-MCU boards

## Changes

**BTT Prefix Standardization:**
- `BIGTREE_SKR_PRO` → `BTT_SKR_PRO`
- `BIGTREE_GTR_V1_0` → `BTT_GTR_V1_0`
- `BIGTREE_BTT002` → `BTT_BTT002`
- `BIGTREE_E3_RRF` → `BTT_E3_RRF`
- ... and all related `*_usb_flash_drive` variants

**SKR 2 MCU-Based Naming:**
- `BIGTREE_SKR_2` → `STM32F407VG_btt`
- `BIGTREE_SKR_2_USB` → `STM32F407VG_btt_USB`
- `BIGTREE_SKR_2_F429` → `STM32F429VG_btt`
- `BIGTREE_SKR_2_F429_USB` → `STM32F429VG_btt_USB`
- ... and corresponding `*_debug` variants

## Scope

- [x] CI workflow configurations
- [x] Pin definitions & comments
- [x] PlatformIO board JSON files
- [x] Board variant directories (`MARLIN_BIGTREE_*` → `MARLIN_BTT_*`)
- [x] Build environment definitions (ini files)
- [x] Test configurations
- [x] Error messages in pin files
- [x] Debug launch configurations
- [x] Renamed environment mapping (ini/renamed.ini)