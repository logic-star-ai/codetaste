#!/bin/bash
set -e

# --- Configuration ---
REPO_ROOT="/testbed"
AGENT_SCRIPT="/agent/run_agent"
AGENT_SETUP_SCRIPT="/agent/setup_agent.sh"
AGENT_SYSTEM_SETUP_SCRIPT="/agent/setup_system.sh"
DIFF_INPUT="/input/patch.diff"
DIFF_OUTPUT="/output/prediction.diff"
SARIF_OUTPUT="/output/rules.sarif"
SARIF_OUTPUT_POSITIVE="/output/rules_positive.sarif"
SARIF_OUTPUT_NEGATIVE="/output/rules_negative.sarif"
RULES_OUTPUT_POSITIVE="/output/rules_positive.yml"
RULES_OUTPUT_NEGATIVE="/output/rules_negative.yml"
RULES_DIR="/rules"
RULES_POSITIVE="/rules/rules_positive.yml"
RULES_NEGATIVE="/rules/rules_negative.yml"
TASK_DESC_DIR="/task_description"

# Ensure we are in the repo
cd "$REPO_ROOT"

# --- Helper Functions ---

function setup_env() {
    echo "-> [Setup] Running system setup (if needed)..."
    if [ -f "/scripts/setup_system.sh" ]; then
        sudo bash /scripts/setup_system.sh || true
    fi
}

function block_network() {
    echo "-> [Security] Sinkholing GitHub domains..."
    echo "127.0.0.1 github.com"                | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 api.github.com"            | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 raw.githubusercontent.com" | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 gist.github.com"           | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 codeload.github.com"       | sudo tee -a /etc/hosts > /dev/null
    echo "127.0.0.1 www.github.com"            | sudo tee -a /etc/hosts > /dev/null
}

function create_restricted_user() {
    if ! id "agent_user" &>/dev/null; then
        echo "-> [Security] Creating restricted 'agent_user'..."
        sudo useradd -m -s /bin/bash agent_user
    fi

    echo "-> [Security] Transferring repo ownership to agent_user..."
    sudo chown -R agent_user:agent_user "$REPO_ROOT"

    # Set permissions for various directories
    if [ -d "/output" ]; then sudo chmod -R 777 "/output"; fi
    if [ -d "/agent" ]; then sudo chmod -R 755 "/agent"; fi
    if [ -d "/scripts" ]; then sudo chmod -R 755 "/scripts"; fi
    if [ -d "/task_description" ]; then sudo chmod -R 755 "/task_description"; fi
    sudo chmod -R 777 /home/benchmarker
    sudo chmod -R 777 /opt
}


PRE_AGENT_HASH=$(git rev-parse HEAD)
export PYTHONIOENCODING=utf-8
export LC_ALL=C.UTF-8

case "$1" in
    "inference")
        echo "=== Mode: Inference ==="
        setup_env
        block_network
        create_restricted_user
        if [ ! -f "$AGENT_SCRIPT" ]; then
            echo "Error: Agent script not found at $AGENT_SCRIPT"
            exit 1
        fi
        if [ -f "$AGENT_SYSTEM_SETUP_SCRIPT" ]; then
            echo "=== Running Agent System Setup Script ==="
            sudo bash "$AGENT_SYSTEM_SETUP_SCRIPT"
        fi

        # Restricted Execution
        echo "=== Dropping Privileges: Switching to 'agent_user' ==="
        if sudo -E -u agent_user bash -c '
            [ -f /scripts/setup_shell.sh ] && source /scripts/setup_shell.sh || true
            [ -f "$AGENT_SETUP_SCRIPT" ] && source "$AGENT_SETUP_SCRIPT"
            exec "$0" "$@"
        ' "$AGENT_SCRIPT" "$(cat "$TASK_DESC_DIR/description.md")"; then
            echo "=== Agent finished successfully ==="
        else
            echo "=== Agent failed with exit code $? ==="
        fi

        # Harvest Results
        echo "=== Extracting Diff ==="
        sudo chown -R benchmarker:benchmarker "$REPO_ROOT"
        cd "$REPO_ROOT"
        git config --global --add safe.directory "$REPO_ROOT"
        git add -A
        git diff --cached --binary "$PRE_AGENT_HASH" > "$DIFF_OUTPUT"
        
        echo "Diff saved to $DIFF_OUTPUT"
        ;;

    "eval_test")
        echo "=== Mode: Evaluation (Test) ==="
        git reset --hard --recurse-submodules HEAD
        git clean -xdf
        git checkout "$PRE_AGENT_HASH"
        if [ -f "$DIFF_INPUT" ]; then
            echo "Applying patch from $DIFF_INPUT..."
            git apply --allow-binary-replacement --3way "$DIFF_INPUT"
        else
            echo "No diff file found at $DIFF_INPUT"
        fi

        # Run verification using the scripts created during bootstrap
        /scripts/run_tests
        ;;

    "eval_rule")
        echo "=== Mode: Evaluation (Static Analysis) ==="
        git reset --hard --recurse-submodules HEAD
        git clean -xdf
        git checkout "$PRE_AGENT_HASH"
        if [ -f "$DIFF_INPUT" ]; then
            echo "Applying patch from $DIFF_INPUT..."
            git apply --allow-binary-replacement --3way "$DIFF_INPUT"
        else
            echo "No diff file found at $DIFF_INPUT"
        fi

        echo "Running Opengrep with positive rules..."
        sudo chmod -R 755 "$RULES_DIR"

        # Scan with positive rules
        if [ -f "$RULES_POSITIVE" ]; then
            echo "-> Scanning with positive rules: $RULES_POSITIVE"
            opengrep scan --timeout-threshold 0 --timeout 0 --max-memory 0 -f "$RULES_POSITIVE" --sarif-output "$SARIF_OUTPUT_POSITIVE" .
            sudo chown benchmarker:benchmarker "$SARIF_OUTPUT_POSITIVE"
            cat "$RULES_POSITIVE" > "$RULES_OUTPUT_POSITIVE"
            echo "-> Positive SARIF output saved to $SARIF_OUTPUT_POSITIVE"
        else
            echo "-> Warning: Positive rules not found at $RULES_POSITIVE"
        fi

        # Scan with negative rules
        if [ -f "$RULES_NEGATIVE" ]; then
            echo "-> Scanning with negative rules: $RULES_NEGATIVE"
            opengrep scan --timeout-threshold 0 --timeout 0 --max-memory 0 -f "$RULES_NEGATIVE" --sarif-output "$SARIF_OUTPUT_NEGATIVE" .
            sudo chown benchmarker:benchmarker "$SARIF_OUTPUT_NEGATIVE"
            cat "$RULES_NEGATIVE" > "$RULES_OUTPUT_NEGATIVE"
            echo "-> Negative SARIF output saved to $SARIF_OUTPUT_NEGATIVE"
        else
            echo "-> Warning: Negative rules not found at $RULES_NEGATIVE"
        fi

        echo "=== Static analysis complete ==="
        ;;

    *)
        echo "Usage: $0 {inference|eval_test|eval_rule}"
        exit 1
        ;;
esac