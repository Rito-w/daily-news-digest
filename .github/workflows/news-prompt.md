# Cron 任务提示词模板

在你的 cron 任务中使用这个提示词调用 AI 生成新闻：

---

## 提示词

```
请为以下 RSS 文章生成每日新闻摘要（中英双语）：

{RSS 文章列表 JSON}

输出格式要求：

# 📰 每日新闻摘要 · {日期}

*更新时间：{时间}*

---

## 🔥 今日看点

- 3-5 句今日重点总结
- 基于文章内容提炼

## 📋 新闻列表

### 1. [文章标题](文章链接)
*来源名称 · 月日*

文章摘要（2-3 句，中文，简洁明了）

---

### 2. [文章标题](文章链接)
*来源名称 · 月日*

文章摘要（2-3 句，中文）

---

（继续 10-15 条新闻）

*自动生成于 {时间}*
```

---

## 输出示例

```markdown
# 📰 每日新闻摘要 · 2026 年 03 月 07 日

*更新时间：2026-03-07 09:05*

---

## 🔥 今日看点

- OpenAI 发布 GPT-5.4 和 GPT-5.4-Pro 新模型
- Google 更新 Gemini 3.1 Flash-Lite
- 开发者工具和安全话题持续热门

## 📋 新闻列表

### 1. [Quoting Ally Piechowski](https://simonwillison.net/2026/Mar/6/ally-piechowski/)
*Simon Willison's Weblog · 3 月 6 日*

AI 研究员 Ally Piechowski 分享了对开发者的建议，提出了几个值得思考的问题：你最不敢触碰的代码领域是什么？上次周五部署是什么时候？

---

### 2. [Anthropic and the Pentagon](https://simonwillison.net/2026/Mar/6/anthropic-and-the-pentagon/)
*Simon Willison's Weblog · 3 月 6 日*

Bruce Schneier 撰文分析了 Anthropic 与五角大楼的合作，认为这是迄今为止最理性和务实的讨论。

---

### 3. [Introducing GPT‑5.4](https://simonwillison.net/2026/Mar/5/introducing-gpt54/)
*Simon Willison's Weblog · 3 月 5 日*

OpenAI 发布两个新 API 模型 gpt-5.4 和 gpt-5.4-pro，同时更新 ChatGPT 和 Codex。

---

（继续...）

*自动生成于 2026-03-07 09:05*
```

---

## Cron 任务示例

```bash
# 每天早上 9:05
5 9 * * * cd /Volumes/myDisk/workplace/daily-news-digest && \
  # 1. 抓取 RSS
  node ~/.openclaw/skills/ai-daily-digest-main/scripts/fetch-rss.mjs \
    --hours 24 \
    --sources ~/.openclaw/skills/ai-daily-digest-main/references/sources.json \
    > /tmp/news-raw.json && \
  # 2. 调用 AI 生成摘要
  openclaw sessions send --message "请根据以下新闻生成摘要：$(cat /tmp/news-raw.json)" \
    > news/$(date +\%Y-\%m-\%d).zh.md && \
  # 3. 复制最新版
  cp news/$(date +\%Y-\%m-\%d).zh.md news/latest.zh.md && \
  # 4. 提交推送
  git add -A && \
  git commit -m "docs: $(date +\%Y-\%m-\%d)" && \
  git push
```

---

## 格式说明

| 元素 | 格式 | 示例 |
|------|------|------|
| 标题 | `### [标题](链接)` | `### 1. [标题](https://...)` |
| 来源时间 | `*来源 · 月日*` | `*Simon Willison's Weblog · 3 月 6 日*` |
| 摘要 | 2-3 句中文 | 简洁明了，无需"简介："前缀 |
| 分隔 | `---` | 每条新闻之间 |
