import json
import logging
from pathlib import Path

from refactoring_benchmark.inference.models import (
    AgentConfig,
    AgentInfo,
    ExecutionContext,
    InferenceConfig,
    MultiplanMetadata,
    ModelInfo,
)
from refactoring_benchmark.inference.steps.inference import InferenceStep
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


def test_plan_step_reuses_successful_plan(tmp_path, monkeypatch):
    """PlanStep skips container run when a successful plan already exists."""
    config = _make_config(tmp_path)
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True)
    logger = logging.getLogger("test.plan")
    logger.addHandler(logging.NullHandler())
    instance = _make_instance()

    plan_metadata = {
        "finish_reason": "success",
        "finish_time": "2025-01-01T00:00:00Z",
    }
    (output_dir / "plan_metadata.json").write_text(
        json.dumps(plan_metadata), encoding="utf-8"
    )
    (output_dir / "refactoring_plan.md").write_text("plan", encoding="utf-8")

    step = PlanStep(instance, config, output_dir, logger, client=object())

    def fail_run(*args, **kwargs):
        raise AssertionError("Container should not run when reusing a plan")

    step.executor.run = fail_run
    plan_path = step.run()

    assert plan_path == output_dir / "refactoring_plan.md"


def test_multiplan_step_reuses_successful_multiplan(tmp_path, monkeypatch):
    """MultiplanStep reuses existing plans and skips judging/containers."""
    config = _make_config(tmp_path)
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True)
    logger = logging.getLogger("test.multiplan")
    logger.addHandler(logging.NullHandler())
    instance = _make_instance()

    plans_dir = output_dir / "refactoring_plans"
    plans_dir.mkdir(parents=True)
    for i in range(5):
        (plans_dir / f"refactoring_plan{i}.md").write_text(
            f"plan {i}", encoding="utf-8"
        )

    metadata = MultiplanMetadata(
        start_time="2025-01-01T00:00:00Z",
        finish_time="2025-01-01T00:10:00Z",
        finish_reason="success",
        plans_generated=5,
        selected_plan_index=2,
    )
    metadata.save_to_json(output_dir / "multiplan_metadata.json")

    step = MultiplanStep(instance, config, output_dir, logger, client=object())

    def fail_run(*args, **kwargs):
        raise AssertionError("Container should not run when reusing multiplan")

    step.executor.run = fail_run
    monkeypatch.setattr(
        "refactoring_benchmark.inference.steps.multiplan.judge_best_plan",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("Judge should not run when reusing multiplan")
        ),
    )

    content = step.run()
    assert content == "plan 2"


def test_inference_step_uses_context_for_description_selection(tmp_path, monkeypatch):
    """InferenceStep selects description source based on context fields."""
    config = _make_config(tmp_path)
    output_dir = tmp_path / "output"
    output_dir.mkdir(parents=True)
    logger = logging.getLogger("test.inference")
    logger.addHandler(logging.NullHandler())
    instance = _make_instance()

    captured = {"description_type": None, "content": None}

    def fake_prepare_temp_task_description(instance, logger, description_type=None, content=None):
        captured["description_type"] = description_type
        captured["content"] = content
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
        description_type="standard",
        description_type_suffix="_multiplan",
        plan_content="plan",
    )
    assert step.run(context) is True
    assert captured["description_type"] is None
    assert captured["content"] == "plan"

    plan_path = output_dir / "refactoring_plan.md"
    plan_path.write_text("plan file", encoding="utf-8")
    context = ExecutionContext(
        description_type="standard",
        description_type_suffix="_plan",
        plan_path=plan_path,
    )
    assert step.run(context) is True
    assert captured["description_type"] is None
    assert captured["content"] == "plan file"

    context = ExecutionContext(description_type="standard")
    assert step.run(context) is True
    assert captured["description_type"] == "standard"
    assert captured["content"] is None
