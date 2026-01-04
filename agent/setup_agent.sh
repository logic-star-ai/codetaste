#!/bin/bash
sudo chown -R agent_user:agent_user /tmp/claude /tmp && echo "✅ Changed ownership of /tmp/claude and /tmp to agent_user"
if ! command -v claude &> /dev/null; then
    npm install -g @anthropic-ai/claude-code
fi

# THIS SCRIPT IS RUN AS `benchmarker` USER WITH PASSWORDLESS SUDO ACCESS. THE `run_agent` SCRIPT IS EXECUTED BY `agent_user` and doesn't have sudo access, make sure to transfer ownership where needed.

