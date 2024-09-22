# Playwright Server

Python application for a web-based playwright browser-server (chromium is beeing used)

## Installing Playwright Server

```
#!/bin/bash

# Install curl
apt-get update && apt-get install curl -y

# Run install script
source <(curl -s https://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@raw.githubusercontent.com/Neofix-IT/Playwright-Server/refs/heads/main/install.sh)
```

## Update

```
# Reinstall tool
uv tool install "git+https://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@github.com/Neofix-IT/Playwright-Server@main"

# Reinstall playwright dependencies
uvx playwright install --with-deps
```