# Playwright Server

Python application for a web-based playwright browser-server (chromium is beeing used). Serving on port 39584

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
uv tool install --python 3.12 "git+https://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@github.com/Neofix-IT/Playwright-Server@main"

# Reinstall playwright dependencies
uvx playwright install --with-deps
```

## Usage

```
# Run server on localhost (no public access)
playwright_server run

# Run server public, exposing port 39584
playwright_server run-public
```

## Limitations

- Calculations of margin of the selector element not possible! This is due to the complexity of margin collapsing. Please use a wrapper element if required.
- If any table row exceeds the max-height, proper calculation won't be possible. By default, this element will be returned even though it exceeds the max-height.