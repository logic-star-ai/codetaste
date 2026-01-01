# Refactor ingest CLI to use subcommand architecture

## Summary
Refactor the ingest CLI from a monolithic command with connector-prefixed options to a subcommand-based architecture where each connector has its own subcommand.

## Why
- Current approach is becoming unwieldy as number of connectors grows (19+ connectors)
- Option name conflicts require verbose prefixes (`--s3-anonymous`, `--dropbox-token`, etc.)
- Cannot enforce connector-specific required fields without complex validation logic
- Difficult to discover which options apply to which connector

## Changes

### CLI Structure
- Convert from single `@click.command()` to `@click.group()` with subcommands
- Each connector gets its own subcommand: `s3`, `azure`, `dropbox`, `github`, `gitlab`, `reddit`, `slack`, `discord`, `wikipedia`, `gdrive`, `biomed`, `onedrive`, `outlook`, `local`, `elasticsearch`, `confluence`, `gcs`, `fsspec`
- Shared options (e.g., `--num-processes`, `--verbose`, `--partition-strategy`) dynamically added to all subcommands
- Connector-specific options only available under their subcommand

### Parameter Naming
- Remove connector prefixes: `--s3-anonymous` → `--anonymous`, `--dropbox-token` → `--token`, `--github-url` → `--url`, etc.
- Rename for consistency: `--local-input-path` → `--input-path`, `--biomed-path` → `--path`, `--slack-channels` → `--channels`

### Code Organization
```
unstructured/ingest/
├── cli/
│   ├── cli.py              # Main group command
│   ├── common.py           # Shared options, config mappers, validators
│   └── cmds/               # Subcommand definitions
│       ├── s3.py
│       ├── azure.py
│       └── ...
├── runner/                  # Business logic per connector
│   ├── s3.py
│   ├── azure.py
│   └── ...
├── processor.py            # Core processing logic (extracted from main.py)
└── main.py                 # Entry point (now just calls get_cmd())
```

### Additional Improvements
- Separate CLI parsing from processing logic
- Extract `Processor` class from `MainProcess`
- Create `ProcessorConfigs` dataclass for processor-related configs
- Add runner functions for each connector to encapsulate setup logic
- Improve logger to avoid duplicate handlers
- Scrub sensitive fields (`account_key`, `api_key`, `token`, `client_id`, `client_cred`) from logs
- Support running via Python API in addition to CLI

## Usage Examples

**Before:**
```bash
unstructured-ingest \
  --remote-url s3://bucket/path \
  --s3-anonymous \
  --structured-output-dir output
```

**After:**
```bash
unstructured-ingest s3 \
  --remote-url s3://bucket/path \
  --anonymous \
  --structured-output-dir output
```

## Breaking Changes
- All connector invocations now require subcommand as first argument
- Connector-specific options renamed (prefixes removed)
- Some options renamed for consistency (e.g., `--start-date`/`--end-date` for Slack instead of `--oldest`/`--latest`)