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

# Generate website
website_dir = Path("website")
website_dir.mkdir(exist_ok=True)

index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily News Digest - 每日新闻摘要</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        header p {{ opacity: 0.9; font-size: 1.1em; }}
        .lang-switch {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .lang-switch a {{
            background: white;
            color: #667eea;
            padding: 8px 20px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
        }}
        .lang-switch a.active {{
            background: #667eea;
            color: white;
        }}
        .news-content {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .news-content h1, .news-content h2, .news-content h3 {{
            color: #333;
            margin: 20px 0 10px 0;
        }}
        .news-content a {{
            color: #667eea;
            text-decoration: none;
        }}
        .news-content a:hover {{ text-decoration: underline; }}
        .highlights {{
            background: #f8f9ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 0 10px 10px 0;
        }}
        .highlights h2 {{ color: #667eea; margin-bottom: 15px; }}
        .highlights ul {{ list-style: none; padding-left: 20px; }}
        .highlights li {{ padding: 8px 0; }}
        .highlights li:before {{ content: "🔥"; margin-right: 8px; }}
        footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        .news-item {{
            padding: 20px 0;
            border-bottom: 1px solid #eee;
        }}
        .news-item:last-child {{ border-bottom: none; }}
        .meta {{ font-size: 0.9em; color: #666; margin: 5px 0; }}
    </style>
</head>
<body>
    <header>
        <h1>📰 Daily News Digest</h1>
        <p>每日新闻摘要 · 中英双语版</p>
    </header>
    <div class="lang-switch">
        <a href="index.html" class="active">中文</a>
        <a href="index.en.html">English</a>
    </div>
    <div class="news-content">
        {md_cn.replace("# 📰 每日新闻摘要 · ", "<h1>📰 ").replace("## ", "</h1><h2>").replace("### ", "</h2><h3>").replace("\n\n", "</p><p>")}
    </div>
    <footer>
        <p>Automatically generated · 自动生成</p>
        <p><a href="https://github.com/Rito-w/daily-news-digest" target="_blank">GitHub</a> · 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </footer>
</body>
</html>
"""

index_en_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily News Digest</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        header p {{ opacity: 0.9; font-size: 1.1em; }}
        .lang-switch {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .lang-switch a {{
            background: white;
            color: #667eea;
            padding: 8px 20px;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
        }}
        .lang-switch a.active {{
            background: #667eea;
            color: white;
        }}
        .news-content {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .news-content h1, .news-content h2, .news-content h3 {{
            color: #333;
            margin: 20px 0 10px 0;
        }}
        .news-content a {{
            color: #667eea;
            text-decoration: none;
        }}
        .news-content a:hover {{ text-decoration: underline; }}
        .highlights {{
            background: #f8f9ff;
            border-left: 4px solid #667eea;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 0 10px 10px 0;
        }}
        .highlights h2 {{ color: #667eea; margin-bottom: 15px; }}
        .highlights ul {{ list-style: none; padding-left: 20px; }}
        .highlights li {{ padding: 8px 0; }}
        .highlights li:before {{ content: "🔥"; margin-right: 8px; }}
        footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        .news-item {{
            padding: 20px 0;
            border-bottom: 1px solid #eee;
        }}
        .news-item:last-child {{ border-bottom: none; }}
        .meta {{ font-size: 0.9em; color: #666; margin: 5px 0; }}
    </style>
</head>
<body>
    <header>
        <h1>📰 Daily News Digest</h1>
        <p>English Version · 英文版</p>
    </header>
    <div class="lang-switch">
        <a href="index.html">中文</a>
        <a href="index.en.html" class="active">English</a>
    </div>
    <div class="news-content">
        {md_en.replace("# 📰 Daily News Digest · ", "<h1>📰 ").replace("## ", "</h1><h2>").replace("### ", "</h2><h3>").replace("\n\n", "</p><p>")}
    </div>
    <footer>
        <p>Automatically generated</p>
        <p><a href="https://github.com/Rito-w/daily-news-digest" target="_blank">GitHub</a> · Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </footer>
</body>
</html>
"""

(website_dir / "index.html").write_text(index_html, encoding="utf-8")
(website_dir / "index.en.html").write_text(index_en_html, encoding="utf-8")

print("✅ Website generated")
