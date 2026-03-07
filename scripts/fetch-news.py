#!/usr/bin/env python3
"""
每日新闻抓取脚本
从多个来源抓取新闻并生成 Markdown 格式的报告
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 尝试导入第三方库
try:
    import feedparser
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"❌ 缺少依赖库：{e}")
    print("请运行：pip install feedparser requests beautifulsoup4")
    sys.exit(1)

# 配置
NEWS_DIR = Path(__file__).parent.parent / "news"
SOURCES_FILE = Path(__file__).parent / "sources.json"
OUTPUT_DATE = datetime.now().strftime("%Y-%m-%d")
OUTPUT_FILE = NEWS_DIR / f"{OUTPUT_DATE}.md"

# 确保新闻目录存在
NEWS_DIR.mkdir(parents=True, exist_ok=True)


def fetch_rss_feed(url, limit=5):
    """抓取 RSS/Atom feed"""
    try:
        feed = feedparser.parse(url)
        entries = []
        for entry in feed.entries[:limit]:
            entries.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")[:200]  # 限制摘要长度
            })
        return entries
    except Exception as e:
        print(f"⚠️  RSS 抓取失败 {url}: {e}")
        return []


def fetch_weibo_hot_search():
    """抓取微博热搜（模拟）"""
    # 实际使用时需要调用微博 API 或爬取
    return [
        {"title": "热搜示例 1", "link": "https://weibo.com"},
        {"title": "热搜示例 2", "link": "https://weibo.com"},
        {"title": "热搜示例 3", "link": "https://weibo.com"},
    ]


def fetch_zhihu_hot():
    """抓取知乎热榜（模拟）"""
    # 实际使用时需要调用知乎 API 或爬取
    return [
        {"title": "知乎热榜示例 1", "link": "https://zhihu.com"},
        {"title": "知乎热榜示例 2", "link": "https://zhihu.com"},
        {"title": "知乎热榜示例 3", "link": "https://zhihu.com"},
    ]


def fetch_github_trending(limit=5):
    """抓取 GitHub Trending"""
    url = "https://github-trends-api.vercel.app/weekly"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [
                {
                    "title": f"{item['name']} - {item['description'] or '无描述'}",
                    "link": item["url"],
                    "stars": item["stars"]
                }
                for item in data[:limit]
            ]
    except Exception as e:
        print(f"⚠️  GitHub Trending 抓取失败：{e}")
    return []


def generate_markdown(news_data):
    """生成 Markdown 格式的新闻报告"""
    md = f"""# 📰 Daily News Digest · {OUTPUT_DATE}

*自动生成于 {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*

---

## 🔥 今日热点

### 微博热搜
"""
    
    for i, item in enumerate(news_data.get("weibo", [])[:5], 1):
        md += f"{i}. [{item['title']}]({item['link']})\n"
    
    md += "\n### 知乎热榜\n"
    for i, item in enumerate(news_data.get("zhihu", [])[:5], 1):
        md += f"{i}. [{item['title']}]({item['link']})\n"
    
    md += "\n## 🤖 AI/技术\n\n"
    for item in news_data.get("tech", []):
        md += f"- [{item['title']}]({item['link']})\n"
    
    md += "\n## 💻 GitHub Trending\n\n"
    for item in news_data.get("github", []):
        md += f"- ⭐ {item['stars']} [{item['title']}]({item['link']})\n"
    
    md += "\n## 📈 财经\n\n"
    for item in news_data.get("finance", []):
        md += f"- [{item['title']}]({item['link']})\n"
    
    md += "\n## 🎮 游戏\n\n"
    for item in news_data.get("gaming", []):
        md += f"- [{item['title']}]({item['link']})\n"
    
    md += "\n---\n\n"
    md += f"*数据来源于公开 RSS feeds 和 API，更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return md


def main():
    """主函数"""
    print(f"🚀 开始抓取新闻 · {OUTPUT_DATE}")
    
    news_data = {
        "weibo": fetch_weibo_hot_search(),
        "zhihu": fetch_zhihu_hot(),
        "github": fetch_github_trending(),
        "tech": [],
        "finance": [],
        "gaming": []
    }
    
    # 抓取技术新闻 RSS
    tech_feeds = [
        "https://simonwillison.net/atom/everything/",
        "https://hnrss.org/frontpage",
    ]
    
    for feed_url in tech_feeds:
        news_data["tech"].extend(fetch_rss_feed(feed_url, limit=3))
    
    # 生成 Markdown
    md_content = generate_markdown(news_data)
    
    # 保存文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"✅ 新闻已保存到：{OUTPUT_FILE}")
    print(f"📊 统计：")
    print(f"   - 微博热搜：{len(news_data['weibo'])} 条")
    print(f"   - 知乎热榜：{len(news_data['zhihu'])} 条")
    print(f"   - GitHub Trending: {len(news_data['github'])} 条")
    print(f"   - 技术新闻：{len(news_data['tech'])} 条")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
