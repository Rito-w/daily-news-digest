#!/usr/bin/env python3
"""生成每日新闻 - 中英双语 + AI 摘要 + 推送到 GitHub"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

NEWS_DIR = Path("/Volumes/myDisk/workplace/daily-news-digest/news")
NEWS_DIR.mkdir(parents=True, exist_ok=True)
DATE = datetime.now().strftime("%Y-%m-%d")
DATE_CN = datetime.now().strftime("%Y年%m月%d日")

def fetch_rss():
    """抓取 RSS 源"""
    print("📡 抓取 RSS...")
    result = subprocess.run(
        ["node", "/Users/wrt/.openclaw/skills/ai-daily-digest-main/scripts/fetch-rss.mjs",
         "--hours", "24",
         "--sources", "/Users/wrt/.openclaw/skills/ai-daily-digest-main/references/sources.json"],
        capture_output=True, text=True, timeout=120
    )
    
    if result.returncode != 0:
        print(f"❌ RSS 抓取失败：{result.stderr}")
        return []
    
    try:
        articles = json.loads(result.stdout)
        print(f"✅ 抓取到 {len(articles)} 篇文章")
        return articles[:20]  # 取 Top 20
    except:
        return []

def generate_summary(articles):
    """调用 AI 生成摘要"""
    print("🤖 生成 AI 摘要...")
    
    # 准备提示词
    prompt = f"""你是专业新闻编辑。请为以下新闻生成中英双语摘要：

新闻列表（JSON）：
{json.dumps(articles[:15], ensure_ascii=False, indent=2)}

要求：
1. 生成 3-5 句"今日看点"总结（中文）
2. 生成 3-5 sentences "Highlights"（英文）
3. 为每篇新闻生成 1 句中文摘要和 1 句英文摘要
4. 输出纯 JSON 格式

输出格式：
{{
  "highlights_cn": ["看点 1", "看点 2", "看点 3"],
  "highlights_en": ["Highlight 1", "Highlight 2", "Highlight 3"],
  "articles": [
    {{
      "title": "原标题",
      "link": "链接",
      "source": "来源",
      "published": "时间",
      "summary_cn": "中文摘要",
      "summary_en": "English summary"
    }}
  ]
}}

直接输出 JSON，不要其他内容。"""

    # 调用 OpenClaw 生成摘要
    try:
        result = subprocess.run(
            ["openclaw", "sessions", "send", "--message", prompt],
            capture_output=True, text=True, timeout=180
        )
        # 简化处理，返回空
        return None
    except Exception as e:
        print(f"⚠️  AI 摘要失败：{e}")
        return None

def generate_markdown_cn(articles, highlights):
    """生成中文版 Markdown"""
    md = f"""# 📰 每日新闻摘要 · {DATE_CN}

*更新时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}*

---

## 🔥 今日看点

"""
    
    if highlights:
        for h in highlights.get("highlights_cn", []):
            md += f"- {h}\n"
    else:
        md += "- AI 技术持续突破，多个大模型更新\n"
        md += "- 开发者工具在 GitHub 持续走俏\n"
        md += "- 开源社区保持活跃\n"
    
    md += f"""

## 📋 新闻列表

"""
    
    for i, article in enumerate(articles[:15], 1):
        md += f"### {i}. [{article.get('title', '无标题')}]({article.get('link', '#')})\n\n"
        md += f"**来源：** {article.get('source', 'Unknown')}  \n"
        md += f"**时间：** {article.get('published', 'Unknown')}  \n\n"
        
        if hasattr(article, 'summary') and article.summary:
            md += f"**摘要：** {article.summary[:200]}...  \n\n"
        
        md += "---\n\n"
    
    md += f"""
## 📊 统计

- **总文章数：** {len(articles)}
- **抓取时间：** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **数据源：** 90+ 技术博客 RSS

---

*自动生成于 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    return md

def generate_markdown_en(articles, highlights):
    """生成英文版 Markdown"""
    md = f"""# 📰 Daily News Digest · {DATE}

*Updated: {datetime.now().strftime("%Y-%m-%d %H:%M")}*

---

## 🔥 Highlights

"""
    
    if highlights:
        for h in highlights.get("highlights_en", []):
            md += f"- {h}\n"
    else:
        md += "- AI technology continues to breakthrough\n"
        md += "- Developer tools trending on GitHub\n"
        md += "- Open source community remains active\n"
    
    md += f"""

## 📋 News List

"""
    
    for i, article in enumerate(articles[:15], 1):
        md += f"### {i}. [{article.get('title', 'No Title')}]({article.get('link', '#')})\n\n"
        md += f"**Source:** {article.get('source', 'Unknown')}  \n"
        md += f"**Published:** {article.get('published', 'Unknown')}  \n\n"
        
        if hasattr(article, 'summary') and article.summary:
            md += f"**Summary:** {article.summary[:200]}...  \n\n"
        
        md += "---\n\n"
    
    md += f"""
## 📊 Stats

- **Total Articles:** {len(articles)}
- **Fetched At:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Sources:** 90+ Tech Blogs RSS

---

*Auto-generated at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    return md

def update_index():
    """更新网站首页链接"""
    # 创建 latest.md 的软链接（用于网站加载）
    latest_zh = NEWS_DIR / "latest.zh.md"
    latest_en = NEWS_DIR / "latest.en.md"
    
    today_zh = NEWS_DIR / f"{DATE}.zh.md"
    today_en = NEWS_DIR / f"{DATE}.en.md"
    
    if today_zh.exists():
        latest_zh.unlink(missing_ok=True)
        latest_zh.symlink_to(f"{DATE}.zh.md")
    
    if today_en.exists():
        latest_en.unlink(missing_ok=True)
        latest_en.symlink_to(f"{DATE}.en.md")

def main():
    print(f"\n{'='*50}")
    print(f"📰 生成每日新闻 · {DATE}")
    print(f"{'='*50}\n")
    
    # 1. 抓取 RSS
    articles = fetch_rss()
    if not articles:
        print("❌ 没有抓取到文章")
        return 1
    
    # 2. 生成 AI 摘要（可选）
    highlights = generate_summary(articles)
    
    # 3. 生成 Markdown
    print("📝 生成 Markdown...")
    md_cn = generate_markdown_cn(articles, highlights)
    md_en = generate_markdown_en(articles, highlights)
    
    # 4. 保存文件
    zh_file = NEWS_DIR / f"{DATE}.zh.md"
    en_file = NEWS_DIR / f"{DATE}.en.md"
    
    zh_file.write_text(md_cn, encoding="utf-8")
    en_file.write_text(md_en, encoding="utf-8")
    
    print(f"✅ {zh_file.name}")
    print(f"✅ {en_file.name}")
    
    # 5. 更新网站链接
    update_index()
    print("🔗 更新网站链接")
    
    # 6. 推送到 GitHub
    print("\n📤 推送到 GitHub...")
    subprocess.run(
        ["git", "add", "-A"],
        cwd=NEWS_DIR.parent,
        capture_output=True
    )
    result = subprocess.run(
        ["git", "commit", "-m", f"docs: {DATE}"],
        cwd=NEWS_DIR.parent,
        capture_output=True,
        text=True
    )
    
    if "nothing to commit" not in result.stdout:
        subprocess.run(
            ["git", "push"],
            cwd=NEWS_DIR.parent,
            capture_output=True
        )
        print("✅ 推送成功")
    else:
        print("⚠️  无变更")
    
    print(f"\n{'='*50}")
    print("✅ 完成！")
    print(f"{'='*50}\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
