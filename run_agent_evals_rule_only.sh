#!/bin/bash

NR_INSTANCES=125
NR_EVAL_WORKERS=12
FORCE_EVALUATION="--force" # Set to "--force" or ""

AGENT_IDS=(
  "codex-v0.77.0-gpt-5.1-codex-mini"
  "codex-v0.77.0-gpt-5.2"
  "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct"
  "claude-code-v2.0.76-sonnet45"
)

RUNS=(
  "instructed:"
  "open:"
  "open:--plan"
  "open:--multiplan"
)

get_output_dir() {
  local description_type="$1"
  local plan_flag="$2"
  local output_dir

  case "$description_type" in
    instructed) output_dir="./outputs/instructed/direct" ;;
    open)       output_dir="./outputs/open/direct" ;;
    *) echo "Error: Unknown DESCRIPTION_TYPE: $description_type"; return 1 ;;
  esac

  if [ "$plan_flag" == "--plan" ]; then
    output_dir="${output_dir%/direct}/plan"
  elif [ "$plan_flag" == "--multiplan" ]; then
    output_dir="${output_dir%/direct}/multiplan"
  fi

  echo "$output_dir"
}

failures=()

for agent_id in "${AGENT_IDS[@]}"; do
  for run in "${RUNS[@]}"; do
    IFS=":" read -r description_type plan_flag <<< "$run"
    output_dir="$(get_output_dir "$description_type" "$plan_flag")" || exit 1

    echo "Evaluating $agent_id | $description_type $plan_flag -> $output_dir"
    if ! python -m refactoring_benchmark.scripts.evaluate \
        --instances "$NR_INSTANCES" \
        --nr-workers "$NR_EVAL_WORKERS" \
        --agent-id "$agent_id" \
        --output-dir "$output_dir" \
        --create-rule-report \
        --skip-tests \
        $FORCE_EVALUATION; then
      failures+=("$agent_id | $description_type $plan_flag")
    fi
  done
done

if [ "${#failures[@]}" -ne 0 ]; then
  echo "Some evaluations failed:"
  for failure in "${failures[@]}"; do
    echo "  - $failure"
  done
  # exit 1
fi

echo "All evaluations completed successfully."
