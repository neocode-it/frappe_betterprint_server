#!/bin/bash

# Get required deps
apt-get update && apt-get install sudo git curl -y

# Add bin dir of the tool to environment variables
echo 'export "$HOME/.local/bin"' >> ~/.bashrc
echo 'export "$HOME/.local/bin"' >> ~/.profile
export PATH="$PATH:$HOME/.local/bin"

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.cargo/env

# Install tool
uv tool install ./Playwright-Server/dist/*.whl

https://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@raw.githubusercontent.com/Neofix-IT/Playwright-Server/refs/heads/main/install.sh