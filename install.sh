#!/bin/sh

# Get required deps
apt-get update && apt-get install sudo git curl -y

# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh && . $HOME/.cargo/env

# Add bin dir (Location of the installed UV tool) to environment variables
#
# adding $HOME/.local/bin to PATH is required for UV tools in general
# Reference: https://docs.astral.sh/uv/guides/integration/docker/#using-installed-tools
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.profile
export PATH="$HOME/.local/bin:$PATH"

# Install tool
# 
# Reference: https://docs.astral.sh/uv/guides/tools/#installing-tools
# Python is explicit specified (which is required if there is an older incompatible python version installed)
uv tool install --python 3.12 "git+https://github.com/neocode-it/frappe_betterprint_server@main"

# Install playwright dependencies
uvx playwright install chromium --with-deps
