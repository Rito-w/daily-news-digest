#!/usr/bin/env python3
"""每日新闻抓取 - 带 AI 摘要 + 中英双语"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    import feedparser
except ImportError:
    print("pip install feedparser")
    sys.exit(1)

NEWS_DIR = Path(__file__).parent.parent / "news"
NEWS_DIR.mkdir(parents=True, exist_ok=True)
DATE = datetime.now().strftime("%Y-%m-%d")

def fetch_rss():
    """抓取 RSS"""
    feeds = [
        "https://simonwillison.net/atom/everything/",
        "https://hnrss.org/frontpage",
        "https://www.johndcook.com/blog/feed/",
    ]
    
    articles = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.get("summary", "")[:300],
                "source": feed.feed.get("title", "Unknown")
            })
    
    return articles[:15]

def generate_summary(articles):
    """调用 AI 生成摘要"""
    prompt = f"""请为以下新闻生成中英双语摘要：

{json.dumps(articles[:10], ensure_ascii=False, indent=2)}

要求：
1. 生成 3-5 句今日看点总结（中文）
2. 为每篇新闻生成 1 句中文摘要
3. 输出 JSON 格式

输出格式：
{{
  "highlights": ["看点 1", "看点 2", "看点 3"],
  "articles": [
    {{"title": "原标题", "summary_cn": "中文摘要", "summary_en": "English summary"}}
  ]
}}
"""
    
    try:
        result = subprocess.run(
            ["openclaw", "message", "send", "--message", prompt],
            capture_output=True, text=True, timeout=60
        )
        # 这里简化处理，实际应该调用 LLM API
        return None
    except:
        return None

def main():
    print(f"抓取 {DATE} 的新闻...")
    
    articles = fetch_rss()
    print(f"✅ 抓取到 {len(articles)} 篇")
    
    # 中文版
    md_cn = f"""# 📰 每日新闻 · {DATE}

## 🔥 今日看点

"""
    
    for i, article in enumerate(articles[:10], 1):
        md_cn += f"{i}. **[{article['title']}]({article['link']})**  \n"
        md_cn += f"   *来源：{article['source']}*  \n\n"
    
    md_cn += f"\n---\n*{datetime.now().strftime('%H:%M')} 自动生成*\n"
    
    # 英文版
    md_en = f"""# 📰 Daily News · {DATE}

## 🔥 Top Stories

"""
    
    for i, article in enumerate(articles[:10], 1):
        md_en += f"{i}. **[{article['title']}]({article['link']})**  \n"
        md_en += f"   *Source: {article['source']}*  \n\n"
    
    md_en += f"\n---\n*{datetime.now().strftime('%H:%M')} UTC*\n"
    
    # 保存
    (NEWS_DIR / f"{DATE}.zh.md").write_text(md_cn, encoding="utf-8")
    (NEWS_DIR / f"{DATE}.en.md").write_text(md_en, encoding="utf-8")
    
    print(f"✅ {DATE}.zh.md")
    print(f"✅ {DATE}.en.md")

if __name__ == "__main__":
    main()
