# Bootstrap Phase

The bootstrap phase prepares **per‑instance container images** and baseline test metrics. It produces two images per instance: a setup image and a runtime image.

## Entry point
```bash
python -m refactoring_benchmark.cli.bootstrap
```

## What it does
1. **Load instances** from `instances.csv`.
2. **Setup phase** (`bootstrap/setup.py`)
   - Clone repo at `golden_commit_hash` in a base container.
   - Run the setup agent (Claude) to prepare the environment.
   - Run tests on **golden** and **base** commits and record metrics.
   - Commit the container as the **setup image**.
3. **Runtime phase** (`bootstrap/runtime.py`)
   - Inject `refactoring_benchmark/bootstrap/entrypoint.sh` and rule assets.
   - Apply security hardening and prepare for agent execution.
   - Commit the container as the **runtime image**.

## Outputs
- `instance_images/<owner>/<repo>/<hash>/instance_metadata.json`
- Podman images:
  - `ghcr.io/logic-star-ai/codetaste/<id>__setup`
  - `ghcr.io/logic-star-ai/codetaste/<id>__runtime`

## Key flags
- `--force-full-build`: rebuild setup + runtime from scratch.
- `--force-runtime-build`: rebuild runtime image only.
- `--rerun-metrics`: reuse setup image and only recompute metrics.

## Notes
- Requires `ANTHROPIC_API_KEY` for the setup agent.
- The bootstrap phase will **skip** instances that already have metadata unless forced.
