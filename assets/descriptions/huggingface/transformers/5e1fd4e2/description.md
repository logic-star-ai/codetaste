# Refactor sub-config loading in composite models

## Summary

Consolidate sub-config loading logic from composite models into the base `PretrainedConfig` class, eliminating redundant `from_pretrained` overrides across ~40+ model configurations.

## Why

- **Code duplication**: Each composite model (CLIP, BLIP, Llava, etc.) implements nearly identical `from_pretrained` logic to extract sub-configs
- **Maintainability**: Changes to loading behavior require updating each model individually
- **Consistency**: No standardized way to identify and load sub-configs from composite configurations

## Changes

### Core Infrastructure

**`PretrainedConfig`** additions:
- `base_config_key: str` – key name in parent config dict (e.g. `"text_config"`, `"vision_config"`)
- `sub_configs: Dict[str, Type]` – registry of sub-config classes for composite models

**Loading logic** (`from_pretrained`):
- Extract sub-config dict using `base_config_key` if present
- Fallback matching via `model_type` for configs shared across models (e.g. `LlamaConfig`)

### Model Updates

Remove `from_pretrained` overrides from sub-configs in:
- Vision-language models: `CLIP`, `BLIP*`, `Llava*`, `Idefics*`, `Mllama`, `Kosmos2`, `PaliGemma`, `Qwen2VL`, `Siglip`...
- Multi-modal encoders: `ALIGN`, `AltCLIP`, `BridgeTower`, `CLAP`, `CLIPSeg`, `Flava`, `GroupViT`, `Owlv(2|it)`, `X-CLIP`...
- Composite architectures: `Bark`, `CLVP`, `Chameleon`, `Dbrx`, `EncoderDecoder`, `FastSpeech2Conformer`, `Musicgen*`...

Add metadata to all affected configs:
```python
# Sub-configs
class XTextConfig(PretrainedConfig):
    base_config_key = "text_config"
    
# Composite configs  
class XConfig(PretrainedConfig):
    sub_configs = {"text_config": XTextConfig, "vision_config": XVisionConfig}
```

### Testing

- New test: `create_and_test_config_from_and_save_pretrained_composite()` validates load-save-load pipeline for sub-configs
- Updated `ConfigTester` to verify sub-config loading matches composite config extraction
- Added `common_properties` parameter to test config-specific attributes

### Modeling

Update attention implementation dispatch to use `config.sub_configs.keys()` instead of iterating all config attributes.

## Notes

- `is_composition` flag cleaned up (was inconsistently used/named)
- `AutoConfig` used in `sub_configs` for models with pluggable components (e.g. `Blip2`, `Idefics2`)
- Maintains backward compatibility – no breaking changes to config APIs