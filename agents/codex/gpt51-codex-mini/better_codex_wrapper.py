import asyncio
import os
import signal
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional

# --- Configuration ---
MAX_BUDGET_USD = float(os.environ.get("MAX_BUDGET_USD", 11))
INPUT_TOKEN_PRICE = float(os.environ.get("INPUT_TOKEN_PRICE", 1.75 / 1e6))
CACHED_INPUT_TOKEN_PRICE = float(os.environ.get("CACHED_INPUT_TOKEN_PRICE", 0.175 / 1e6))
OUTPUT_TOKEN_PRICE = float(os.environ.get("OUTPUT_TOKEN_PRICE", 14.0 / 1e6))
TIMEOUT_SEC = float(os.environ.get("TIMEOUT_SEC", 4800))  # 80 minutes
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
            all_jsonl_files = list(SESSIONS_DIR.rglob("*.jsonl"))
            if not all_jsonl_files:
                return
            latest_file = max(all_jsonl_files, key=lambda p: p.stat().st_mtime)
            if self.jsonl_path != latest_file:
                print(f"Monitoring session: {latest_file.name}")
                self.jsonl_path = latest_file
                self.last_pos = 0
        except Exception:
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

                        if msg_type == "turn_context":
                            self.model = payload.get("model", self.model)
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

async def run_limited_task_async(prompt: str, unknown_args: list) -> bool:
    monitor = SessionMonitor()
    start_time_dt = datetime.now(timezone.utc)
    last_read_dt = datetime.now(timezone.utc)
    start_time_str = start_time_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Execute codex directly without the shell 'timeout' command
    cmd = ["codex", "exec"] + unknown_args + ["--", prompt]
    print(f"Starting task: {' '.join(cmd[:10])}...")

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=sys.stdout.fileno(),
        stderr=asyncio.subprocess.PIPE,
        start_new_session=True,
        limit=2*1024*1024,
    )
    additional_info = {}
    reason = "success"
    current_cost = 0.0

    try:
        # Loop as long as the process is running
        while proc.returncode is None:
            # 1. Check Clock
            elapsed = (datetime.now(timezone.utc) - start_time_dt).total_seconds()
            if elapsed > TIMEOUT_SEC:
                print(f"\n[!] KILL: Time limit reached ({elapsed:.0f}s).")
                proc.terminate()
                reason = "timeout"
                break
            
            elapsed_since_last_read = (datetime.now(timezone.utc) - last_read_dt).total_seconds()
            if elapsed_since_last_read > 20 * 60:
                print(f"\n[!] No progress in 20min ({elapsed_since_last_read:.0f}s). Timeout.")
                proc.terminate()
                reason = "timeout"
                break

            # 2. Check Budget
            monitor.update()
            tmp_cost = compute_cost(monitor.tokens)
            if tmp_cost != current_cost:
                print(f"Cost: ${tmp_cost:.4f} ({get_timestamp()})")
                current_cost = tmp_cost
            
            if current_cost >= MAX_BUDGET_USD:
                print(f"\n[!] KILL: Budget exceeded (${current_cost:.4f}).")
                proc.terminate()
                reason = "budget_exceeded"
                break

            # 3. Read Stderr (Non-blocking)
            try:
                chunk_task = asyncio.create_task(proc.stderr.read(4096))
                chunk = await asyncio.wait_for(chunk_task, timeout=0.2)
                
                if chunk:
                    sys.stderr.buffer.write(chunk)
                    sys.stderr.buffer.flush()
                    last_read_dt = datetime.now(timezone.utc)
                elif proc.stderr.at_eof():
                    break
            except asyncio.TimeoutError:
                continue

        # Wait for the process to actually exit after termination or completion
        try:
            exit_code = await asyncio.wait_for(proc.wait(), timeout=5.0)
        except asyncio.TimeoutError:
            print("[!] Process unresponsive. Sending SIGKILL to group.")
            try:
                pgid = os.getpgid(proc.pid)
                os.killpg(pgid, signal.SIGKILL)
            except Exception:
                proc.kill()

            try:
                # communicate() is the best way to drain the pipe
                _, stderr_data = await asyncio.wait_for(proc.communicate(), timeout=5.0)
                if stderr_data:
                    remaining_text = stderr_data.decode(errors="replace").strip()
                    print(f"Remaining Output: {remaining_text}", file=sys.stderr, flush=True)
                exit_code = proc.returncode
            except asyncio.TimeoutError:
                print("[!] Pipes stayed open (orphaned children?). Moving on.")
                exit_code = -1

        if reason == "success" and exit_code != 0:
            reason = "error"

    except Exception as e:
        print(f"Execution Error: {e}")
        reason = "execution_error"
        additional_info["exception"] = str(e)
        exit_code = 1

    _finalize_output(reason, monitor.tokens, monitor.model, start_time_str, exit_code, last_read_dt, additional_info)
    return True

def _finalize_output(reason: str, tokens: dict, model: str, start_time: str, exit_code: int, last_read_dt: datetime, additional_info: Dict[str, str] = {}) -> None:
    result = {
        "finish_reason": reason,
        "finish_time": get_timestamp(),
        "start_time": start_time,
        "cost_usd": compute_cost(tokens),
        "additional": {
            "exit_code": exit_code,
            "tokens": tokens,
            "model": model,
            "seconds_since_last_read": (datetime.now(timezone.utc) - last_read_dt).total_seconds(),
            **additional_info
        }
    }
    print("\n--- FINAL RESULT ---")
    print()
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

    try:
        asyncio.run(run_limited_task_async(prompt, unknown))
    except KeyboardInterrupt:
        sys.exit(130)
    sys.exit(0)

if __name__ == "__main__":
    main()