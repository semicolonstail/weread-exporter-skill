#!/usr/bin/env python3
"""
WeRead Exporter Skill - Export WeRead books to various formats

Usage as a skill:
  Input JSON: {"book_id": "xxx", "formats": ["epub", "pdf"], "headless": false, ...}
"""

import argparse
import asyncio
import json
import os
import sys

# Add project root to path
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)


def main():
    parser = argparse.ArgumentParser(
        prog="weread-exporter-skill",
        description="WeRead book exporter skill"
    )
    parser.add_argument(
        "--skill-input",
        help="JSON input for skill execution"
    )

    args = parser.parse_args()

    # If skill input is provided, parse and execute
    if args.skill_input:
        try:
            input_data = json.loads(args.skill_input)
            skill_main(input_data)
        except json.JSONDecodeError as e:
            print(f"Error parsing skill input: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Show usage information
        print("=" * 60)
        print("WeRead Exporter Skill")
        print("=" * 60)
        print()
        print("This skill exports WeRead books to various formats.")
        print()
        print("Usage:")
        print("  /export-weread-book <book_id> [options]")
        print()
        print("Parameters:")
        print("  book_id       (required)  The WeRead book ID")
        print("                           Get it from: https://weread.qq.com/web/bookDetail/{id}")
        print()
        print("Options:")
        print("  formats       (optional)  Output format(s): epub, pdf, mobi, txt, md")
        print("                           Default: epub")
        print("  headless      (optional)  Run chrome in headless mode (default: false)")
        print("  force_login   (optional)  Force login first (default: false)")
        print("  load_timeout  (optional)  Load chapter timeout in seconds (default: 60)")
        print("  load_interval (optional)  Load chapter interval in seconds (default: 30)")
        print()
        print("Examples:")
        print('  /export-weread-book 08232ac0720befa90825d88')
        print('  /export-weread-book 08232ac0720befa90825d88 --formats epub pdf')
        print('  /export-weread-book 08232ac0720befa90825d88 --formats epub --headless true')
        print()
        print("Output:")
        print("  Exported files are saved to: ./output/")
        print()
        print("=" * 60)


def skill_main(input_data):
    """Main skill execution function"""
    # Validate required parameters
    book_id = input_data.get("book_id")
    if not book_id:
        print("Error: book_id is required", file=sys.stderr)
        sys.exit(1)

    # Get formats with default - always include epub if pdf is requested
    formats = input_data.get("formats", ["epub", "pdf"])
    if isinstance(formats, str):
        formats = [formats]

    # Auto-add epub if pdf is requested and epub is not included
    if "pdf" in formats and "epub" not in formats:
        formats.append("epub")

    # Build command arguments
    cmd_args = ["-m", "weread_exporter", "-b", book_id]
    for fmt in formats:
        cmd_args.extend(["-o", fmt])

    # Default to force_login for better compatibility
    force_login = input_data.get("force_login", True)
    if force_login:
        cmd_args.append("--force-login")

    # Optional parameters
    if input_data.get("headless"):
        cmd_args.append("--headless")

    if input_data.get("load_timeout"):
        cmd_args.extend(["--load-timeout", str(input_data["load_timeout"])])

    if input_data.get("load_interval"):
        cmd_args.extend(["--load-interval", str(input_data["load_interval"])])

    # Execute the exporter
    print(f"Exporting WeRead book: {book_id}")
    print(f"Formats: {', '.join(formats)}")
    print()

    import subprocess
    result = subprocess.run(
        [sys.executable] + cmd_args,
        cwd=PROJECT_DIR,
        check=True
    )

    # Show output location
    output_dir = os.path.join(PROJECT_DIR, "output")
    print()
    print("=" * 60)
    print(f"Export completed! Check output directory: {output_dir}")
    print("=" * 60)

    # List exported files
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        if files:
            print("Exported files:")
            for f in sorted(files):
                fpath = os.path.join(output_dir, f)
                if os.path.isfile(fpath):
                    size = os.path.getsize(fpath)
                    size_mb = size / (1024 * 1024)
                    print(f"  - {f} ({size_mb:.2f} MB)")

    return result.returncode


if __name__ == "__main__":
    main()
