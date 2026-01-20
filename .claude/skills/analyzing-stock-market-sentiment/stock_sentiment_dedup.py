"""
Stock Sentiment Data Deduplication Script

This script removes duplicate entries from stock sentiment analysis CSV files,
keeping the first occurrence with the highest like_count.

Usage:
    python stock_sentiment_dedup.py --comments input_comments.csv --output dedup_comments.csv
    python stock_sentiment_dedup.py --contents input_contents.csv --output dedup_contents.csv
    python stock_sentiment_dedup.py --comments comments.csv --contents contents.csv --output-dir deduplicated/

Features:
    - Removes duplicate comments/contents based on text content
    - Preserves the entry with the highest like_count among duplicates
    - Supports both comments and contents CSV files
    - Provides detailed statistics before and after deduplication
    - Creates new files without modifying originals
"""

import argparse
import pandas as pd
import os
from pathlib import Path
from typing import Tuple, Optional


def get_project_paths():
    """
    获取项目路径（锚定到.claude文件夹）

    Returns:
        dict: {
            'project_root': 项目根目录,
            'data_dir': 数据目录
        }
    """
    script_dir = Path(__file__).parent
    # .claude/skills/analyzing-stock-market-sentiment/ -> .claude/
    claude_dir = script_dir.parent.parent
    project_root = claude_dir.parent

    return {
        'project_root': project_root,
        'data_dir': project_root / "data" / "xhs" / "csv"
    }


def load_csv_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV file with error handling.

    Args:
        file_path: Path to the CSV file

    Returns:
        DataFrame containing the CSV data

    Raises:
        FileNotFoundError: If the file doesn't exist
        pd.errors.EmptyDataError: If the file is empty
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        df = pd.read_csv(file_path)
        print(f"✓ Successfully loaded: {file_path}")
        print(f"  Columns: {', '.join(df.columns.tolist())}")
        return df
    except pd.errors.EmptyDataError:
        raise ValueError(f"File is empty: {file_path}")
    except Exception as e:
        raise Exception(f"Error reading {file_path}: {str(e)}")


def deduplicate_data(df: pd.DataFrame, content_column: str = 'content',
                     like_column: str = 'like_count') -> Tuple[pd.DataFrame, dict]:
    """
    Remove duplicate entries based on content, keeping the one with highest like_count.

    Deduplication Logic:
        1. Group by content column (text similarity)
        2. Within each group, find the row with highest like_count
        3. Keep only that row, remove others
        4. Maintain original order of first occurrences

    Args:
        df: Input DataFrame
        content_column: Column name containing text content to compare
        like_column: Column name containing like/interaction count

    Returns:
        Tuple of (deduplicated DataFrame, statistics dictionary)
    """
    if df.empty:
        return df, {
            'original_count': 0,
            'duplicate_count': 0,
            'unique_count': 0,
            'duplicate_rate': 0.0
        }

    # Check if required columns exist
    if content_column not in df.columns:
        raise ValueError(f"Column '{content_column}' not found in DataFrame. "
                        f"Available columns: {', '.join(df.columns)}")

    # Handle missing like_column
    if like_column not in df.columns:
        print(f"⚠ Warning: Column '{like_column}' not found. Using default value of 0.")
        df[like_column] = 0

    original_count = len(df)

    # Remove rows with empty/NaN content
    df_clean = df.dropna(subset=[content_column]).copy()
    empty_count = original_count - len(df_clean)

    if empty_count > 0:
        print(f"\n⚠ Removed {empty_count} rows with empty content")

    # Normalize content for deduplication (case-insensitive, trimmed)
    df_clean['_normalized_content'] = df_clean[content_column].str.strip().str.lower()

    # Sort by like_count descending (so highest likes come first within each content group)
    df_sorted = df_clean.sort_values(by=like_column, ascending=False)

    # Remove duplicates based on normalized content, keeping first occurrence (which has highest like_count)
    df_dedup = df_sorted.drop_duplicates(
        subset=['_normalized_content'],
        keep='first'
    )

    # Remove temporary column
    df_dedup = df_dedup.drop(columns=['_normalized_content'])

    # Restore original order (sort by original index)
    df_dedup = df_dedup.sort_index()

    duplicate_count = len(df_clean) - len(df_dedup)
    unique_count = len(df_dedup)
    duplicate_rate = (duplicate_count / original_count * 100) if original_count > 0 else 0

    statistics = {
        'original_count': original_count,
        'empty_removed': empty_count,
        'duplicate_count': duplicate_count,
        'unique_count': unique_count,
        'duplicate_rate': duplicate_rate
    }

    return df_dedup, statistics


def print_statistics(stats: dict, data_type: str = "entries"):
    """
    Print deduplication statistics in a formatted way.

    Args:
        stats: Statistics dictionary from deduplicate_data()
        data_type: Type of data (e.g., "comments", "contents")
    """
    print(f"\n{'='*60}")
    print(f"📊 DEDUPLICATION STATISTICS ({data_type.upper()})")
    print(f"{'='*60}")
    print(f"Original count:     {stats['original_count']:,}")

    if stats.get('empty_removed', 0) > 0:
        print(f"Empty removed:      {stats['empty_removed']:,}")

    print(f"Duplicate count:    {stats['duplicate_count']:,}")
    print(f"Unique count:       {stats['unique_count']:,}")
    print(f"Duplicate rate:     {stats['duplicate_rate']:.2f}%")
    print(f"{'='*60}\n")

    # Interpretation
    if stats['duplicate_rate'] > 50:
        print("⚠️  High duplicate rate detected (>50%). Consider data quality issues.")
    elif stats['duplicate_rate'] > 20:
        print("⚠️  Moderate duplicate rate detected (>20%). Normal for social media data.")
    else:
        print("✓ Duplicate rate is within acceptable range.")


def save_deduplicated_data(df: pd.DataFrame, output_path: str):
    """
    Save deduplicated DataFrame to CSV file.

    Args:
        df: Deduplicated DataFrame
        output_path: Path for output CSV file
    """
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"✓ Created output directory: {output_dir}")

    # Save to CSV
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"✓ Saved deduplicated data: {output_path}")
    print(f"  Total records: {len(df):,}")


def process_file(input_path: str, output_path: str, data_type: str) -> bool:
    """
    Process a single file: load, deduplicate, save, and report statistics.

    Args:
        input_path: Path to input CSV file
        output_path: Path to output CSV file
        data_type: Type of data ('comments' or 'contents')

    Returns:
        True if successful, False otherwise
    """
    try:
        print(f"\n{'#'*60}")
        print(f"# Processing {data_type.upper()}")
        print(f"{'#'*60}")

        # Load data
        df = load_csv_data(input_path)

        # Deduplicate
        content_column = 'content'  # Most common column name for text content
        like_column = 'like_count'  # Most common column name for likes

        # Try alternative column names if defaults don't exist
        if content_column not in df.columns:
            possible_columns = ['text', 'comment_text', 'comment', 'note_text', 'desc']
            for col in possible_columns:
                if col in df.columns:
                    content_column = col
                    print(f"ℹ Using '{content_column}' as content column")
                    break

        if like_column not in df.columns:
            possible_like_columns = ['likes', 'liked_count', 'praise_count', 'thumbs_up']
            for col in possible_like_columns:
                if col in df.columns:
                    like_column = col
                    print(f"ℹ Using '{like_column}' as like count column")
                    break

        df_dedup, stats = deduplicate_data(df, content_column, like_column)

        # Print statistics
        print_statistics(stats, data_type)

        # Save
        save_deduplicated_data(df_dedup, output_path)

        return True

    except Exception as e:
        print(f"\n❌ Error processing {data_type}: {str(e)}")
        return False


def find_latest_csv_files(data_dir: str = None) -> Tuple[Optional[str], Optional[str]]:
    """
    自动查找最新的CSV文件

    Args:
        data_dir: 数据目录路径（默认自动查找）

    Returns:
        (comments_file, contents_file) 找到的文件路径，未找到返回None
    """
    if data_dir is None:
        paths = get_project_paths()
        data_dir = paths['data_dir']
    else:
        data_dir = Path(data_dir)

    data_path = data_dir

    if not data_path.exists():
        print(f"⚠️  数据目录不存在: {data_dir}")
        return None, None

    # 查找 comments 和 contents 文件
    comments_files = list(data_path.glob("*comments*.csv"))
    contents_files = list(data_path.glob("*contents*.csv"))

    # 按修改时间排序，取最新的
    comments_file = max(comments_files, key=lambda f: f.stat().st_mtime) if comments_files else None
    contents_file = max(contents_files, key=lambda f: f.stat().st_mtime) if contents_files else None

    return comments_file, contents_file


def main():
    """
    Main function to handle command-line arguments and execute deduplication.
    """
    parser = argparse.ArgumentParser(
        description='Deduplicate stock sentiment analysis CSV files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 自动模式：查找 data/xhs/csv/ 最新文件，输出到同目录 -dedup.csv
  python stock_sentiment_dedup.py --auto

  # 指定文件去重
  python stock_sentiment_dedup.py --comments data/comments.csv --output data/comments_dedup.csv

  # 去重 contents
  python stock_sentiment_dedup.py --contents data/contents.csv --output data/contents_dedup.csv

  # 去重两个文件到指定目录
  python stock_sentiment_dedup.py --comments data/comments.csv --contents data/contents.csv --output-dir deduplicated/
        """
    )

    parser.add_argument('--auto', action='store_true',
                        help='自动模式：查找 data/xhs/csv/ 最新文件')
    parser.add_argument('--data-dir', type=str, default=None,
                        help='自动模式的数据目录（默认: 自动从项目根目录查找）')
    parser.add_argument('--comments', type=str,
                        help='Path to comments CSV file')
    parser.add_argument('--contents', type=str,
                        help='Path to contents CSV file')
    parser.add_argument('--output', type=str,
                        help='Output CSV file path (for single file input)')
    parser.add_argument('--output-dir', type=str, default='deduplicated',
                        help='Output directory for deduplicated files (default: deduplicated/)')
    parser.add_argument('--prefix', type=str, default='',
                        help='Prefix for output filenames (default: none)')

    args = parser.parse_args()

    print(f"\n{'='*60}")
    print("🧹 STOCK SENTIMENT DATA DEDUPLICATION TOOL")
    print(f"{'='*60}")

    success_count = 0

    # 自动模式
    if args.auto:
        print(f"\n🔍 自动模式：查找最新CSV文件...")
        print(f"   数据目录: {args.data_dir}")

        comments_file, contents_file = find_latest_csv_files(args.data_dir)

        if not comments_file and not contents_file:
            print("\n❌ 未找到任何CSV文件")
            return

        if comments_file:
            print(f"   ✓ 找到评论文件: {comments_file.name}")
            # 输出到同目录，添加 -dedup 后缀
            output_path = comments_file.parent / f"{comments_file.stem}-dedup.csv"
            if process_file(str(comments_file), str(output_path), "comments"):
                success_count += 1

        if contents_file:
            print(f"   ✓ 找到内容文件: {contents_file.name}")
            output_path = contents_file.parent / f"{contents_file.stem}-dedup.csv"
            if process_file(str(contents_file), str(output_path), "contents"):
                success_count += 1

    # 手动模式
    else:
        # Validate inputs
        if not args.comments and not args.contents:
            parser.error("请指定 --auto 自动模式，或提供 --comments/--contents 文件路径")

        # Process comments file
        if args.comments:
            if args.output and not args.contents:
                # Single file mode with custom output path
                output_path = args.output
            else:
                # Directory mode
                output_path = os.path.join(args.output_dir, f"{args.prefix}comments_dedup.csv")

            if process_file(args.comments, output_path, "comments"):
                success_count += 1

        # Process contents file
        if args.contents:
            if args.output and not args.comments:
                # Single file mode with custom output path
                output_path = args.output
            else:
                # Directory mode
                output_path = os.path.join(args.output_dir, f"{args.prefix}contents_dedup.csv")

            if process_file(args.contents, output_path, "contents"):
                success_count += 1

    # Final summary
    print(f"\n{'='*60}")
    if success_count == 2:
        print("✅ SUCCESS: Both files processed successfully!")
    elif success_count == 1:
        print("✅ SUCCESS: One file processed successfully!")
    else:
        print("❌ FAILED: No files were processed")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
