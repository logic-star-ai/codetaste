# Using Ubuntu 24.04 (Noble Numbat)
FROM ubuntu:24.04

# Avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# 1. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git wget jq unzip sudo locales ca-certificates \
    build-essential gcc g++ clang cmake pkg-config \
    python3 python3-pip python3-venv python3-dev \
    libssl-dev zlib1g-dev libffi-dev libsqlite3-dev \
    libjpeg-dev libpng-dev libtiff-dev libfreetype6-dev \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://raw.githubusercontent.com/opengrep/opengrep/v1.8.2/install.sh | bash
ENV PATH="/home/benchmarker/.opengrep/cli/latest:$PATH"

# 2. Define NVM directory and Node version
ENV NVM_DIR /opt/nvm
ENV NODE_VERSION v20.18.1

# 3. Create NVM directory and install NVM
RUN mkdir -p $NVM_DIR && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# 4. Install Node and NPM
# We run this in a single shell session to ensure 'nvm' is available
RUN . $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && \
    nvm alias default $NODE_VERSION && \
    nvm use default

# 5. Set up global environment for ALL users
RUN echo "export NVM_DIR=$NVM_DIR" >> /etc/bash.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /etc/bash.bashrc && \
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> /etc/bash.bashrc

RUN chmod -R 777 /opt

# 7. Add Node binaries to the system PATH so they work without sourcing bashrc
ENV PATH $NVM_DIR/versions/node/$NODE_VERSION/bin:$PATH

# 8. Example: Install global packages available to everyone
RUN npm install -g @anthropic-ai/claude-code
RUN npm install -g typescript ts-node eslint prettier \
     vitest vercel
RUN npx playwright install chromium --with-deps
RUN mkdir -p /home/benchmarker/.cache/npm-warmup && \
    cd /home/benchmarker/.cache/npm-warmup && \
    npm init -y && \
    npm install react react-dom next tailwindcss lucide-react zod @tanstack/react-query

# Create a non-root test user to verify access
RUN echo "benchmarker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p /scripts /rules /testbed && useradd -m -s /bin/bash benchmarker && \
    chown -R benchmarker:benchmarker /scripts /rules /testbed

RUN chmod -R 777 /home/benchmarker 

USER benchmarker
WORKDIR /testbed
ENV ANTHROPIC_API_KEY=""
CMD ["sleep", "infinity"]