#!/usr/bin/env bash
set -euo pipefail

NR_INSTANCES=100
NR_WORKERS=12
INSTANCES_CSV="instances.csv"

OUTPUT_DIRS=(
  "outputs/instructed/direct"
  "outputs/open/direct"
  "outputs/open/plan"
  "outputs/open/multiplan"
)

AGENT_IDS=(
  "golden_agent"
  "null_agent"
  "claude-code-v2.0.76-sonnet45"
  "claude-code-v2.1.71-minimax-m2.7"
  "codex-v0.77.0-gpt-5.1-codex-mini"
  "codex-v0.77.0-gpt-5.2"
  "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct"
)

for output_dir in "${OUTPUT_DIRS[@]}"; do
  if [ ! -d "$output_dir" ]; then
    echo "Skipping missing output directory: $output_dir"
    continue
  fi

  for agent_id in "${AGENT_IDS[@]}"; do
    echo "Evaluating $agent_id in $output_dir with default rules"

    python -m refactoring_benchmark.cli.evaluate \
      --instances "$NR_INSTANCES" \
      --instances-csv "$INSTANCES_CSV" \
      --nr-workers "$NR_WORKERS" \
      --agent-id "$agent_id" \
      --output-dir "$output_dir" \
      --force \
      --skip-tests
  done
done
