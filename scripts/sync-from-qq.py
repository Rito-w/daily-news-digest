#!/usr/bin/env python3
"""从 QQ Bot 同步新闻到 GitHub"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

NEWS_DIR = Path(__file__).parent.parent / "news"
NEWS_DIR.mkdir(parents=True, exist_ok=True)

def get_today_news():
    """从会话历史获取今日新闻"""
    # 读取今天的会话记录
    sessions_dir = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 查找今天的会话
    for session_file in sessions_dir.glob("*.jsonl"):
        content = session_file.read_text()
        if "AI 简报推送" in content and today in content:
            # 提取新闻内容
            return extract_news(content)
    
    return None

def extract_news(content):
    """从会话内容提取新闻"""
    # 简化处理，实际应该解析 JSONL
    lines = content.split("\n")
    news = []
    for line in lines:
        if "📰" in line or "http" in line:
            news.append(line)
    return "\n".join(news[-50:])  # 取最后 50 行

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"同步 {today} 的新闻...")
    
    news = get_today_news()
    
    if news:
        # 中文版
        (NEWS_DIR / f"{today}.zh.md").write_text(
            f"# 📰 每日新闻 · {today}\n\n{news}\n",
            encoding="utf-8"
        )
        
        # 英文版（简单翻译）
        (NEWS_DIR / f"{today}.en.md").write_text(
            f"# 📰 Daily News · {today}\n\n{news}\n",
            encoding="utf-8"
        )
        
        print(f"✅ 同步完成")
    else:
        print("⚠️ 未找到今日新闻")

if __name__ == "__main__":
    main()
