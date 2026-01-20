# 股市情绪分析器 - 快速开始

## 📦 安装

```bash
cd .claude/skills/analyzing-stock-market-sentiment
```

## 🚀 快速使用

### 1. 先用 MediaCrawler 爬取数据

编辑 `config/base_config.py`：

```python
PLATFORM = "xhs"  # 或 dy/bili/wb
KEYWORDS = "紫金矿业,601899"
CRAWLER_MAX_NOTES_COUNT = 50
ENABLE_GET_COMMENTS = True
SAVE_DATA_OPTION = "csv"
```

运行爬虫：

```bash
uv run python main.py
```

### 2. 分析情绪

```bash
python stock_sentiment.py ../../../data/xhs/csv/search_comments_2026-01-20.csv \
                           ../../../data/xhs/csv/search_contents_2026-01-20.csv \
                           "紫金矿业"
```

## 📊 输出内容

- ✅ 多空情绪分布（看涨78.1% vs 看跌21.0%）
- ✅ 价格目标统计（平均预期30.23元）
- ✅ 投资行为分析（加仓74条 vs 减仓43条）
- ✅ 核心关注主题（黄金285条、铜价70条）
- ✅ 看涨/看跌理由 Top 10
- ✅ 投资者故事（十年十倍、卖飞、买少）
- ✅ 风险信号识别（情绪过热、FOMO）
- ✅ 综合投资洞察

## 💡 核心功能

| 功能 | 说明 |
|------|------|
| **多空分析** | 看涨/看跌/观望/未明确，净多头情绪 |
| **价格目标** | 提取评论中的价格，统计热门价位 |
| **行为识别** | 加仓/减仓/持有，判断投资者意图 |
| **主题提取** | 黄金、铜价、业绩、估值等 |
| **风险检测** | 情绪过热、FOMO、获利回吐 |

## 📖 完整文档

查看 [SKILL.md](./SKILL.md) 了解详细使用说明
