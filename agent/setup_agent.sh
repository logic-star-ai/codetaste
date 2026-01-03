#!/bin/bash
sudo chown -R agent_user:agent_user /tmp/claude /tmp && echo "✅ Changed ownership of /tmp/claude and /tmp to agent_user"
if ! command -v claude &> /dev/null; then
    npm install -g @anthropic-ai/claude-code
fi
