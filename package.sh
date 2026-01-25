#!/bin/bash
# 打包脚本 - 创建可分享的分发包

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  WeRead Exporter 打包脚本${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# 获取版本号
VERSION=$(python3 -c 'import weread_exporter; print(weread_exporter.VERSION)' 2>/dev/null || echo "latest")
PACKAGE_NAME="weread-exporter-${VERSION}"
DIST_DIR="dist"

# 创建临时目录
echo -e "${YELLOW}创建分发包...${NC}"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# 复制必要文件
echo -e "${YELLOW}复制文件...${NC}"
rsync -av --exclude='*.pyc' \
  --exclude='__pycache__' \
  --exclude='.git' \
  --exclude='*.log' \
  --exclude='venv' \
  --exclude='.DS_Store' \
  --exclude='output' \
  --exclude='cache' \
  --exclude='build' \
  --exclude='*.egg-info' \
  --exclude='.pytest_cache' \
  . "$DIST_DIR/$PACKAGE_NAME/"

# 创建压缩包
echo -e "${YELLOW}创建压缩包...${NC}"
cd "$DIST_DIR"
tar -czf "${PACKAGE_NAME}.tar.gz" "$PACKAGE_NAME"
zip -rq "${PACKAGE_NAME}.zip" "$PACKAGE_NAME"
cd ..

# 显示结果
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  打包完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "生成的文件："
echo "  - ${DIST_DIR}/${PACKAGE_NAME}.tar.gz"
echo "  - ${DIST_DIR}/${PACKAGE_NAME}.zip"
echo ""
echo "分享给朋友后，他们只需："
echo "  1. 解压文件"
echo "  2. 运行 ./install.sh (macOS/Linux) 或 install.bat (Windows)"
echo ""
echo -e "${GREEN}完成！${NC}"
