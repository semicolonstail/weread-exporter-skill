#!/usr/bin/env python3
"""
WeRead Exporter MCP Server
Provides tools for exporting WeRead books.
"""

import asyncio
import json
import logging
import os
import subprocess
import sys

# Add project root to path (parent of .claude-plugin directory)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)


async def main():
    """MCP Server entry point"""
    # Read messages from stdin
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            message = json.loads(line.strip())
            await handle_message(message)
        except EOFError:
            break
        except Exception as e:
            logging.error(f"Error: {e}", exc_info=True)


async def handle_message(message):
    """Handle MCP messages"""
    if message.get("method") == "initialize":
        # Respond with server capabilities
        response = {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {
                "serverInfo": {
                    "name": "weread-exporter",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {
                        "listChanged": False
                    }
                }
            }
        }
        print(json.dumps(response))
        sys.stdout.flush()

    elif message.get("method") == "tools/list":
        # List available tools
        response = {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {
                "tools": [
                    {
                        "name": "export_weread_book",
                        "description": "Export a WeRead book to specified format(s). Book ID can be obtained from: https://weread.qq.com/web/bookDetail/{book_id}",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "book_id": {
                                    "type": "string",
                                    "description": "The WeRead book ID (e.g., 08232ac0720befa90825d88)"
                                },
                                "formats": {
                                    "type": "array",
                                    "description": "Output format(s)",
                                    "items": {
                                        "type": "string",
                                        "enum": ["epub", "pdf", "mobi", "txt", "md"]
                                    },
                                    "default": ["epub", "pdf"]
                                },
                                "headless": {
                                    "type": "boolean",
                                    "description": "Run chrome in headless mode",
                                    "default": False
                                },
                                "force_login": {
                                    "type": "boolean",
                                    "description": "Force login first (default: true for better compatibility)",
                                    "default": True
                                },
                                "load_timeout": {
                                    "type": "integer",
                                    "description": "Load chapter page timeout in seconds",
                                    "default": 60
                                },
                                "load_interval": {
                                    "type": "integer",
                                    "description": "Load chapter page interval in seconds",
                                    "default": 30
                                }
                            },
                            "required": ["book_id"]
                        }
                    }
                ]
            }
        }
        print(json.dumps(response))
        sys.stdout.flush()

    elif message.get("method") == "tools/call":
        # Execute a tool
        await handle_tool_call(message)


async def handle_tool_call(message):
    """Handle tool execution"""
    tool_name = message.get("params", {}).get("name")
    arguments = message.get("params", {}).get("arguments", {})

    if tool_name == "export_weread_book":
        result = await export_weread_book(arguments)
        response = {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }
        }
    else:
        response = {
            "jsonrpc": "2.0",
            "id": message.get("id"),
            "error": {
                "code": -32601,
                "message": f"Unknown tool: {tool_name}"
            }
        }

    print(json.dumps(response))
    sys.stdout.flush()


async def export_weread_book(arguments):
    """Export a WeRead book"""
    book_id = arguments.get("book_id")
    if not book_id:
        return "Error: book_id is required"

    # Get formats with default - always include epub if pdf is requested
    formats = arguments.get("formats", ["epub", "pdf"])
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
    force_login = arguments.get("force_login", True)
    if force_login:
        cmd_args.append("--force-login")

    # Optional parameters
    if arguments.get("headless"):
        cmd_args.append("--headless")

    if arguments.get("load_timeout"):
        cmd_args.extend(["--load-timeout", str(arguments["load_timeout"])])

    if arguments.get("load_interval"):
        cmd_args.extend(["--load-interval", str(arguments["load_interval"])])

    # Execute the exporter
    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            *cmd_args,
            cwd=PROJECT_DIR,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        output = ""
        if stdout:
            output += stdout.decode('utf-8')
        if stderr:
            output += stderr.decode('utf-8')

        if process.returncode != 0:
            return f"Export failed (exit code {process.returncode}):\n{output}"

        # List exported files
        output_dir = os.path.join(PROJECT_DIR, "output")
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
            if files:
                output += "\n\nExported files:\n"
                for f in sorted(files):
                    fpath = os.path.join(output_dir, f)
                    size = os.path.getsize(fpath)
                    size_mb = size / (1024 * 1024)
                    output += f"  - {f} ({size_mb:.2f} MB)\n"

        return f"Export completed!\n\n{output}"

    except Exception as e:
        return f"Error during export: {e}"


if __name__ == "__main__":
    asyncio.run(main())
