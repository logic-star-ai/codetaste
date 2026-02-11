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
  ifr_ratio
  precision_overall
  precision_added
  precision_removed
  total_score
)

AGENTS=(
  "codex-v0.77.0-gpt-5.1-codex-mini"
  "claude-code-v2.0.76-sonnet45"
  "codex-v0.77.0-gpt-5.2"
  "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct"
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
    for xlabel_variant in xlabel no_xlabel; do
      local -a legend_args=()
      local -a xlabel_args=()

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

      if [ "$xlabel_variant" == "no_xlabel" ]; then
        xlabel_args+=(--no-xlabel)
      fi

      local plot_dir="plots/${group_name}/${legend_variant}/${xlabel_variant}"
      mkdir -p "$plot_dir"

      python -m refactoring_benchmark.scripts.analyze \
        $(printf ' --metric %q' "${METRICS[@]}") \
        $(printf ' --agent-id %q' "${AGENTS[@]}") \
        $(printf ' --output-dir %q' "${output_dirs[@]}") \
        "${COMMON_ARGS[@]}" \
        "${legend_args[@]}" \
        "${xlabel_args[@]}" \
        --plots-dir "$plot_dir" | tee "$plot_dir/analysis.log"
    done
  done
}

run_group "instructed" "./outputs/instructed/direct"
run_group "open" "./outputs/open/direct" "./outputs/open/plan" "./outputs/open/multiplan"

# Examples for other datasets:
# run_group "standard_cp" "./outputs_legacy/output_cp"
# run_group "abstract_cp" "./outputs_legacy/output_abstract_cp" "./outputs_legacy/output_abstract_plan_cp" "./outputs_legacy/output_abstract_multiplan_cp"
