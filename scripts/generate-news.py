#!/usr/bin/env python3
"""每日新闻生成脚本 - 中英双语"""

import feedparser
from datetime import datetime
from pathlib import Path

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
            "source": feed.feed.get("title", "Unknown"),
            "published": entry.get("published", "")
        })

date = datetime.now().strftime("%Y-%m-%d")
date_cn = datetime.now().strftime("%Y年%m月%d日")

# Generate Chinese version
md_cn = f"""# 📰 每日新闻摘要 · {date_cn}

*更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}*

---

## 🔥 今日看点

- AI 技术持续突破，多个大模型更新
- 开发者工具在 GitHub 持续走俏
- 开源社区保持活跃

## 📋 新闻列表

"""

for i, article in enumerate(articles[:15], 1):
    md_cn += f"### {i}. [{article['title']}]({article['link']})\n\n"
    md_cn += f"**来源：** {article['source']}  \n"
    md_cn += f"**时间：** {article['published']}  \n\n"
    if article['summary']:
        md_cn += f"**摘要：** {article['summary']}...  \n\n"
    md_cn += "---\n\n"

md_cn += f"\n*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

# Generate English version
md_en = f"""# 📰 Daily News Digest · {date}

*Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}*

---

## 🔥 Highlights

- AI technology continues to breakthrough
- Developer tools trending on GitHub
- Open source community remains active

## 📋 News List

"""

for i, article in enumerate(articles[:15], 1):
    md_en += f"### {i}. [{article['title']}]({article['link']})\n\n"
    md_en += f"**Source:** {article['source']}  \n"
    md_en += f"**Published:** {article['published']}  \n\n"
    if article['summary']:
        md_en += f"**Summary:** {article['summary']}...  \n\n"
    md_en += "---\n\n"

md_en += f"\n*Auto-generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

# Save files
news_dir = Path("news")
news_dir.mkdir(exist_ok=True)

(news_dir / f"{date}.zh.md").write_text(md_cn, encoding="utf-8")
(news_dir / f"{date}.en.md").write_text(md_en, encoding="utf-8")
(news_dir / "latest.zh.md").write_text(md_cn, encoding="utf-8")
(news_dir / "latest.en.md").write_text(md_en, encoding="utf-8")

print(f"✅ Generated news for {date}")
print(f"📊 Total articles: {len(articles)}")
