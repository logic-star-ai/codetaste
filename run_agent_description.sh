#!/bin/bash

# --- CONFIGURATION ---
# To switch agents, simply uncomment the one you want to use
# AGENT_DIR="./agents/codex/gpt51-codex-mini"; AGENT_ID="codex-v0.77.0-gpt-5.1-codex-mini"
AGENT_DIR="./agents/codex/gpt52"; AGENT_ID="codex-v0.77.0-gpt-5.2"
# AGENT_DIR="./agents/qwen-code/qwen3-coder-30b-a3b-instruct"; AGENT_ID="qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct"
# AGENT_DIR="./agents/claude/sonnet45"; AGENT_ID="claude-code-v2.0.76-sonnet45"

# Change this variable to switch task descriptions
DESCRIPTION_TYPE="abstract" # Options: standard, nano, problem, open, abstract

INSTANCES_CSV="./instances.csv"
NR_INSTANCES=20
# Inference
# FORCE_INFERENCE in ["--force", "--force-unsuccessful", ""]; REUSE_PLAN_ON_FORCE in ["--reuse-successful-plan", ""]; PLAN in ["--multiplan", "--plan", ""]
FORCE_INFERENCE=""; REUSE_PLAN_ON_FORCE=""; PLAN="--plan"
# FORCE_INFERENCE=""; REUSE_PLAN_ON_FORCE=""; PLAN=""

# Evaluation
FORCE_EVALUATION="" # Set to "--force" or ""

NR_INFERENCE_WORKERS=20
if [ $AGENT_ID == "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" ]; then
    NR_INFERENCE_WORKERS=5; # local
fi

# --- DYNAMIC OUTPUT DIRECTORY MAPPING ---
case "$DESCRIPTION_TYPE" in
    standard) OUTPUT_DIR="./output" ;;
    nano)     OUTPUT_DIR="./output_nano" ;;
    problem)  OUTPUT_DIR="./output_problem" ;;
    open)     OUTPUT_DIR="./output_open" ;;
    abstract) OUTPUT_DIR="./output_abstract" ;;
    *) echo "Error: Unknown DESCRIPTION_TYPE: $DESCRIPTION_TYPE"; exit 1 ;;
esac

if [ "$PLAN" == "--plan" ]; then
    OUTPUT_DIR="${OUTPUT_DIR}_plan"
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

# 2. Evaluation Step
python -m refactoring_benchmark.scripts.evaluate \
    --instances "$NR_INSTANCES" \
    --nr-workers 5 \
    --agent-id "$AGENT_ID" \
    --output-dir "$OUTPUT_DIR" \
    $FORCE_EVALUATION

echo "Process completed successfully."