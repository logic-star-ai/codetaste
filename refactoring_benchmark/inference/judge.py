"""LLM judge module for selecting the best refactoring plan from multiple candidates."""

import logging
import os
import re
import time
from typing import Dict, Tuple, Optional

from refactoring_benchmark.utils.logger import get_logger

logger = get_logger(__name__)


def judge_best_plan(
    original_description: str, candidate_plans: Dict[int, str], api_key: Optional[str] = None
) -> Tuple[int, Dict[str, any]]:
    """
    Use an LLM (Claude Sonnet) to judge which candidate plan best matches the original task description.

    Args:
        original_description: The original task description from description.md
        candidate_plans: Dictionary mapping plan index to plan content (e.g., {0: content0, 1: content1, ...})
        api_key: Optional API key for Anthropic. If None, uses ANTHROPIC_API_KEY env var

    Returns:
        Tuple of (selected_plan_index, judge_metadata)
        where judge_metadata contains: cost_usd, latency_seconds, reasoning (optional)

    Raises:
        ValueError: If fewer than 2 plans provided, or if API response is invalid
        RuntimeError: If API call fails
        ImportError: If anthropic package is not installed
    """
    try:
        import anthropic
    except ImportError:
        raise ImportError(
            "anthropic package is required for multiplan mode. "
            "Install it with: pip install anthropic"
        )

    # Validate inputs
    num_plans = len(candidate_plans)
    if num_plans < 2:
        raise ValueError(f"Need at least 2 candidate plans, got {num_plans}")

    expected_indices = set(range(num_plans))
    if set(candidate_plans.keys()) != expected_indices:
        raise ValueError(f"Candidate plans must be indexed 0-{num_plans-1} consecutively")

    # Get API key
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY environment variable not set. "
                "Required for multiplan mode LLM judge."
            )

    # Construct judge prompt
    judge_prompt = _construct_judge_prompt(original_description, candidate_plans)
    # Make API call
    logger.info("Calling Anthropic API (Sonnet) to judge best plan...")
    start_time = time.time()

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            temperature=0.0,
            messages=[{"role": "user", "content": judge_prompt}],
        )
    except Exception as e:
        logger.error(f"Anthropic API call failed: {e}")
        raise RuntimeError(f"Failed to call Anthropic API: {e}")

    latency = time.time() - start_time

    # Extract response content
    if not response.content or len(response.content) == 0:
        raise RuntimeError("Anthropic API returned empty response")

    response_text = response.content[0].text

    # Parse selected plan index
    selected_index = _parse_plan_selection(response_text, max_index=num_plans - 1)
    if selected_index is None:
        raise ValueError(
            f"Could not parse valid plan selection from judge response: {response_text}"
        )

    # Calculate cost (approximate, based on token usage)
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens
    cost_usd = _calculate_cost(input_tokens, output_tokens)

    # Construct metadata
    judge_metadata = {
        "selected_plan_index": selected_index,
        "judge_cost_usd": cost_usd,
        "judge_latency_seconds": round(latency, 2),
        "judge_reasoning": str(response_text),  # Full response includes reasoning
        "judge_input_tokens": input_tokens,
        "judge_output_tokens": output_tokens,
    }

    logger.info(
        f"Judge selected plan {selected_index} "
        f"(cost: ${cost_usd:.4f}, latency: {latency:.2f}s)"
    )

    return selected_index, judge_metadata


def _construct_judge_prompt(original_description: str, candidate_plans: Dict[int, str]) -> str:
    """Construct the prompt for the LLM judge."""
    num_plans = len(candidate_plans)
    plan_numbers = ", ".join(str(i) for i in range(num_plans - 1)) + f", or {num_plans - 1}"

    # Convert small numbers to words for better readability
    num_words = {2: "TWO", 3: "THREE", 4: "FOUR", 5: "FIVE", 6: "SIX", 7: "SEVEN", 8: "EIGHT", 9: "NINE"}
    num_display = num_words.get(num_plans, str(num_plans))

    prompt = f"""You are evaluating multiple refactoring plans for a software engineering task.

Your goal is to select the plan that BEST matches the original task description in terms of similarity / overlap.

Below is the ORIGINAL TASK DESCRIPTION:

---
{original_description}
---

Now, here are {num_display} CANDIDATE REFACTORING PLANS:

"""

    # Add each candidate plan dynamically
    for i in sorted(candidate_plans.keys()):
        prompt += f"""PLAN {i}:
---
{candidate_plans[i]}
---

"""

    prompt += f"""Based on your analysis, which plan ({plan_numbers}) BEST matches the original task description?

Provide your reasoning briefly, then state your final selection clearly as:
SELECTED: [plan number]

Your selection:"""

    return prompt


def _parse_plan_selection(response_text: str, max_index: int) -> Optional[int]:
    """
    Parse the selected plan index from the judge's response.

    Args:
        response_text: The judge's response text
        max_index: Maximum valid plan index (e.g., 4 for 5 plans)

    Looks for patterns like:
    - "SELECTED: 2"
    - "Plan 3"
    - Just "2" on a line by itself

    Returns:
        Plan index or None if parsing fails
    """
    # Try explicit SELECTED: pattern first
    match = re.search(r"SELECTED:\s*(\d+)", response_text, re.IGNORECASE)
    if match:
        index = int(match.group(1))
        if 0 <= index <= max_index:
            return index

    # Try "Plan N" pattern
    match = re.search(r"Plan\s*(\d+)", response_text, re.IGNORECASE)
    if match:
        index = int(match.group(1))
        if 0 <= index <= max_index:
            return index

    # Try standalone digit in last few lines
    lines = response_text.strip().split("\n")
    for line in reversed(lines[-3:]):  # Check last 3 lines
        line = line.strip()
        if line.isdigit():
            index = int(line)
            if 0 <= index <= max_index:
                return index

    return None


def _calculate_cost(input_tokens: int, output_tokens: int) -> float:
    """
    Calculate approximate API cost in USD.

    Pricing as of 2025 (approximate):
    - Sonnet 4.5: $3.00 per MTok input, $15.00 per MTok output
    """
    input_cost_per_mtok = 3.0
    output_cost_per_mtok = 15.0

    input_cost = (input_tokens / 1_000_000) * input_cost_per_mtok
    output_cost = (output_tokens / 1_000_000) * output_cost_per_mtok

    return input_cost + output_cost
