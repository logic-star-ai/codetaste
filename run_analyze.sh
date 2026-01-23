python -m refactoring_benchmark.scripts.analyze \
    --metric precision_overall \
    --metric precision_added \
    --metric precision_removed \
    --metric f1 \
    --metric ifr \
    --metric ifr_added \
    --metric ifr_removed \
    --metric diff_added_lines \
    --metric diff_removed_lines \
    --metric diff_delta_lines \
    --metric ifr_ratio \
    --metric test_success \
    --metric ifr_x_test_success \
    --metric cost \
    --agent-id "codex-v0.77.0-gpt-5.1-codex-mini" \
    --agent-id "claude-code-v2.0.76-sonnet45" \
    --agent-id "codex-v0.77.0-gpt-5.2" \
    --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    --agent-id "null_agent" \
    --agent-id "golden_agent" \
    --output-dir "./output_abstract" \
    --output-dir "./output_abstract_plan" \
    --output-dir "./output_abstract_multiplan" \
    --output-dir "./output" \
    --output-dir "./output_open" \
    --statistics
    # --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    # --output-dir "./output_abstract" \
    # --output-dir "./output_nano" \
    # --plot-type bar