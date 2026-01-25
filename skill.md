# WeRead Exporter

Export WeRead (微信读书) books to various formats: EPUB, PDF, MOBI, TXT, and Markdown.

## Usage

When the user asks to export a WeRead book, use this skill to do it.

### ⚠️ Login Requirement (First Time)

**IMPORTANT:** The first time you run the export command, you must log in to your WeRead account:

1. The tool will open a Chrome/Chromium browser window automatically
2. A QR code will be displayed on the screen
3. Use your WeChat mobile app to scan the QR code to log in
4. After successful login, the export process will begin automatically
5. Your login session will be saved for future exports (no need to login again)

If you're not logged in, the export will fail. Make sure to complete the login when prompted.

### Getting Book ID

To get a WeRead book ID:
1. Go to https://weread.qq.com/
2. Search for the target book
3. Open the book detail page
4. The URL format is: `https://weread.qq.com/web/bookDetail/{book_id}`
5. Copy the book_id from the URL

Example: If URL is `https://weread.qq.com/web/bookDetail/08232ac0720befa90825d88`, the book_id is `08232ac0720befa90825d88`

### Command Syntax

```bash
# Basic usage - export to epub and pdf
python -m weread_exporter -b <book_id> -o epub -o pdf

# Export to specific formats
python -m weread_exporter -b <book_id> -o epub -o pdf -o mobi

# Headless mode (no browser window)
python -m weread_exporter -b <book_id> -o epub --headless

# With custom login timeout (default is 60 seconds)
python -m weread_exporter -b <book_id> -o epub --login-timeout 120

# With custom chapter loading timeout
python -m weread_exporter -b <book_id> -o epub --load-timeout 120
```

### Parameters

- `-b, --book-id` (required): The WeRead book ID
- `-o, --output` (optional): Output format(s) - epub, pdf, mobi, txt, md. Default: epub, pdf
- `--headless` (optional): Run in headless mode (no browser window)
- `--force-login` (optional): Force login first. Default: true
- `--login-timeout` (optional): Login QR code timeout in seconds. Default: 60
- `--load-timeout` (optional): Load chapter page timeout in seconds. Default: 60
- `--load-interval` (optional): Load chapter page interval in seconds. Default: 30

### Output Files

Exported files are saved to the `./output/` directory in the current working directory.

### Format Notes

- **epub** - Best for mobile devices and e-readers
- **pdf** - Best for desktop viewing and printing
- **mobi** - Best for Kindle devices (Linux only, requires kindlegen)
- **txt** - Plain text format for quick viewing
- **md** - Markdown format for further editing
- **Note**: When exporting to PDF, EPUB is automatically generated first (required for PDF conversion)

## Examples

User: "Export the WeRead book 08232ac0720befa90825d88 to epub"
Assistant: (runs: `python -m weread_exporter -b 08232ac0720befa90825d88 -o epub`)
Note: If this is your first time, a browser will open with a QR code - scan it with WeChat to log in

User: "I want to download this WeRead book as PDF: 08232ac0720befa90825d88"
Assistant: (runs: `python -m weread_exporter -b 08232ac0720befa90825d88 -o epub -o pdf`)

User: "Export WeRead book 08232ac0720befa90825d88 in headless mode to epub"
Assistant: (runs: `python -m weread_exporter -b 08232ac0720befa90825d88 -o epub --headless`)

User: "Convert WeRead book 08232ac0720befa90825d88 to epub, pdf, and txt"
Assistant: (runs: `python -m weread_exporter -b 08232ac0720befa90825d88 -o epub -o pdf -o txt`)

## Notes

- **REQUIRES LOGIN**: First run will open a browser with WeChat QR code - scan with your WeChat mobile app to log in
- The tool requires Chrome/Chromium browser to be installed
- Login session is saved after first use - no need to login again for subsequent exports
- Headless mode is recommended for server environments (but make sure you're already logged in)
- Large books may take longer to export
- Make sure Python dependencies are installed: `pip install -e .`
