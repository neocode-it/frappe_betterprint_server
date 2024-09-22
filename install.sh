#!/bin/bash

# Get required deps
apt-get update && apt-get install sudo git curl -y

# Add bin dir of the tool to environment variables
echo '. "$HOME/.local/bin"' >> ~/.bashrc
echo '. "$HOME/.local/bin"' >> ~/.profile
export PATH="$PATH:$HOME/.local/bin"

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.cargo/env

# Install tool
uv tool install ./Playwright-Server/dist/*.whl