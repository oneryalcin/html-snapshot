"""Capture a PNG screenshot of a local HTML file using Playwright.

Usage (with uvx):

    uvx --with playwright python html_snapshot.py path/to/file.html --output slide.png

Before first run, install the Playwright browser binaries:

    uvx playwright install chromium
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from playwright.sync_api import Browser, sync_playwright


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a local HTML file to PNG via Playwright"
    )
    parser.add_argument("html_path", type=Path, help="Path to the local HTML file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="PNG output path (defaults to <html_path>.png)",
    )
    parser.add_argument(
        "--width", type=int, default=1400, help="Viewport width in pixels"
    )
    parser.add_argument(
        "--height", type=int, default=900, help="Viewport height in pixels"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Seconds to wait after load before capturing",
    )
    parser.add_argument(
        "--no-full-page",
        action="store_true",
        help="Capture only the viewport instead of the full page",
    )
    parser.add_argument(
        "--no-auto-install",
        action="store_true",
        help="Skip automatic Playwright browser install (requires chromium to be pre-installed)",
    )
    return parser.parse_args(argv)


def default_browsers_path() -> Path:
    env_path = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if env_path:
        return Path(env_path)

    home = Path.home()
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", home / "AppData/Local"))
        return base / "ms-playwright"
    if sys.platform == "darwin":
        return home / "Library/Caches/ms-playwright"
    return home / ".cache/ms-playwright"


def chromium_installed() -> bool:
    browsers_dir = default_browsers_path()
    if not browsers_dir.exists():
        return False
    return any(browsers_dir.glob("chromium-*"))


def ensure_chromium_installed(auto_install: bool) -> None:
    if chromium_installed():
        return
    if not auto_install:
        raise RuntimeError(
            "Chromium browser binaries are missing. "
            "Run `uvx playwright install chromium` and try again."
        )
    if not shutil.which("playwright"):
        raise RuntimeError(
            "Playwright CLI not found. Install dependencies or set PLAYWRIGHT_BROWSERS_PATH."
        )
    print(
        "Chromium runtime not found; installing via `playwright install chromium`...",
        file=sys.stderr,
    )
    try:
        subprocess.run(["playwright", "install", "chromium"], check=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Automatic Chromium install failed. Run `uvx playwright install chromium` manually."
        ) from exc


def capture_screenshot(
    browser: Browser,
    html_path: Path,
    output_path: Path,
    width: int,
    height: int,
    delay: float,
    full_page: bool,
) -> None:
    page = browser.new_page(viewport={"width": width, "height": height})
    page.goto(html_path.as_uri(), wait_until="networkidle")
    if delay > 0:
        page.wait_for_timeout(int(delay * 1000))
    page.screenshot(path=output_path, full_page=full_page)
    page.close()


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)

    html_path = args.html_path.resolve()
    if not html_path.exists():
        print(f"Error: HTML file not found: {html_path}", file=sys.stderr)
        return 1

    output_path = args.output.resolve() if args.output else html_path.with_suffix(".png")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    ensure_chromium_installed(auto_install=not args.no_auto_install)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        try:
            capture_screenshot(
                browser=browser,
                html_path=html_path,
                output_path=output_path,
                width=args.width,
                height=args.height,
                delay=args.delay,
                full_page=not args.no_full_page,
            )
        finally:
            browser.close()

    print(f"Saved screenshot to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
