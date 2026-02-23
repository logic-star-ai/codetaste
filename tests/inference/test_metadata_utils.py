import json
from pathlib import Path

import pytest

from refactoring_benchmark.inference.models import InferenceMetadata
from refactoring_benchmark.inference.utils import finalize_step_metadata


def test_finalize_step_metadata_raises_when_missing(tmp_path: Path) -> None:
    src = tmp_path / "inference_metadata.json"
    dst = tmp_path / "plan_metadata.json"

    with pytest.raises(FileNotFoundError):
        finalize_step_metadata(src, dst, "instructed", "plan")


def test_finalize_step_metadata_updates_description_and_mode(tmp_path: Path) -> None:
    src = tmp_path / "inference_metadata.json"
    dst = tmp_path / "plan_metadata.json"
    metadata = {"finish_reason": "success"}
    src.write_text(json.dumps(metadata), encoding="utf-8")

    finalize_step_metadata(src, dst, "open", "multiplan")

    saved = InferenceMetadata.load_from_json(dst)
    assert saved.description_type == "open"
    assert saved.mode == "multiplan"
