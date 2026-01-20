"""
Test script to validate deduplication logic with sample data.

This script creates sample CSV files, runs deduplication, and verifies results.
"""

import pandas as pd
import os
import sys
from stock_sentiment_dedup import deduplicate_data, save_deduplicated_data, load_csv_data


def create_test_data():
    """
    Create test CSV files with known duplicates for validation.

    Test scenarios covered:
    1. Exact duplicates with different like counts
    2. Case-insensitive duplicates
    3. Whitespace differences
    4. Empty content removal
    5. Unique entries (should be kept)
    """

    print("\n" + "="*60)
    print("CREATING TEST DATA")
    print("="*60)

    # Test comments data
    comments_data = {
        'content': [
            'This stock will go to the moon! 🚀',  # ID: 1, likes: 45
            'This stock will go to the moon! 🚀',  # ID: 2, likes: 12 (duplicate, lower likes)
            'Great earnings report',               # ID: 3, likes: 23 (unique)
            'Buy now before it\'s too late',       # ID: 4, likes: 8 (unique)
            'THIS STOCK WILL GO TO THE MOON! 🚀',  # ID: 5, likes: 30 (case-insensitive duplicate)
            '   Great earnings report   ',         # ID: 6, likes: 15 (whitespace duplicate, lower)
            '',                                    # ID: 7, likes: 5 (empty content)
            'Strong buy recommendation',           # ID: 8, likes: 18 (unique)
            'This stock will go to the moon! 🚀',  # ID: 9, likes: 50 (duplicate, highest likes!)
            'Bearish trend ahead',                 # ID: 10, likes: 7 (unique)
        ],
        'like_count': [45, 12, 23, 8, 30, 15, 5, 18, 50, 7],
        'user': ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'user8', 'user9', 'user10']
    }

    comments_df = pd.DataFrame(comments_data)
    test_comments_file = 'test_comments.csv'
    comments_df.to_csv(test_comments_file, index=False)
    print(f"✓ Created test file: {test_comments_file}")
    print(f"  Total records: {len(comments_df)}")
    print(f"  Expected duplicates: 4 (3x 'moon', 1x 'earnings')")
    print(f"  Expected unique: 6 (after removing 1 empty)")

    # Test contents data
    contents_data = {
        'content': [
            'Apple stock analysis Q4 2024',  # ID: 1
            'Apple stock analysis Q4 2024',  # ID: 2 (duplicate)
            'Tesla vs BYD comparison',       # ID: 3 (unique)
            'NVDA earnings preview',         # ID: 4 (unique)
            'apple stock analysis q4 2024',  # ID: 5 (case-insensitive duplicate)
        ],
        'like_count': [100, 50, 75, 120, 80],
        'title': ['Apple Analysis', 'Apple Analysis Duplicate', 'Tesla Comparison',
                  'NVDA Preview', 'Apple Analysis Lowercase']
    }

    contents_df = pd.DataFrame(contents_data)
    test_contents_file = 'test_contents.csv'
    contents_df.to_csv(test_contents_file, index=False)
    print(f"\n✓ Created test file: {test_contents_file}")
    print(f"  Total records: {len(contents_df)}")
    print(f"  Expected duplicates: 2 (Apple)")
    print(f"  Expected unique: 3")

    return test_comments_file, test_contents_file


def run_deduplication_tests():
    """
    Run deduplication tests and verify results.
    """

    print("\n" + "="*60)
    print("RUNNING DEDUPLICATION TESTS")
    print("="*60)

    # Create test data
    test_comments, test_contents = create_test_data()

    test_results = []

    # Test 1: Comments deduplication
    print("\n" + "-"*60)
    print("TEST 1: Comments Deduplication")
    print("-"*60)

    try:
        df_comments = load_csv_data(test_comments)
        df_comments_dedup, stats = deduplicate_data(df_comments)

        print(f"\nResults:")
        print(f"  Original: {stats['original_count']}")
        print(f"  Empty removed: {stats['empty_removed']}")
        print(f"  Duplicates removed: {stats['duplicate_count']}")
        print(f"  Final unique: {stats['unique_count']}")

        # Verify expectations
        expected_unique = 6  # 7 non-empty - 1 duplicate ('earnings') - 2 duplicate ('moon')
        expected_duplicates = 4  # 3x 'moon' duplicates + 1x 'earnings' duplicate
        expected_empty = 1

        success = (
            stats['unique_count'] == expected_unique and
            stats['duplicate_count'] == expected_duplicates and
            stats['empty_removed'] == expected_empty
        )

        test_results.append(("Comments Deduplication", success, stats))

        if success:
            print(f"\n✅ TEST PASSED: Results match expectations")
        else:
            print(f"\n❌ TEST FAILED: Results don't match expectations")
            print(f"   Expected: {expected_unique} unique, {expected_duplicates} duplicates, {expected_empty} empty")
            print(f"   Got: {stats['unique_count']} unique, {stats['duplicate_count']} duplicates, {stats['empty_removed']} empty")

        # Show which records were kept
        print(f"\nRecords kept (showing content and like_count):")
        for idx, row in df_comments_dedup.iterrows():
            content_preview = row['content'][:50] + '...' if len(row['content']) > 50 else row['content']
            print(f"  - {content_preview}: {row['like_count']} likes")

        # Verify highest likes kept for duplicates
        moon_entries = df_comments_dedup[df_comments_dedup['content'].str.contains('moon', case=False, na=False)]
        if not moon_entries.empty:
            moon_likes = moon_entries['like_count'].values[0]
            if moon_likes == 50:
                print(f"\n✅ VERIFIED: 'Moon' entry kept has highest likes (50)")
            else:
                print(f"\n❌ ERROR: 'Moon' entry has {moon_likes} likes, expected 50")

    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}")
        test_results.append(("Comments Deduplication", False, None))

    # Test 2: Contents deduplication
    print("\n" + "-"*60)
    print("TEST 2: Contents Deduplication")
    print("-"*60)

    try:
        df_contents = load_csv_data(test_contents)
        df_contents_dedup, stats = deduplicate_data(df_contents)

        print(f"\nResults:")
        print(f"  Original: {stats['original_count']}")
        print(f"  Duplicates removed: {stats['duplicate_count']}")
        print(f"  Final unique: {stats['unique_count']}")

        # Verify expectations
        expected_unique = 3  # 5 - 2 duplicates (Apple)

        success = (
            stats['unique_count'] == expected_unique and
            stats['duplicate_count'] == 2
        )

        test_results.append(("Contents Deduplication", success, stats))

        if success:
            print(f"\n✅ TEST PASSED: Results match expectations")
        else:
            print(f"\n❌ TEST FAILED: Results don't match expectations")
            print(f"   Expected: {expected_unique} unique, 2 duplicates")
            print(f"   Got: {stats['unique_count']} unique, {stats['duplicate_count']} duplicates")

        # Show which records were kept
        print(f"\nRecords kept:")
        for idx, row in df_contents_dedup.iterrows():
            print(f"  - {row['content']}: {row['like_count']} likes")

    except Exception as e:
        print(f"\n❌ TEST ERROR: {str(e)}")
        test_results.append(("Contents Deduplication", False, None))

    # Save deduplicated test files
    print("\n" + "-"*60)
    print("SAVING DEDUPLICATED TEST FILES")
    print("-"*60)

    try:
        save_deduplicated_data(df_comments_dedup, 'test_comments_dedup.csv')
        save_deduplicated_data(df_contents_dedup, 'test_contents_dedup.csv')
    except Exception as e:
        print(f"⚠️  Could not save test files: {e}")

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success, _ in test_results if success)
    total = len(test_results)

    for test_name, success, stats in test_results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Deduplication logic is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please review the results.")

    # Cleanup
    print("\n" + "-"*60)
    print("CLEANUP")
    print("-"*60)
    print("Test files created (you can manually delete them):")
    print("  - test_comments.csv")
    print("  - test_contents.csv")
    print("  - test_comments_dedup.csv")
    print("  - test_contents_dedup.csv")

    cleanup = input("\nDelete test files? (y/n): ").strip().lower()
    if cleanup == 'y':
        for file in ['test_comments.csv', 'test_contents.csv',
                     'test_comments_dedup.csv', 'test_contents_dedup.csv']:
            if os.path.exists(file):
                os.remove(file)
                print(f"  ✓ Deleted: {file}")

    return passed == total


if __name__ == "__main__":
    print("\n" + "="*60)
    print("STOCK SENTIMENT DEDUPLICATION - TEST SUITE")
    print("="*60)

    try:
        all_passed = run_deduplication_tests()
        sys.exit(0 if all_passed else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
