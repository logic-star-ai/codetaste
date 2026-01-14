import os
import subprocess
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from time import sleep
from typing import Dict, Any, Optional

# --- Configuration ---
MAX_BUDGET_USD = float(os.environ.get("MAX_BUDGET_USD", 7.5))
INPUT_TOKEN_PRICE = float(os.environ.get("INPUT_TOKEN_PRICE", 1.75 / 1e6))
CACHED_INPUT_TOKEN_PRICE = float(os.environ.get("CACHED_INPUT_TOKEN_PRICE", 0.175 / 1e6))
OUTPUT_TOKEN_PRICE = float(os.environ.get("OUTPUT_TOKEN_PRICE", 14.0 / 1e6))
SESSIONS_DIR = Path.home() / ".codex" / "sessions"

print(f"Using MAX_BUDGET_USD={MAX_BUDGET_USD}, INPUT_TOKEN_PRICE={INPUT_TOKEN_PRICE}, CACHED_INPUT_TOKEN_PRICE={CACHED_INPUT_TOKEN_PRICE}, OUTPUT_TOKEN_PRICE={OUTPUT_TOKEN_PRICE}")

class SessionMonitor:
    def __init__(self):
        self.jsonl_path: Optional[Path] = None
        self.last_pos = 0
        self.tokens = {}
        self.model = "unknown"

    def _find_latest_session(self):
        """Locates the newest jsonl file in the newest session directory."""
        try:
            # 1. Find all 'jsonl' files recursively
            all_jsonl_files = list(SESSIONS_DIR.rglob("*.jsonl"))
            if not all_jsonl_files:
                return

            # 2. Get the file with the latest modification time
            # This effectively finds the 'latest file' in the 'latest dir'
            latest_file = max(all_jsonl_files, key=lambda p: p.stat().st_mtime)
            print(f"Latest session file found: {latest_file}")
            if self.jsonl_path != latest_file:
                self.jsonl_path = latest_file
                self.last_pos = 0 # Reset if we switched to a newer session file
        except Exception as e:
            pass

    def update(self):
        """Incrementally reads new lines from the JSONL file."""
        if not self.jsonl_path:
            self._find_latest_session()
            if not self.jsonl_path: return

        try:
            with open(self.jsonl_path, "r") as f:
                f.seek(self.last_pos)
                for line in f:
                    try:
                        data = json.loads(line)
                        msg_type = data.get("type")
                        payload = data.get("payload", {})

                        # Extract Model from turn_context
                        if msg_type == "turn_context":
                            if self.model != payload.get("model", self.model):
                                print(f"Updated model to: {payload.get('model')}")
                                self.model = payload.get("model", self.model)

                        # Extract Tokens from token_count
                        elif msg_type == "event_msg" and payload.get("type") == "token_count":
                            info = payload.get("info")
                            if info:
                                self.tokens = info.get("total_token_usage", self.tokens)
                    except json.JSONDecodeError:
                        continue
                self.last_pos = f.tell()
        except Exception:
            pass

def compute_cost(usage_dict: Optional[Dict[str, Any]]) -> float:
    if not usage_dict: return 0.0
    try:
        total_input = usage_dict.get("input_tokens", 0)
        cached_input = usage_dict.get("cached_input_tokens", 0)
        output_tokens = usage_dict.get("output_tokens", 0)

        standard_input = max(0, total_input - cached_input)
        cost = (
            (standard_input * INPUT_TOKEN_PRICE) +
            (cached_input * CACHED_INPUT_TOKEN_PRICE) +
            (output_tokens * OUTPUT_TOKEN_PRICE)
        )
        return float(cost)
    except (KeyError, TypeError, ValueError):
        return 0.0

def get_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def run_limited_task(prompt: str, unknown_args: list) -> bool:
    monitor = SessionMonitor()
    start_time = get_timestamp()
    cmd = ["codex", "exec"] + unknown_args + ["--", prompt]
    cmd_str = " ".join(cmd)
    cmd_str = "\n".join(cmd_str.splitlines()[:5] + (["..."] if len(cmd_str.splitlines()) > 5 else []))
    print(f"Running command: {cmd_str}")
    current_cost = 0.0
    try:
        with subprocess.Popen(
            cmd, 
            stdout=sys.stdout, 
            stderr=subprocess.PIPE, 
            text=True, 
            bufsize=1
        ) as proc:
            
            for line in proc.stderr:
                print(line, end="", flush=True)
                # 1. Update metadata from session file
                monitor.update()
                
                # 2. Check Budget
                tmp_cost = compute_cost(monitor.tokens)
                if tmp_cost != current_cost:
                    print(f"\nUpdated Cost: ${tmp_cost:.4f}.")
                    current_cost = tmp_cost
                if current_cost >= MAX_BUDGET_USD:
                    print(f"\n[!] KILL: Budget exceeded (${current_cost:.4f} > ${MAX_BUDGET_USD}).")
                    proc.terminate()
                    _finalize_output("budget_exceeded", monitor.tokens, monitor.model, start_time, 1)
                    return True

            status = proc.wait()
            # Final sync for last tokens
            monitor.update()
            
            reason = "success" if status == 0 else "error"
            _finalize_output(reason, monitor.tokens, monitor.model, start_time, status)
            return True

    except Exception as e:
        print(f"Execution Error: {e}")
        _finalize_output("execution_error", monitor.tokens, monitor.model, start_time, 1)
        return False

def _finalize_output(reason: str, tokens: dict, model: str, start_time: str, exit_code: int):
    """Prints the final JSON output."""
    result = {
        "finish_reason": reason,
        "finish_time": get_timestamp(),
        "start_time": start_time,
        "cost_usd": compute_cost(tokens),
        "additional": {
            "exit_code": exit_code,
            "tokens": tokens,
            "model": model
        }
    }
    print(json.dumps(result), flush=True)

def main():
    parser = argparse.ArgumentParser(add_help=False)
    _, unknown = parser.parse_known_args()

    prompt = None
    if not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
    elif unknown:
        prompt = unknown.pop()

    if not prompt:
        print("Error: No prompt provided.")
        sys.exit(1)

    success = run_limited_task(prompt, unknown)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()