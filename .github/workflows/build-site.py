#!/usr/bin/env python3
"""从 Markdown 生成网站 - 简洁专业风格"""

from datetime import datetime
from pathlib import Path
import re

# Read latest news
try:
    with open("news/latest.zh.md", "r", encoding="utf-8") as f:
        news_zh = f.read()
    with open("news/latest.en.md", "r", encoding="utf-8") as f:
        news_en = f.read()
    
    # Generate history list
    news_dir = Path("news")
    history_items = []
    for file in sorted(news_dir.glob("*.zh.md"), reverse=True):
        if file.name != "latest.zh.md" and file.name != "HISTORY.md":
            date = file.stem
            history_items.append({
                "date": date,
                "zh": file.name,
                "en": f"{date}.en.md"
            })
except:
    news_zh = "# 暂无新闻\n\n新闻将在每天早上生成"
    news_en = "# No news yet\n\nNews will be generated daily"
    history_items = []

# Simple Markdown to HTML
def md_to_html(md):
    html = md
    # Headers
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', html)
    # Horizontal rule
    html = html.replace("---", "<hr>")
    # Line breaks
    html = html.replace("\n\n", "</p><p>")
    return f"<p>{html}</p>"

def generate_html(content, lang="zh"):
    if lang == "zh":
        title = "每日新闻摘要"
        subtitle = "中英双语版"
        zh_active = 'class="active"'
        en_active = ''
        footer_text = "自动生成"
        time_label = "更新时间"
    else:
        title = "Daily News Digest"
        subtitle = "English Version"
        zh_active = ''
        en_active = 'class="active"'
        footer_text = "Automatically generated"
        time_label = "Updated"
    
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --text: #1f2937;
            --text-light: #6b7280;
            --bg: #ffffff;
            --bg-alt: #f9fafb;
            --border: #e5e7eb;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.7;
            color: var(--text);
            background: var(--bg-alt);
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        header {{
            background: var(--bg);
            border-bottom: 1px solid var(--border);
            padding: 30px 0;
        }}
        header h1 {{
            font-size: 1.8em;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 5px;
        }}
        header p {{
            color: var(--text-light);
            font-size: 1em;
        }}
        .nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid var(--border);
            background: var(--bg);
        }}
        .nav-links {{
            display: flex;
            gap: 20px;
        }}
        .nav-links a {{
            color: var(--text-light);
            text-decoration: none;
            font-size: 0.95em;
            transition: color 0.2s;
        }}
        .nav-links a:hover {{
            color: var(--primary);
        }}
        .nav-links a.active {{
            color: var(--primary);
            font-weight: 600;
        }}
        .lang-switch {{
            display: flex;
            gap: 10px;
        }}
        .lang-switch a {{
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.9em;
            font-weight: 500;
            transition: all 0.2s;
        }}
        .lang-switch a {{
            background: var(--bg-alt);
            color: var(--text-light);
        }}
        .lang-switch a.active {{
            background: var(--primary);
            color: white;
        }}
        main {{
            padding: 30px 0;
        }}
        .content {{
            background: var(--bg);
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .content h1 {{
            font-size: 1.6em;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border);
        }}
        .content h2 {{
            font-size: 1.3em;
            margin: 30px 0 15px 0;
            color: var(--text);
        }}
        .content h3 {{
            font-size: 1.1em;
            margin: 25px 0 10px 0;
        }}
        .content h3 a {{
            color: var(--primary);
            text-decoration: none;
        }}
        .content h3 a:hover {{
            text-decoration: underline;
        }}
        .content p {{
            margin: 10px 0;
            color: var(--text);
        }}
        .content strong {{
            color: var(--text);
            font-weight: 600;
        }}
        .content hr {{
            border: none;
            border-top: 1px solid var(--border);
            margin: 25px 0;
        }}
        .meta {{
            font-size: 0.9em;
            color: var(--text-light);
            margin: 5px 0;
        }}
        .highlights {{
            background: var(--bg-alt);
            border-left: 3px solid var(--primary);
            padding: 20px;
            margin: 25px 0;
            border-radius: 0 8px 8px 0;
        }}
        .highlights h2 {{
            margin-top: 0;
            color: var(--primary);
            font-size: 1.1em;
        }}
        .highlights ul {{
            list-style: none;
            padding-left: 0;
        }}
        .highlights li {{
            padding: 6px 0;
            padding-left: 24px;
            position: relative;
        }}
        .highlights li:before {{
            content: "•";
            color: var(--primary);
            font-weight: bold;
            position: absolute;
            left: 0;
        }}
        .news-item {{
            padding: 20px 0;
        }}
        footer {{
            text-align: center;
            padding: 30px 0;
            color: var(--text-light);
            font-size: 0.9em;
            border-top: 1px solid var(--border);
            margin-top: 40px;
        }}
        footer a {{
            color: var(--primary);
            text-decoration: none;
        }}
        footer a:hover {{
            text-decoration: underline;
        }}
        .history-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .history-table th,
        .history-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        .history-table th {{
            background: var(--bg-alt);
            font-weight: 600;
            color: var(--text-light);
        }}
        .history-table a {{
            color: var(--primary);
            text-decoration: none;
        }}
        @media (max-width: 600px) {{
            .content {{
                padding: 25px;
            }}
            header h1 {{
                font-size: 1.5em;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    </header>
    
    <nav class="nav">
        <div class="container" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="nav-links">
                <a href="index.html">首页</a>
                <a href="history.html">历史</a>
            </div>
            <div class="lang-switch">
                <a href="index.html" {zh_active}>中文</a>
                <a href="index.en.html" {en_active}>English</a>
            </div>
        </div>
    </nav>
    
    <main class="container">
        <div class="content">
            {md_to_html(content)}
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>{footer_text} · <a href="https://github.com/Rito-w/daily-news-digest" target="_blank" rel="noopener">GitHub</a> · {time_label}: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </div>
    </footer>
</body>
</html>
"""

def generate_history_html(items, lang="zh"):
    if lang == "zh":
        title = "历史新闻"
        subtitle = "每日新闻摘要"
        zh_active = 'class="active"'
        en_active = ''
        table_header = "| 日期 | 中文版 | English |"
    else:
        title = "History"
        subtitle = "Daily News Digest"
        zh_active = ''
        en_active = 'class="active"'
        table_header = "| Date | Chinese | English |"
    
    rows = ""
    for item in items:
        rows += f'<tr><td>{item["date"]}</td><td><a href="{item["zh"]}">{item["date"]}.zh</a></td><td><a href="{item["en"]}">{item["date"]}.en</a></td></tr>\n'
    
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --text: #1f2937;
            --text-light: #6b7280;
            --bg: #ffffff;
            --bg-alt: #f9fafb;
            --border: #e5e7eb;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.7;
            color: var(--text);
            background: var(--bg-alt);
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        header {{
            background: var(--bg);
            border-bottom: 1px solid var(--border);
            padding: 30px 0;
        }}
        header h1 {{
            font-size: 1.8em;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 5px;
        }}
        header p {{
            color: var(--text-light);
            font-size: 1em;
        }}
        .nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 1px solid var(--border);
            background: var(--bg);
        }}
        .nav-links {{
            display: flex;
            gap: 20px;
        }}
        .nav-links a {{
            color: var(--text-light);
            text-decoration: none;
            font-size: 0.95em;
            transition: color 0.2s;
        }}
        .nav-links a:hover {{
            color: var(--primary);
        }}
        .nav-links a.active {{
            color: var(--primary);
            font-weight: 600;
        }}
        .lang-switch {{
            display: flex;
            gap: 10px;
        }}
        .lang-switch a {{
            padding: 6px 12px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 0.9em;
            font-weight: 500;
            transition: all 0.2s;
        }}
        .lang-switch a {{
            background: var(--bg-alt);
            color: var(--text-light);
        }}
        .lang-switch a.active {{
            background: var(--primary);
            color: white;
        }}
        main {{
            padding: 30px 0;
        }}
        .content {{
            background: var(--bg);
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .content h1 {{
            font-size: 1.6em;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid var(--border);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background: var(--bg-alt);
            font-weight: 600;
            color: var(--text-light);
        }}
        a {{
            color: var(--primary);
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        footer {{
            text-align: center;
            padding: 30px 0;
            color: var(--text-light);
            font-size: 0.9em;
            border-top: 1px solid var(--border);
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    </header>
    
    <nav class="nav">
        <div class="container" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
            <div class="nav-links">
                <a href="index.html">首页</a>
                <a href="history.html" class="active">历史</a>
            </div>
            <div class="lang-switch">
                <a href="history.html" {zh_active}>中文</a>
                <a href="history.en.html" {en_active}>English</a>
            </div>
        </div>
    </nav>
    
    <main class="container">
        <div class="content">
            <h1>{title}</h1>
            <table>
                <thead>
                    <tr>
                        <th>日期</th>
                        <th>中文版</th>
                        <th>English</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>Automatically generated · <a href="https://github.com/Rito-w/daily-news-digest" target="_blank">GitHub</a></p>
        </div>
    </footer>
</body>
</html>
"""

# Generate pages
website_dir = Path("website")
website_dir.mkdir(exist_ok=True)
(website_dir / "index.html").write_text(generate_html(news_zh, "zh"), encoding="utf-8")
(website_dir / "index.en.html").write_text(generate_html(news_en, "en"), encoding="utf-8")
(website_dir / "history.html").write_text(generate_history_html(history_items, "zh"), encoding="utf-8")
(website_dir / "history.en.html").write_text(generate_history_html(history_items, "en"), encoding="utf-8")

print("✅ Website built")
