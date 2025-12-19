import docker
from docker.models.containers import Container as DockerContainer
import csv
import json
import os
import sys
import logging
from utils.prompts import SETUP_PROMPT_PYTHON

# --- CONFIGURATION ---
CSV_FILE = "instances.csv"
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
LOG_DIR = "logs"

# --- LOGGER SETUP ---
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging to write to agent_runtime.log
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "agent_runtime.log"),
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger("agent_logger")

# --- PODMAN / DOCKER CONNECTION ---
try:
    # This automatically picks up DOCKER_HOST if set for Podman
    client = docker.from_env()
    client.ping()
except Exception as e:
    print(f"Error: Could not connect to Docker/Podman: {e}")
    print("Run: export DOCKER_HOST=unix:///run/user/$(id -u)/podman/podman.sock")
    sys.exit(1)

def stream_exec(container, cmd, env=None):
    full_output = []
    print(f"DEBUG: Starting exec of {cmd[0]}...")
    
    exec_instance = container.exec_run(
        cmd=cmd,
        environment=env or {},
        stream=True,
        tty=True,
        demux=False # Ensure we get a single stream
    )

    # Use a timeout-based approach to see if we are stuck
    try:
        acc = ""
        for chunk in exec_instance.output:
            if chunk:
                decoded = chunk.decode('utf-8', errors='replace')
                acc += decoded
                try:
                    json_obj = json.loads(acc)
                    pretty_json = json.dumps(json_obj, indent=2)
                    
                    # LOGGED TO FILE INSTEAD OF PRINTED
                    logger.info(f"JSON Output:\n{pretty_json}")
                    
                    full_output.append(decoded)
                    acc = ""
                except json.JSONDecodeError:
                    pass
    except Exception as e:
        print(f"\nStream Error: {e}")
    
    return "".join(full_output)

def bootstrap_instance(row):
    owner, repo = row['owner'], row['repo']
    golden_hash = row['golden_commit_hash']
    buggy_hash = row['commit_hash']
    lang = row['language']
    
    tag_name = f"benchmark/{owner}-{repo}:{buggy_hash[:8]}"
    print(f"\n{'='*60}")
    print(f"🚀 BOOTSTRAPPING: {owner}/{repo}")
    print(f"{'='*60}\n")

    # 1. Start Container
    base_img = f"benchmark-base-{lang}" 
    try:
        container: DockerContainer = client.containers.run(
            base_img, 
            detach=True, 
            environment={"ANTHROPIC_API_KEY": API_KEY},
            working_dir="/testbed"
        )
    except Exception as e:
        print(f"❌ Skipping {repo}: Base image {base_img} not found or error: {e}")
        return

    try:
        # 2. CLONE & CHECKOUT GOLDEN
        print(f"-> Shallow Cloning of {repo}...")
        url = f"https://github.com/{owner}/{repo}.git"
        container.exec_run("git init .")
        container.exec_run(f"git remote add origin {url}")
        container.exec_run(f"git fetch --depth 2 origin {golden_hash}")
        container.exec_run(f"git checkout {golden_hash}")

        # 3. RUN CLAUDE AGENT TO SETUP ENVIRONMENT
        prompt = SETUP_PROMPT_PYTHON if lang.lower() == "python" else ""
        
        print("-> Claude Agent is taking control...")
        agent_env = {"ANTHROPIC_API_KEY": API_KEY}
        agent_cmd = ["claude", "-p", prompt, "--dangerously-skip-permissions", "--verbose", "--output-format", "stream-json"]
        
        raw_log = stream_exec(container, agent_cmd, env=agent_env)
        
        with open(f"{LOG_DIR}/setup_{repo}.log", "w") as f:
            f.write(raw_log)

        # 4. CAPTURE GOLDEN METRICS
        print("\n-> Verifying Golden Metrics...")
        container.exec_run("git reset --hard HEAD && git clean -fd")
        container.exec_run(f"git checkout {golden_hash}")
        res = container.exec_run("/scripts/run_tests")
        output_lines = res.output.decode().strip().split('\n')
        try:
            golden_metrics = json.loads(output_lines[-1])
            print(f"✅ Golden Metrics: {golden_metrics}")
        except (json.JSONDecodeError, IndexError):
            print("❌ Failed to parse Golden Metrics. Agent likely failed setup.")
            return

        # 5. SWITCH TO BUGGY (Regression)
        print(f"-> Regressing to Buggy Commit: {buggy_hash}")
        container.exec_run("git reset --hard HEAD && git clean -fd")
        container.exec_run(f"git checkout {buggy_hash}")
        
        # 6. CAPTURE START METRICS (Baseline)
        res = container.exec_run("/scripts/run_tests")
        try:
            output_lines = res.output.decode().strip().split('\n')
            start_metrics = json.loads(output_lines[-1])
        except:
            start_metrics = {"passed": 0, "failed": -1, "total": 0, "error": "Crashed"}
        
        print(f"📉 Start Metrics (Buggy): {start_metrics}")

        # 7. SAVE METADATA
        meta = {
            "owner": owner, "repo": repo,
            "golden_metrics": golden_metrics,
            "start_metrics": start_metrics,
            "hashes": {"golden": golden_hash, "buggy": buggy_hash}
        }
        
        # Write metadata to the container for future reference
        meta_json = json.dumps(meta).replace("'", "'\\''")
        container.exec_run(f"bash -c 'echo \"{meta_json}\" > /home/benchmarker/benchmark_meta.json'")

        # 8. COMMIT (Freeze Image)
        repo_part = f"localhost/benchmark/{owner}-{repo}"
        tag_part = buggy_hash[:8]
        try:
            container.commit(repository=repo_part, tag=tag_part)
            print(f"✨ SUCCESS: Created {repo_part}:{tag_part}")
        except Exception as e:
            print(f"❌ Commit Failed: {e}")

    except Exception as e:
        print(f"💥 CRITICAL FAILURE for {repo}: {e}")
    finally:
        print(f"-> Cleaning up container...")
        try:
            container.stop(timeout=1)
            container.remove(force=True)
        except Exception as net_err:
            if "permission denied" in str(net_err):
                print("-> Container removed (swallowed Podman netns warning).")
            else:
                print(f"-> Cleanup warning: {net_err}")

def main():
    if not os.path.exists(LOG_DIR): 
        os.makedirs(LOG_DIR)
        
    if not API_KEY:
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        sys.exit(1)

    with open(CSV_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bootstrap_instance(row)

if __name__ == "__main__":
    main()