# Update the uv tool (force-reinstall)
uv tool install --reinstall --python 3.12 "git+https://github.com/neocode-it/frappe_betterprint_server@main"

# Update playwright dependencies
uvx playwright install chromium --with-deps