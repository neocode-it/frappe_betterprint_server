#!/bin/bash

# Get required deps
apt-get update && apt-get install sudo git curl -y

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.cargo/env

# Add bin dir of the tool to environment variables
#
# adding $HOME/.local/bin to PATH is required for UV tools
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#using-installed-tools
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
export PATH="$HOME/.local/bin:$PATH"

# Install tool
# 
# Reference: https://docs.astral.sh/uv/guides/tools/#installing-tools
# Python is explicit specified (which is required if there is an older incompatible python version installed)
uv tool install --python 3.12 "git+https://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@github.com/Neofix-IT/Playwright-Server@main"

# Install playwright dependencies
uvx playwright install --with-deps
