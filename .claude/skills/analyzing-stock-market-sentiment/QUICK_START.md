# Quick Start Guide - Stock Sentiment Deduplication

## Installation

```bash
# Install pandas if not already installed
uv add pandas
```

## Basic Usage

### 1. Deduplicate Comments Only

```bash
cd d:\MediaCrawler-main\.claude\skills\analyzing-stock-market-sentiment

python stock_sentiment_dedup.py --comments ../../data/xhs/csv/search_comments_2026-01-20.csv --output ../../data/xhs/csv/comments_dedup.csv
```

### 2. Deduplicate Contents Only

```bash
python stock_sentiment_dedup.py --contents ../../data/xhs/csv/search_contents_2026-01-20.csv --output ../../data/xhs/csv/contents_dedup.csv
```

### 3. Deduplicate Both Files (Recommended)

```bash
python stock_sentiment_dedup.py \
    --comments ../../data/xhs/csv/search_comments_2026-01-20.csv \
    --contents ../../data/xhs/csv/search_contents_2026-01-20.csv \
    --output-dir ../../data/xhs/csv/deduplicated/
```

## Common Scenarios

### Scenario 1: After Crawling Stock Data

```bash
# Step 1: Crawl data (from MediaCrawler root)
uv run python main.py

# Step 2: Deduplicate (from skill directory)
cd .claude/skills/analyzing-stock-market-sentiment
python stock_sentiment_dedup.py \
    --comments ../../data/xhs/csv/search_comments_*.csv \
    --contents ../../data/xhs/csv/search_contents_*.csv \
    --output-dir ../../data/xhs/csv/deduplicated/

# Step 3: Analyze deduplicated data
python ../analyzing-social-media-data/main.py \
    --input ../../data/xhs/csv/deduplicated/contents_dedup.csv
```

### Scenario 2: Processing Multiple Platforms

```bash
# Deduplicate Xiaohongshu data
python stock_sentiment_dedup.py \
    --comments ../../data/xhs/csv/comments.csv \
    --contents ../../data/xhs/csv/contents.csv \
    --output-dir ../../data/xhs/dedup/ \
    --prefix xhs_

# Deduplicate Douyin data
python stock_sentiment_dedup.py \
    --comments ../../data/dy/csv/comments.csv \
    --contents ../../data/dy/csv/contents.csv \
    --output-dir ../../data/dy/dedup/ \
    --prefix dy_

# Deduplicate Weibo data
python stock_sentiment_dedup.py \
    --comments ../../data/wb/csv/comments.csv \
    --contents ../../data/wb/csv/contents.csv \
    --output-dir ../../data/wb/dedup/ \
    --prefix wb_
```

## Understanding the Output

### Example Output

```
============================================================
📊 DEDUPLICATION STATISTICS (COMMENTS)
============================================================
Original count:     1,234
Duplicate count:    234
Unique count:       1,000
Duplicate rate:     18.97%
============================================================

✓ Duplicate rate is within acceptable range.
✓ Saved deduplicated data: deduplicated/comments_dedup.csv
  Total records: 1,000
```

### What This Means

- **Original count**: Total records before deduplication (1,234)
- **Duplicate count**: Records removed as duplicates (234)
- **Unique count**: Unique records kept (1,000)
- **Duplicate rate**: Percentage of duplicates (18.97%)

### Interpreting Duplicate Rates

- **0-10%**: Excellent quality
- **10-20%**: Normal for social media
- **20-50%**: Acceptable, monitor data collection
- **50%+**: Investigate data collection issues

## Troubleshooting

### Error: "File not found"

```bash
# Check actual file location
ls ../../data/xhs/csv/

# Use correct filename
python stock_sentiment_dedup.py --comments ../../data/xhs/csv/ACTUAL_FILENAME.csv
```

### Error: "Column 'content' not found"

The script auto-detects these column names:
- Content: `content`, `text`, `comment_text`, `comment`, `note_text`
- Likes: `like_count`, `likes`, `liked_count`, `praise_count`

If using custom columns, modify the script or rename your CSV columns.

## Advanced Usage

### Custom Output Prefix

```bash
# Add prefix to output files
python stock_sentiment_dedup.py \
    --comments comments.csv \
    --contents contents.csv \
    --output-dir clean/ \
    --prefix clean_

# Output: clean/clean_comments.csv, clean/clean_contents.csv
```

### Python Script Integration

```python
from stock_sentiment_dedup import load_csv_data, deduplicate_data, save_deduplicated_data

# Load and deduplicate
df = load_csv_data("comments.csv")
df_clean, stats = deduplicate_data(df)
save_deduplicated_data(df_clean, "comments_dedup.csv")

print(f"Removed {stats['duplicate_count']} duplicates")
```

## File Locations

- **Script**: `d:\MediaCrawler-main\.claude\skills\analyzing-stock-market-sentiment\stock_sentiment_dedup.py`
- **Documentation**: `d:\MediaCrawler-main\.claude\skills\analyzing-stock-market-sentiment\DEDUPLICATION_README.md`
- **Examples**: `d:\MediaCrawler-main\.claude\skills\analyzing-stock-market-sentiment\example_dedup_usage.py`

## Tips

1. **Always keep backups** - Original files are never modified
2. **Check statistics** - Review duplicate rates to assess data quality
3. **Process in batches** - Use `--output-dir` for multiple files
4. **Verify results** - Spot-check deduplicated files before analysis
5. **Use absolute paths** - Avoid path issues when running from different directories

## Next Steps

After deduplication, use the `analyzing-social-media-data` skill to analyze your clean data:

```bash
cd ../analyzing-social-media-data
python main.py --input ../../data/xhs/csv/deduplicated/contents_dedup.csv
```
