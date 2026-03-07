#!/bin/bash
# 设置本地 cron 定时任务脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_CMD="python3"

# 检查 Python
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ 未找到 Python3，请安装后重试"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
$PYTHON_CMD -m pip install -q -r "$PROJECT_DIR/requirements.txt"

# 创建 cron 任务
CRON_JOB="0 8 * * * cd $PROJECT_DIR && $PYTHON_CMD scripts/fetch-news.py && git add -A && git commit -m \"docs: 每日新闻 \$(date +\\%Y-\\%m-\\%d)\" && git push origin main"

# 检查是否已存在
if crontab -l 2>/dev/null | grep -q "daily-news-digest"; then
    echo "⚠️  Cron 任务已存在"
    crontab -l | grep "daily-news-digest"
else
    # 添加 cron 任务
    (crontab -l 2>/dev/null | grep -v "daily-news-digest"; echo "$CRON_JOB") | crontab -
    echo "✅ Cron 任务已添加："
    echo "   每天 8:00 AM 自动抓取新闻并推送"
fi

echo ""
echo "📋 当前 cron 任务列表："
crontab -l | grep "daily-news-digest" || echo "无"

echo ""
echo "💡 手动运行测试："
echo "   cd $PROJECT_DIR && python3 scripts/fetch-news.py"
