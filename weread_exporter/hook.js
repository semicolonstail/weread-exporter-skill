() => {
  if (!location.pathname.startsWith("/web/reader/")) return;
  history.scrollRestoration = "manual";

  // The reader paints some parts on canvas and puts others in positioned DOM layers.
  const canvases = new WeakMap();
  const proto = CanvasRenderingContext2D.prototype;
  const fillText = proto.fillText;
  const clearRect = proto.clearRect;

  proto.fillText = function (text, x, y, ...args) {
    const result = fillText.call(this, text, x, y, ...args);
    if (this.globalAlpha === 0) return result;

    text = String(text);
    if (text.startsWith("abcdefghijklmn")) return result;
    const matrix = this.getTransform();
    const left = matrix.a * x + matrix.c * y + matrix.e;
    const top = matrix.b * x + matrix.d * y + matrix.f;
    const fontSize = parseFloat(this.font.match(/([\d.]+)px/)?.[1]) || 20;
    const items = canvases.get(this.canvas) || new Map();
    items.set(`${left}:${top}`, {
      x: left, y: top, text, size: fontSize * matrix.d,
      width: this.measureText(text).width * matrix.a,
    });
    canvases.set(this.canvas, items);
    return result;
  };

  proto.clearRect = function (x, y, width, height) {
    const items = canvases.get(this.canvas);
    if (items) {
      const matrix = this.getTransform();
      const left = x * matrix.a + matrix.e;
      const top = y * matrix.d + matrix.f;
      for (const [key, item] of items) {
        if (item.x + item.width >= left && item.x < left + width * matrix.a &&
            item.y >= top && item.y - item.size < top + height * matrix.d) {
          items.delete(key);
        }
      }
    }
    return clearRect.call(this, x, y, width, height);
  };

  const visible = element => element.getClientRects().length && getComputedStyle(element).visibility !== "hidden";

  window.wereadExportSnapshot = () => {
    const chapter = document.querySelector(".readerChapterContent");
    const reader = document.querySelector(".readerContent");
    const footer = document.querySelector(".readerFooter");
    const button = [...(footer?.querySelectorAll("button, a") || [])]
      .filter(visible).map(element => element.innerText.trim());
    const access = [...(reader?.querySelectorAll("button, a") || [])]
      .filter(visible).map(element => element.innerText.trim())
      .find(label => /^(登录后|请登录|扫码登录|购买后|付费阅读|订阅后|试读结束|开通会员|购买本[书章]|立即购买)/.test(label));
    const items = [];

    for (const canvas of chapter?.querySelectorAll("canvas") || []) {
      const rect = canvas.getBoundingClientRect();
      if (!rect.width || !rect.height || !canvas.width || !canvas.height) continue;
      const sx = rect.width / canvas.width;
      const sy = rect.height / canvas.height;
      for (const item of canvases.get(canvas)?.values() || []) {
        items.push({
          kind: "text", layer: "canvas", x: rect.left + item.x * sx,
          y: rect.top + scrollY + item.y * sy, text: item.text,
          width: item.width * sx, size: item.size * sy,
        });
      }
    }

    for (const element of chapter?.querySelectorAll(
      ".passage-content [data-wr-role='text'], .passage-content img, .passage-content pre, .passage-content hr"
    ) || []) {
      const rect = element.getBoundingClientRect();
      if (!rect.width || !rect.height || !visible(element)) continue;
      if (element.closest("pre") && element.tagName !== "PRE") continue;
      const style = getComputedStyle(element);
      const size = parseFloat(style.fontSize) || 20;
      const kind = { IMG: "image", HR: "rule", PRE: "code" }[element.tagName] || "text";
      const text = kind === "image" ? element.currentSrc || element.src : element.textContent;
      if (kind === "image" && !/^https?:\/\//.test(text)) continue;
      items.push({
        kind, layer: "dom", id: element.getAttribute("data-wr-id"),
        x: rect.left, y: rect.top + scrollY + (kind === "text" ? size : 0),
        width: rect.width, size, text,
      });
    }

    const scroller = document.scrollingElement;
    return {
      items, access, next: button.includes("下一页"),
      more: button.includes("下一章"),
      top: scrollY, height: scroller.scrollHeight, viewport: innerHeight,
    };
  };
}
