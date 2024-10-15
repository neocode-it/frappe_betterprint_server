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

Page size defaults to A4. Other available formats:

- Letter: 8.5in x 11in
- Legal: 8.5in x 14in
- Tabloid: 11in x 17in
- Ledger: 17in x 11in
- A0: 33.1in x 46.8in
- A1: 23.4in x 33.1in
- A2: 16.54in x 23.4in
- A3: 11.7in x 16.54in
- A4: 8.27in x 11.7in
- A5: 5.83in x 8.27in
- A6: 4.13in x 5.83in
