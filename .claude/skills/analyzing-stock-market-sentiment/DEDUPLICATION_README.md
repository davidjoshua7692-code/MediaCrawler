# Stock Sentiment Data Deduplication Tool

A Python script to remove duplicate entries from stock sentiment analysis CSV files, intelligently keeping the version with the highest engagement (like_count).

## Features

- **Smart Deduplication**: Removes duplicate comments/contents based on text content
- **Engagement Preservation**: Keeps the entry with highest `like_count` among duplicates
- **Dual Support**: Works with both comments and contents CSV files
- **Detailed Statistics**: Shows before/after metrics and duplicate rates
- **Safe Operation**: Creates new files without modifying originals
- **Flexible I/O**: Command-line arguments for custom input/output paths

## Requirements

```bash
pip install pandas
```

## Installation

The script is located at:
```
.claude/skills/analyzing-stock-market-sentiment/stock_sentiment_dedup.py
```

## Usage

### Method 1: Command Line (Recommended)

#### Deduplicate a single file (comments):
```bash
python stock_sentiment_dedup.py --comments data/comments.csv --output data/comments_dedup.csv
```

#### Deduplicate a single file (contents):
```bash
python stock_sentiment_dedup.py --contents data/contents.csv --output data/contents_dedup.csv
```

#### Deduplicate both files to a directory:
```bash
python stock_sentiment_dedup.py --comments data/comments.csv --contents data/contents.csv --output-dir deduplicated/
```

#### Use custom output directory and prefix:
```bash
python stock_sentiment_dedup.py --comments comments.csv --contents contents.csv --output-dir clean/ --prefix clean_
```

### Method 2: Python Script

```python
from stock_sentiment_dedup import load_csv_data, deduplicate_data, save_deduplicated_data

# Load
df = load_csv_data("data/comments.csv")

# Deduplicate (keeps entry with highest like_count)
df_dedup, stats = deduplicate_data(
    df,
    content_column='content',
    like_column='like_count'
)

# Save
save_deduplicated_data(df_dedup, "data/comments_dedup.csv")
```

## Command-Line Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `--comments` | string | No* | Path to comments CSV file |
| `--contents` | string | No* | Path to contents CSV file |
| `--output` | string | No | Output CSV file path (for single file) |
| `--output-dir` | string | No | Output directory (default: `deduplicated/`) |
| `--prefix` | string | No | Prefix for output filenames (default: none) |

*At least one of `--comments` or `--contents` must be specified.

## How It Works

### Deduplication Logic

1. **Group by Content**: Identifies entries with identical text content (case-insensitive, whitespace-trimmed)
2. **Sort by Engagement**: Within each duplicate group, sorts by `like_count` descending
3. **Keep First**: Retains the first entry (which has highest likes) and removes others
4. **Preserve Order**: Maintains original chronological order of first occurrences

### Column Detection

The script automatically detects common column names:
- **Content**: `content`, `text`, `comment_text`, `comment`, `note_text`
- **Likes**: `like_count`, `likes`, `liked_count`, `praise_count`, `thumbs_up`

If no like column is found, all duplicates are treated as equal (keeps first occurrence).

## Output Example

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

## Statistics Interpretation

| Duplicate Rate | Interpretation |
|----------------|----------------|
| 0-10% | Excellent data quality |
| 10-20% | Normal for social media data |
| 20-50% | Moderate duplicate rate, acceptable |
| >50% | High duplicate rate, check data quality issues |

## Examples

### Example 1: Stock Comments from Social Media

**Input** (`comments.csv`):
| content | like_count | user |
|---------|------------|------|
| "This stock will moon!" | 45 | user1 |
| "This stock will moon!" | 12 | user2 |
| "Great earnings report" | 23 | user3 |
| "This stock will MOON!" | 8 | user4 |

**Output** (`comments_dedup.csv`):
| content | like_count | user |
|---------|------------|------|
| "This stock will moon!" | 45 | user1 |
| "Great earnings report" | 23 | user3 |

*Result: 2 duplicates removed, kept the version with 45 likes*

### Example 2: Processing Multiple Files

```bash
# Process both comments and contents
python stock_sentiment_dedup.py \
    --comments data/xhs/csv/search_comments_2026-01-20.csv \
    --contents data/xhs/csv/search_contents_2026-01-20.csv \
    --output-dir data/xhs/csv/deduplicated/
    --prefix dedup_
```

**Output files:**
- `data/xhs/csv/deduplicated/dedup_comments.csv`
- `data/xhs/csv/deduplicated/dedup_contents.csv`

## Error Handling

The script provides clear error messages for common issues:

- **File not found**: `❌ File not found: comments.csv`
- **Empty file**: `❌ File is empty: contents.csv`
- **Missing column**: `❌ Column 'content' not found in DataFrame`
- **Invalid CSV**: `❌ Error reading file: ...`

## Tips

1. **Always backup**: The script creates new files, but keep originals backed up
2. **Check statistics**: Review duplicate rates to assess data quality
3. **Batch processing**: Use `--output-dir` to process multiple files efficiently
4. **Custom columns**: The script auto-detects columns, but you can modify `process_file()` for custom column names
5. **Case sensitivity**: Deduplication is case-insensitive ("STOCK" = "stock")

## Troubleshooting

### Issue: "Column 'content' not found"
**Solution**: Your CSV uses different column names. The script will auto-detect common alternatives like `text`, `comment`, `note_text`.

### Issue: High duplicate rate (>50%)
**Solution**: This may indicate:
- Data collection issues (same page scraped multiple times)
- Platform with many bot/spam comments
- Need to review data collection parameters

### Issue: Empty output file
**Solution**: Check that:
- Input file is not empty
- Content column has non-empty values
- File encoding is UTF-8 compatible

## Integration with MediaCrawler

This tool works seamlessly with MediaCrawler output:

```bash
# 1. Crawl data
uv run python main.py

# 2. Locate CSV files
# data/xhs/csv/search_contents_2026-01-20.csv
# data/xhs/csv/search_comments_2026-01-20.csv

# 3. Deduplicate
cd .claude/skills/analyzing-stock-market-sentiment/
python stock_sentiment_dedup.py \
    --comments data/xhs/csv/search_comments_2026-01-20.csv \
    --contents data/xhs/csv/search_contents_2026-01-20.csv \
    --output-dir data/xhs/csv/deduplicated/

# 4. Analyze deduplicated data
python ../analyzing-social-media-data/main.py \
    --input data/xhs/csv/deduplicated/contents_dedup.csv
```

## License

Part of the MediaCrawler project. Used for stock sentiment analysis data cleaning.
