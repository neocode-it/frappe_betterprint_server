#!/bin/bash

# Get required deps
apt-get update && apt-get install sudo git curl -y

# Add bin dir of the tool to environment variables
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
export PATH="$HOME/.local/bin:$PATH"

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.cargo/env

# Install tool
uv tool install "git+https://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@github.com/Neofix-IT/Playwright-Server@main"

# Install playwright dependencies
uvx playwright install --with-deps