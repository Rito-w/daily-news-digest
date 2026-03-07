#!/usr/bin/env python3
"""从主会话历史同步 AI 简报到 GitHub"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
import sys

NEWS_DIR = Path("/Volumes/myDisk/workplace/daily-news-digest/news")
NEWS_DIR.mkdir(parents=True, exist_ok=True)

def get_main_session_key():
    """获取主会话 key"""
    result = subprocess.run(
        ["openclaw", "sessions", "list", "--json"],
        capture_output=True, text=True
    )
    sessions = json.loads(result.stdout)
    for s in sessions.get("sessions", []):
        if s.get("channel") == "qqbot":
            return s.get("key")
    return None

def get_session_history(session_key, limit=50):
    """获取会话历史"""
    result = subprocess.run(
        ["openclaw", "sessions", "history", "--json", "--limit", str(limit), session_key],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def extract_news_from_history(history):
    """从历史中提取 AI 简报"""
    news = []
    for msg in history.get("messages", []):
        content = msg.get("content", "")
        if "📰" in content or "今日看点" in content:
            news.append(content)
    return "\n\n".join(news[-2:])  # 取最近 2 条

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today}] 同步 AI 简报到 GitHub...")
    
    session_key = get_main_session_key()
    if not session_key:
        print("❌ 未找到主会话")
        return 1
    
    history = get_session_history(session_key, limit=100)
    news = extract_news_from_history(history)
    
    if not news:
        print("⚠️ 未找到今日新闻")
        return 0
    
    # 保存中文版
    zh_file = NEWS_DIR / f"{today}.zh.md"
    zh_file.write_text(f"# 📰 每日新闻 · {today}\n\n{news}\n", encoding="utf-8")
    
    # 保存英文版（暂用中文）
    en_file = NEWS_DIR / f"{today}.en.md"
    en_file.write_text(f"# 📰 Daily News · {today}\n\n{news}\n", encoding="utf-8")
    
    print(f"✅ {zh_file.name}")
    print(f"✅ {en_file.name}")
    
    # 推送到 GitHub
    print("📤 推送到 GitHub...")
    subprocess.run(
        ["git", "add", "-A"],
        cwd="/Volumes/myDisk/workplace/daily-news-digest"
    )
    subprocess.run(
        ["git", "commit", "-m", f"docs: {today}"],
        cwd="/Volumes/myDisk/workplace/daily-news-digest"
    )
    subprocess.run(
        ["git", "push"],
        cwd="/Volumes/myDisk/workplace/daily-news-digest"
    )
    
    print("✅ 推送完成")
    return 0

if __name__ == "__main__":
    sys.exit(main())
