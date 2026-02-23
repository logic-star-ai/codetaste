import json
import logging
from pathlib import Path

import pytest

from refactoring_benchmark.inference.models import (
    AgentConfig,
    AgentInfo,
    ExecutionContext,
    InferenceConfig,
    ModelInfo,
)
from refactoring_benchmark.inference.runner import InstanceInferenceRunner
from refactoring_benchmark.inference.steps.executor import ContainerExecutor
from refactoring_benchmark.inference.steps.multiplan import MultiplanStep
from refactoring_benchmark.inference.steps.plan import PlanStep
from refactoring_benchmark.utils.models import InstanceRow


def _make_config(tmp_path: Path) -> InferenceConfig:
    agent_config = AgentConfig(
        id="agent-1",
        agent=AgentInfo(name="agent", provider="test"),
        model=ModelInfo(name="model", provider="test"),
    )
    return InferenceConfig(
        agent_dir=tmp_path / "agent",
        output_dir=tmp_path,
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
        description_type="instructed",
        mode="direct",
        plan_timeout=10,
    )


def _make_instance() -> InstanceRow:
    return InstanceRow(
        owner="99designs",
        repo="gqlgen",
        golden_commit_hash="a9965fbd85f0f5aff1aebf2652d40fcd1ce6eb4f",
        commit_hash="d5c9f896419142f6378639b6eec93584fbf829ed",
        category="basic",
        language="go",
    )


def test_should_skip_respects_force_flags(tmp_path):
    """should_skip honors force and force_unsuccessful for failed outputs."""
    config = _make_config(tmp_path)
    instance = _make_instance()
    runner = InstanceInferenceRunner(instance, config)
    runner.output_dir.mkdir(parents=True, exist_ok=True)
    (runner.output_dir / "prediction.diff").write_text("diff", encoding="utf-8")
    (runner.output_dir / "inference_metadata.json").write_text(
        json.dumps({"finish_reason": "error", "description_type": "instructed", "mode": "direct"}), encoding="utf-8"
    )

    print("skip check: default flags", flush=True)
    print(f"output_dir={runner.output_dir}", flush=True)
    print("finish_reason=error", flush=True)
    should_skip, _ = runner.should_skip()
    assert should_skip is True

    config.force_unsuccessful = True
    runner = InstanceInferenceRunner(instance, config)
    runner.output_dir.mkdir(parents=True, exist_ok=True)
    (runner.output_dir / "prediction.diff").write_text("diff", encoding="utf-8")
    (runner.output_dir / "inference_metadata.json").write_text(
        json.dumps({"finish_reason": "error", "description_type": "instructed", "mode": "direct"}), encoding="utf-8"
    )
    print("skip check: force_unsuccessful=True", flush=True)
    should_skip, _ = runner.should_skip()
    assert should_skip is False

    config.force = True
    runner = InstanceInferenceRunner(instance, config)
    runner.output_dir.mkdir(parents=True, exist_ok=True)
    (runner.output_dir / "prediction.diff").write_text("diff", encoding="utf-8")
    (runner.output_dir / "inference_metadata.json").write_text(
        json.dumps({"finish_reason": "error", "description_type": "instructed", "mode": "direct"}), encoding="utf-8"
    )
    print("skip check: force=True", flush=True)
    should_skip, _ = runner.should_skip()
    assert should_skip is False


def test_plan_reuse_with_force_and_reuse_successful_plan(tmp_path):
    """PlanStep reuses successful plan when force + reuse_successful_plan is set."""
    config = _make_config(tmp_path)
    config.mode = "plan"
    config.force = True
    config.reuse_successful_plan = True
    instance = _make_instance()
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "plan_metadata.json").write_text(
        json.dumps({"finish_reason": "success"}), encoding="utf-8"
    )
    (output_dir / "refactoring_plan.md").write_text("plan", encoding="utf-8")

    print("plan reuse: force=True reuse_successful_plan=True", flush=True)
    print(f"output_dir={output_dir}", flush=True)
    step = PlanStep(instance, config, output_dir, logging.getLogger("test"), client=object())
    step.executor.run = lambda *args, **kwargs: (_ for _ in ()).throw(
        AssertionError("executor.run should not be called")
    )
    assert step.run() == output_dir / "refactoring_plan.md"


def test_plan_incomplete_artifacts_reruns(tmp_path, monkeypatch):
    """PlanStep reruns when plan_metadata exists but plan file is missing."""
    config = _make_config(tmp_path)
    config.mode = "plan"
    instance = _make_instance()
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "plan_metadata.json").write_text(
        json.dumps({"finish_reason": "success"}), encoding="utf-8"
    )

    print("plan rerun: plan_metadata exists, plan file missing", flush=True)
    print(f"output_dir={output_dir}", flush=True)
    temp_dir = tmp_path / "tmp_plan"
    temp_dir.mkdir(parents=True)
    monkeypatch.setattr(
        "refactoring_benchmark.inference.steps.plan.prepare_temp_plan_description",
        lambda *_args, **_kwargs: temp_dir,
    )

    step = PlanStep(instance, config, output_dir, logging.getLogger("test"), client=object())
    called = {"run": False}

    def fake_run(*args, **kwargs):
        called["run"] = True
        return False

    step.executor.run = fake_run
    assert step.run() is None
    assert called["run"] is True
    step.cleanup_temp_dir()


def test_multiplan_incomplete_artifacts_reruns(tmp_path, monkeypatch):
    """MultiplanStep reruns when multiplan metadata exists but plans are missing."""
    config = _make_config(tmp_path)
    config.mode = "multiplan"
    instance = _make_instance()
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(parents=True)
    (output_dir / "multiplan_metadata.json").write_text(
        json.dumps({"finish_reason": "success", "selected_plan_index": 0}),
        encoding="utf-8",
    )
    plans_dir = output_dir / "refactoring_plans"
    plans_dir.mkdir(parents=True)
    for i in range(4):
        (plans_dir / f"refactoring_plan{i}.md").write_text("plan", encoding="utf-8")

    print("multiplan rerun: metadata exists but 1 plan missing", flush=True)
    print(f"output_dir={output_dir}", flush=True)
    print(f"plans_dir={plans_dir}", flush=True)
    temp_dir = tmp_path / "tmp_multiplan"
    temp_dir.mkdir(parents=True)
    monkeypatch.setattr(
        "refactoring_benchmark.inference.steps.multiplan.prepare_temp_multiplan_description",
        lambda *_args, **_kwargs: temp_dir,
    )

    step = MultiplanStep(instance, config, output_dir, logging.getLogger("test"), client=object())
    called = {"run": False}

    def fake_run(*args, **kwargs):
        called["run"] = True
        return False

    step.executor.run = fake_run
    assert step.run() is None
    assert called["run"] is True
    step.cleanup_temp_dir()


def test_container_executor_timeout_plan_metadata(tmp_path, monkeypatch):
    """Plan timeout writes error_planmode with plan mode."""
    config = _make_config(tmp_path)
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(parents=True)
    temp_dir = tmp_path / "task"
    temp_dir.mkdir(parents=True)
    logger = logging.getLogger("test.plan.timeout")
    logger.addHandler(logging.NullHandler())
    instance = _make_instance()

    class FakeContainer:
        def wait(self, timeout):
            raise Exception("timeout")

        def remove(self, force=True):
            return None

    monkeypatch.setattr(
        "refactoring_benchmark.podman.utils.safe_container_run",
        lambda *args, **kwargs: FakeContainer(),
    )
    monkeypatch.setattr(
        "refactoring_benchmark.podman.utils.stop_container",
        lambda *_args, **_kwargs: None,
    )

    executor = ContainerExecutor(instance, config, output_dir, logger, client=object())
    context = ExecutionContext(description_type="instructed", mode="plan")
    assert executor.run("plan", 1, temp_dir, context=context) is False

    metadata_path = output_dir / "inference_metadata.json"
    assert metadata_path.exists()
    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    print("timeout plan metadata:", data, flush=True)
    assert data["finish_reason"] == "error_planmode"
    assert data["description_type"] == "instructed"
    assert data["mode"] == "plan"


def test_container_executor_timeout_multiplan_metadata(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Multiplan timeout writes error_multiplan with multiplan mode."""
    config = _make_config(tmp_path)
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(parents=True)
    temp_dir = tmp_path / "task"
    temp_dir.mkdir(parents=True)
    logger = logging.getLogger("test.multiplan.timeout")
    logger.addHandler(logging.NullHandler())
    instance = _make_instance()

    class FakeContainer:
        def wait(self, timeout):
            raise Exception("timeout")

        def remove(self, force=True):
            return None

    monkeypatch.setattr(
        "refactoring_benchmark.podman.utils.safe_container_run",
        lambda *args, **kwargs: FakeContainer(),
    )
    monkeypatch.setattr(
        "refactoring_benchmark.podman.utils.stop_container",
        lambda *_args, **_kwargs: None,
    )

    executor = ContainerExecutor(instance, config, output_dir, logger, client=object())
    context = ExecutionContext(description_type="instructed", mode="multiplan")
    assert executor.run("multiplan", 1, temp_dir, context=context) is False

    metadata_path = output_dir / "inference_metadata.json"
    assert metadata_path.exists()
    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    print("timeout multiplan metadata:", data, flush=True)
    assert data["finish_reason"] == "error_multiplan"
    assert data["description_type"] == "instructed"
    assert data["mode"] == "multiplan"
