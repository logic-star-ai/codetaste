import os
import subprocess
import sys
import json
import argparse
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# --- Configuration ---
MAX_LINES = int(os.environ.get("MAX_LINES", 1000))
INPUT_TOKEN_PRICE = float(os.environ.get("INPUT_TOKEN_PRICE", 1.25 / 1e6))
CACHED_INPUT_TOKEN_PRICE = float(os.environ.get("CACHED_INPUT_TOKEN_PRICE", 0.125 / 1e6))
OUTPUT_TOKEN_PRICE = float(os.environ.get("OUTPUT_TOKEN_PRICE", 10.0 / 1e6))

def compute_cost(usage_dict: Optional[Dict[str, Any]]) -> float:
    """
    Calculates the cost of a request based on token usage.
    Assumes 'input_tokens' includes 'cached_input_tokens'.
    """
    if not usage_dict:
        return -1.0
    
    try:
        total_input = usage_dict.get("input_tokens", 0)
        cached_input = usage_dict.get("cached_input_tokens", 0)
        output_tokens = usage_dict.get("output_tokens", 0)

        # Calculate distinct parts to avoid double-charging
        standard_input = max(0, total_input - cached_input)
        
        cost = (
            (standard_input * INPUT_TOKEN_PRICE) +
            (cached_input * CACHED_INPUT_TOKEN_PRICE) +
            (output_tokens * OUTPUT_TOKEN_PRICE)
        )
        return float(cost)
    except (KeyError, TypeError, ValueError):
        return -1.0

def get_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def run_limited_task(prompt: str, unknown_args: list) -> bool:
    line_count = 0
    token_metadata = {}
    start_time = get_timestamp()
    cmd = ["codex", "exec"] + unknown_args + ["--", prompt]
    try:
        with subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=sys.stderr, 
            text=True, 
            bufsize=1
        ) as proc:
            
            for line in proc.stdout:
                # Identify token usage metadata line
                if line.startswith("{") and '"usage"' in line:
                    try:
                        data = json.loads(line)
                        token_metadata = data.get("usage", {})
                        continue  # Do not print usage JSON to stdout
                    except json.JSONDecodeError:
                        pass

                # Handle line limit enforcement
                line_count += 1
                if line_count > MAX_LINES:
                    print(f"\n[!] KILL: Line limit ({MAX_LINES}) exceeded.", file=sys.stderr)
                    proc.terminate()
                    _finalize_output("max_lines_exceeded", line_count, token_metadata, start_time)
                    return True # keep prediction.diff even if we hit line limit

                print(line, end="", flush=True)

            status = proc.wait()
            reason = "success" if status == 0 else "error"
            _finalize_output(reason, line_count, token_metadata, start_time, status)
            return status == 0

    except Exception as e:
        print(f"Execution Error: {e}", file=sys.stderr)
        return False

def _finalize_output(reason: str, lines: int, tokens: dict, start_time: str, exit_code: int = 0):
    """Helper to print the final execution summary as JSON."""
    result = {
        "finish_reason": reason,
        "finish_time": get_timestamp(),
        "start_time": start_time,
        "cost_usd": compute_cost(tokens),
        "additional": {
            "lines": lines,
            "exit_code": exit_code,
            "tokens": tokens
        }
    }
    print(json.dumps(result))

def main():
    parser = argparse.ArgumentParser(add_help=False)
    _, unknown = parser.parse_known_args()

    # Determine prompt source: Stdin (pipe) or final CLI argument
    prompt = None
    if not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    elif unknown:
        prompt = unknown.pop()

    if not prompt:
        print("Error: No prompt provided.", file=sys.stderr)
        sys.exit(1)

    success = run_limited_task(prompt, unknown)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()