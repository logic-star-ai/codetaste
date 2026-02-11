import json
import logging
from pathlib import Path

from refactoring_benchmark.inference.models import (
    AgentConfig,
    AgentInfo,
    ExecutionContext,
    InferenceConfig,
    ModelInfo,
)
from refactoring_benchmark.inference.steps.executor import ContainerExecutor
from refactoring_benchmark.inference.steps.inference import InferenceStep
from refactoring_benchmark.utils.models import InstanceRow


def _make_config(tmp_path: Path) -> InferenceConfig:
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
        description_type="instructed",
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


def test_container_executor_timeout_uses_context_suffix(tmp_path, monkeypatch):
    """Timeout metadata uses ExecutionContext suffix for description_type."""
    config = _make_config(tmp_path)
    output_dir = tmp_path / "outputs"
    output_dir.mkdir(parents=True)
    temp_dir = tmp_path / "task"
    temp_dir.mkdir(parents=True)
    logger = logging.getLogger("test.executor")
    logger.addHandler(logging.NullHandler())
    instance = _make_instance()

    class FakeContainer:
        def wait(self, timeout):
            raise Exception("timeout")

        def remove(self, force=True):
            return None

    def fake_safe_container_run(*args, **kwargs):
        return FakeContainer()

    def fake_stop_container(container):
        return None

    monkeypatch.setattr(
        "refactoring_benchmark.podman.utils.safe_container_run",
        fake_safe_container_run,
    )
    monkeypatch.setattr(
        "refactoring_benchmark.podman.utils.stop_container",
        fake_stop_container,
    )

    executor = ContainerExecutor(instance, config, output_dir, logger, client=object())
    context = ExecutionContext(
        description_type="instructed",
        description_type_suffix="_plan",
    )
    success = executor.run("inference", 1, temp_dir, context=context)
    assert success is False

    metadata_path = output_dir / "inference_metadata.json"
    assert metadata_path.exists()
    data = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert data["finish_reason"] == "timeout"
    assert data["description_type"] == "instructed_plan"


def test_inference_step_writes_context_description_type(tmp_path, monkeypatch):
    """Inference writes context.full_description_type into metadata."""
    config = _make_config(tmp_path)
    output_dir: Path = tmp_path / "outputs"
    output_dir.mkdir(parents=True)
    logger = logging.getLogger("test.inference")
    logger.addHandler(logging.NullHandler())
    instance = _make_instance()

    def fake_prepare_temp_task_description(*args, **kwargs):
        task_dir = tmp_path / "task"
        task_dir.mkdir(parents=True, exist_ok=True)
        (task_dir / "description.md").write_text("desc", encoding="utf-8")
        return task_dir

    monkeypatch.setattr(
        "refactoring_benchmark.inference.steps.inference.prepare_temp_task_description",
        fake_prepare_temp_task_description,
    )

    step = InferenceStep(instance, config, output_dir, logger, client=object())

    def fake_run(mode, timeout, temp_dir, context=None):
        metadata = {"finish_reason": "success"}
        (output_dir / "inference_metadata.json").write_text(
            json.dumps(metadata), encoding="utf-8"
        )
        (output_dir / "prediction.diff").write_text("", encoding="utf-8")
        return True

    step.executor.run = fake_run

    context = ExecutionContext(
        description_type="open",
        description_type_suffix="_multiplan",
        plan_content="plan",
    )
    assert step.run(context) is True

    data = json.loads(
        (output_dir / "inference_metadata.json").read_text(encoding="utf-8")
    )
    assert data["description_type"] == "open_multiplan"


def test_execution_context_full_description_type():
    """ExecutionContext concatenates base description_type and suffix."""
    context = ExecutionContext(
        description_type="instructed",
        description_type_suffix="_plan",
    )
    assert context.full_description_type == "instructed_plan"

    context = ExecutionContext(description_type="instructed")
    assert context.full_description_type == "instructed"
