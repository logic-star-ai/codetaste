import logging

from refactoring_benchmark.inference.models import (
    AgentConfig,
    AgentInfo,
    InferenceConfig,
    ModelInfo,
)
from refactoring_benchmark.inference import runner as runner_module
from refactoring_benchmark.utils.models import InstanceRow


def _make_config(tmp_path: str) -> InferenceConfig:
    agent_config = AgentConfig(
        id="agent-1",
        agent=AgentInfo(name="agent", provider="test"),
        model=ModelInfo(name="model", provider="test"),
    )
    return InferenceConfig(
        agent_dir=tmp_path / "agent",
        output_dir=tmp_path / "out",
        instances_csv=tmp_path / "instances.csv",
        nr_workers=1,
        timeout=10,
        instances_limit=1,
        force=False,
        force_unsuccessful=False,
        reuse_successful_plan=False,
        agent_config=agent_config,
        sanitized_agent_id="agent-1",
        env_vars={},
        description_type="standard",
        plan=False,
        multiplan=False,
        plan_timeout=10,
    )


def _make_instance() -> InstanceRow:
    return InstanceRow(
        owner="owner",
        repo="repo",
        golden_commit_hash="g" * 40,
        commit_hash="c" * 40,
        category="basic",
        language="python",
    )


def test_runner_wires_plan_context(tmp_path, monkeypatch):
    """Runner passes plan context to InferenceStep when plan is enabled."""
    config = _make_config(tmp_path)
    config.plan = True
    instance = _make_instance()

    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.output_exists",
        lambda *_args, **_kwargs: False,
    )
    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.get_instance_output_dir",
        lambda *_args, **_kwargs: tmp_path / "output",
    )
    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.copy_agent_config",
        lambda *_args, **_kwargs: None,
    )

    class FakeClient:
        def close(self):
            return None

    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.podman_utils.get_local_client",
        lambda *_args, **_kwargs: FakeClient(),
    )

    captured = {}

    class FakePlanStep:
        def __init__(self, *args, **kwargs):
            return None

        def run(self):
            return tmp_path / "output" / "refactoring_plan.md"

        def cleanup_temp_dir(self):
            return None

    class FakeInferenceStep:
        def __init__(self, *args, **kwargs):
            return None

        def run(self, context):
            captured["suffix"] = context.description_type_suffix
            captured["plan_path"] = context.plan_path
            captured["plan_content"] = context.plan_content
            return True

        def cleanup_temp_dir(self):
            return None

    monkeypatch.setattr(runner_module, "PlanStep", FakePlanStep)
    monkeypatch.setattr(runner_module, "InferenceStep", FakeInferenceStep)

    runner = runner_module.InstanceInferenceRunner(instance, config)
    assert runner.run() is True
    assert captured["suffix"] == "_plan"
    assert captured["plan_path"] == tmp_path / "output" / "refactoring_plan.md"
    assert captured["plan_content"] is None


def test_runner_wires_multiplan_context(tmp_path, monkeypatch):
    """Runner passes multiplan context to InferenceStep when enabled."""
    config = _make_config(tmp_path)
    config.multiplan = True
    instance = _make_instance()

    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.output_exists",
        lambda *_args, **_kwargs: False,
    )
    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.get_instance_output_dir",
        lambda *_args, **_kwargs: tmp_path / "output",
    )
    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.copy_agent_config",
        lambda *_args, **_kwargs: None,
    )

    class FakeClient:
        def close(self):
            return None

    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.podman_utils.get_local_client",
        lambda *_args, **_kwargs: FakeClient(),
    )

    captured = {}

    class FakeMultiplanStep:
        def __init__(self, *args, **kwargs):
            return None

        def run(self):
            return "plan content"

        def cleanup_temp_dir(self):
            return None

    class FakeInferenceStep:
        def __init__(self, *args, **kwargs):
            return None

        def run(self, context):
            captured["suffix"] = context.description_type_suffix
            captured["plan_path"] = context.plan_path
            captured["plan_content"] = context.plan_content
            return True

        def cleanup_temp_dir(self):
            return None

    monkeypatch.setattr(runner_module, "MultiplanStep", FakeMultiplanStep)
    monkeypatch.setattr(runner_module, "InferenceStep", FakeInferenceStep)

    runner = runner_module.InstanceInferenceRunner(instance, config)
    assert runner.run() is True
    assert captured["suffix"] == "_multiplan"
    assert captured["plan_path"] is None
    assert captured["plan_content"] == "plan content"


def test_runner_wires_standard_context(tmp_path, monkeypatch):
    """Runner passes standard context when no plan/multiplan is set."""
    config = _make_config(tmp_path)
    instance = _make_instance()

    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.output_exists",
        lambda *_args, **_kwargs: False,
    )
    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.get_instance_output_dir",
        lambda *_args, **_kwargs: tmp_path / "output",
    )
    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.copy_agent_config",
        lambda *_args, **_kwargs: None,
    )

    class FakeClient:
        def close(self):
            return None

    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.podman_utils.get_local_client",
        lambda *_args, **_kwargs: FakeClient(),
    )

    captured = {}

    class FakeInferenceStep:
        def __init__(self, *args, **kwargs):
            return None

        def run(self, context):
            captured["suffix"] = context.description_type_suffix
            captured["plan_path"] = context.plan_path
            captured["plan_content"] = context.plan_content
            return True

        def cleanup_temp_dir(self):
            return None

    monkeypatch.setattr(runner_module, "InferenceStep", FakeInferenceStep)

    runner = runner_module.InstanceInferenceRunner(instance, config)
    assert runner.run() is True
    assert captured["suffix"] == ""
    assert captured["plan_path"] is None
    assert captured["plan_content"] is None


def test_runner_skips_when_output_exists(tmp_path, monkeypatch):
    """Runner returns early without constructing steps when output exists."""
    config = _make_config(tmp_path)
    instance = _make_instance()

    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.output_exists",
        lambda *_args, **_kwargs: True,
    )

    class FakeMetadata:
        finish_reason = "success"

    monkeypatch.setattr(
        "refactoring_benchmark.inference.runner.InferenceMetadata.load_from_json",
        lambda *_args, **_kwargs: FakeMetadata(),
    )

    class FailStep:
        def __init__(self, *args, **kwargs):
            raise AssertionError("Steps should not be constructed when skipping")

    monkeypatch.setattr(runner_module, "PlanStep", FailStep)
    monkeypatch.setattr(runner_module, "MultiplanStep", FailStep)
    monkeypatch.setattr(runner_module, "InferenceStep", FailStep)

    runner = runner_module.InstanceInferenceRunner(instance, config)
    assert runner.run() is True
