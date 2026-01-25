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

**macOS / Linux:**
```bash
git clone https://github.com/semicolonstail/weread-exporter-skill.git
cd weread-exporter
./install.sh
```

**Windows:**
```cmd
git clone https://github.com/semicolonstail/weread-exporter-skill.git
cd weread-exporter
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

### ⚠️ 重要：首次使用需要登录

**首次运行必须登录微信读书账号：**

1. 工具会自动打开 Chrome/Chromium 浏览器窗口
2. 屏幕上会显示微信登录二维码
3. 使用**微信手机 App** 扫描二维码进行登录
4. 登录成功后，导出流程将自动开始
5. 登录状态会被保存，后续导出无需再次登录

如果未登录，导出将失败。请在看到二维码提示时完成登录。

### 在 Claude Code 中使用

```
Export the WeRead book with ID 08232ac0720befa90825d88 to epub and pdf formats
```

### 命令行使用

```bash
# 基础用法
python -m weread_exporter -b <book_id> -o epub -o pdf

# 无头模式（不显示浏览器）
python -m weread_exporter -b <book_id> -o epub --headless

# 自定义超时时间
python -m weread_exporter -b <book_id> -o epub --load-timeout 120

# 自定义登录超时时间（默认 60 秒）
python -m weread_exporter -b <book_id> -o epub --login-timeout 120
```

### 获取书籍 ID

1. 访问 https://weread.qq.com/
2. 搜索目标书籍
3. 打开书籍详情页
4. URL 格式：`https://weread.qq.com/web/bookDetail/08232ac0720befa90825d88`
5. 书籍 ID 就是 `/web/bookDetail/` 后面的部分（如 `08232ac0720befa90825d88`）

## 📦 输出格式说明

| 格式 | 说明 | 推荐场景 |
|------|------|----------|
| EPUB | 适合手机端访问 | 手机、平板阅读 |
| PDF | 适合电脑端访问 | 电脑、打印 |
| MOBI | 适合 Kindle 访问 | Kindle 设备（仅限 Linux） |
| TXT | 纯文本格式 | 快速查看、文本分析 |
| Markdown | Markdown 格式 | 二次编辑、转换 |

导出的文件保存在 `./output/` 目录

## 📌 注意事项

- **登录要求**：首次运行会打开浏览器显示微信登录二维码，请使用微信手机 App 扫码登录
- **浏览器要求**：需要安装 Chrome 或 Chromium 浏览器
- **登录状态**：首次登录后会保存登录状态，后续使用无需重复登录
- **付费章节**：如果书籍包含付费章节，工具会在遇到付费内容时自动停止并提示登录
- **无限循环保护**：工具内置了多重检测机制，防止在免费章节末尾无限循环：
  - 检测登录提示文字（"登录后阅读"、"请登录"等）
  - 检测重复章节内容
  - 限制单章最大页数（50页）
- **无头模式**：服务器环境建议使用 `--headless` 参数（但需确保已完成首次登录）
- **大文件导出**：书籍页数较多时，导出时间会较长，请耐心等待
- **格式限制**：导出 PDF 时会自动先生成 EPUB（转换需要）

## 🔧 实现原理

通过 Hook Web 页面中的 Canvas 函数，获取绘制到 Canvas 中的文本及样式等信息，转换成 markdown 格式，保存到本地文件，然后再转换成最终的 EPUB 或 PDF 格式，而 MOBI 格式则是使用 kindlegen 工具从 EPUB 格式转换来的。

## 🛠️ 开发

```bash
# 克隆仓库
git clone https://github.com/semicolonstail/weread-exporter-skill.git
cd weread-exporter

# 安装开发依赖
pip3 install -e .

# 运行测试
pytest
```

## 📝 命令行参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `-b, --book-id` | string | 是 | - | 微信读书书籍 ID |
| `-o, --output` | string | 否 | epub, pdf | 输出格式：epub, pdf, mobi, txt, md |
| `--headless` | boolean | 否 | false | 无头模式运行 |
| `--force-login` | boolean | 否 | true | 强制登录 |
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
