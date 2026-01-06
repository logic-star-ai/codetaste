# Standardize binary naming with `llama-` prefix

Rename all example binaries to use consistent `llama-` prefix across the project:
- `main` → `llama-cli`
- `server` → `llama-server`  
- `llava-cli` → `llama-llava-cli`
- All other examples: `*` → `llama-*`

Exception: `rpc-server` unchanged