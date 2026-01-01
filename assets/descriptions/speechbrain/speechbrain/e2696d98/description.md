# Title
-----
Move files with optional dependencies to `integrations/` folder

# Summary
-------
Reorganize codebase to separate core toolkit from code requiring optional external libraries by moving all external-dependent modules to `speechbrain/integrations/`.

# Why
---
- Keep core toolkit **lightweight** and easy to install
- Reduce maintenance burden from conflicting/changing dependencies
- Make it **explicit** which code relies on optional libraries
- Apply stricter testing requirements to external integrations
- Only test integrations before releases (not every CI run)
- Easier to identify/remove broken integrations

# What Was Moved
---------------
**HuggingFace models:**
- `speechbrain.lobes.models.huggingface_transformers` → `speechbrain.integrations.huggingface`
- `speechbrain.wordemb` → `speechbrain.integrations.huggingface.wordemb`

**Audio tokenizers:**
- `...discrete.speechtokenizer` → `speechbrain.integrations.audio_tokenizers.speechtokenizer_interface`
- `...discrete.wavtokenizer` → `speechbrain.integrations.audio_tokenizers.wavtokenizer_interface`
- `...models.kmeans` → `speechbrain.integrations.audio_tokenizers.kmeans`

**NLP tools:**
- `...models.flair` → `speechbrain.integrations.nlp`
- `...models.spacy` → `speechbrain.integrations.nlp`
- `speechbrain.utils.bleu` → `speechbrain.integrations.nlp.bleu`

**Alignment tools:**
- `speechbrain.alignment.ctc_segmentation` → `speechbrain.integrations.alignment.ctc_seg`
- `speechbrain.processing.diarization` → `speechbrain.integrations.alignment.diarization`

**Other:**
- `speechbrain.k2_integration` → `speechbrain.integrations.k2_fsa`
- `speechbrain.decoders.language_model` → `speechbrain.integrations.decoders.kenlm_scorer`

**Deprecated:**
- `speechbrain.lobes.models.fairseq_wav2vec`
- `speechbrain.utils.kmeans`

# Implementation Details
-----------------------
- Added deprecation redirects in old file locations
- Updated **all** imports across recipes/code
- Added README files to integration submodules
- Created `.run-third-party.sh` test script
- Updated `conftest.py` to exclude integrations from standard tests
- Removed optional deps from main CI workflow
- Updated documentation in `contributing.md`

# Requirements for New Integrations
-----------------------------------
- Runnable doctest examples in docstrings
- Tests in `integrations/tests/` folder
- **80%+ code coverage**
- README with installation instructions