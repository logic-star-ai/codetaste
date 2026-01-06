# Rename `bt_audio_codec_qos` to `bt_bap_qos_cfg` for clarity

The QoS structure is not related to a codec but rather to a stream, making the "Codec" name misleading. Rename to align with BAP/ASCS specification terminology.