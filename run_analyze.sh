python -m refactoring_benchmark.scripts.analyze \
    --metric precision_overall \
    --metric f1 \
    --metric ifr \
    --metric ifr_added \
    --metric ifr_removed \
    --metric test_success \
    --metric ifr_x_test_success \
    --metric cost \
    --agent-id "codex-v0.77.0-gpt-5.2" \
    --agent-id "codex-v0.77.0-gpt-5.1-codex-mini" \
    --agent-id "qwen-code-v0.6.2-qwen3-coder-30b-a3b-instruct" \
    --agent-id "claude-code-v2.0.76-sonnet45" \
    --statistics \
    # --plot-type bar