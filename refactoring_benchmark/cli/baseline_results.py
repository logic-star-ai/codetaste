"""Populate baseline test results by running pseudo-agent tests multiple times."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

from refactoring_benchmark.evaluation.models import TestMetrics
from refactoring_benchmark.evaluation.parser import parse_test_output
from refactoring_benchmark.evaluation.runner import (
    cleanup_temp_rules_dir,
    prepare_temp_rules_dir,
    run_test_evaluation,
)
from refactoring_benchmark.utils.common import (
    ensure_entrypoint_executable,
    load_instances_from_csv,
)
from refactoring_benchmark.utils.logger import get_logger, setup_logging
from refactoring_benchmark.utils.paths import BASELINE_RESULTS_DIR, PSEUDO_AGENTS_DIR


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Populate baseline test results for golden and null agents.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--instances",
        type=int,
        default=15,
        help="Number of instances to run from the CSV file",
    )
    parser.add_argument(
        "--instances-csv",
        type=Path,
        default=Path("./instances.csv"),
        help="Path to the instances CSV file",
    )
    parser.add_argument(
        "--nr-workers",
        type=int,
        default=4,
        help="Number of parallel workers (threads)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PSEUDO_AGENTS_DIR,
        help="Base directory for pseudo-agent outputs",
    )
    parser.add_argument(
        "--baseline-dir",
        type=Path,
        default=BASELINE_RESULTS_DIR,
        help="Directory to store baseline test results",
    )
    parser.add_argument(
        "--timeout-test",
        type=int,
        default=1200,
        help="Timeout in seconds for test evaluation (default: 20 minutes)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=5,
        help="Number of test runs per agent per instance",
    )
    parser.add_argument(
        "--agents",
        nargs="+",
        default=["golden_agent", "null_agent"],
        help="Agent IDs to run (default: golden_agent null_agent)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing baseline results",
    )

    args = parser.parse_args()
    args.instances_csv = args.instances_csv.resolve()
    args.output_dir = args.output_dir.resolve()
    args.baseline_dir = args.baseline_dir.resolve()
    return args


def _prediction_diff_path(output_dir: Path, instance, agent_id: str) -> Path:
    return output_dir / instance.owner / instance.repo / instance.short_hash / agent_id / "prediction.diff"


def _baseline_result_path(baseline_dir: Path, instance, agent_id: str) -> Path:
    return baseline_dir / instance.owner / instance.repo / instance.short_hash / f"{agent_id}.jsonl"


def _baseline_logs_dir(baseline_dir: Path, instance, agent_id: str) -> Path:
    return baseline_dir / instance.owner / instance.repo / instance.short_hash / "logs" / agent_id


def _write_metric_line(path: Path, metrics: TestMetrics | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        payload = None if metrics is None else metrics.model_dump()
        fh.write(json.dumps(payload) + "\n")


def _run_single_test(
    instance, agent_id: str, prediction_diff: Path, rules_dir: Path, timeout: int, logger
) -> tuple[TestMetrics | None, str]:
    eval_dir = Path(tempfile.mkdtemp(prefix=f"baseline-{instance.id}-{agent_id}-"))
    try:
        test_metrics, test_stdout = run_test_evaluation(
            instance,
            prediction_diff,
            eval_dir,
            timeout,
            logger,
            rules_dir,
        )
        if test_metrics is None:
            test_metrics = parse_test_output(test_stdout)
        return test_metrics, test_stdout
    finally:
        try:
            shutil.rmtree(eval_dir)
        except Exception:
            pass


def populate_instance_baseline(instance, args, logger) -> bool:
    rules_dir = prepare_temp_rules_dir(instance, logger)
    if rules_dir is None:
        logger.error(f"Skipping {instance.id}: missing rules assets for evaluation")
        return False

    try:
        for agent_id in args.agents:
            result_path = _baseline_result_path(args.baseline_dir, instance, agent_id)
            if result_path.exists() and not args.force:
                logger.warning(f"Skipping {instance.id} ({agent_id}): baseline results already exist")
                continue
            if result_path.exists() and args.force:
                result_path.unlink()

            prediction_diff = _prediction_diff_path(args.output_dir, instance, agent_id)
            if not prediction_diff.exists():
                logger.warning(f"Missing prediction.diff for {instance.id} ({agent_id}) at {prediction_diff}")
                continue

            logger.info(f"Running baseline tests for {instance.id} ({agent_id})")
            for run_idx in range(1, args.runs + 1):
                logger.info(f"  Run {run_idx}/{args.runs}")
                metrics, test_stdout = _run_single_test(
                    instance,
                    agent_id,
                    prediction_diff,
                    rules_dir,
                    args.timeout_test,
                    logger,
                )
                _write_metric_line(result_path, metrics)
                logs_dir = _baseline_logs_dir(args.baseline_dir, instance, agent_id)
                logs_dir.mkdir(parents=True, exist_ok=True)
                log_index = run_idx - 1
                (logs_dir / f"{log_index}_stdout.txt").write_text(test_stdout)
        return True
    finally:
        cleanup_temp_rules_dir(rules_dir, logger)


def main() -> None:
    args = parse_args()

    log_dir = Path("logs") / "baseline_results"
    log_dir.mkdir(parents=True, exist_ok=True)
    setup_logging(str(log_dir))
    logger = get_logger("baseline_results")

    ensure_entrypoint_executable(Path("./entrypoint.sh"), logger)

    if not args.instances_csv.exists():
        logger.error(f"Instances CSV not found: {args.instances_csv}")
        raise SystemExit(1)

    instances = load_instances_from_csv(args.instances_csv)
    if not instances:
        logger.warning("No instances found in CSV")
        return

    instances_to_run = instances[: args.instances]
    if len(instances_to_run) < len(instances):
        logger.info(f"Running first {len(instances_to_run)} instances (--instances={args.instances})")
    else:
        logger.info(f"Running all {len(instances_to_run)} instances")

    results = {"success": 0, "failed": 0}

    executor = ThreadPoolExecutor(max_workers=args.nr_workers)
    try:
        future_to_instance = {
            executor.submit(
                populate_instance_baseline,
                inst,
                args,
                get_logger(inst.id, use_stdout=False, log_subdir="baseline_results"),
            ): inst
            for inst in instances_to_run
        }
        with tqdm(total=len(instances_to_run), desc="Baseline Results", unit="instance") as pbar:
            for future in as_completed(future_to_instance):
                instance = future_to_instance[future]
                try:
                    ok = future.result()
                    if ok:
                        results["success"] += 1
                    else:
                        results["failed"] += 1
                except Exception as exc:
                    results["failed"] += 1
                    logger.error(f"{instance.id} failed: {exc}")
                pbar.update(1)
    finally:
        executor.shutdown(wait=False, cancel_futures=True)

    total = results["success"] + results["failed"]
    logger.info("=" * 60)
    logger.info("Baseline Results Summary:")
    logger.info(f"  Total: {total}")
    logger.info(f"  Success: {results['success']}")
    logger.info(f"  Failed: {results['failed']}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
