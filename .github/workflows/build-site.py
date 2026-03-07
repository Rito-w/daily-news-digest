#!/usr/bin/env python3
"""从 Markdown 生成网站"""

from datetime import datetime
from pathlib import Path

# Read latest news
try:
    with open("news/latest.zh.md", "r", encoding="utf-8") as f:
        news_zh = f.read()
    with open("news/latest.en.md", "r", encoding="utf-8") as f:
        news_en = f.read()
except:
    news_zh = "# 暂无新闻\n\n新闻将在每天早上生成"
    news_en = "# No news yet\n\nNews will be generated daily"

# Simple Markdown to HTML
def md_to_html(md):
    html = md
    # Headers
    html = html.replace("# ", "<h1>").replace("\n", "</h1>\n")
    html = html.replace("## ", "<h2>").replace("\n", "</h2>\n")
    html = html.replace("### ", "<h3>").replace("\n", "</h3>\n")
    # Bold
    html = html.replace("**", "<strong>", 1).replace("**", "</strong>", 1)
    # Links
    import re
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank">\1</a>', html)
    # Line breaks
    html = html.replace("---", "<hr>")
    return html

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
        {md_to_html(news_zh)}
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
        {md_to_html(news_en)}
    </div>
    <footer>
        <p>Automatically generated</p>
        <p><a href="https://github.com/Rito-w/daily-news-digest" target="_blank">GitHub</a> · Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </footer>
</body>
</html>
"""

Path("website").mkdir(exist_ok=True)
Path("website/index.html").write_text(index_html, encoding="utf-8")
Path("website/index.en.html").write_text(index_en_html, encoding="utf-8")

print("✅ Website built")
