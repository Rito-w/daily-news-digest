#!/usr/bin/env python3
"""从 Markdown 生成网站"""

from datetime import datetime
from pathlib import Path
import re

# Read latest news
news_dir = Path("news")
news_zh = ""
news_en = ""
history_items = []

try:
    with open(news_dir / "latest.zh.md", "r", encoding="utf-8") as f:
        news_zh = f.read()
    with open(news_dir / "latest.en.md", "r", encoding="utf-8") as f:
        news_en = f.read()
    
    # Generate history list
    for file in sorted(news_dir.glob("*.zh.md"), reverse=True):
        if file.name not in ["latest.zh.md", "HISTORY.md"]:
            date = file.stem
            history_items.append({
                "date": date,
                "zh": file.name,
                "en": f"{date}.en.md"
            })
except Exception as e:
    print(f"⚠️ 读取新闻失败：{e}")
    news_zh = "# 暂无新闻\n\n新闻将在每天早上生成"
    news_en = "# No news yet\n\nNews will be generated daily"

def md_to_html(md):
    """简单 Markdown 转 HTML"""
    html = md
    html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', html)
    html = html.replace("---", "<hr>")
    html = html.replace("\n\n", "</p><p>")
    return f"<p>{html}</p>"

def generate_html(content, lang="zh"):
    """生成 HTML 页面"""
    titles = {
        "zh": ("每日新闻摘要", "中英双语版", "首页", "历史", "中文", "English", "自动生成", "更新时间"),
        "en": ("Daily News Digest", "English Version", "Home", "History", "中文", "English", "Automatically generated", "Updated")
    }
    t = titles[lang]
    active = 'class="active"' if lang == "zh" else ''
    active_en = '' if lang == "zh" else 'class="active"'
    
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t[0]}</title>
    <style>
        :root {{ --primary: #2563eb; --text: #1f2937; --text-light: #6b7280; --bg: #ffffff; --bg-alt: #f9fafb; --border: #e5e7eb; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.7; color: var(--text); background: var(--bg-alt); }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 20px; }}
        header {{ background: var(--bg); border-bottom: 1px solid var(--border); padding: 30px 0; }}
        header h1 {{ font-size: 1.8em; font-weight: 700; margin-bottom: 5px; }}
        header p {{ color: var(--text-light); }}
        .nav {{ display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid var(--border); background: var(--bg); }}
        .nav-links {{ display: flex; gap: 20px; }}
        .nav-links a {{ color: var(--text-light); text-decoration: none; }}
        .nav-links a:hover {{ color: var(--primary); }}
        .lang-switch {{ display: flex; gap: 10px; }}
        .lang-switch a {{ padding: 6px 12px; border-radius: 6px; text-decoration: none; font-size: 0.9em; background: var(--bg-alt); color: var(--text-light); }}
        .lang-switch a.active {{ background: var(--primary); color: white; }}
        main {{ padding: 30px 0; }}
        .content {{ background: var(--bg); border-radius: 12px; padding: 40px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .content h1 {{ font-size: 1.6em; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid var(--border); }}
        .content h2 {{ font-size: 1.3em; margin: 30px 0 15px 0; }}
        .content h3 {{ font-size: 1.1em; margin: 25px 0 10px 0; }}
        .content h3 a {{ color: var(--primary); text-decoration: none; }}
        .content h3 a:hover {{ text-decoration: underline; }}
        .content hr {{ border: none; border-top: 1px solid var(--border); margin: 25px 0; }}
        .highlights {{ background: var(--bg-alt); border-left: 3px solid var(--primary); padding: 20px; margin: 25px 0; }}
        .highlights h2 {{ margin-top: 0; color: var(--primary); font-size: 1.1em; }}
        .highlights ul {{ list-style: none; }}
        .highlights li {{ padding: 6px 0; padding-left: 24px; position: relative; }}
        .highlights li:before {{ content: "•"; color: var(--primary); font-weight: bold; position: absolute; left: 0; }}
        .meta {{ font-size: 0.9em; color: var(--text-light); margin: 5px 0; }}
        footer {{ text-align: center; padding: 30px 0; color: var(--text-light); font-size: 0.9em; border-top: 1px solid var(--border); margin-top: 40px; }}
        footer a {{ color: var(--primary); text-decoration: none; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{ background: var(--bg-alt); font-weight: 600; }}
        a {{ color: var(--primary); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <header><div class="container"><h1>{t[0]}</h1><p>{t[1]}</p></div></header>
    <nav class="nav"><div class="container" style="display:flex;justify-content:space-between;width:100%;">
        <div class="nav-links"><a href="index.html">{t[2]}</a><a href="history.html">{t[3]}</a></div>
        <div class="lang-switch"><a href="index.html" {active}>{t[4]}</a><a href="index.en.html" {active_en}>{t[5]}</a></div>
    </div></nav>
    <main class="container"><div class="content">{md_to_html(content)}</div></main>
    <footer><div class="container"><p>{t[6]} · <a href="https://github.com/Rito-w/daily-news-digest">GitHub</a> · {t[7]}: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p></div></footer>
</body>
</html>"""

def generate_history_html(items, lang="zh"):
    """生成历史页面"""
    t = ("历史新闻", "每日新闻摘要", "首页", "历史", "中文", "English") if lang == "zh" else ("History", "Daily News Digest", "Home", "History", "中文", "English")
    active = 'class="active"' if lang == "zh" else ''
    
    rows = "".join([f'<tr><td>{i["date"]}</td><td><a href="{i["zh"]}">{i["date"]}.zh</a></td><td><a href="{i["en"]}">{i["date"]}.en</a></td></tr>' for i in items])
    
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>{t[0]}</title>
    <style>
        :root {{ --primary: #2563eb; --text: #1f2937; --text-light: #6b7280; --bg: #ffffff; --bg-alt: #f9fafb; --border: #e5e7eb; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.7; color: var(--text); background: var(--bg-alt); }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 20px; }}
        header {{ background: var(--bg); border-bottom: 1px solid var(--border); padding: 30px 0; }}
        header h1 {{ font-size: 1.8em; font-weight: 700; }}
        .nav {{ display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid var(--border); background: var(--bg); }}
        .nav-links a {{ color: var(--text-light); text-decoration: none; margin-right: 20px; }}
        .nav-links a:hover {{ color: var(--primary); }}
        .lang-switch a {{ padding: 6px 12px; border-radius: 6px; text-decoration: none; background: var(--bg-alt); color: var(--text-light); }}
        .lang-switch a.active {{ background: var(--primary); color: white; }}
        .content {{ background: var(--bg); border-radius: 12px; padding: 40px; margin: 30px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{ background: var(--bg-alt); }}
        a {{ color: var(--primary); }}
        footer {{ text-align: center; padding: 30px 0; color: var(--text-light); border-top: 1px solid var(--border); }}
    </style>
</head>
<body>
    <header><div class="container"><h1>{t[0]}</h1><p>{t[1]}</p></div></header>
    <nav class="nav"><div class="container" style="display:flex;justify-content:space-between;width:100%;">
        <div class="nav-links"><a href="index.html">{t[2]}</a><a href="history.html" class="active">{t[3]}</a></div>
        <div class="lang-switch"><a href="history.html" {active}>{t[4]}</a><a href="history.en.html">{t[5]}</a></div>
    </div></nav>
    <main class="container"><div class="content"><h1>{t[0]}</h1><table><thead><tr><th>日期</th><th>中文版</th><th>English</th></tr></thead><tbody>{rows}</tbody></table></div></main>
    <footer><p>GitHub · <a href="https://github.com/Rito-w/daily-news-digest">Rito-w/daily-news-digest</a></p></footer>
</body>
</html>"""

# Generate all pages
website_dir = Path("website")
website_dir.mkdir(exist_ok=True)
(website_dir / "index.html").write_text(generate_html(news_zh, "zh"), encoding="utf-8")
(website_dir / "index.en.html").write_text(generate_html(news_en, "en"), encoding="utf-8")
(website_dir / "history.html").write_text(generate_history_html(history_items, "zh"), encoding="utf-8")
(website_dir / "history.en.html").write_text(generate_history_html(history_items, "en"), encoding="utf-8")

print(f"✅ Website built ({len(history_items)} history items)")
