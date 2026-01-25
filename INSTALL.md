# WeRead Exporter 快速安装指南

## 一键安装（推荐）

### macOS / Linux

```bash
./install.sh
```

### Windows

```cmd
install.bat
```

---

## 手动安装

如果自动安装失败，可以尝试手动安装：

### 1. 安装 Python 依赖

```bash
pip3 install -e .
```

### 2. 安装 Claude 插件

```bash
claude plugin install --scope user .claude-plugin/
```

---

## 使用方法

### 在 Claude Code 中使用

```
Export the WeRead book with ID 08232ac0720befa90825d88 to epub and pdf formats
```

### 命令行直接使用

```bash
# 导出为 epub
python -m weread_exporter -b <book_id> -o epub

# 导出为多种格式
python -m weread_exporter -b <book_id> -o epub -o pdf -o txt

# 无头模式（不显示浏览器窗口）
python -m weread_exporter -b <book_id> -o epub --headless
```

---

## 获取书籍 ID

1. 访问 https://weread.qq.com/
2. 搜索目标书籍
3. 打开书籍详情页
4. URL 格式：`https://weread.qq.com/web/bookDetail/08232ac0720befa90825d88`
5. 书籍 ID 就是 `/web/bookDetail/` 后面的部分

---

## 支持的导出格式

| 格式 | 说明 |
|------|------|
| epub | 适合移动设备阅读 |
| pdf | 适合桌面端查看 |
| mobi | 适合 Kindle 设备（仅限 Linux） |
| txt | 纯文本格式 |
| md | Markdown 格式 |

---

## 输出位置

导出的文件保存在 `./output/` 目录

---

## 常见问题

### Q: 提示找不到 claude 命令？
A: 请先安装 Claude Code CLI：https://claude.ai/download

### Q: 提示找不到 python3 或 pip3？
A: 请确保已安装 Python 3.7 或更高版本

### Q: 导出失败？
A: 尝试使用 `--headless` 参数，或增加 `--load-timeout` 时间

---

## 免责声明

本工具仅供技术研究使用，请勿用于商业或非法用途。
