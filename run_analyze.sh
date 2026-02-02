LEGEND=""

DIR=plots/standard
if [ "$LEGEND" == "--no-legend" ]; then
    PLOT_DIR="$DIR/no_legend/"
else
    PLOT_DIR="$DIR/legend/"
fi
mkdir -p "$PLOT_DIR"

python -m refactoring_benchmark.scripts.analyze \
    --metric strict_ifr_x_test_success \
    --metric test_success \
    --metric cost \
    --metric ifr \
    --metric ifr_x_test_success \
    --metric ifr_added_x_test_success \
    --metric ifr_removed_x_test_success \
    --metric ifr_added \
    --metric ifr_removed \
    --metric ifr_ratio \
    --metric precision_overall \
    --metric precision_added \
    --metric precision_removed \
    --metric total_score \
    --agent-id "codex-v0.77.0-gpt-5.1-codex-mini" \
    --agent-id "claude-code-v2.0.76-sonnet45" \
    --agent-id "codex-v0.77.0-gpt-5.2" \
    --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    --output-dir "./output" \
    --plot-type bar \
    $LEGEND \
    --statistics \
    --plots-dir "$PLOT_DIR" | tee "$PLOT_DIR/analysis.log"
    # --output-dir "./output_open" \
    # --output-dir "./output" \
    # --agent-id "null_agent" \
    # --agent-id "golden_agent" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --output-dir "./output_abstract" \
    # --output-dir "./output_nano" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --metric f1 \
    # --metric diff_added_lines \
    # --metric diff_removed_lines \
    # --metric diff_delta_lines \
LEGEND=""

DIR=plots/standard
if [ "$LEGEND" == "--no-legend" ]; then
    PLOT_DIR="$DIR/no_legend/"
else
    PLOT_DIR="$DIR/legend/"
fi
mkdir -p "$PLOT_DIR"

python -m refactoring_benchmark.scripts.analyze \
    --metric strict_ifr_x_test_success \
    --metric test_success \
    --metric cost \
    --metric ifr \
    --metric ifr_x_test_success \
    --metric ifr_added_x_test_success \
    --metric ifr_removed_x_test_success \
    --metric ifr_added \
    --metric ifr_removed \
    --metric ifr_ratio \
    --metric precision_overall \
    --metric precision_added \
    --metric precision_removed \
    --metric total_score \
    --agent-id "codex-v0.77.0-gpt-5.1-codex-mini" \
    --agent-id "claude-code-v2.0.76-sonnet45" \
    --agent-id "codex-v0.77.0-gpt-5.2" \
    --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    --output-dir "./output" \
    --plot-type bar \
    --statistics \
    $LEGEND \
    --plots-dir "$PLOT_DIR" | tee "$PLOT_DIR/analysis.log"
    # --output-dir "./output_open" \
    # --output-dir "./output" \
    # --agent-id "null_agent" \
    # --agent-id "golden_agent" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --output-dir "./output_abstract" \
    # --output-dir "./output_nano" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --metric f1 \
    # --metric diff_added_lines \
    # --metric diff_removed_lines \
    # --metric diff_delta_lines \


LEGEND="--no-legend"

DIR=plots/standard
if [ "$LEGEND" == "--no-legend" ]; then
    PLOT_DIR="$DIR/no_legend/"
else
    PLOT_DIR="$DIR/legend/"
fi
mkdir -p "$PLOT_DIR"

python -m refactoring_benchmark.scripts.analyze \
    --metric strict_ifr_x_test_success \
    --metric test_success \
    --metric cost \
    --metric ifr \
    --metric ifr_x_test_success \
    --metric ifr_added_x_test_success \
    --metric ifr_removed_x_test_success \
    --metric ifr_added \
    --metric ifr_removed \
    --metric ifr_ratio \
    --metric precision_overall \
    --metric precision_added \
    --metric precision_removed \
    --metric total_score \
    --agent-id "codex-v0.77.0-gpt-5.1-codex-mini" \
    --agent-id "claude-code-v2.0.76-sonnet45" \
    --agent-id "codex-v0.77.0-gpt-5.2" \
    --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    --output-dir "./output" \
    --plot-type bar \
    --statistics \
    $LEGEND \
    --plots-dir "$PLOT_DIR" | tee "$PLOT_DIR/analysis.log"
    # --output-dir "./output_open" \
    # --output-dir "./output" \
    # --agent-id "null_agent" \
    # --agent-id "golden_agent" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --output-dir "./output_abstract" \
    # --output-dir "./output_nano" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --metric f1 \
    # --metric diff_added_lines \
    # --metric diff_removed_lines \
    # --metric diff_delta_lines \


LEGEND=""

DIR=plots/abstract
if [ "$LEGEND" == "--no-legend" ]; then
    PLOT_DIR="$DIR/no_legend/"
else
    PLOT_DIR="$DIR/legend/"
fi
mkdir -p "$PLOT_DIR"

python -m refactoring_benchmark.scripts.analyze \
    --metric strict_ifr_x_test_success \
    --metric test_success \
    --metric cost \
    --metric ifr \
    --metric ifr_x_test_success \
    --metric ifr_added_x_test_success \
    --metric ifr_removed_x_test_success \
    --metric ifr_added \
    --metric ifr_removed \
    --metric ifr_ratio \
    --metric precision_overall \
    --metric precision_added \
    --metric precision_removed \
    --metric total_score \
    --agent-id "codex-v0.77.0-gpt-5.1-codex-mini" \
    --agent-id "claude-code-v2.0.76-sonnet45" \
    --agent-id "codex-v0.77.0-gpt-5.2" \
    --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    --output-dir "./output_abstract" \
    --output-dir "./output_abstract_plan" \
    --output-dir "./output_abstract_multiplan" \
    --plot-type bar \
    --statistics \
    $LEGEND \
    --plots-dir "$PLOT_DIR" | tee "$PLOT_DIR/analysis.log"
    # --output-dir "./output_open" \
    # --output-dir "./output" \
    # --agent-id "null_agent" \
    # --agent-id "golden_agent" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --output-dir "./output_abstract" \
    # --output-dir "./output_nano" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --metric f1 \
    # --metric diff_added_lines \
    # --metric diff_removed_lines \
    # --metric diff_delta_lines \

LEGEND="--no-legend"

DIR=plots/abstract
if [ "$LEGEND" == "--no-legend" ]; then
    PLOT_DIR="$DIR/no_legend/"
else
    PLOT_DIR="$DIR/legend/"
fi
mkdir -p "$PLOT_DIR"

python -m refactoring_benchmark.scripts.analyze \
    --metric strict_ifr_x_test_success \
    --metric test_success \
    --metric cost \
    --metric ifr \
    --metric ifr_x_test_success \
    --metric ifr_added_x_test_success \
    --metric ifr_removed_x_test_success \
    --metric ifr_added \
    --metric ifr_removed \
    --metric ifr_ratio \
    --metric precision_overall \
    --metric precision_added \
    --metric precision_removed \
    --metric total_score \
    --agent-id "codex-v0.77.0-gpt-5.1-codex-mini" \
    --agent-id "claude-code-v2.0.76-sonnet45" \
    --agent-id "codex-v0.77.0-gpt-5.2" \
    --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    --output-dir "./output_abstract" \
    --output-dir "./output_abstract_plan" \
    --output-dir "./output_abstract_multiplan" \
    --plot-type bar \
    --statistics \
    $LEGEND \
    --plots-dir "$PLOT_DIR" | tee "$PLOT_DIR/analysis.log"
    # --output-dir "./output_open" \
    # --output-dir "./output" \
    # --agent-id "null_agent" \
    # --agent-id "golden_agent" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --output-dir "./output_abstract" \
    # --output-dir "./output_nano" \
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --metric f1 \
    # --metric diff_added_lines \
    # --metric diff_removed_lines \
    # --metric diff_delta_lines \