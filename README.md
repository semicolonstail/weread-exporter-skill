# WeRead Exporter

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-purple)](https://claude.ai/download)

> 微信读书书籍导出工具 - 支持导出为 EPUB、PDF、MOBI、TXT、Markdown 格式

**关键词**：微信读书导出、weread exporter、微信读书下载、epub转换、pdf转换、kindle、claude code skill、书籍导出、电子书转换

[![GitHub stars](https://img.shields.io/github/stars/semicolonstail/weread-exporter-skill?style=social)](https://github.com/semicolonstail/weread-exporter-skill/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/semicolonstail/weread-exporter-skill?style=social)](https://github.com/semicolonstail/weread-exporter-skill/network/members)

## ✨ 特性

- 📚 **多格式导出**：支持 EPUB、PDF、MOBI、TXT、Markdown 格式
- 🤖 **Claude Code 集成**：可作为 Claude Code Skill 使用，自然语言导出书籍
- 🖥️ **命令行工具**：独立的命令行工具，支持多种参数配置
- 🌐 **智能抓取**：通过 Hook Canvas 技术获取高质量内容
- 📱 **多平台支持**：支持 macOS、Linux、Windows

## 📸 截图

![WeRead Exporter Screenshot](screenshot.jpg)

## 🚀 快速开始

### 方式一：一键安装（推荐）

从当前仓库的 Code 菜单复制克隆链接，克隆后进入仓库目录。

**macOS / Linux:**
```bash
./install.sh
```

**Windows:**
```cmd
install.bat
```

### 方式二：手动安装

```bash
# 安装 Python 依赖
pip3 install -e .

# Claude Code 会自动检测项目中的 .mcp.json 配置
```

详细安装说明请查看 [INSTALL.md](INSTALL.md)

## 📖 使用方法

### 登录和导出

安装 Chrome 或 Chromium 后，在同一个目录中登录和导出。首次使用或会话过期时，运行登录命令，用手机微信扫描浏览器中的二维码并确认。

```bash
python -m weread_exporter.login
python -m weread_exporter -b 'BOOK_URL_OR_ID' -o epub
```

`-b` 接受微信读书官网的书籍详情页、阅读页链接或书籍 ID。只有书名时，可先在 [微信读书](https://weread.qq.com/) 搜索对应版本。

登录后可用 `--headless` 在后台导出，或重复 `-o` 选择多种格式。

```bash
python -m weread_exporter --headless -b 'BOOK_URL_OR_ID' -o epub -o pdf
```

如需在导出命令中重新扫码，使用 `--force-login` 并保留可见的浏览器窗口。

### 在 Claude Code 中使用

```
Export the WeRead book with ID 08232ac0720befa90825d88 to epub and pdf formats
```

## 📦 输出格式说明

| 格式 | 说明 | 推荐场景 |
|------|------|----------|
| EPUB | 适合手机端访问 | 手机、平板阅读 |
| PDF | 适合电脑端访问 | 电脑、打印 |
| MOBI | 适合 Kindle 访问 | Kindle 设备（仅限 Linux） |
| TXT | 纯文本格式 | 快速查看、文本分析 |
| Markdown | Markdown 格式 | 二次编辑、转换 |

EPUB、PDF、MOBI 和 TXT 写入 `output/`。逐章 Markdown 保存在 `cache/web-reader/BOOK_ID/chapters/`。登录会话保存在当前目录的 `cache/cookie.txt`，请保留在本机。

## 🔧 实现原理

导出器为 Chrome 创建独立的临时配置，按网页阅读器的目录逐章加载已获授权的内容，采集画布及页面渲染的文字和图片。遇到访问限制或章节加载失败时会停止。MOBI 由 Linux 上的 kindlegen 将 EPUB 转换得到。

## 🛠️ 开发

```bash
# 在仓库根目录安装开发依赖
pip3 install -e .

# 运行测试
pytest
```

## 📝 命令行参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `-b, --book-id` | string | 是 | - | 微信读书官网书籍链接或 ID |
| `-o, --output-format` | string | 否 | epub | 支持 epub、pdf、mobi、txt、md，可重复指定 |
| `--headless` | boolean | 否 | false | 无头模式运行 |
| `--force-login` | boolean | 否 | false | 打开可见浏览器重新扫码 |
| `--login-timeout` | int | 否 | 60 | 登录超时时间（秒） |
| `--load-timeout` | int | 否 | 60 | 加载超时时间（秒） |
| `--load-interval` | int | 否 | 30 | 加载间隔时间（秒） |

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## ⚠️ 免责声明

本工具仅作技术研究之用，请勿用于商业或违法用途。由于使用本工具导致的侵权或其它问题，本工具不承担任何责任！

## 🙏 致谢

- 原项目：[drunkdream/weread-exporter](https://github.com/drunkdream/weread-exporter)
- Claude Code Skill 扩展

## 📮 联系方式

- 作者：xujinmeng
- 项目链接：[https://github.com/semicolonstail/weread-exporter-skill](https://github.com/semicolonstail/weread-exporter-skill)

---

如果这个项目对您有帮助，请给一个 ⭐️ Star！
