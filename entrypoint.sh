#!/bin/bash
set -e

# --- Configuration ---
REPO_ROOT="/testbed"
AGENT_SCRIPT="/agent/run_agent"
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
function preserve_env() {
    echo "-> [Security] Applying Sudo Environment Fix (Disabling secure_path/env_reset)..."
    # We use tee to create a new sudoers override file
    echo 'Defaults !env_reset' | sudo tee /etc/sudoers.d/testbed_env > /dev/null
    echo 'Defaults !secure_path' | sudo tee -a /etc/sudoers.d/testbed_env > /dev/null
    # Explicitly keep critical variables to handle edge-case sudo configurations
    echo 'Defaults env_keep += "PATH VIRTUAL_ENV PYTHONPATH NODE_PATH NVM_DIR NVM_BIN"' | sudo tee -a /etc/sudoers.d/testbed_env > /dev/null
    sudo chmod 0440 /etc/sudoers.d/testbed_env
}

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

function revoke_sudo() {
    echo "-> [Security] Revoking sudo access for benchmarker..."
    # Secure the rules directory so the agent cannot read it
    sudo chown -R root:root /rules
    sudo chmod -R 700 /rules
    # Remove the sudo privilege line added in the Dockerfile
    sudo sed -i '/benchmarker ALL=(ALL) NOPASSWD:ALL/d' /etc/sudoers
    # Clear any cached sudo credentials
    sudo -k
}

preserve_env

# Permissions
if [ -d "/output" ]; then sudo chmod -R 777 "/output"; fi
if [ -d "/agent" ]; then sudo chmod -R 755 "/agent"; fi
if [ -d "/scripts" ]; then sudo chmod -R 755 "/scripts"; fi
if [ -d "/task_description" ]; then sudo chmod -R 755 "/task_description"; fi
sudo chmod -R 700 /rules

# basic setup
PRE_AGENT_HASH=$(git rev-parse HEAD)
export PYTHONIOENCODING=utf-8
export LC_ALL=C.UTF-8
setup_env

case "$1" in
    "inference")
        echo "=== Mode: Inference ==="
        if [ ! -f "$AGENT_SCRIPT" ]; then
            echo "Error: Agent script not found at $AGENT_SCRIPT"
            exit 1
        fi

        if [ ! -f "$TASK_DESC_DIR/description.md" ]; then
            echo "Error: Task description directory not found at $TASK_DESC_DIR"
            exit 1
        fi

        # Agent System Setup Script Can Still Use Github via sudo
        if [ -f "$AGENT_SYSTEM_SETUP_SCRIPT" ]; then
            echo "=== Running Agent System Setup Script ==="
            sudo bash "$AGENT_SYSTEM_SETUP_SCRIPT"
        fi
        
        block_network
        revoke_sudo
        
        # Restricted Execution (Runs as benchmarker, no sudo available)
        if bash -c "
            [ -f /scripts/setup_shell.sh ] && source /scripts/setup_shell.sh
            bash \"$AGENT_SCRIPT\"
        "; then
            echo "=== Agent finished successfully ==="
        else
            echo "=== Agent failed with exit code $? ==="
            exit $?
        fi
        
        # Harvest Results
        echo "=== Extracting Diff ==="
        cd "$REPO_ROOT"
        git config --global --add safe.directory "$REPO_ROOT"
        git add -A
        git diff --cached --binary "$PRE_AGENT_HASH" > "$DIFF_OUTPUT"
        
        echo "Diff saved to $DIFF_OUTPUT"
        ;;

    "plan")
        echo "=== Mode: Plan ==="
        if [ ! -f "$AGENT_SCRIPT" ]; then
            echo "Error: Agent script not found at $AGENT_SCRIPT"
            exit 1
        fi

        if [ ! -f "$TASK_DESC_DIR/description.md" ]; then
            echo "Error: Task description directory not found at $TASK_DESC_DIR"
            exit 1
        fi

        # Agent System Setup Script Can Still Use Github
        if [ -f "$AGENT_SYSTEM_SETUP_SCRIPT" ]; then
            echo "=== Running Agent System Setup Script ==="
            sudo bash "$AGENT_SYSTEM_SETUP_SCRIPT"
        fi
        
        block_network
        revoke_sudo
        
        # Restricted Execution
        if bash -c "
            [ -f /scripts/setup_shell.sh ] && source /scripts/setup_shell.sh
            bash \"$AGENT_SCRIPT\"
        "; then
            echo "=== Agent finished successfully ==="
        else
            echo "=== Agent failed with exit code $? ==="
            exit $?
        fi
        
        if [ ! -f "/output/refactoring_plan.md" ]; then
            echo "Error: Agent did not produce a refactoring_plan.md in /output"
            exit 1
        fi
        ;;

    "multiplan")
        echo "=== Mode: Multiplan ==="
        if [ ! -f "$AGENT_SCRIPT" ]; then
            echo "Error: Agent script not found at $AGENT_SCRIPT"
            exit 1
        fi

        if [ ! -f "$TASK_DESC_DIR/description.md" ]; then
            echo "Error: Task description directory not found at $TASK_DESC_DIR"
            exit 1
        fi

        # Agent System Setup Script Can Still Use Github
        if [ -f "$AGENT_SYSTEM_SETUP_SCRIPT" ]; then
            echo "=== Running Agent System Setup Script ==="
            sudo bash "$AGENT_SYSTEM_SETUP_SCRIPT"
        fi
        
        block_network
        revoke_sudo

        # Restricted Execution
        if bash -c "
            [ -f /scripts/setup_shell.sh ] && source /scripts/setup_shell.sh
            bash \"$AGENT_SCRIPT\"
        "; then
            echo "=== Agent finished successfully ==="
        else
            echo "=== Agent failed with exit code $? ==="
            exit $?
        fi
        

        # Validate that plans were generated
        PLANS_DIR="/output/refactoring_plans"
        if [ ! -d "$PLANS_DIR" ]; then
            echo "Error: Agent did not create refactoring_plans directory in /output"
            exit 1
        fi

        # Count plan files
        PLAN_COUNT=$(find "$PLANS_DIR" -maxdepth 1 -name "refactoring_plan*.md" -type f | wc -l)
        if [ "$PLAN_COUNT" -lt 2 ]; then
            echo "Error: Agent produced $PLAN_COUNT plans (need at least 2)"
            exit 1
        fi

        echo "=== Multiplan validation successful: $PLAN_COUNT plans generated ==="
        ;;

    "eval_test")
        echo "=== Mode: Evaluation (Test) ==="
        git reset --hard --recurse-submodules HEAD
        git clean -xdff
        git checkout "$PRE_AGENT_HASH"
        if [ -f "$DIFF_INPUT" ]; then
            echo "Applying patch from $DIFF_INPUT..."
            git apply --allow-empty --allow-binary-replacement --3way "$DIFF_INPUT"
        else
            echo "No diff file found at $DIFF_INPUT"
        fi

        # Copy instance metadata to output
        if [ -f "/rules/instance_metadata.json" ]; then
            cat /rules/instance_metadata.json > /output/instance_metadata.json
            echo "-> Copied instance_metadata.json to output"
        fi

        # Run verification using the scripts created during bootstrap
        setup_env
        source /scripts/setup_shell.sh
        /scripts/run_tests
        ;;

    "eval_rule")
        echo "=== Mode: Evaluation (Static Analysis) ==="
        git reset --hard --recurse-submodules HEAD
        git clean -xdff
        git checkout "$PRE_AGENT_HASH"
        if [ -f "$DIFF_INPUT" ]; then
            echo "Applying patch from $DIFF_INPUT..."
            git apply --allow-empty --allow-binary-replacement --3way "$DIFF_INPUT"
        else
            echo "No diff file found at $DIFF_INPUT"
        fi

        # Copy instance metadata to output
        if [ -f "/rules/instance_metadata.json" ]; then
            cat /rules/instance_metadata.json > /output/instance_metadata.json
            echo "-> Copied instance_metadata.json to output"
        fi

        echo "Running Opengrep with positive rules..."
        sudo chmod -R 755 "$RULES_DIR"

        # Setup default .semgrepignore
        cat /rules/default.semgrepignore > /testbed/.semgrepignore
        echo "-> Applied default .semgrepignore to /testbed"

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
        echo "Usage: $0 {inference|plan|multiplan|eval_test|eval_rule}"
        exit 1
        ;;
esac