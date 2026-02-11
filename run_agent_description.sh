#!/bin/bash

# --- CONFIGURATION ---
# To switch agents, simply uncomment the one you want to use
# AGENT_DIR="./agents/codex/gpt51-codex-mini"; AGENT_ID="codex-v0.77.0-gpt-5.1-codex-mini"
# AGENT_DIR="./agents/codex/gpt52"; AGENT_ID="codex-v0.77.0-gpt-5.2"
AGENT_DIR="./agents/qwen-code/qwen3-coder-30b-a3b-instruct"; AGENT_ID="qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct"
# AGENT_DIR="./agents/claude/sonnet45"; AGENT_ID="claude-code-v2.0.76-sonnet45"

# Change this variable to switch task descriptions
DESCRIPTION_TYPE="open" # Options: instructed, open

INSTANCES_CSV="./instances.csv"
NR_INSTANCES=125
# Inference
# FORCE_INFERENCE in ["--force", "--force-unsuccessful", ""]; REUSE_PLAN_ON_FORCE in ["--reuse-successful-plan", ""]; PLAN in ["--multiplan", "--plan", ""]
FORCE_INFERENCE="--force-unsuccessful"; REUSE_PLAN_ON_FORCE=""; PLAN="--plan"
# FORCE_INFERENCE="--force-unsuccessful"; REUSE_PLAN_ON_FORCE=""; PLAN="--plan"
# FORCE_INFERENCE=""; REUSE_PLAN_ON_FORCE=""; PLAN=""

# Evaluation
FORCE_EVALUATION="" # Set to "--force" or ""

NR_INFERENCE_WORKERS=8
if [ $AGENT_ID == "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" ]; then
    NR_INFERENCE_WORKERS=4; # local
fi

# --- DYNAMIC OUTPUT DIRECTORY MAPPING ---
case "$DESCRIPTION_TYPE" in
    instructed) OUTPUT_DIR="./outputs/instructed/direct" ;;
    open) OUTPUT_DIR="./outputs/open/direct" ;;
    *) echo "Error: Unknown DESCRIPTION_TYPE: $DESCRIPTION_TYPE"; exit 1 ;;
esac

if [ "$PLAN" == "--plan" ]; then
    OUTPUT_DIR="${OUTPUT_DIR%/direct}/plan"
fi
if [ "$PLAN" == "--multiplan" ]; then
    OUTPUT_DIR="${OUTPUT_DIR%/direct}/multiplan"
fi

echo "Running benchmark for Agent: $AGENT_ID"
echo "Task Type: $DESCRIPTION_TYPE -> Output: $OUTPUT_DIR"

# --- EXECUTION ---

# 1. Inference Step
# Note: Ensure your environment variables (ANTHROPIC_API_KEY, etc.) are exported in your shell
python -m refactoring_benchmark.scripts.inference \
    --instances "$NR_INSTANCES" \
    --nr-workers "$NR_INFERENCE_WORKERS" \
    --agent-dir "$AGENT_DIR" \
    --env ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY" \
    --env OPENAI_API_KEY="$OPENAI_API_KEY" \
    --env OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
    --description-type "$DESCRIPTION_TYPE" \
    --instances-csv "$INSTANCES_CSV" \
    $PLAN \
    $REUSE_PLAN_ON_FORCE \
    $FORCE_INFERENCE

if [ $? -ne 0 ]; then
    echo "Inference step failed. Skipping evaluation."
else 
    echo "Inference step completed successfully."
    python -m refactoring_benchmark.scripts.evaluate \
        --instances "$NR_INSTANCES" \
        --nr-workers 5 \
        --agent-id "$AGENT_ID" \
        --output-dir "$OUTPUT_DIR" \
        $FORCE_EVALUATION
    python -m refactoring_benchmark.scripts.evaluate \
        --instances "$NR_INSTANCES" \
        --nr-workers 5 \
        --agent-id "$AGENT_ID" \
        --output-dir "$OUTPUT_DIR" \
        --retry-null-tests
    python -m refactoring_benchmark.scripts.evaluate \
        --instances "$NR_INSTANCES" \
        --nr-workers 5 \
        --agent-id "$AGENT_ID" \
        --output-dir "$OUTPUT_DIR" \
        --retry-null-tests
    echo "Process completed successfully."
fi
