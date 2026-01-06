# Refactor sub-config loading in composite models

Consolidate sub-config loading logic from composite models into the base `PretrainedConfig` class, eliminating redundant `from_pretrained` overrides across ~40+ model configurations.