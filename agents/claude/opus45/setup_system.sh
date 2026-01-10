#!/bin/bash
if ! command -v claude &> /dev/null; then
    npm install -g @anthropic-ai/claude-code
fi

# THIS SCRIPT IS RUN AS `benchmarker` USER WITH PASSWORDLESS SUDO ACCESS. THE `run_agent` SCRIPT IS EXECUTED BY `agent_user` AND DOESN'T HAVE SUDO ACCESS, MAKE SURE TO TRANSFER OWNERSHIP WHERE NEEDED.

