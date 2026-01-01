#!/bin/bash
set -e

START_TIME=$(date +%s)
cd /testbed

echo "=== Example Refactoring Agent ==="
echo "Task description:"
cat /task_description/README.md 2>/dev/null || echo "No task description found"

# Example: Just create a simple change for demonstration
echo "// Refactored by example agent" >> README.md

# That's it! No need to:
# - Generate prediction.diff (entrypoint.sh does this automatically)
# - Create agent_metadata.json (use static agent_config.json instead)

# Optional: Track runtime metrics if you want
END_TIME=$(date +%s)
EXECUTION_TIME=$((END_TIME - START_TIME))

cat > /output/run_metrics.json <<EOF
{
  "execution_time_seconds": ${EXECUTION_TIME},
  "total_input_tokens": 0,
  "total_output_tokens": 0
}
EOF

echo "=== Agent Complete ==="
echo "Changes made to codebase - system will capture diff automatically"
