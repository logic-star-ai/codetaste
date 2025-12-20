#!/bin/bash
set -e

# --- Configuration ---
REPO_ROOT="/testbed"
AGENT_SCRIPT="/agent/run_agent"
DIFF_INPUT="/input/patch.diff"
DIFF_OUTPUT="/output/prediction.diff"
SARIF_OUTPUT="/output/rules.sarif"
RULES_DIR="/rules"

# Ensure we are in the repo
cd "$REPO_ROOT"

# --- Helper Functions ---

function reset_env() {
    # Run as benchmarker (Privileged)
    echo "-> [Setup] Resetting git state..."
    git reset --hard HEAD > /dev/null 2>&1
    git clean -xdf > /dev/null 2>&1

    echo "-> [Setup] Sourcing environment..."
    # Source the environment script created by Claude during bootstrap
    if [ -f "/scripts/setup_env.sh" ]; then
        source /scripts/setup_env.sh
    else
        echo "Error: /scripts/setup_env.sh not found."
        exit 1
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

    # Ensure agent can write to output directory
    if [ -d "/output" ]; then
        sudo chown -R agent_user:agent_user "/output"
    fi

    # Allow agent to execute the mounted agent script
    if [ -d "/agent" ]; then
        sudo chmod -R 755 "/agent"
    fi

    # Ensure agent can read task descriptions
    if [ -d "/task_description" ]; then
        sudo chown -R agent_user:agent_user "/task_description"
        sudo chmod -R 755 "/task_description"
    fi
}

# --- Main Mode Logic ---

case "$1" in
    "inference")
        echo "=== Mode: Inference ==="

        # 1. Privileged Setup (As 'benchmarker')
        block_network
        reset_env       # Revert to clean 'Buggy' commit
        sanitize_git    # Delete the 'Golden' commit artifacts
        create_restricted_user # Prepare user

        if [ ! -f "$AGENT_SCRIPT" ]; then
            echo "Error: Agent script not found at $AGENT_SCRIPT"
            exit 1
        fi

        # 2. Restricted Execution (As 'agent_user')
        echo "=== Dropping Privileges: Switching to 'agent_user' ==="
        chmod +x "$AGENT_SCRIPT"

        # Run agent. -E preserves ENV vars (Conda PATH, API Keys, etc.)
        # agent_user CANNOT sudo, CANNOT access /rules, CANNOT reach GitHub
        if sudo -E -u agent_user "$AGENT_SCRIPT"; then
            echo "=== Agent finished successfully ==="
        else
            echo "=== Agent failed with exit code $? ==="
        fi

        # 3. Harvest Results
        echo "=== Extracting Diff ==="
        # We diff against the sanitized HEAD.
        # Output is owned by agent_user, but we can read it.
        git diff HEAD > "$DIFF_OUTPUT"
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
        sudo opengrep scan --rules "$RULES_DIR" --format sarif --output "$SARIF_OUTPUT" .

        # Fix ownership so the host can read the result
        sudo chown benchmarker:benchmarker "$SARIF_OUTPUT"
        echo "SARIF output saved to $SARIF_OUTPUT"
        ;;

    *)
        echo "Usage: $0 {inference|eval_test|eval_rule}"
        exit 1
        ;;
esac
