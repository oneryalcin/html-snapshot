# html-snapshot

Capture a PNG screenshot from a local HTML presentation using Playwright.

## Quick start

### Zero-install (recommended)

```bash
# one-time: install the Chromium runtime that Playwright needs
uvx playwright install chromium

# run the tool directly from PyPI (no pip install required)
uvx html-snapshot /path/to/slide.html --output slide.png
```

`uvx` downloads the `html-snapshot` package into a temporary, isolated environment every time you run it, so your main Python setup stays clean.
If Chromium is missing, the tool attempts to run `playwright install chromium` automatically (disable with `--no-auto-install`).

Once the package is published to PyPI you can install it and use the console entry point:

```bash
pip install html-snapshot
html-snapshot /path/to/slide.html --output slide.png
```

### Persistent installation with uv

If you call the tool often, keep it on your PATH with:

```bash
uv tool install html-snapshot

# later
html-snapshot /path/to/slide.html --output slide.png
```

Need a newer version? `uv tool upgrade html-snapshot` fetches the latest release.

## CLI options

| Option | Description |
| ------ | ----------- |
| `html_path` | Path to the local HTML file to render |
| `-o / --output` | Output PNG path (default: same as input with `.png` suffix) |
| `--width` / `--height` | Viewport size (default: 1400×900) |
| `--delay` | Seconds to wait after load before capturing |
| `--no-full-page` | Capture only the viewport instead of the full page |

## Development

```bash
uv venv           # optional: create a local env for hacking
uv pip install -r requirements.txt  # not necessary if using uvx
```

For remote execution straight from GitHub (without PyPI), run:

```bash
uvx --with playwright python gh:oneryalcin/html-snapshot/html_snapshot.py sample.html
```
