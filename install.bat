@echo off
REM WeRead Exporter Installation Script for Windows
REM 一键安装脚本 (Windows)

setlocal enabledelayedexpansion

echo ==========================================
echo   WeRead Exporter 安装向导
echo ==========================================
echo.

REM 检查是否在项目根目录
if not exist "setup.py" (
    echo [错误] 请在项目根目录运行此脚本
    pause
    exit /b 1
)

if not exist ".claude-plugin" (
    echo [错误] 请在项目根目录运行此脚本
    pause
    exit /b 1
)

REM 检查 Python
echo [检查] 正在检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 python，请先安装 Python 3.7 或更高版本
    echo         访问 https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [成功] 找到 Python %PYTHON_VERSION%
echo.

REM 检查 pip
echo [检查] 正在检查 pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 pip
    echo         请确保 Python 安装时选择了 pip 组件
    pause
    exit /b 1
)
echo [成功] pip 已就绪
echo.

REM 安装依赖
echo [安装] 正在安装 Python 依赖包...
pip install -e .
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo [成功] 依赖安装完成
echo.

REM 检查 Claude Code CLI
echo [检查] 正在检查 Claude Code CLI...
claude --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Claude Code CLI
    echo         请访问 https://claude.ai/download 安装 Claude Code
    pause
    exit /b 1
)
echo [成功] Claude Code CLI 已安装
echo.

REM 安装插件
echo [安装] 正在安装 Claude 插件...
claude plugin install --scope user .claude-plugin\
if errorlevel 1 (
    echo [错误] 插件安装失败
    echo         您可以手动运行: claude plugin install --scope user .claude-plugin\
    pause
    exit /b 1
)
echo [成功] 插件安装成功
echo.

REM 显示使用说明
echo ==========================================
echo [成功] 安装完成！
echo ==========================================
echo.
echo 使用方法：
echo   1. 在 Claude Code 中使用：
echo      "Export the WeRead book with ID ^<book_id^> to epub"
echo.
echo   2. 或者直接命令行使用：
echo      python -m weread_exporter -b ^<book_id^> -o epub
echo.
echo   更多信息请查看 INSTALL.md
echo.
pause
