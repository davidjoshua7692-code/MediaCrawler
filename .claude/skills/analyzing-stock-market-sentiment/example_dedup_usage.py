"""
Example usage of the stock sentiment deduplication script.

This demonstrates how to use the deduplication tool programmatically.
"""

from stock_sentiment_dedup import load_csv_data, deduplicate_data, print_statistics, save_deduplicated_data


def example_deduplication():
    """
    Example showing how to use the deduplication functions directly in Python code.
    """
    print("\n" + "="*60)
    print("EXAMPLE: Deduplicating Stock Comments")
    print("="*60)

    # Example 1: Deduplicate comments
    comments_file = "data/comments.csv"  # Replace with actual path
    output_comments = "data/comments_dedup.csv"

    try:
        # Load data
        print("\n1. Loading comments data...")
        df_comments = load_csv_data(comments_file)

        # Deduplicate (keeping entries with highest like_count)
        print("\n2. Deduplicating based on content...")
        df_dedup, stats = deduplicate_data(
            df_comments,
            content_column='content',  # Column with text to compare
            like_column='like_count'   # Column to determine which duplicate to keep
        )

        # Show statistics
        print("\n3. Deduplication statistics:")
        print_statistics(stats, "comments")

        # Save result
        print("\n4. Saving deduplicated data...")
        save_deduplicated_data(df_dedup, output_comments)

        print("\n✅ Example completed successfully!")

    except FileNotFoundError as e:
        print(f"\n❌ File not found: {e}")
        print("💡 Tip: Update the file paths in example_dedup_usage.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def example_both_files():
    """
    Example showing how to deduplicate both comments and contents files.
    """
    print("\n" + "="*60)
    print("EXAMPLE: Deduplicating Both Comments and Contents")
    print("="*60)

    files = [
        ("data/comments.csv", "deduplicated/comments.csv", "comments"),
        ("data/contents.csv", "deduplicated/contents.csv", "contents"),
    ]

    for input_file, output_file, file_type in files:
        try:
            print(f"\n--- Processing {file_type} ---")
            df = load_csv_data(input_file)
            df_dedup, stats = deduplicate_data(df)
            print_statistics(stats, file_type)
            save_deduplicated_data(df_dedup, output_file)
        except FileNotFoundError:
            print(f"⚠️  Skipped {file_type}: File not found - {input_file}")
        except Exception as e:
            print(f"⚠️  Error processing {file_type}: {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("STOCK SENTIMENT DEDUPLICATION - USAGE EXAMPLES")
    print("="*60)

    print("\nThis script demonstrates two ways to use the deduplication tool:")
    print("\n1. Command-line usage (recommended for most users):")
    print("   python stock_sentiment_dedup.py --comments data/comments.csv --output data/clean.csv")
    print("   python stock_sentiment_dedup.py --comments comments.csv --contents contents.csv --output-dir clean/")

    print("\n2. Programmatic usage (for Python scripts):")
    print("   See example_deduplication() function below")

    print("\n" + "-"*60)
    print("Running example...")
    print("-"*60)

    # Run the example
    example_deduplication()
