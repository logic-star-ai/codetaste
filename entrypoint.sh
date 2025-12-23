#!/bin/bash
set -e

# --- Configuration ---
REPO_ROOT="/testbed"
AGENT_SCRIPT="/agent/run_agent"
DIFF_INPUT="/input/patch.diff"
DIFF_OUTPUT="/output/prediction.diff"
SARIF_OUTPUT="/output/rules.sarif"
RULES_DIR="/rules"
TASK_DESC_DIR="/task_description"

# Ensure we are in the repo
cd "$REPO_ROOT"

# --- Helper Functions ---

function reset_env() {
    # Run as benchmarker (Privileged)
    echo "-> [Setup] Resetting git state..."
    git reset --hard HEAD > /dev/null 2>&1
    git clean -xdf > /dev/null 2>&1

    echo "-> [Setup] Running system setup (if needed)..."
    if [ -f "/scripts/setup_system.sh" ]; then
        sudo bash /scripts/setup_system.sh || true
    fi

    echo "-> [Setup] Sourcing shell environment..."
    # Source the shell environment script created by Claude during bootstrap
    if [ -f "/scripts/setup_shell.sh" ]; then
        source /scripts/setup_shell.sh || true
    else
        echo "Error: /scripts/setup_shell.sh not found."
    fi
}

function block_network() {
    echo "-> [Security] Sinkholing GitHub domains..."
    # Redirect GitHub to localhost to prevent fetching external code/solutions
    echo "127.0.0.1 github.com"                | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 api.github.com"            | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 raw.githubusercontent.com" | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 gist.github.com"           | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 codeload.github.com"       | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 www.github.com"            | sudo tee -a /etc/hosts > /dev/null
}

function sanitize_git() {
    echo "-> [Security] Sanitizing Git History (Deleting the Future)..."

    # 1. Remove remote to prevent fetching
    if git remote | grep -q origin; then
        git remote remove origin
    fi

    # 2. Kill references to the Golden commit
    rm -f .git/FETCH_HEAD

    # 3. Expire reflogs (removes "undo" history that might point to Golden)
    git reflog expire --expire=now --all

    # 4. Prune unreachable objects (The Golden Commit itself)
    # This physically removes the commit object from disk
    git gc --prune=now --aggressive > /dev/null 2>&1 || true

    echo "-> [Security] Git history scrubbed. Only HEAD (Buggy) remains."
}

function create_restricted_user() {
    if ! id "agent_user" &>/dev/null; then
        echo "-> [Security] Creating restricted 'agent_user'..."
        sudo useradd -m -s /bin/bash agent_user
    fi

    # Grant agent_user FULL rights to the repo (they need to edit code)
    echo "-> [Security] Transferring repo ownership to agent_user..."
    sudo chown -R agent_user:agent_user "$REPO_ROOT"

    # Ensure agent can write to output directory (and benchmarker can write diff later)
    if [ -d "/output" ]; then
        sudo chmod -R 777 "/output"
    fi

    # Allow agent to execute the mounted agent script
    if [ -d "/agent" ]; then
        sudo chmod -R 755 "/agent"
    fi

    if [ -d "/scripts" ]; then
        sudo chmod -R 755 "/scripts"
    fi

    # Ensure agent can read task descriptions
    if [ -d "/task_description" ]; then
        sudo chown -R agent_user:agent_user "/task_description"
        sudo chmod -R 755 "/task_description"
    fi

    echo "-> [Security] Setting permissions ..."
    sudo chmod -R 777 /home/benchmarker 
    sudo chmod -R 777 /opt
}

# --- Main Mode Logic ---

case "$1" in
    "inference")
        echo "=== Mode: Inference ==="

        # 1. Privileged Setup (As 'benchmarker')
        block_network
        reset_env       # Revert to clean 'Buggy' commit
        sanitize_git    # Delete the 'Golden' commit artifacts

        PRE_AGENT_HASH=$(git rev-parse HEAD)

        create_restricted_user # Prepare user

        if [ ! -f "$AGENT_SCRIPT" ]; then
            echo "Error: Agent script not found at $AGENT_SCRIPT"
            exit 1
        fi

        # 2. Restricted Execution (As 'agent_user')
        echo "=== Dropping Privileges: Switching to 'agent_user' ==="

        # Run agent. -E preserves ENV vars (Conda PATH, API Keys, etc.)
        # agent_user CANNOT sudo, CANNOT access /rules, CANNOT reach GitHub
        if sudo -E -u agent_user bash -c '
            [ -f /scripts/setup_shell.sh ] && source /scripts/setup_shell.sh || true
            exec "$0" "$@"
        ' "$AGENT_SCRIPT" "$(cat "$TASK_DESC_DIR/description.md")"; then
            echo "=== Agent finished successfully ==="
        else
            echo "=== Agent failed with exit code $? ==="
        fi

        # 3. Harvest Results
        echo "=== Extracting Diff ==="
        # Transfer ownership back to benchmarker to allow git operations
        sudo chown -R benchmarker:benchmarker "$REPO_ROOT"
        # Save the diff between pre- and post-agent run
        cd "$REPO_ROOT"
        git config --global --add safe.directory "$REPO_ROOT"
        git add -A
        git diff "$PRE_AGENT_HASH" > "$DIFF_OUTPUT"
        echo "Diff saved to $DIFF_OUTPUT"
        ;;

    "eval_test")
        echo "=== Mode: Evaluation (Test) ==="
        reset_env

        if [ -f "$DIFF_INPUT" ]; then
            echo "Applying patch from $DIFF_INPUT..."
            git apply "$DIFF_INPUT" --allow-empty
        fi

        # Run verification using the scripts created during bootstrap
        /scripts/run_tests
        ;;

    "eval_rule")
        echo "=== Mode: Evaluation (Static Analysis) ==="
        reset_env

        if [ -f "$DIFF_INPUT" ]; then
            echo "Applying patch from $DIFF_INPUT..."
            git apply "$DIFF_INPUT" --allow-empty
        fi

        echo "Running Opengrep..."
        # Uses sudo to read the locked /rules directory (root:root 700)
        opengrep scan --rules "$RULES_DIR" --format sarif --output "$SARIF_OUTPUT" .

        # Fix ownership so the host can read the result
        sudo chown benchmarker:benchmarker "$SARIF_OUTPUT"
        echo "SARIF output saved to $SARIF_OUTPUT"
        ;;

    *)
        echo "Usage: $0 {inference|eval_test|eval_rule}"
        exit 1
        ;;
esac
