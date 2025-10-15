# html-snapshot

Capture ppt-canvas HTML slides as PNGs and (optionally) emit a structured layout report for automated checks.

## Quick start (no install)

```bash
# one-time: ensure Playwright's Chromium runtime is available
uvx playwright install chromium

# generate a slide screenshot, plus an optional JSON layout report
uvx html-snapshot /path/to/slide.html \
    --output slide.png \
    --report slide.json
```

`uvx` runs the tool in an isolated environment downloaded from PyPI. The script auto-installs Chromium if it is missing (skip with `--no-auto-install`).

## Install once, reuse often

Prefer a persistent CLI?

```bash
uv tool install html-snapshot   # adds `html-snapshot` to your PATH

html-snapshot /path/to/slide.html --output slide.png --report slide.json
```

Or use pip:

```bash
pip install html-snapshot
html-snapshot /path/to/slide.html --output slide.png
```

## CLI options

| Option | Description |
| ------ | ----------- |
| `html_path` | Path to the local HTML file to render |
| `-o / --output` | Output PNG path (default: input with `.png` suffix) |
| `--report` | Optional JSON layout report (words, bounding boxes, warnings) |
| `--width` / `--height` | Viewport size (default: 1400×900) |
| `--delay` | Wait time after load before capture |
| `--no-full-page` | Capture only the viewport |
| `--no-auto-install` | Require Chromium to be pre-installed |

## Direct-from-GitHub fallback

If you’d rather run the latest commit without PyPI:

```bash
uvx --with playwright python gh:oneryalcin/html-snapshot/html_snapshot.py sample.html
```
