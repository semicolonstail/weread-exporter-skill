"""Open WeRead's QR sign-in without exporting a book."""

import argparse
import asyncio
import os
from pathlib import Path
import sys

from .webpage import WeReadWebPage


async def sign_in(state_dir, timeout):
    cache = state_dir / "cache"
    page = WeReadWebPage("", cookie_path=cache / "cookie.txt", webcache_path=cache)
    try:
        await page.launch(force_login=True, login_timeout=timeout)
    finally:
        await page.close()


def main():
    parser = argparse.ArgumentParser(description="Sign in to WeRead in a separate Chrome window")
    parser.add_argument("--timeout", type=int, default=300, help="seconds to wait for WeChat")
    parser.add_argument(
        "--state-dir", type=Path, default=Path.cwd(),
        help="the export working directory (default: current directory)",
    )
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    os.umask(0o077)
    try:
        asyncio.run(sign_in(args.state_dir, args.timeout))
    except Exception as error:
        print(f"微信读书登录失败：{error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
