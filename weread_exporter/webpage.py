"""Read the official WeRead site in a separate Chrome session."""

import asyncio
import html
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import urlsplit

import pyppeteer

from . import utils


_ROOT = "https://weread.qq.com"
_STATE = re.compile(r"window\.__INITIAL_STATE__\s*=\s*")
_LOGIN_CONTROL = """() => [...document.querySelectorAll(
    'a.wr_index_page_top_section_header_action_link, button.navBar_link_Login'
)].find(element => element.innerText.trim() === '登录' && element.getClientRects().length)"""
_LOGIN_MODAL = ".wr_login_modal_wrapper"
_QR_READY = """() => {
    const modal = document.querySelector('.wr_login_modal_wrapper');
    if (!modal?.getClientRects().length) return false;
    const image = modal.querySelector('img.wr_login_modal_qr_img');
    const frame = modal.querySelector('iframe[src]');
    return Boolean((image?.complete && image.naturalWidth > 100) ||
        (frame?.clientWidth > 100 && frame.clientHeight > 100 && frame.src.startsWith('https:')));
}"""
_READY = """(previous) => {
    const view = window.wereadExportSnapshot?.();
    if (!view) return false;
    const marker = view.items.slice(0, 40).map(item => item.text).join('');
    return view.access || (view.items.length && marker !== previous);
}"""


def normalize_book_id(value):
    """Accept a raw ID or an official book detail/reader URL."""
    if "://" in value:
        parsed = urlsplit(value)
        match = re.fullmatch(r"/web/(?:bookDetail|reader)/([a-zA-Z0-9]+)(?:/)?", parsed.path)
        if parsed.scheme != "https" or parsed.netloc != "weread.qq.com" or not match:
            raise ValueError("请使用微信读书官网的书籍详情页或阅读页链接。")
        value = match.group(1)
    # The reader appends a hash of the chapter UID after the book ID.
    value = value.split("k", 1)[0]
    if value.isdecimal():
        value = utils.wr_hash(value)
    if not re.fullmatch(r"[0-9a-f]+(?:g[0-9a-f]+)*", value):
        raise ValueError("无效的微信读书书籍 ID。")
    return value


class WeReadWebPage:
    root_url = _ROOT

    def __init__(self, book_id, cookie_path=None, webcache_path=None):
        self._book_id = book_id
        self._reader_url = f"{_ROOT}/web/reader/{book_id}"
        self._cookie_path = Path(cookie_path or Path(webcache_path or "cache") / "cookie.txt")
        self._cookie = self._load_cookie()
        self._browser = None
        self._page = None
        self._book_info = None
        self._markdown = None

    @staticmethod
    def _check_chrome():
        for name in ("chrome", "google-chrome", "chromium"):
            executable = shutil.which(name)
            if executable:
                return executable
        if sys.platform == "darwin":
            path = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
            if path.is_file():
                return str(path)
        raise utils.ChromeNotInstalledError("请安装 Google Chrome，或将 Chrome 加入 PATH。")

    @property
    def has_session(self):
        return bool(self._cookie.get("wr_vid") not in (None, "", "0") and self._cookie.get("wr_skey"))

    def _load_cookie(self):
        if not self._cookie_path.is_file():
            return {}
        text = self._cookie_path.read_text(encoding="utf-8")
        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            result = dict(field.strip().split("=", 1) for field in text.split(";") if "=" in field)
        if not isinstance(result, dict):
            return {}
        return {key: value for key, value in result.items() if isinstance(value, str)}

    def _save_cookie(self):
        self._cookie_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w", dir=self._cookie_path.parent, encoding="utf-8", delete=False
        ) as file:
            temp_path = Path(file.name)
            try:
                json.dump(self._cookie, file)
                file.close()
                temp_path.replace(self._cookie_path)
            finally:
                if temp_path.exists():
                    temp_path.unlink()

    async def launch(self, headless=False, force_login=False, mock_user_agent=False,
                     proxy_server=None, login_timeout=60):
        if force_login and headless:
            raise ValueError("扫码登录需要可见的 Chrome 窗口。")
        if not force_login and not self.has_session:
            raise utils.LoginRequiredError("缺少登录记录，请先运行 python -m weread_exporter.login。")

        chrome = self._check_chrome()
        args = ["--window-size=1440,1000"]
        if proxy_server:
            args.append(f"--proxy-server={proxy_server}")
        if sys.platform == "linux" and os.getuid() == 0:
            args.append("--no-sandbox")

        self._browser = await pyppeteer.launch(
            executablePath=chrome, headless=headless, args=args,
            defaultViewport={"width": 1440, "height": 1000},
            autoClose=False, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
        )
        self._page = (await self._browser.pages())[0]
        if mock_user_agent:
            await self._page.setUserAgent(utils.generate_user_agent())
        if force_login:
            await self.login(timeout=login_timeout)
        else:
            await self._page.setCookie(*[
                {"url": _ROOT, "name": name, "value": value, "secure": True}
                for name, value in self._cookie.items()
            ])
        if self._book_id:
            await self._page.setCookie({
                "url": _ROOT, "name": "wr_useHorizonReader", "value": "0", "secure": True,
            })
            hook = Path(__file__).with_name("hook.js").read_text(encoding="utf-8")
            await self._page.evaluateOnNewDocument(hook)
            self._book_info = await self._read_book_info()

    async def close(self):
        try:
            if self._browser:
                await self._browser.close()
        finally:
            self._browser = self._page = None

    async def login(self, timeout=60):
        await self._page.goto(_ROOT, waitUntil="domcontentloaded", timeout=45000)
        await self._page.bringToFront()
        # The server-rendered link can appear before the page binds its click handler.
        for attempt in range(3):
            control = await self._page.waitForFunction(_LOGIN_CONTROL, {"timeout": 15000})
            try:
                await control.asElement().click()
            finally:
                await control.dispose()
            try:
                await self._page.waitForSelector(_LOGIN_MODAL, {"visible": True, "timeout": 4000})
                break
            except pyppeteer.errors.TimeoutError:
                if attempt == 2:
                    raise RuntimeError("微信读书登录窗口未打开。") from None
        try:
            await self._page.waitForFunction(_QR_READY, {"timeout": 25000})
        except pyppeteer.errors.TimeoutError:
            raise RuntimeError("微信读书登录窗口已打开，但二维码未加载。") from None
        print("微信读书登录二维码已显示，请使用手机微信扫码并确认。", flush=True)

        deadline = asyncio.get_running_loop().time() + timeout
        while asyncio.get_running_loop().time() < deadline:
            cookies = {item["name"]: item["value"] for item in await self._page.cookies(_ROOT)}
            if cookies.get("wr_vid") not in (None, "", "0") and cookies.get("wr_skey"):
                self._cookie = cookies
                self._save_cookie()
                print("微信读书已登录，登录状态已保存。", flush=True)
                return
            await asyncio.sleep(1)
        raise utils.LoginRequiredError("微信读书扫码登录已超时。")

    async def _open_reader(self, url, timeout):
        response = await self._page.goto(url, waitUntil="domcontentloaded", timeout=timeout * 1000)
        if response is None:
            # The reader can change its URL in place while a new navigation starts.
            await self._page.goto("about:blank")
            response = await self._page.goto(url, waitUntil="domcontentloaded", timeout=timeout * 1000)
        if not response or not response.ok:
            status = response.status if response else "无响应"
            raise RuntimeError(f"微信读书阅读页加载失败（HTTP {status}）。")
        document = await response.text()
        match = _STATE.search(document)
        if not match:
            raise RuntimeError("阅读页未提供书籍数据，请检查网页是否正常打开。")
        state, _ = json.JSONDecoder().raw_decode(document, match.end())
        if not str((state.get("user") or {}).get("vid") or "").strip("0"):
            raise utils.LoginRequiredError("微信读书会话已过期，请先重新扫码登录。")
        return state.get("reader") or {}

    async def _read_book_info(self):
        reader = await self._open_reader(self._reader_url, timeout=45)
        info = reader.get("bookInfo") or {}
        chapters = reader.get("chapterInfos") or []
        if not info.get("title") or not chapters:
            raise utils.BookAccessError("微信读书未提供可读目录，请在浏览器中确认该书的网页阅读权限。")
        return {
            "title": info["title"],
            "author": info.get("author") or "",
            "cover": info.get("cover") or "",
            "intro": info.get("intro") or "",
            "chapters": [{
                "id": chapter["chapterUid"],
                "title": chapter.get("title") or info["title"],
                "level": max(chapter.get("level") or 1, 1),
                "words": chapter.get("wordCount") or 0,
                "anchors": chapter.get("anchors") or [],
            } for chapter in chapters],
        }

    async def get_book_info(self):
        return self._book_info

    async def _snapshot(self):
        view = await self._page.evaluate("window.wereadExportSnapshot()")
        if view.get("access"):
            if "登录" in view["access"]:
                raise utils.LoginRequiredError("阅读页要求登录，请重新扫码。")
            raise utils.BookAccessError(f"阅读页提示「{view['access']}」，导出已停止。")
        return view

    async def _read_section(self, timeout, previous=None):
        await self._page.waitForFunction(_READY, {"timeout": timeout * 1000}, previous)
        await self._page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        await asyncio.sleep(0.25)
        items = {}
        for _ in range(500):
            view = await self._snapshot()
            for item in view["items"]:
                key = (item["layer"], item.get("id") or (
                    item["kind"], round(item["x"]), round(item["y"]), item["text"],
                ))
                items[key] = item
            if view["height"] - view["top"] - view["viewport"] <= 2:
                return view, items.values()
            await self._page.evaluate(
                "(top) => window.scrollTo({top, behavior: 'instant'})",
                view["top"] + round(view["viewport"] * 0.7),
            )
            await asyncio.sleep(0.25)
        raise utils.LoadChapterFailedError("滚动到章节底部超时。")

    async def goto_chapter(self, chapter_id, timeout=60):
        self._markdown = None
        url = self._reader_url + "k" + utils.wr_hash(str(chapter_id))
        reader = await self._open_reader(url, timeout=timeout)
        chapter = reader.get("currentChapter") or {}
        if str(chapter.get("chapterUid")) != str(chapter_id):
            raise utils.BookAccessError(f"阅读器未打开请求的章节 {chapter_id}。")
        sections = []
        previous = None
        for _ in range(50):
            view, items = await self._read_section(timeout, previous)
            markdown = self._format_section(items)
            if not markdown.strip() or markdown in sections:
                raise utils.LoadChapterFailedError(f"章节 {chapter_id} 的正文为空或页面重复。")
            sections.append(markdown)
            if not view["next"]:
                title = chapter.get("title") or self._book_info["title"]
                text = "\n\n".join(sections)
                first_line, _, rest = text.partition("\n")
                if "".join(html.unescape(first_line).split()) == "".join(title.split()):
                    text = rest.lstrip("\n")
                self._markdown = f"## {html.escape(title, quote=False)}\n\n{text}"
                return
            previous = "".join(item["text"] or "" for item in view["items"][:40])
            await self._page.click(".readerFooter .readerFooter_button")
        raise utils.LoadChapterFailedError(f"章节 {chapter_id} 超过分页上限。")

    async def get_markdown(self):
        if not self._markdown:
            raise utils.LoadChapterFailedError("阅读页未提供可导出的正文。")
        return self._markdown

    @staticmethod
    def _format_section(items):
        # Overlay text and canvas text can briefly coexist as the viewport moves.
        ordered = sorted(items, key=lambda item: (item["y"], item["x"]))
        rows = []
        for item in ordered:
            kind = item["kind"]
            if kind != "text":
                rows.append([item])
            elif rows and rows[-1][0]["kind"] == "text" and item["y"] - rows[-1][0]["y"] < 7:
                rows[-1].append(item)
            else:
                rows.append([item])

        output = []
        previous = None
        for row in rows:
            row.sort(key=lambda item: (item["x"], item["layer"] != "dom"))
            first = row[0]
            if first["kind"] == "text":
                parts = []
                last = None
                for item in row:
                    if last and abs(item["x"] - last["x"]) < 3 and item["text"] == last["text"]:
                        continue
                    parts.append(item["text"] or "")
                    last = item
                text = "".join(parts).strip()
                if not text:
                    continue
                text = html.escape(text, quote=False)
                if previous is None or first["y"] - previous["y"] > first["size"] * 2.1 or (
                    first["x"] - previous["x"] > first["size"]
                ):
                    output.append("")
                elif output and re.search(r"[A-Za-z0-9]$", output[-1]) and re.match(r"[A-Za-z0-9]", text):
                    output[-1] += " "
                output.append(text)
                previous = first
            else:
                value = first["text"] or ""
                if first["kind"] == "image":
                    text = "![](" + value.replace("(", "%28").replace(")", "%29") + ")"
                elif first["kind"] == "code":
                    text = "```\n" + value.rstrip() + "\n```"
                else:
                    text = "------"
                output.extend(("", text, ""))
                previous = None
        return "\n".join(output).strip()
