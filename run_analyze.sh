#!/usr/bin/env bash
set -euo pipefail

METRICS=(
  strict_ifr_x_test_success
  test_success
  cost
  ifr
  ifr_x_test_success
  ifr_added_x_test_success
  ifr_removed_x_test_success
  ifr_added
  ifr_removed
  precision_overall
  precision_added
  precision_removed
  f1_score
)

AGENTS_DEFAULT=(
  "codex-v0.77.0-gpt-5.1-codex-mini"
  "claude-code-v2.0.76-sonnet45"
  "codex-v0.77.0-gpt-5.2"
  "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct"
)

AGENTS_COMBINED=(
  "${AGENTS_DEFAULT[@]}"
  "golden_agent"
  "null_agent"
)

COMMON_ARGS=(
  --plot-type bar
  --statistics
)

run_group() {
  local group_name=$1
  shift
  local -a output_dirs=("$@")

  for legend_variant in no_legend legend_upper_left legend_upper_right legend_lower_left; do
    local -a legend_args=()

    case "$legend_variant" in
      no_legend)
        legend_args+=(--no-legend)
        ;;
      legend_upper_left)
        legend_args+=(--legend-position upper_left)
        ;;
      legend_upper_right)
        legend_args+=(--legend-position upper_right)
        ;;
      legend_lower_left)
        legend_args+=(--legend-position lower_left)
        ;;
    esac

    local plot_dir="plots/${group_name}/${legend_variant}"
    mkdir -p "$plot_dir"

    python -m refactoring_benchmark.cli.analyze \
      $(printf ' --metric %q' "${METRICS[@]}") \
      $(printf ' --agent-id %q' "${AGENTS[@]}") \
      $(printf ' --output-dir %q' "${output_dirs[@]}") \
      $( [ "$group_name" == "instructed" ] && echo "--ytick-step 10" ) \
      "${COMMON_ARGS[@]}" \
      "${legend_args[@]}" \
      --plots-dir "$plot_dir" | tee "$plot_dir/analysis.log"
  done
}

AGENTS=("${AGENTS_DEFAULT[@]}")
run_group "instructed" "./outputs/instructed/direct"
run_group "open" "./outputs/open/direct" "./outputs/open/plan" "./outputs/open/multiplan"
AGENTS=("${AGENTS_COMBINED[@]}")
run_group "combined" "./outputs/instructed/direct" "./outputs/open/direct" "./outputs/open/plan" "./outputs/open/multiplan"
