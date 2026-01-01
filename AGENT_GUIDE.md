# Agent Guide: Running Refactoring Tasks

This guide explains how to create an agent to participate in the refactoring benchmark.

## Overview

Your agent runs inside a containerized environment with:
- The codebase to refactor at `/testbed`
- Task description at `/task_description/README.md`
- Your agent script at `/agent/run_agent`
- Your agent config at `/agent/agent_config.json`
- Output directory at `/output` for results

**The system automatically creates `prediction.diff` from your changes** - your agent just needs to modify the code!

## Required Files

### 1. Agent Configuration (Required)

**File**: `agent/agent_config.json`

A static JSON file describing your agent:

```json
{
  "agent_name": "claude-code-refactorer",
  "agent_version": "1.0.0",
  "model_name": "claude-sonnet-4.5",
  "model_provider": "anthropic",
  "developer": "your-name"
}
```

This file is version-controlled with your agent and doesn't change between runs.

### 2. Agent Script (Required)

**File**: `agent/run_agent`

Your script just needs to make changes to `/testbed`. The system automatically captures the diff.

```bash
#!/bin/bash
cd /testbed

# Read the task
TASK=$(cat /task_description/README.md)

# Make your changes
# ... your refactoring logic ...

# That's it! No need to create diffs or write metadata
```

### 3. Runtime Metrics (Optional)

**File**: `output/run_metrics.json`

Optionally track execution metrics:

```json
{
  "execution_time_seconds": 45.3,
  "total_input_tokens": 12500,
  "total_output_tokens": 3200,
  "total_cost_usd": 0.15
}
```

These get merged with your static config. Only include what you can actually measure!

## Configuration Fields

### In `agent_config.json` (Static)

**Required**:
- `agent_name`: Identifier (e.g., "claude-sonnet-4.5")
- `agent_version`: Version (e.g., "1.0.0")

**Recommended**:
- `model_name`: Model used (e.g., "claude-sonnet-4.5")
- `model_provider`: Provider (e.g., "anthropic", "openai")
- `temperature`: Sampling temperature
- `developer`: Your name/team

**Optional**:
- `prompt_template`: Template identifier
- `custom_config`: Any agent-specific config
- `experiment_id`: For grouping runs

### In `run_metrics.json` (Runtime - Optional)

- `execution_time_seconds`: How long it took
- `total_input_tokens`: Tokens consumed
- `total_output_tokens`: Tokens generated
- `total_cost_usd`: Cost in USD

## Complete Examples

### Minimal Agent (Just Refactor!)

**`agent/agent_config.json`**:
```json
{
  "agent_name": "my-simple-agent",
  "agent_version": "1.0.0",
  "developer": "alex"
}
```

**`agent/run_agent`**:
```bash
#!/bin/bash
cd /testbed

# Just make your changes - that's it!
sed -i 's/old_pattern/new_pattern/g' *.py
```

Done! The system handles everything else.

### Agent with LLM + Metrics Tracking

**`agent/agent_config.json`**:
```json
{
  "agent_name": "claude-code-refactorer",
  "agent_version": "1.0.0",
  "model_name": "claude-sonnet-4.5",
  "model_provider": "anthropic",
  "temperature": 1.0,
  "developer": "alex"
}
```

**`agent/run_agent`**:
```bash
#!/bin/bash
set -e

START_TIME=$(date +%s)
cd /testbed

# Read task and refactor with Claude
TASK=$(cat /task_description/README.md)
claude -p "Refactor: $TASK" > /tmp/log 2>&1

# Optional: Track runtime metrics
END_TIME=$(date +%s)
TOKENS_IN=$(grep "input tokens" /tmp/log | awk '{print $NF}' || echo "0")
TOKENS_OUT=$(grep "output tokens" /tmp/log | awk '{print $NF}' || echo "0")

cat > /output/run_metrics.json <<EOF
{
  "execution_time_seconds": $((END_TIME - START_TIME)),
  "total_input_tokens": ${TOKENS_IN},
  "total_output_tokens": ${TOKENS_OUT}
}
EOF
```

## Evaluation Process

After your agent runs, the benchmark will evaluate your submission:

### 1. Test Evaluation

Your diff is applied and tests are run:
```bash
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    -v $(pwd)/output:/output \
    localhost/benchmark/<instance>:runtime \
    eval_test
```

**Success criteria** depend on setup quality:
- **Both commits valid**: Agent tests must be within bounds `[min(base, golden), max(base, golden)]`
- **One commit valid**: Tests marked as `test_trivial` (weak evaluation)
- **Neither valid**: Tests marked as `test_not_setup` (no evaluation possible)

### 2. Rule Evaluation

Static analysis rules check if your refactoring follows instructions:
```bash
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    -v $(pwd)/output:/output \
    localhost/benchmark/<instance>:runtime \
    eval_rule
```

**Instruction Following Rate (IFR)**:
```
IFR = (positive_rules_matched + negative_rules_avoided) / total_rules
```

### 3. Overall Success

Success depends on test outcome:
- **test_success**: IFR >= 0.80 (clean success)
- **test_trivial**: IFR >= 0.95 (questionable success - flag for review)
- **test_not_setup**: IFR >= 0.95 (questionable success - flag for review)
- **test_fail**: Failure (tests out of bounds)
- **test_error**: Failure (agent crashed)

## Running Your Agent

### Setup

```bash
# 1. Create agent config (once)
mkdir -p agent
cat > agent/agent_config.json <<EOF
{
  "agent_name": "my-agent",
  "agent_version": "1.0.0",
  "model_name": "claude-sonnet-4.5",
  "developer": "your-name"
}
EOF

# 2. Create agent script
cat > agent/run_agent <<'EOF'
#!/bin/bash
cd /testbed
claude -p "$(cat /task_description/README.md)"
EOF
chmod +x agent/run_agent
```

### Local Testing

```bash
# Run on one instance
docker run --rm \
    --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $(pwd)/agent:/agent \
    -v $(pwd)/output:/output \
    localhost/benchmark/<owner>__<repo>-<hash>__runtime \
    inference

# Check what was created
ls -la output/prediction.diff  # Auto-generated from your changes
cat agent/agent_config.json     # Your static config
```

### Batch Evaluation

```bash
# Run on all instances
poetry run python -m refactoring_benchmark.scripts.inference

# Analyze results
poetry run python -m refactoring_benchmark.scripts.analyze_results
```

## Tips for Success

1. **Start with agent_config.json** - Required for attribution and comparison
2. **Track runtime metrics if possible** - Helps with cost-effectiveness analysis
3. **Test locally first** - Verify on one instance before batch runs
4. **Use experiment_id** - Group related runs for easier analysis
5. **Keep it simple** - Your script just needs to make changes, system handles the rest
6. **The system auto-generates prediction.diff** - No need to create it yourself!

## Comparing Multiple Agents

The analysis script will automatically compare agents if multiple are present:

```bash
poetry run python -m refactoring_benchmark.scripts.analyze_results
```

Metrics reported per agent:
- Success rate (overall and by test outcome)
- Average IFR
- Regression rate
- Cost efficiency (cost per success)
- Execution time
