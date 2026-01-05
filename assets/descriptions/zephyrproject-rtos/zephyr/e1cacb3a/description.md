# Title
-----
Rename `bt_audio_codec_qos` to `bt_bap_qos_cfg` for clarity

# Summary
-------
The QoS structure is not related to a codec but rather to a stream, making the "Codec" name misleading. Rename to align with BAP/ASCS specification terminology.

# Why
---
- Current name `bt_audio_codec_qos` incorrectly suggests QoS is codec-related
- QoS is actually stream-related, not codec-related
- BAP and ASCS specs refer to this as "QoS configuration"
- Structure is defined and used by BAP, so `bt_bap` prefix is more appropriate than `bt_audio`

# Changes
--------
Rename throughout codebase:
- **Struct**: `bt_audio_codec_qos` → `bt_bap_qos_cfg`
- **Enum**: `bt_audio_codec_qos_framing` → `bt_bap_qos_cfg_framing`
- **Preference struct**: `bt_audio_codec_qos_pref` → `bt_bap_qos_cfg_pref`
- **Macros**: `BT_AUDIO_CODEC_QOS_*` → `BT_BAP_QOS_CFG_*`
- **PHY constants**: `BT_AUDIO_CODEC_QOS_{1M,2M,CODED}` → `BT_BAP_QOS_CFG_{1M,2M,CODED}`
- **Framing values**: `BT_AUDIO_CODEC_QOS_FRAMING_*` → `BT_BAP_QOS_CFG_FRAMING_*`
- All related functions, parameters, and helper macros

# Scope
------
- API headers (`audio.h`, `bap.h`, `bap_lc3_preset.h`, `cap.h`, `gmap_lc3_preset.h`)
- Implementation files (`ascs.c`, `bap_*.c`)
- Samples and tests
- Migration guide documentation

# Migration
----------
Applications using old naming can migrate via search-and-replace:
- `bt_audio_codec_qos` → `bt_bap_qos_cfg`
- `BT_AUDIO_CODEC_QOS` → `BT_BAP_QOS_CFG`