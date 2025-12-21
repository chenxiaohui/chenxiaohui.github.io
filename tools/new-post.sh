#!/bin/bash

# 创建新博客文章的脚本
# Usage: ./tools/new-post.sh "文章标题"

set -e

# 检查参数
if [ -z "$1" ]; then
    echo "使用方法: ./tools/new-post.sh \"文章标题\""
    echo "示例: ./tools/new-post.sh \"我的新文章\""
    exit 1
fi

TITLE="$1"

# 生成 slug (小写,空格替换为连字符,移除特殊字符)
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')

# 获取当前日期
DATE=$(date +%Y-%m-%d)
DATETIME=$(date "+%Y-%m-%d %H:%M")
DATEONLY=$(date +%Y%m%d)

# 生成文件名
FILENAME="_posts/${DATE}-${SLUG}.md"

# 检查文件是否已存在
if [ -f "$FILENAME" ]; then
    echo "错误: 文件已存在: $FILENAME"
    exit 1
fi

# 创建文件内容
cat > "$FILENAME" <<EOF
---
layout: article
title: "$TITLE"
key: $SLUG
date: $DATETIME
published: true
categories: "技术"
comments: true
---

这里写文章摘要...

<!--more-->

## 正文标题

这里是文章正文内容...

EOF

echo "✓ 创建新文章: $FILENAME"
echo "✓ 标题: $TITLE"
echo "✓ 日期: $DATETIME"
echo ""
echo "后续步骤:"
echo "  1. 编辑文章: $FILENAME"
echo "  2. 本地预览: bun run serve"
echo "  3. 提交发布: git add $FILENAME && git commit -m 'modify $DATEONLY' && git push"

# 如果系统有 code 命令 (VS Code),自动打开文件
if command -v code &> /dev/null; then
    echo ""
    echo "正在用 VS Code 打开文件..."
    code "$FILENAME"
fi
