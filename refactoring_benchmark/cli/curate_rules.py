"""Curate additive rules with recorded or LLM-generated judge decisions."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import Any

import yaml
from tqdm import tqdm

from refactoring_benchmark.utils.common import load_instances_from_csv

DEFAULT_RULES_DIR = Path("./assets/rules")
DEFAULT_OUTPUT_DIR = Path("./assets/rules-curated")
DEFAULT_DESCRIPTIONS_DIR = Path("./assets/descriptions")
DEFAULT_DIFFS_DIR = Path("./assets/diffs")
DEFAULT_INSTANCES_CSV = Path("./instances.csv")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-pro-preview")
GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
GEMINI_API_ROOT = "https://generativelanguage.googleapis.com/v1beta"
INPUT_COST_PER_MTOK = 2.0
CACHED_INPUT_COST_PER_MTOK = 0.2
OUTPUT_COST_PER_MTOK = 12.0
HIGH_TIER_INPUT_COST_PER_MTOK = 4.0
HIGH_TIER_CACHED_INPUT_COST_PER_MTOK = 0.4
HIGH_TIER_OUTPUT_COST_PER_MTOK = 18.0
HIGH_TIER_PROMPT_TOKEN_THRESHOLD = 200_000
JUDGE_RULES_PER_REQUEST = 5
DECISION_RE = re.compile(r"Decision:\s*(Yes|No)\b", re.IGNORECASE)
JSON_SEPARATORS = (",", ":")
REQUEST_TIMEOUT_SECONDS = 180
REQUEST_ATTEMPTS = 2
MAX_DIFF_MB = 0.5
MAX_DIFF_BYTES = int(MAX_DIFF_MB * 1024 * 1024)
MAX_DESCRIPTION_BYTES = 6_000
LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a curated rule root by filtering additive rules with LLM-as-a-judge decisions.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--rules-dir", type=Path, default=DEFAULT_RULES_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--instances-csv", type=Path, default=DEFAULT_INSTANCES_CSV)
    parser.add_argument(
        "--decisions-jsonl",
        type=Path,
        help="Apply existing judge decisions instead of calling an LLM.",
    )
    parser.add_argument(
        "--judge",
        action="store_true",
        help="Call Gemini for missing decisions.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of instances to process.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output directory.")
    args = parser.parse_args()

    args.rules_dir = args.rules_dir.resolve()
    args.output_dir = args.output_dir.resolve()
    args.instances_csv = args.instances_csv.resolve()
    args.descriptions_dir = DEFAULT_DESCRIPTIONS_DIR.resolve()
    args.diffs_dir = DEFAULT_DIFFS_DIR.resolve()
    if args.decisions_jsonl:
        args.decisions_jsonl = args.decisions_jsonl.resolve()
    return args


def load_rule_file(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data.get("rules", []), list):
        raise ValueError(f"Expected a 'rules' list in {path}")
    return data


def write_rule_file(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)


def instance_key_from_rules_file(rules_file: Path, rules_root: Path) -> str:
    relative = rules_file.relative_to(rules_root)
    return str(relative.parent)


def discover_positive_rule_files(rules_root: Path, instances_csv: Path, limit: int | None) -> list[Path]:
    instances = load_instances_from_csv(instances_csv)
    if limit is not None:
        instances = instances[:limit]
    files = []
    for instance in instances:
        rules_file = rules_root / instance.owner / instance.repo / instance.short_hash / "rules_positive.yml"
        if not rules_file.exists():
            raise FileNotFoundError(f"Missing positive rules file: {rules_file}")
        files.append(rules_file)
    return files


def decision_cache_key(instance: str, rule_id: str) -> str:
    parts = instance.split("/")
    if len(parts) < 2:
        raise ValueError(f"Expected instance path owner/repo/hash, got: {instance}")
    return f"{parts[0]}_{parts[1]}_{rule_id}"


def load_decisions(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None or not path.exists():
        return {}
    decisions: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            instance = record.get("instance")
            rule_id = record.get("rule_id")
            if not instance or not rule_id:
                raise ValueError(f"Decision record {path}:{line_number} is missing instance or rule_id")
            cache_key = record.get("cache_key")
            if not isinstance(cache_key, str):
                cache_key = decision_cache_key(instance, rule_id)
                record["cache_key"] = cache_key
            decisions[cache_key] = record
    return decisions


def estimate_gemini_cost_usd(usage: dict[str, Any] | None) -> float | None:
    if usage is None:
        return None
    input_tokens = usage.get("promptTokenCount")
    output_tokens = usage.get("candidatesTokenCount")
    if not isinstance(input_tokens, int | float) or not isinstance(output_tokens, int | float):
        return None
    cached_tokens = usage.get("cachedContentTokenCount", 0)
    if not isinstance(cached_tokens, int | float):
        cached_tokens = 0
    uncached_input_tokens = max(input_tokens - cached_tokens, 0)
    input_cost_per_mtok = INPUT_COST_PER_MTOK
    cached_input_cost_per_mtok = CACHED_INPUT_COST_PER_MTOK
    output_cost_per_mtok = OUTPUT_COST_PER_MTOK
    if input_tokens > HIGH_TIER_PROMPT_TOKEN_THRESHOLD:
        input_cost_per_mtok = HIGH_TIER_INPUT_COST_PER_MTOK
        cached_input_cost_per_mtok = HIGH_TIER_CACHED_INPUT_COST_PER_MTOK
        output_cost_per_mtok = HIGH_TIER_OUTPUT_COST_PER_MTOK
    return (
        uncached_input_tokens / 1_000_000 * input_cost_per_mtok
        + cached_tokens / 1_000_000 * cached_input_cost_per_mtok
        + output_tokens / 1_000_000 * output_cost_per_mtok
    )


def decision_cost_usd(decision: dict[str, Any]) -> float | None:
    judge = decision.get("judge")
    cost = judge.get("cost_usd") if isinstance(judge, dict) else None
    return cost if isinstance(cost, int | float) else None


def format_cost(cost: float | None) -> str:
    return "n/a" if cost is None else f"${cost:.4f}"


def projected_total_cost(observed_cost: float | None, completed: int, total: int) -> float | None:
    if observed_cost is None or completed == 0:
        return None
    return observed_cost / completed * total


def chunk_rules(rules: list[dict[str, Any]], chunk_size: int) -> list[list[dict[str, Any]]]:
    return [rules[start : start + chunk_size] for start in range(0, len(rules), chunk_size)]


def parallel_instances_from_env() -> int:
    raw_value = os.environ.get("NR_PARALLEL_INSTANCES", "1")
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"NR_PARALLEL_INSTANCES must be an integer, got: {raw_value}") from exc
    if value < 1:
        raise ValueError(f"NR_PARALLEL_INSTANCES must be at least 1, got: {value}")
    return value


def filter_positive_rules(
    rules_data: dict[str, Any],
    instance: str,
    decisions: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    kept_rules = []
    used_decisions = []
    for rule in rules_data.get("rules", []):
        rule_id = rule.get("id")
        if not rule_id:
            raise ValueError(f"Positive rule without id in {instance}")
        decision = decisions.get(decision_cache_key(instance, rule_id))
        if decision is None:
            raise ValueError(f"Missing curation decision for {instance}:{rule_id}")
        used_decisions.append(decision)
        keep = decision.get("keep")
        if not isinstance(keep, bool):
            raise ValueError(f"Decision missing boolean keep field: {decision}")
        if keep:
            kept_rules.append(rule)
    curated = dict(rules_data)
    curated["rules"] = kept_rules
    return curated, used_decisions


def read_optional_text(path: Path, max_bytes: int) -> str:
    if not path.exists():
        return ""
    return path.read_bytes()[:max_bytes].decode("utf-8", errors="replace")


def codebase_from_instance(instance: str) -> str:
    parts = instance.split("/")
    if len(parts) >= 2:
        return "/".join(parts[:2])
    return instance


def build_judge_prompt(instance: str, rules: list[dict[str, Any]], description: str, golden_diff: str) -> str:
    rules_yaml = yaml.safe_dump(rules, sort_keys=False)
    codebase = codebase_from_instance(instance)
    return f"""You will be given Semgrep rules for the codebase : {codebase}.
Each Semgrep rule is used to check whether the refactoring provided in the unified diff has been completed according to the provided task description.

For each rule, output whether the rule is generic enough to capture refactorings that are semantically equivalent.

Output "Yes" if the rule is generic enough.
Output "No" if the rule corresponds to an arbitrary naming decision.

A rule corresponds to an arbitrary naming ("No") decision if it requires the refactoring to use an arbitrary name or convention that is non obvious. The task description should not be used as an indicator on whether a naming decision is arbitrary or not.

A rule is considered generic ("Yes") if either
    a) it requires no particular name.
    b) the name directly follows from the repository conventions that exist before the change.
    c) the entities used in the rule already exist before the change.
    d) the required patterns are directly imposed by an external package and thus outside of the decision scope of the contributor.

Output exactly a JSON array. Include one object for every input rule, with these fields:
- "rule_id": the exact input rule id.
- "decision": either "Yes" or "No".
- "reason": a concise explanation for that rule.

The refactoring task description is:
{description}

The (truncated) diff is given by:
```diff
{golden_diff}
```

The Semgrep Rules are given by:
```yaml
{rules_yaml}
```
"""


def strip_json_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```json") and stripped.endswith("```"):
        return stripped.removeprefix("```json").removesuffix("```").strip()
    if stripped.startswith("```") and stripped.endswith("```"):
        return stripped.removeprefix("```").removesuffix("```").strip()
    return stripped


def parse_judge_response(text: str, expected_rule_ids: set[str]) -> list[dict[str, Any]]:
    try:
        records = json.loads(strip_json_fence(text))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Judge response was not valid JSON: {text}") from exc
    if not isinstance(records, list):
        raise ValueError(f"Judge response must be a JSON array: {text}")

    parsed: list[dict[str, Any]] = []
    seen_rule_ids: set[str] = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError(f"Judge response array item must be an object: {record}")
        rule_id = record.get("rule_id")
        decision = record.get("decision")
        reason = record.get("reason")
        if not isinstance(rule_id, str) or rule_id not in expected_rule_ids:
            raise ValueError(f"Judge response has unexpected rule_id: {record}")
        if rule_id in seen_rule_ids:
            raise ValueError(f"Judge response has duplicate rule_id: {rule_id}")
        if decision not in {"Yes", "No"}:
            raise ValueError(f"Judge response has invalid decision: {record}")
        if not isinstance(reason, str):
            raise ValueError(f"Judge response has invalid reason: {record}")
        parsed.append({"rule_id": rule_id, "keep": decision == "Yes", "reason": reason})
        seen_rule_ids.add(rule_id)

    missing_rule_ids = expected_rule_ids - seen_rule_ids
    if missing_rule_ids:
        raise ValueError(f"Judge response missed rule ids: {sorted(missing_rule_ids)}")
    return parsed


def model_path(model: str) -> str:
    return model if model.startswith("models/") else f"models/{model}"


def gemini_generate_content_url(model: str) -> str:
    model_path_value = model_path(model)
    quoted_model_path = urllib.parse.quote(model_path_value, safe="/")
    return f"{GEMINI_API_ROOT}/{quoted_model_path}:generateContent"


def extract_gemini_text(payload: dict[str, Any]) -> str:
    candidates = payload.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError(f"Gemini response did not contain candidates: {payload}")
    parts = candidates[0].get("content", {}).get("parts", [])
    text_parts = [part["text"] for part in parts if isinstance(part, dict) and isinstance(part.get("text"), str)]
    if not text_parts:
        raise ValueError(f"Gemini response did not contain text: {payload}")
    return "\n".join(text_parts)


def is_timeout_error(exc: BaseException) -> bool:
    if isinstance(exc, TimeoutError):
        return True
    if isinstance(exc, urllib.error.URLError):
        return isinstance(exc.reason, TimeoutError)
    return False


def request_json(url: str, api_key: str, payload: dict[str, Any] | None) -> dict[str, Any]:
    body = None if payload is None else json.dumps(payload, separators=JSON_SEPARATORS).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"X-goog-api-key": api_key, "Content-Type": "application/json"},
        method="GET" if payload is None else "POST",
    )
    for attempt in range(1, REQUEST_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                raw = response.read().decode("utf-8")
            return json.loads(raw)
        except (TimeoutError, urllib.error.URLError) as exc:
            if is_timeout_error(exc) and attempt < REQUEST_ATTEMPTS:
                LOGGER.warning("Gemini request timed out; retrying once")
                continue
            raise RuntimeError(f"Gemini request failed: {exc}") from exc
    raise RuntimeError("Gemini request failed")


def read_instance_context(instance: str, descriptions_dir: Path, diffs_dir: Path) -> tuple[str, str]:
    description = read_optional_text(descriptions_dir / instance / "description.md", max_bytes=MAX_DESCRIPTION_BYTES)
    golden_diff = read_optional_text(diffs_dir / instance / "golden.diff", max_bytes=MAX_DIFF_BYTES)
    return description, golden_diff


def build_generate_request(
    instance: str,
    rules: list[dict[str, Any]],
    description: str,
    golden_diff: str,
) -> dict[str, Any]:
    return {
        "contents": [{"role": "user", "parts": [{"text": build_judge_prompt(instance, rules, description, golden_diff)}]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
    }


def judge_rules(
    instance: str,
    rules: list[dict[str, Any]],
    description: str,
    golden_diff: str,
    api_key: str,
) -> list[dict[str, Any]]:
    response = request_json(
        gemini_generate_content_url(GEMINI_MODEL),
        api_key,
        build_generate_request(instance, rules, description, golden_diff),
    )
    text = extract_gemini_text(response)
    parsed = parse_judge_response(text, {rule["id"] for rule in rules})
    usage = response.get("usageMetadata")
    request_cost = estimate_gemini_cost_usd(usage if isinstance(usage, dict) else None)
    rule_cost = None if request_cost is None else request_cost / len(parsed)
    decisions = []
    for parsed_decision in parsed:
        rule_id = parsed_decision["rule_id"]
        decisions.append(
            {
                "instance": instance,
                "rule_id": rule_id,
                "cache_key": decision_cache_key(instance, rule_id),
                "keep": parsed_decision["keep"],
                "reason": parsed_decision["reason"],
                "judge": {
                    "model": GEMINI_MODEL,
                    "cost_usd": rule_cost,
                    "request_cost_usd": request_cost,
                    "request_rule_count": len(parsed),
                    "usage": usage,
                },
                "raw_response": text,
            }
        )
    return decisions


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")


def copy_negative_rules(src_instance_dir: Path, dst_instance_dir: Path) -> None:
    negative_src = src_instance_dir / "rules_negative.yml"
    if not negative_src.exists():
        raise FileNotFoundError(f"Missing negative rules file: {negative_src}")
    dst_instance_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(negative_src, dst_instance_dir / "rules_negative.yml")


def judge_instance_rules(
    instance: str,
    rules: list[dict[str, Any]],
    descriptions_dir: Path,
    diffs_dir: Path,
    api_key: str,
    decisions_path: Path,
    decisions: dict[str, dict[str, Any]],
    progress: tqdm,
    progress_lock: Lock,
    progress_state: dict[str, Any],
    total_missing_rules: int,
) -> None:
    description, golden_diff = read_instance_context(instance, descriptions_dir, diffs_dir)
    LOGGER.info("Judging %d uncached rules for %s", len(rules), instance)
    instance_kept = 0
    instance_rejected = 0
    instance_cost = 0.0
    judged_rules = 0
    for rules_chunk in chunk_rules(rules, JUDGE_RULES_PER_REQUEST):
        chunk_decisions = judge_rules(instance, rules_chunk, description, golden_diff, api_key)
        for decision in chunk_decisions:
            instance_kept += int(decision["keep"])
            instance_rejected += int(not decision["keep"])
            cost = decision_cost_usd(decision)
            if cost is not None:
                instance_cost += cost
            with progress_lock:
                decisions[decision["cache_key"]] = decision
                append_jsonl(decisions_path, decision)
                if cost is not None:
                    observed_cost = progress_state["observed_cost"]
                    progress_state["observed_cost"] = cost if observed_cost is None else observed_cost + cost
                progress_state["judged_requests"] += 1
                expected_cost = projected_total_cost(
                    progress_state["observed_cost"],
                    progress_state["judged_requests"],
                    total_missing_rules,
                )
                progress.update(1)
                progress.set_postfix(
                    cost=format_cost(progress_state["observed_cost"]),
                    expected_cost=format_cost(expected_cost),
                )
        judged_rules += len(chunk_decisions)
        LOGGER.info("Judged %d/%d uncached rules for %s", judged_rules, len(rules), instance)
    LOGGER.info(
        "Finished Gemini judgments for %s: kept=%d rejected=%d cost=%s",
        instance,
        instance_kept,
        instance_rejected,
        format_cost(instance_cost),
    )


def curate_rules(args: argparse.Namespace) -> None:
    if args.output_dir.exists() and args.force:
        shutil.rmtree(args.output_dir)
    decisions_path = args.decisions_jsonl or (args.output_dir / "curation_positive.jsonl")
    can_resume_judge = args.judge and decisions_path.exists()
    if args.output_dir.exists() and any(args.output_dir.iterdir()) and not can_resume_judge:
        raise FileExistsError(f"Output directory already exists and is not empty: {args.output_dir}")

    api_key = os.environ.get(GEMINI_API_KEY_ENV) if args.judge else None
    if args.judge and not api_key:
        raise ValueError(f"--judge requires API key in ${GEMINI_API_KEY_ENV}")

    decisions = load_decisions(decisions_path if args.judge else args.decisions_jsonl)
    positive_files = discover_positive_rule_files(args.rules_dir, args.instances_csv, args.limit)
    kept_rules = 0
    rejected_rules = 0
    observed_cost: float | None = None
    judged_requests = 0
    missing_rules_by_instance: dict[str, list[dict[str, Any]]] = {}

    if args.judge:
        for positive_path in positive_files:
            instance = instance_key_from_rules_file(positive_path, args.rules_dir)
            positive_data = load_rule_file(positive_path)
            for rule in positive_data.get("rules", []):
                rule_id = rule.get("id")
                if not rule_id:
                    raise ValueError(f"Positive rule without id in {instance}")
                if decision_cache_key(instance, rule_id) not in decisions:
                    missing_rules_by_instance.setdefault(instance, []).append(rule)
        total_missing_rules = sum(len(rules) for rules in missing_rules_by_instance.values())
        total_missing_requests = sum(
            len(chunk_rules(rules, JUDGE_RULES_PER_REQUEST)) for rules in missing_rules_by_instance.values()
        )
        LOGGER.info(
            "Prepared Gemini judge requests for %d uncached rules in %d requests across %d instances",
            total_missing_rules,
            total_missing_requests,
            len(missing_rules_by_instance),
        )
        parallel_instances = parallel_instances_from_env()
        LOGGER.info("Judging with %d parallel instances", parallel_instances)
        judge_progress = tqdm(total=total_missing_rules, desc="Judging rules", unit="rule")
        progress_lock = Lock()
        progress_state: dict[str, Any] = {"observed_cost": observed_cost, "judged_requests": judged_requests}
        try:
            with ThreadPoolExecutor(max_workers=parallel_instances) as executor:
                futures = [
                    executor.submit(
                        judge_instance_rules,
                        instance,
                        rules,
                        args.descriptions_dir,
                        args.diffs_dir,
                        api_key,
                        decisions_path,
                        decisions,
                        judge_progress,
                        progress_lock,
                        progress_state,
                        total_missing_rules,
                    )
                    for instance, rules in missing_rules_by_instance.items()
                ]
                for future in as_completed(futures):
                    future.result()
        finally:
            judge_progress.close()
        observed_cost = progress_state["observed_cost"]
        judged_requests = progress_state["judged_requests"]

    progress = tqdm(positive_files, desc="Curating rule files", unit="instance")
    summary_path = args.output_dir / "curation_summary.jsonl"
    if summary_path.exists():
        summary_path.unlink()
    for positive_path in progress:
        instance = instance_key_from_rules_file(positive_path, args.rules_dir)
        src_instance_dir = positive_path.parent
        dst_instance_dir = args.output_dir / instance
        positive_data = load_rule_file(positive_path)

        curated_positive, used_decisions = filter_positive_rules(positive_data, instance, decisions)
        kept_rules += len(curated_positive.get("rules", []))
        rejected_rules += len(used_decisions) - len(curated_positive.get("rules", []))
        write_rule_file(dst_instance_dir / "rules_positive.yml", curated_positive)
        copy_negative_rules(src_instance_dir, dst_instance_dir)
        append_jsonl(
            summary_path,
            {
                "instance": instance,
                "positive_rules_total": len(positive_data.get("rules", [])),
                "positive_rules_kept": len(curated_positive.get("rules", [])),
                "positive_rules_rejected": len(used_decisions) - len(curated_positive.get("rules", [])),
            },
        )
        progress.set_postfix(
            uncached_rules=sum(len(rules) for rules in missing_rules_by_instance.values()) if args.judge else 0,
            kept=kept_rules,
            rejected=rejected_rules,
            cost=format_cost(observed_cost),
        )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    curate_rules(parse_args())


if __name__ == "__main__":
    main()
