# Frappe Betterprint Server

Python application for a web-based playwright browser-server (chromium is beeing used). Serving on port 39584

## Installing Betterprint Server

```
#!/bin/bash

# Install curl
apt-get update && apt-get install curl -y

# Run install script
source <(curl -s https://raw.githubusercontent.com/neocode-it/frappe_betterprint_server/refs/heads/main/install.sh)
```

## Update

```
# Reinstall tool
uv tool install --python 3.12 "git+https://github.com/neocode-it/frappe_betterprint_server@main"

# Reinstall playwright dependencies
uvx playwright install --with-deps
```

## Usage

```
# Run server on localhost (no public access)
betterprint_server run

# Run server public, exposing port 39584
betterprint_server run-public
```

## Limitations

- Calculations of margin of the selector element not possible! This is due to the complexity of margin collapsing. Please use a wrapper element if required.
- If any table row exceeds the max-height, proper calculation won't be possible. By default, this element will be returned even though it exceeds the max-height.