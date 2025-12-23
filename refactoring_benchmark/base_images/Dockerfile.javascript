FROM ubuntu:24.04

# 1. Environment & Global Configs
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    # Node/JS Paths
    NVM_DIR=/usr/local/nvm \
    BUN_INSTALL=/home/benchmarker/.bun \
    # Combined Path
    PATH="/home/benchmarker/.local/bin:/home/benchmarker/.bun/bin:/home/benchmarker/.local/share/pnpm:/usr/local/nvm/versions/node/v20.18.0/bin:$PATH"

RUN useradd -m -s /bin/bash benchmarker

# 2. System Core & Build Essentials (Includes your original lib list + browser deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git wget jq unzip sudo locales ca-certificates \
    build-essential gcc g++ clang cmake pkg-config \
    python3 python3-pip python3-venv python3-dev \
    libssl-dev zlib1g-dev libffi-dev libsqlite3-dev \
    # Media/Image libs for React/Next.js image processing
    libjpeg-dev libpng-dev libtiff-dev libfreetype6-dev \
    # Browser deps for Playwright/Cypress
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# 3. Install UV (Kept for Python-based JS tooling/scripts)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 4. Node.js Runtimes (NVM, Bun, and PNPM)
RUN mkdir -p $NVM_DIR \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && . $NVM_DIR/nvm.sh \
    && nvm install 20 && nvm alias default 20
RUN . $NVM_DIR/nvm.sh && \
    ln -s $(which node) /usr/local/bin/node && \
    ln -s $(which npm) /usr/local/bin/npm && \
    ln -s $(which npx) /usr/local/bin/npx
RUN curl -fsSL https://bun.sh/install | bash

# 5. Create User & Permissions (Aligned with your original structure)
RUN echo "benchmarker ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p /scripts /rules /testbed && \
    chown -R benchmarker:benchmarker /scripts /rules /testbed /usr/local/nvm

USER benchmarker
WORKDIR /testbed

# 6. Global Tooling (Original Opengrep + JS Essentials)
RUN curl -fsSL https://raw.githubusercontent.com/opengrep/opengrep/v1.8.2/install.sh | bash
ENV PATH="/home/benchmarker/.opengrep/cli/latest:$PATH"
RUN npm install -g @anthropic-ai/claude-code


RUN npm install -g typescript ts-node eslint prettier \
     vitest vercel

# 7. Playwright Pre-caching
RUN npx playwright install chromium --with-deps

# 8. React/Frontend Dependency Pre-cache (Warm up the npm cache)
RUN mkdir -p /home/benchmarker/.cache/npm-warmup && \
    cd /home/benchmarker/.cache/npm-warmup && \
    npm init -y && \
    npm install react react-dom next tailwindcss lucide-react zod @tanstack/react-query && \
    cd /testbed && rm -rf /home/benchmarker/.cache/npm-warmup

ENV ANTHROPIC_API_KEY=""
CMD ["sleep", "infinity"]