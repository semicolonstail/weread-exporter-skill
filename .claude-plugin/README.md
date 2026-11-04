# WeRead Exporter Skill for Claude Code

This is a Claude Code skill (MCP server) for exporting WeRead (微信读书) books to various formats.

## Files

```
.claude-plugin/
├── plugin.json      # Plugin manifest
├── mcp_server.py    # MCP server implementation
├── skill.py         # Standalone skill script
└── README.md        # This file
```

## Installation

### 1. Install Dependencies

```bash
pip3 install -e .
```

### 2. Configure MCP Server

The `.mcp.json` file in the project root configures the MCP server. It will be automatically detected by Claude Code when you work in this directory.

### 3. Alternative: Install as User Plugin

To make the skill available globally:

```bash
claude plugin install --scope user .claude-plugin/
```

## Usage

### Getting the Book ID

1. Go to https://weread.qq.com/
2. Search for your target book
3. Open the book detail page
4. The URL format is: `https://weread.qq.com/web/bookDetail/08232ac0720befa90825d88`
5. The book ID is the part after `/web/bookDetail/` (e.g., `08232ac0720befa90825d88`)

### Using in Claude Code

Once the plugin is loaded, you can ask Claude to export books:

```
Export the WeRead book with ID 08232ac0720befa90825d88 to epub and pdf formats
```

```
Please export WeRead book 08232ac0720befa90825d88 in headless mode
```

### Direct Command Line Usage

You can also use the tool directly without Claude Code:

```bash
# Sign in from the project directory before the first CLI export
python -m weread_exporter.login

# Using the main exporter
python -m weread_exporter -b <book_id> -o epub -o pdf

# Using the standalone skill script
python .claude-plugin/skill.py

# Example with headless mode
python -m weread_exporter -b 08232ac0720befa90825d88 -o epub --headless
```

## Tool Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `book_id` | string | Yes | - | The WeRead book ID or official URL |
| `formats` | array | No | ["epub", "pdf"] | Output format(s): epub, pdf, mobi, txt, md. Note: epub is auto-included when pdf is specified |
| `headless` | boolean | No | false | Run chrome in headless mode |
| `force_login` | boolean | No | automatic | Open QR sign-in in a visible browser when no session has been saved |
| `load_timeout` | integer | No | 60 | Load chapter page timeout in seconds |
| `load_interval` | integer | No | 30 | Load chapter page interval in seconds |

## Format Guide

- **epub** - Best for mobile devices
- **pdf** - Best for desktop viewing
- **mobi** - Best for Kindle devices (Linux only)
- **txt** - Plain text format
- **md** - Markdown format

## Output

Exported files are saved to the `./output/` directory in your project.

## Example Commands

```bash
# Export to epub only
python -m weread_exporter -b 08232ac0720befa90825d88 -o epub

# Export to multiple formats
python -m weread_exporter -b 08232ac0720befa90825d88 -o epub -o pdf -o txt

# Export in headless mode (no browser window)
python -m weread_exporter -b 08232ac0720befa90825d88 -o epub --headless

# Export with custom timeout settings
python -m weread_exporter -b 08232ac0720befa90825d88 -o epub --load-timeout 120 --load-interval 60
```

## Disclaimer

This tool is for technical research purposes only. Do not use for commercial or illegal purposes.
