# WeRead Exporter

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-purple)](https://claude.ai/download)

> 微信读书书籍导出工具 - 支持导出为 EPUB、PDF、MOBI、TXT、Markdown 格式

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
git clone https://github.com/yourusername/weread-exporter.git
cd weread-exporter
./install.sh
```

**Windows:**
```cmd
git clone https://github.com/yourusername/weread-exporter.git
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

## 🔧 实现原理

通过 Hook Web 页面中的 Canvas 函数，获取绘制到 Canvas 中的文本及样式等信息，转换成 markdown 格式，保存到本地文件，然后再转换成最终的 EPUB 或 PDF 格式，而 MOBI 格式则是使用 kindlegen 工具从 EPUB 格式转换来的。

## 🛠️ 开发

```bash
# 克隆仓库
git clone https://github.com/yourusername/weread-exporter.git
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
- 项目链接：[https://github.com/yourusername/weread-exporter](https://github.com/yourusername/weread-exporter)

---

如果这个项目对您有帮助，请给一个 ⭐️ Star！
