import logging

from refactoring_benchmark.evaluation import runner
from refactoring_benchmark.evaluation.runner import (
    cleanup_temp_rules_dir,
    prepare_temp_rules_dir,
)
from refactoring_benchmark.utils.models import InstanceRow


def _instance() -> InstanceRow:
    return InstanceRow(
        owner="owner",
        repo="repo",
        commit_hash="1234567890abcdef",
        golden_commit_hash="fedcba0987654321",
        category="basic",
        language="python",
    )


def test_prepare_temp_rules_dir_uses_explicit_rules_root(tmp_path, monkeypatch) -> None:
    instance = _instance()
    rules_root = tmp_path / "assets" / "rules-curated"
    rules_dir = rules_root / instance.owner / instance.repo / instance.short_hash
    rules_dir.mkdir(parents=True)
    (rules_dir / "rules_positive.yml").write_text("rules: []\n")
    (rules_dir / "rules_negative.yml").write_text("rules: []\n")

    metadata_dir = tmp_path / instance.instance_dir()
    metadata_dir.mkdir(parents=True)
    (metadata_dir / "instance_metadata.json").write_text("{}\n")

    assets_dir = tmp_path / "assets"
    assets_dir.mkdir(exist_ok=True)
    (assets_dir / "default.semgrepignore").write_text("node_modules\n")

    monkeypatch.setattr(runner, "PROJECT_ROOT", tmp_path)

    temp_dir = prepare_temp_rules_dir(instance, rules_root, logging.getLogger("test"))
    try:
        assert temp_dir is not None
        assert (temp_dir / "rules_positive.yml").read_text() == "rules: []\n"
        assert (temp_dir / "rules_negative.yml").read_text() == "rules: []\n"
        assert (temp_dir / "instance_metadata.json").read_text() == "{}\n"
        assert (temp_dir / "default.semgrepignore").read_text() == "node_modules\n"
    finally:
        cleanup_temp_rules_dir(temp_dir, logging.getLogger("test"))


def test_prepare_temp_rules_dir_returns_none_for_missing_rules_root(tmp_path, monkeypatch) -> None:
    instance = _instance()
    metadata_dir = tmp_path / instance.instance_dir()
    metadata_dir.mkdir(parents=True)
    (metadata_dir / "instance_metadata.json").write_text("{}\n")

    monkeypatch.setattr(runner, "PROJECT_ROOT", tmp_path)

    temp_dir = prepare_temp_rules_dir(instance, tmp_path / "missing-rules", logging.getLogger("test"))

    assert temp_dir is None
