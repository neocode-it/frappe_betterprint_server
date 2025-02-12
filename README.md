# Frappe Betterprint Server

Python application for a web-based playwright browser-server (chromium is beeing used). All dimensions will be calculated in Millimeter (mm).

The Webserver is accessible on port 39584

## Installing Betterprint Server

```
# Install curl
apt-get update && apt-get install curl -y

# Run install script (using eval to run it in the current shell)
eval "$(curl -s https://raw.githubusercontent.com/neocode-it/frappe_betterprint_server/refs/heads/main/install.sh)"
```

## Update

```
# Run update script
eval "$(curl -s https://raw.githubusercontent.com/neocode-it/frappe_betterprint_server/refs/heads/main/update.sh)"
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