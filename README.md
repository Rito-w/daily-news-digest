# Daily News Digest 📰

每日新闻摘要 - 自动抓取、整理并推送每日热点新闻。

## 📋 项目说明

本项目自动从多个来源抓取新闻，生成每日摘要并发布到 GitHub。

### 新闻来源

- 🤖 **AI/技术** - Hacker News, GitHub Trending, AI 博客
- 📈 **财经** - 华尔街见闻，彭博社
- 🔥 **热搜** - 微博热搜，知乎热榜
- 🎮 **游戏** - IGN, GameSpot
- ⚽ **体育** - 虎扑，直播吧

## 📁 目录结构

```
daily-news-digest/
├── README.md              # 项目说明
├── scripts/               # 抓取脚本
│   ├── fetch-news.py     # 新闻抓取主脚本
│   └── sources.json      # 新闻源配置
├── news/                  # 每日新闻
│   └── YYYY-MM-DD.md     # 每日新闻文件
└── .github/workflows/
    └── sync.yml          # GitHub Actions 自动同步
```

## 🚀 本地运行

```bash
# 安装依赖
pip install feedparser requests beautifulsoup4

# 运行抓取脚本
python scripts/fetch-news.py

# 查看今日新闻
cat news/$(date +%Y-%m-%d).md
```

## ⏰ 定时任务

### 方式 1：GitHub Actions（推荐）

每天自动运行，推送到 GitHub。

### 方式 2：本地 cron

```bash
# 添加到 crontab
crontab -e

# 每天早上 8 点运行
0 8 * * * cd /Volumes/myDisk/workplace/daily-news-digest && python scripts/fetch-news.py && git add -A && git commit -m "docs: 每日新闻 $(date +\%Y-\%m-\%d)" && git push
```

## 📊 新闻格式

```markdown
# 📰 Daily News Digest · 2026-03-07

## 🔥 今日热点

### 微博热搜
1. xxx
2. xxx
3. xxx

### 知乎热榜
1. xxx
2. xxx
3. xxx

## 🤖 AI/技术

- [标题](链接) - 简短摘要
- [标题](链接) - 简短摘要

## 📈 财经

- [标题](链接) - 简短摘要

## 🎮 游戏

- [标题](链接) - 简短摘要

## ⚽ 体育

- [标题](链接) - 简短摘要

---

*自动生成于 $(date)*
```

## 🛠️ 技术栈

- Python 3.8+
- GitHub Actions
- RSS/Atom feeds
- Web scraping

## 📄 许可证

MIT

---

*Last updated: 2026-03-07*
*Maintainer: @Rito-w*
