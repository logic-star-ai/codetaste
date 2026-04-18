#!/bin/bash

source /opt/nvm/nvm.sh
nvm use 22
sudo chown -R $(whoami) /opt/nvm
npm install -g @anthropic-ai/claude-code@2.1.71

# THIS SCRIPT IS RUN AS `benchmarker` USER WITH PASSWORDLESS SUDO ACCESS. THE `run_agent` SCRIPT DOESN'T HAVE SUDO ACCESS, MAKE SURE TO TRANSFER OWNERSHIP WHERE NEEDED.

