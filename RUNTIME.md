# Runtime Execution Guide

This document explains how to execute the benchmark containers in three different modes: **Inference**, **Test Evaluation**, and **Rule-Based Evaluation**.

## Overview

Each benchmark container includes a runtime router (`entrypoint.sh`) that manages three execution modes:

1. **Inference Mode**: Runs the agent with security restrictions to generate a patch
2. **Test Evaluation Mode**: Applies a patch and runs the test suite
3. **Rule-Based Evaluation Mode**: Applies a patch and runs static analysis with Semgrep/Opengrep

## Architecture

### Build Phase (bootstrap.py)
- Clones repository at buggy commit
- Runs Claude agent to set up environment
- Verifies tests work at both buggy and golden commits
- Saves `/scripts/` directory if criteria met (total >= 10, passed >= 30%)
- Injects `entrypoint.sh` runtime router
- Injects security rules from `rules/{owner}/{repo}/{hash[:8]}/` (locked to root-only access)
- Injects task descriptions from `descriptions/{owner}/{repo}/{hash[:8]}/` (visible to agent)
- Commits container with entrypoint configuration

### Runtime Security Model
During inference, the container enforces:
- **Network Isolation**: GitHub domains redirected to localhost
- **Git Sanitization**: Golden commit physically removed from `.git` database
- **Privilege Separation**: Agent runs as `agent_user` without sudo access
- **Rule Hiding**: Static analysis rules locked to root access only

## Mode 1: Inference

Runs an AI agent to generate a refactoring patch while enforcing security restrictions.

### Input Requirements
- Agent executable script mounted at `/agent/run_agent`
- `ANTHROPIC_API_KEY` environment variable

### Output
- `prediction.diff` - Git diff of all changes made by the agent

### Security Features
- GitHub domains sinkholed to prevent fetching solutions
- Git history sanitized (golden commit removed)
- Runs as restricted `agent_user` (no sudo)
- Cannot access `/rules` directory (evaluation rules hidden)
- Can read `/task_description` directory (task guidance visible)

### Example Usage

```bash
# Basic inference run
docker run --rm \
    --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $(pwd)/my_agent:/agent \
    -v $(pwd)/output:/output \
    localhost/benchmark/ray-project-ray:f781622f \
    inference
```

### Creating an Agent Script

Your agent script at `/agent/run_agent` should:
1. Be executable (`chmod +x`)
2. Make changes to the code in `/testbed`
3. Exit with code 0 on success

Example agent script:
```bash
#!/bin/bash
cd /testbed

# Your agent logic here
# - Analyze code
# - Make refactoring changes
# - Test changes

exit 0
```

## Mode 2: Evaluation (Tests)

Applies a patch and runs the test suite to verify correctness.

### Input Requirements
- Patch file mounted at `/input/patch.diff`

### Output
- JSON test results written to stdout

### Example Usage

```bash
# Run tests on a generated patch
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    localhost/benchmark/ray-project-ray:f781622f \
    eval_test
```

### Output Format

```json
{
  "passed": 42,
  "failed": 0,
  "skipped": 3,
  "total": 45,
  "error": null
}
```

## Mode 3: Evaluation (Static Analysis)

Applies a patch and runs Semgrep/Opengrep rules for quality analysis.

### Input Requirements
- Patch file mounted at `/input/patch.diff`
- Rules pre-installed during build (hidden from agent)

### Output
- `rules.sarif` - SARIF format results

### Example Usage

```bash
# Run static analysis on a generated patch
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    -v $(pwd)/output:/output \
    localhost/benchmark/ray-project-ray:f781622f \
    eval_rule
```

### SARIF Output

The output follows the [SARIF 2.1.0 specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html):

```json
{
  "version": "2.1.0",
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "runs": [{
    "tool": { "driver": { "name": "Semgrep" } },
    "results": [...]
  }]
}
```

## Complete Workflow Example

### 1. Build the benchmark image

```bash
# Set API key for Claude agent
export ANTHROPIC_API_KEY=your_key_here

# Run bootstrap to build images
poetry run python -m refactoring_benchmark.scripts.bootstrap
```

### 2. Run inference

```bash
# Create directories
mkdir -p output agent

# Create a simple agent script
cat > agent/run_agent << 'EOF'
#!/bin/bash
cd /testbed
# Your refactoring logic here
echo "Making refactoring changes..."
# Example: Use Claude CLI or other tools
exit 0
EOF
chmod +x agent/run_agent

# Run inference
docker run --rm \
    --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $(pwd)/agent:/agent \
    -v $(pwd)/output:/output \
    localhost/benchmark/ray-project-ray:f781622f \
    inference
```

### 3. Evaluate with tests

```bash
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    localhost/benchmark/ray-project-ray:f781622f \
    eval_test > output/test_results.json

# Check results
cat output/test_results.json
```

### 4. Evaluate with static analysis

```bash
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    -v $(pwd)/output:/output \
    localhost/benchmark/ray-project-ray:f781622f \
    eval_rule

# View SARIF results
cat output/rules.sarif
```

## Troubleshooting

### Agent script not found
```
Error: Agent script not found at /agent/run_agent
```
**Solution**: Ensure your agent script is:
1. Located at the correct mount path
2. Named `run_agent`
3. Executable (`chmod +x`)

### Network blocked during inference
```
fatal: unable to access 'https://github.com/...': Could not resolve host: github.com
```
**Expected behavior**: This is intentional. GitHub is blocked during inference to prevent cheating.

### Permission denied accessing /rules
**Expected behavior**: The agent cannot access rules. This is a security feature.

### Test failures after applying patch
Check if the patch applies cleanly:
```bash
docker run --rm \
    -v $(pwd)/output/prediction.diff:/input/patch.diff \
    localhost/benchmark/ray-project-ray:f781622f \
    bash -c "cd /testbed && git apply --check /input/patch.diff"
```

## Advanced: Batch Processing

Run inference on multiple instances:

```bash
#!/bin/bash
# batch_inference.sh

for instance in ray-project-ray tensorflow-tensorflow pandas-dev-pandas; do
    echo "Running inference on $instance..."

    docker run --rm \
        --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
        -v $(pwd)/agent:/agent \
        -v $(pwd)/output/$instance:/output \
        localhost/benchmark/$instance:latest \
        inference

    echo "Evaluating $instance with tests..."
    docker run --rm \
        -v $(pwd)/output/$instance/prediction.diff:/input/patch.diff \
        localhost/benchmark/$instance:latest \
        eval_test > output/$instance/test_results.json

    echo "Evaluating $instance with rules..."
    docker run --rm \
        -v $(pwd)/output/$instance/prediction.diff:/input/patch.diff \
        -v $(pwd)/output/$instance:/output \
        localhost/benchmark/$instance:latest \
        eval_rule
done
```

## Container Internals

### Directory Structure
```
/testbed/                      # Repository code (starts at buggy commit)
/scripts/
  ├── setup_env.sh             # Environment setup (created by Claude)
  └── run_tests                # Test runner (created by Claude)
/rules/                        # Static analysis rules (root-only, mode 700)
  ├── rules_positive.yml       # Rules for good patterns (HIDDEN from agent)
  ├── rules_negative.yml       # Rules for anti-patterns (HIDDEN from agent)
  └── ...                      # Other rule files
/task_description/             # Task descriptions (agent-readable, mode 755)
  ├── README.md                # Task overview (VISIBLE to agent)
  ├── task.md                  # Specific objectives (VISIBLE to agent)
  └── ...                      # Other description files
/agent/                        # Mounted: Your agent code
/input/                        # Mounted: Input files (patches)
/output/                       # Mounted: Output files (results)
/usr/local/bin/
  └── entrypoint.sh            # Runtime router
```

### User Accounts
- **benchmarker**: Primary user, has sudo
- **agent_user**: Created during inference, no sudo, owns `/testbed`

### Environment Variables
The container preserves environment variables set during bootstrap, including:
- Python virtual environment paths
- Conda environments
- PATH modifications
- API keys (during inference only)

## Security Considerations

### What the Agent Cannot Do
- Access GitHub (domains sinkholed)
- View the golden commit (physically removed)
- Read static analysis rules (locked to root)
- Use sudo commands
- Access files outside `/testbed` and `/output`

### What the Agent Can Do
- Read/modify all files in `/testbed`
- Read task descriptions in `/task_description`
- Write to `/output`
- Execute non-privileged commands
- Access mounted resources at `/agent`

### Threat Model
The security measures prevent:
1. **Cheating by fetching solutions**: Network blocked
2. **Viewing the answer**: Golden commit removed from git database
3. **Gaming the metrics**: Rules hidden, tests verified during build
4. **Privilege escalation**: Agent runs as unprivileged user

## Performance Tips

1. **Use tmpfs for output**: Speed up I/O
   ```bash
   docker run --tmpfs /output:rw,size=1G ...
   ```

2. **Limit resources**: Prevent runaway agents
   ```bash
   docker run --memory=4g --cpus=2 ...
   ```

3. **Set timeout**: Kill long-running inference
   ```bash
   timeout 30m docker run ...
   ```

## References

- [Bootstrap Script](refactoring_benchmark/scripts/bootstrap.py)
- [Runtime Router](entrypoint.sh)
- [Security Rules](rules/README.md)
- [Data Models](refactoring_benchmark/utils/models.py)
