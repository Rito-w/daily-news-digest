#!/usr/bin/env python3
"""每日新闻抓取 - 同步到 GitHub"""

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
OUTPUT_FILE = NEWS_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.md"


def fetch_news():
    """抓取新闻"""
    feeds = [
        "https://simonwillison.net/atom/everything/",
        "https://hnrss.org/frontpage",
    ]
    
    news = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            news.append(f"- [{entry.title}]({entry.link})")
    
    return news

def main():
    date = datetime.now().strftime("%Y-%m-%d")
    print(f"抓取 {date} 的新闻...")
    
    news = fetch_news()
    
    md = f"# 📰 Daily News · {date}\n\n"
    md += "\n".join(news)
    md += f"\n\n*{datetime.now().strftime('%H:%M')}*\n"
    
    OUTPUT_FILE.write_text(md, encoding="utf-8")
    print(f"✅ {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
