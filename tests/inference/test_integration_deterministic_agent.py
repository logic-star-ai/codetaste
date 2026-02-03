import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from refactoring_benchmark.inference.models import (
    AgentConfig,
    AgentInfo,
    InferenceConfig,
    ModelInfo,
)
from refactoring_benchmark.inference.runner import InstanceInferenceRunner
from refactoring_benchmark.inference.utils import get_instance_output_dir
from refactoring_benchmark.utils.models import InstanceRow

pytestmark = pytest.mark.integration


# def _require_integration_env() -> None:
#     if os.getenv("RUN_INTEGRATION") != "1":
#         pytest.skip("Set RUN_INTEGRATION=1 to enable this test.")


def _require_podman_and_image(image: str) -> None:
    if shutil.which("podman") is None:
        pytest.skip("podman is not available.")
    result = subprocess.run(
        ["podman", "image", "exists", image],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        pytest.skip(f"podman image not found: {image}")


def _make_instance() -> InstanceRow:
    return InstanceRow(
        owner="99designs",
        repo="gqlgen",
        golden_commit_hash="a9965fbd85f0f5aff1aebf2652d40fcd1ce6eb4",
        commit_hash="d5c9f896419142f6378639b6eec93584fbf829ed",
        category="basic",
        language="go",
    )


def _load_agent_config(agent_dir: Path) -> AgentConfig:
    data = json.loads((agent_dir / "agent_config.json").read_text(encoding="utf-8"))
    return AgentConfig.model_validate(data)


def _make_config(
    tmp_path: Path,
    agent_dir: Path,
    agent_config: AgentConfig,
    plan: bool = False,
    multiplan: bool = False,
) -> InferenceConfig:
    return InferenceConfig(
        agent_dir=agent_dir,
        output_dir=tmp_path,
        instances_csv=tmp_path / "instances.csv",
        nr_workers=1,
        timeout=300,
        instances_limit=1,
        force=True,
        force_unsuccessful=False,
        reuse_successful_plan=False,
        agent_config=agent_config,
        sanitized_agent_id=agent_config.id,
        env_vars={},
        description_type="standard",
        plan=plan,
        multiplan=multiplan,
        plan_timeout=120,
    )


def test_deterministic_agent_full_integration(tmp_path, monkeypatch):
    """Run plan, multiplan, and inference flows using a deterministic agent."""
    # _require_integration_env()
    instance = _make_instance()
    image = instance.runtime_image
    _require_podman_and_image(image)

    agent_dir = Path("agents/test/deterministic").resolve()
    agent_config = _load_agent_config(agent_dir)

    print("=== Integration: setup ===", flush=True)
    print(f"instance.id={instance.id}", flush=True)
    print(f"runtime_image={image}", flush=True)
    print(f"agent_dir={agent_dir}", flush=True)
    print(f"tmp_path={tmp_path}", flush=True)

    def fake_judge(_desc, _plans):
        return 0, {
            "judge_reasoning": "deterministic",
            "judge_cost_usd": 0.0,
            "judge_latency_seconds": 0.0,
            "judge_input_tokens": 0,
            "judge_output_tokens": 0,
        }

    monkeypatch.setattr(
        "refactoring_benchmark.inference.steps.multiplan.judge_best_plan",
        fake_judge,
    )

    print("=== Integration: plan mode ===", flush=True)
    plan_output_root = tmp_path / "plan"
    plan_output_root.mkdir(parents=True, exist_ok=True)
    config = _make_config(plan_output_root, agent_dir, agent_config, plan=True)
    print(f"plan_output_root={plan_output_root}", flush=True)
    print(f"plan_output_dir={get_instance_output_dir(instance, config.sanitized_agent_id, plan_output_root)}", flush=True)
    runner = InstanceInferenceRunner(instance, config)
    assert runner.run() is True
    plan_output_dir = get_instance_output_dir(
        instance, config.sanitized_agent_id, plan_output_root
    )
    assert (plan_output_dir / "refactoring_plan.md").exists()
    assert (plan_output_dir / "plan_metadata.json").exists()
    assert (plan_output_dir / "prediction.diff").exists()
    print("plan mode: OK", flush=True)

    print("=== Integration: multiplan mode ===", flush=True)
    multiplan_output_root = tmp_path / "multiplan"
    multiplan_output_root.mkdir(parents=True, exist_ok=True)
    config = _make_config(
        multiplan_output_root, agent_dir, agent_config, multiplan=True
    )
    print(f"multiplan_output_root={multiplan_output_root}", flush=True)
    print(
        f"multiplan_output_dir={get_instance_output_dir(instance, config.sanitized_agent_id, multiplan_output_root)}",
        flush=True,
    )
    runner = InstanceInferenceRunner(instance, config)
    assert runner.run() is True
    multiplan_output_dir = get_instance_output_dir(
        instance, config.sanitized_agent_id, multiplan_output_root
    )
    plans_dir = multiplan_output_dir / "refactoring_plans"
    assert plans_dir.exists()
    assert len(list(plans_dir.glob("refactoring_plan*.md"))) == 5
    assert (multiplan_output_dir / "multiplan_metadata.json").exists()
    assert (multiplan_output_dir / "prediction.diff").exists()
    print("multiplan mode: OK", flush=True)

    print("=== Integration: inference mode ===", flush=True)
    inference_output_root = tmp_path / "inference"
    inference_output_root.mkdir(parents=True, exist_ok=True)
    config = _make_config(inference_output_root, agent_dir, agent_config)
    print(f"inference_output_root={inference_output_root}", flush=True)
    print(
        f"inference_output_dir={get_instance_output_dir(instance, config.sanitized_agent_id, inference_output_root)}",
        flush=True,
    )
    runner = InstanceInferenceRunner(instance, config)
    assert runner.run() is True
    inference_output_dir = get_instance_output_dir(
        instance, config.sanitized_agent_id, inference_output_root
    )
    diff_path = inference_output_dir / "prediction.diff"
    assert diff_path.exists()
    assert diff_path.stat().st_size > 0
    print("inference mode: OK", flush=True)
