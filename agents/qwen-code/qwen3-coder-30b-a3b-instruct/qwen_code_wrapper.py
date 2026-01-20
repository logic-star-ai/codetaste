#!/usr/bin/env python3

import sys
import subprocess
import json
import os
from datetime import datetime, timezone

# Configuration
MAX_BUDGET_USD = float(os.environ.get("MAX_BUDGET_USD", 2.5))
INPUT_TOKEN_PRICE = float(os.environ.get("INPUT_TOKEN_PRICE", 0.07 / 1e6))
OUTPUT_TOKEN_PRICE = float(os.environ.get("OUTPUT_TOKEN_PRICE", 0.27 / 1e6))

assert os.environ.get("OPENAI_API_KEY") is not None, "OPENAI_API_KEY environment variable must be set"
assert os.environ.get("OPENAI_BASE_URL") is not None, "OPENAI_BASE_URL environment variable must be set"
assert os.environ.get("OPENAI_MODEL") is not None, "OPENAI_MODEL environment variable must be set"

def calculate_cost(input_tokens, output_tokens):
    """Calculate cost based on token counts."""
    return (input_tokens * INPUT_TOKEN_PRICE) + (output_tokens * OUTPUT_TOKEN_PRICE)

def parse_usage(data, cumulative=False):
    """Extract usage data from JSON object."""
    message_type = data.get('type', 'unknown')
    if message_type == 'result' and not cumulative:
        return None

    usage = None
    if 'usage' in data:
        usage = data['usage']
    elif 'message' in data and 'usage' in data['message']:
        usage = data['message']['usage']

    if usage:
        input_tokens = usage.get('input_tokens', 0)
        output_tokens = usage.get('output_tokens', 0)
        return input_tokens, output_tokens

    return None

def get_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    args = sys.argv[1:]

    # Ensure --output-format is present for parsing logic
    if '--output-format' not in args:
        args = ['--output-format', 'stream-json'] + args

    cmd = ['qwen'] + args

    # Telemetry goes to stderr to keep stdout clean for the raw model data
    print(f"[WRAPPER] Executing: {' '.join(cmd)}", file=sys.stderr)
    print(f"[WRAPPER] Budget: ${MAX_BUDGET_USD:.2f} | Rates: ${INPUT_TOKEN_PRICE * 1e6:.2f}/M in, ${OUTPUT_TOKEN_PRICE * 1e6:.2f}/M out", file=sys.stderr)
    
    start_time = get_timestamp()
    last_data = None
    model = None
    total_cost = 0.0
    total_input_tokens = 0
    total_output_tokens = 0
    budget_was_exceeded = False
    additional_info = {}
    turns_till_tool_use = 5
    try:
        process = subprocess.Popen(
            cmd,
            stdin=sys.stdin,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            env=os.environ.copy(),
            text=True,
            bufsize=1
        )

        for line in process.stdout:
            # Pass through the raw line to stdout
            print(line, end='', flush=True)
            if "This request requires more credits" in line:
                budget_was_exceeded = True
                additional_info["error_message"] = "Not enough credits for the request. Terminating."
            try:
                data = json.loads(line.strip())
                last_data = data
                usage_data = parse_usage(data)

                # Track Model Name
                data_model = data.get("message", {}).get("model", model)
                if data_model != model:
                    model = data_model
                    print(f"[WRAPPER] Model: {model}", file=sys.stderr, flush=True)

                if usage_data:
                    in_delta, out_delta = usage_data
                    total_input_tokens += in_delta
                    total_output_tokens += out_delta
                    
                    # Calculate total cost based on accumulated deltas
                    total_cost = calculate_cost(total_input_tokens, total_output_tokens)

                    # Print cost update to stderr
                    print(f"[COST] Total: ${total_cost:.6f}", file=sys.stderr, flush=True)

                    # BUDGET ENFORCEMENT
                    if total_cost > MAX_BUDGET_USD:
                        budget_was_exceeded = True
                        print(f"\n[WRAPPER ERROR] budget_exceeded: ${total_cost:.4f} > ${MAX_BUDGET_USD:.4f}", file=sys.stderr)
                        process.terminate()
                        break

            except (json.JSONDecodeError, KeyError):
                # Silent skip on non-json or malformed lines to keep logs clean
                pass

        return_code = process.wait()

        finish_reason = "unknown"
        if budget_was_exceeded:
            finish_reason = "budget_exceeded"
        elif last_data and last_data.get('type') == 'result':
            subtype = last_data.get('subtype', 'unknown')
            if last_data.get('is_error'):
                finish_reason = "error" if subtype == "success" else subtype
            elif last_data.get('num_turns', 1) == 1:
                finish_reason = "error"
                additional_info["error_message"] = "Process returned on first turn."
            elif "[API Error:" in last_data.get('result', "")[:20] + last_data.get('result', "")[-60:]: # can crash with [API Error: Network connection lost.]
                finish_reason = "error"
                additional_info["error_message"] = last_data.get('result', "")
            else:
                finish_reason = subtype

        result = {
            "finish_reason": finish_reason,
            "finish_time": get_timestamp(),
            "start_time": start_time,
            "cost_usd": total_cost,
            "additional": {
                "exit_code": return_code,
                "tokens": {
                    "input_tokens": total_input_tokens,
                    "output_tokens": total_output_tokens,
                    "total_tokens": total_input_tokens + total_output_tokens
                },
                "model": model,
                **additional_info
            }
        }
        
        # Final summary also to stderr to avoid breaking piped commands
        print("\n[WRAPPER] Final Result Summary:", file=sys.stderr)
        print(json.dumps(result))
        
        return 0 # Even if budget exceeded we want to save results

    except FileNotFoundError:
        print("[WRAPPER ERROR] 'qwen' command not found.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[WRAPPER] Interrupted by user", file=sys.stderr)
        process.kill()
        return 130

if __name__ == "__main__":
    sys.exit(main())