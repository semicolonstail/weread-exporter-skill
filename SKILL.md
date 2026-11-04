---
name: weread-exporter
description: Export books the user can read on the WeRead (微信读书) website to EPUB, PDF, TXT, or chapter Markdown. Use for WeChat QR sign-in and exports by book title, official reader or detail URL, or book ID.
---

# WeRead Exporter

Use the official WeRead website and installed Chrome or Chromium. Install the exporter with `python -m pip install -e .` from the repository, or reuse an environment where it is already installed.

## Find the book

Pass an official `/web/bookDetail/…` or `/web/reader/…` URL, or the book ID, to `-b`. If the user gives a title, find the edition on [WeRead](https://weread.qq.com/) and confirm the author when several results match.

## Sign in and export

Use the same local working directory and Python environment for sign-in and exports. Reuse the user's existing export directory when available. Use a dedicated local directory for a new setup.

Run the login-only command if the user requests sign-in or the session is missing or expired. Ask the user to scan and confirm the QR code in WeChat. Continue once the command confirms that it saved the session.

```sh
python -m weread_exporter.login
```

The session stays in `cache/cookie.txt` in the working directory. Keep it local and omit its contents from logs and replies.

```sh
python -m weread_exporter --headless -b 'BOOK_URL_OR_ID' -o epub
```

- Use the requested format or EPUB by default. Repeat `-o` for multiple formats.
- EPUB, PDF and TXT go to `output/`. Markdown files go to `cache/web-reader/BOOK_ID/chapters/`.
- If a chapter fails to open, displays an access restriction or does not render usable content, report the error and distinguish any cached chapters from a finished export.
- Verify the title and chapters in the requested files. If the tool reused a file with the same name, report that it reused the existing file.
