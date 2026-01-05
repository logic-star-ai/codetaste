Title
-----
Reorganize GPU finetuning examples

Summary
-------
Refactor GPU finetuning examples to improve code organization and maintainability by separating different training modes into dedicated folders with shared common utilities.

Why
---
Current structure mixes different training modes (LoRA, QLoRA, QA-LoRA, ReLora) in a single directory with conditional logic, making it difficult to:
- Navigate and understand different finetuning approaches
- Maintain mode-specific configurations and scripts
- Locate relevant examples for a specific training method

Changes
-------
**Directory Structure:**
- Create `common/` folder for shared code:
  - Move `templates/` directory
  - Move `utils/` module
  - Extract common functions (data processing, wandb check, etc.)
- Separate training modes into individual folders:
  - `LoRA/` for LoRA finetuning examples
  - `QLoRA/` with `alpaca-qlora/` and `simple-example/` subdirectories
  - `QA-LoRA/` for QA-LoRA examples
  - `ReLora/` for ReLora examples

**Per Training Mode:**
- Rename scripts to match mode (e.g., `alpaca_lora_finetuning.py`, `alpaca_qlora_finetuning.py`, `alpaca_qalora_finetuning.py`, `alpaca_relora_finetuning.py`)
- Set appropriate default `training_mode` value in each script
- Update import paths for `Prompter` and utilities
- Remove conditional logic for handling different modes
- Add `export_merged_model.py` to each folder
- Update bash scripts and README files

**Additional Examples:**
- Add LLaMA2-13B QLoRA finetuning scripts (1 tile, 1 card, 4 cards)
- Add LLaMA2-70B QLoRA finetuning scripts (1 card, 4 cards) with DeepSpeed ZeRO2 support
- Add `save_low_bit_70b_model.py` for large model optimization

**Documentation Updates:**
- Update all links from `example/GPU/QLoRA-FineTuning` to `example/GPU/LLM-Finetuning/{mode}`
- Update README.md, docs, Docker files, and test scripts
- Revise examples to reflect new directory structure

**Code Quality:**
- Extract shared utility functions into `common/utils/util.py`
- Consolidate `get_train_val_data()`, `wandb_check()`, `merge_adapter()`, etc.
- Simplify each mode-specific script by removing unnecessary conditionals