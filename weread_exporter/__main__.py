import argparse
import asyncio
import logging
import os
import sys


def patch_windows():
    bin_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "bin", "win32")
    os.environ["PATH"] += ";" + bin_path
    if hasattr(os, "add_dll_directory"):
        os.add_dll_directory(bin_path)


async def async_main():
    from . import export, utils, webpage

    parser = argparse.ArgumentParser(
        prog="weread-exporter", description="WeRead book export cmdline tool"
    )
    parser.add_argument("-b", "--book-id", help="book ID or official WeRead URL", required=True)
    parser.add_argument(
        "-o",
        "--output-format",
        help="output file format",
        action="append",
        choices=["md", "epub", "pdf", "mobi", "txt"],
    )
    parser.add_argument(
        "--load-timeout",
        help="load chapter page timeout",
        type=int,
        default=60,
    )
    parser.add_argument(
        "--load-interval",
        help="load chapter page interval time",
        type=int,
        default=30,
    )
    parser.add_argument(
        "--css-file",
        help="overide default css style",
    )
    parser.add_argument(
        "--headless", help="chrome headless", action="store_true", default=False
    )
    parser.add_argument(
        "--force-login", help="force login first", action="store_true", default=False
    )
    parser.add_argument(
        "--login-timeout",
        help="login QR code timeout in seconds (default: 60)",
        type=int,
        default=60,
    )
    parser.add_argument(
        "--use-default-profile",
        help="legacy option, unsupported by current Chrome",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--mock-user-agent",
        help="use mock user-agent",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--proxy-server",
        help="http proxy server, e.g. http://127.0.0.1:8888",
    )
    args = parser.parse_args()
    if args.use_default_profile:
        parser.error("Chrome requires a separate profile for browser automation. Omit --use-default-profile.")
    if args.force_login and args.headless:
        parser.error("--force-login requires a visible Chrome window.")
    if args.load_timeout <= 0 or args.load_interval < 0 or args.login_timeout <= 0:
        parser.error("timeouts must be positive and the load interval cannot be negative")
    args.output_format = args.output_format or ["epub"]
    if "mobi" in args.output_format and "epub" not in args.output_format:
        args.output_format.append("epub")

    extra_css = None
    if args.css_file:
        if not os.path.isfile(args.css_file):
            raise RuntimeError("CSS file %s not exist" % args.css_file)
        with open(args.css_file) as fp:
            extra_css = fp.read()

    if "_" in args.book_id and "://" not in args.book_id:
        book_list = [it["id"] for it in await utils.get_book_list(args.book_id)]
    else:
        book_list = [args.book_id]

    for value in book_list:
        book_id = webpage.normalize_book_id(value)
        logging.info("Exporting book %s", book_id)
        page = webpage.WeReadWebPage(book_id)
        try:
            await page.launch(
                headless=args.headless,
                force_login=args.force_login,
                mock_user_agent=args.mock_user_agent,
                proxy_server=args.proxy_server,
                login_timeout=args.login_timeout,
            )
            save_path = os.path.join("cache", "web-reader", book_id)
            exporter = export.WeReadExporter(page, save_path)
            await exporter.export_markdown(args.load_timeout, args.load_interval)
        finally:
            await page.close()

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        await exporter.pre_process_markdown()
        title = await exporter.get_book_title()
        title = utils.format_filename(title)
        if "epub" in args.output_format:
            save_path = os.path.join(output_dir, "%s.epub" % title)
            if os.path.isfile(save_path):
                logging.info("File %s exist, ignore export" % save_path)
            else:
                await exporter.markdown_to_epub(save_path, extra_css=extra_css)
                logging.info("Save file %s complete" % save_path)

        if "pdf" in args.output_format:
            save_path = os.path.join(output_dir, "%s.pdf" % title)
            if os.path.isfile(save_path):
                logging.info("File %s exist, ignore export" % save_path)
            else:
                image_format = "jpg"
                if sys.platform == "win32":
                    image_format = "png"
                await exporter.markdown_to_pdf(
                    save_path,
                    extra_css=extra_css,
                    image_format=image_format,
                )
                logging.info("Save file %s complete" % save_path)

        if "mobi" in args.output_format:
            if sys.platform != "linux":
                logging.error("Only linux system supported to export mobi format")
                return -1
            epub_path = os.path.join(output_dir, "%s.epub" % title)
            save_path = os.path.join(output_dir, "%s.mobi" % title)
            if os.path.isfile(save_path):
                logging.info("File %s exist, ignore export" % save_path)
            else:
                await exporter.epub_to_mobi(epub_path, save_path)
                if not os.path.isfile(save_path):
                    logging.warning("Create mobi file failed")
                    continue
                logging.info("Save file %s complete" % save_path)

        if "txt" in args.output_format:
            save_path = os.path.join(output_dir, "%s.txt" % title)
            if os.path.isfile(save_path):
                logging.info("File %s exist, ignore export" % save_path)
            else:
                await exporter.markdown_to_txt(save_path)
                logging.info("Save file %s complete" % save_path)
    return 0


def main():
    if sys.platform == "win32":
        patch_windows()
    logging.root.level = logging.INFO
    handler = logging.StreamHandler()
    fmt = "[%(asctime)s][%(levelname)s]%(message)s"
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    from . import utils

    os.umask(0o077)
    try:
        return asyncio.run(async_main())
    except (utils.BookAccessError, utils.LoginRequiredError, utils.ChromeNotInstalledError,
            utils.LoadChapterFailedError, ValueError) as error:
        logging.error("%s", error)
        return 1
    except Exception:
        logging.exception("WeRead export failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
