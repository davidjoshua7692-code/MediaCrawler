#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用数据提取工具 - Universal Data Extractor
支持从MediaCrawler爬取的CSV数据中提取结构化信息

作者: Claude Code
用途: 社交媒体数据分析的通用提取工具
"""

import pandas as pd
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable
from collections import defaultdict
import argparse


class UniversalExtractor:
    """通用数据提取器"""

    def __init__(self, contents_file: str, comments_file: Optional[str] = None):
        """
        初始化提取器

        Args:
            contents_file: 帖子内容CSV文件路径
            comments_file: 评论CSV文件路径（可选）
        """
        self.contents_file = contents_file
        self.comments_file = comments_file
        self.df_contents = None
        self.df_comments = None

        self._load_data()

    def _load_data(self):
        """加载数据"""
        print(f"📂 加载数据文件...")
        self.df_contents = pd.read_csv(self.contents_file)
        print(f"✅ 帖子数据: {len(self.df_contents)} 条")

        if self.comments_file:
            self.df_comments = pd.read_csv(self.comments_file)
            print(f"✅ 评论数据: {len(self.df_comments)} 条")

    def extract_by_keywords(
        self,
        keywords: List[str],
        search_fields: List[str] = ['title', 'desc'],
        top_n: int = 20,
        sort_by: str = 'liked_count',
        ascending: bool = False
    ) -> List[Dict[str, Any]]:
        """
        根据关键词提取数据

        Args:
            keywords: 关键词列表
            search_fields: 搜索的字段列表
            top_n: 返回前N条结果
            sort_by: 排序字段
            ascending: 是否升序

        Returns:
            提取的结果列表
        """
        results = []

        for idx, row in self.df_contents.iterrows():
            # 在指定字段中搜索关键词
            for field in search_fields:
                text = str(row.get(field, ''))
                for keyword in keywords:
                    if keyword.lower() in text.lower():
                        results.append({
                            'title': row.get('title', ''),
                            'desc': str(row.get('desc', ''))[:200],
                            'liked': row.get('liked_count', 0),
                            'collected': row.get('collected_count', 0),
                            'comment_count': row.get('comment_count', 0),
                            'note_id': row.get('note_id', ''),
                            'matched_keyword': keyword,
                            'matched_field': field
                        })
                        break  # 避免重复添加

        # 去重
        seen = set()
        unique_results = []
        for item in results:
            key = (item['title'], item['note_id'])
            if key not in seen:
                seen.add(key)
                unique_results.append(item)

        # 排序
        unique_results.sort(key=lambda x: x.get(sort_by, 0), reverse=not ascending)

        return unique_results[:top_n]

    def extract_by_pattern(
        self,
        pattern: str,
        search_fields: List[str] = ['title', 'desc'],
        top_n: int = 20,
        sort_by: str = 'liked_count'
    ) -> List[Dict[str, Any]]:
        """
        根据正则表达式模式提取数据

        Args:
            pattern: 正则表达式模式
            search_fields: 搜索的字段列表
            top_n: 返回前N条结果
            sort_by: 排序字段

        Returns:
            提取的结果列表
        """
        results = []
        regex = re.compile(pattern)

        for idx, row in self.df_contents.iterrows():
            for field in search_fields:
                text = str(row.get(field, ''))
                match = regex.search(text)

                if match:
                    # 提取匹配的文本
                    matched_text = match.group(0) if match.groups() is None else match.group(1)

                    results.append({
                        'title': row.get('title', ''),
                        'desc': str(row.get('desc', ''))[:200],
                        'liked': row.get('liked_count', 0),
                        'matched_text': matched_text,
                        'note_id': row.get('note_id', '')
                    })
                    break

        results.sort(key=lambda x: x.get(sort_by, 0), reverse=True)
        return results[:top_n]

    def extract_prices(
        self,
        price_patterns: Optional[List[tuple]] = None,
        top_n: int = 20
    ) -> List[Dict[str, Any]]:
        """
        提取价格信息

        Args:
            price_patterns: 自定义价格模式列表，格式: [(正则, 价格类型), ...]
            top_n: 返回前N条结果

        Returns:
            价格信息列表
        """
        if price_patterns is None:
            # 默认价格模式
            price_patterns = [
                (r'(\d+)元.*天', '元/天'),
                (r'(\d+)块.*天', '块/天'),
                (r'(\d+)元.*小时', '元/小时'),
                (r'(\d+)块钱', '元'),
                (r'免费', '免费'),
                (r'(\d+)次.*卡', '次卡'),
                (r'(\d+).*月卡', '月卡'),
            ]

        results = []

        for idx, row in self.df_contents.iterrows():
            text = row.get('title', '') + ' ' + str(row.get('desc', ''))

            for pattern, price_type in price_patterns:
                match = re.search(pattern, text)
                if match:
                    if '免费' in pattern:
                        price_value = '免费'
                    else:
                        price_value = match.group(1) + ' ' + price_type

                    results.append({
                        'title': row.get('title', ''),
                        'price': price_value,
                        'price_type': price_type,
                        'liked': row.get('liked_count', 0),
                        'desc': str(row.get('desc', ''))[:200]
                    })
                    break

        results.sort(key=lambda x: x.get('liked', 0), reverse=True)
        return results[:top_n]

    def extract_locations(
        self,
        location_keywords: Optional[List[str]] = None,
        top_n: int = 10
    ) -> Dict[str, int]:
        """
        提取地理位置信息

        Args:
            location_keywords: 自定义地点关键词列表
            top_n: 返回前N个地点

        Returns:
            地点及其出现次数的字典
        """
        location_counts = defaultdict(int)

        for idx, row in self.df_contents.iterrows():
            text = row.get('title', '') + ' ' + str(row.get('desc', ''))

            if location_keywords:
                keywords = location_keywords
            else:
                # 默认提取常见地点模式
                keywords = re.findall(r'(上海.*?区|上海.*?路|上海.*?广场|上海.*?公园|.*?区|.*?路|.*?广场|.*?公园)', text)

            for keyword in keywords:
                if keyword in text:
                    location_counts[keyword] += 1

        # 排序
        sorted_locations = sorted(location_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_locations[:top_n])

    def extract_top_posts(
        self,
        top_n: int = 20,
        min_likes: int = 0
    ) -> List[Dict[str, Any]]:
        """
        提取热门帖子

        Args:
            top_n: 返回前N条
            min_likes: 最小点赞数过滤

        Returns:
            热门帖子列表
        """
        df_filtered = self.df_contents[self.df_contents.get('liked_count', 0) >= min_likes]
        df_sorted = df_filtered.sort_values('liked_count', ascending=False)

        results = []
        for idx, row in df_sorted.head(top_n).iterrows():
            results.append({
                'title': row.get('title', ''),
                'liked': row.get('liked_count', 0),
                'collected': row.get('collected_count', 0),
                'comments': row.get('comment_count', 0),
                'note_id': row.get('note_id', ''),
                'desc': str(row.get('desc', ''))[:300]
            })

        return results

    def extract_statistics(self) -> Dict[str, Any]:
        """
        提取数据统计信息

        Returns:
            统计信息字典
        """
        stats = {
            'total_posts': len(self.df_contents),
            'total_likes': int(self.df_contents.get('liked_count', 0).sum()),
            'avg_likes': float(self.df_contents.get('liked_count', 0).mean()),
            'max_likes': int(self.df_contents.get('liked_count', 0).max()),
            'total_comments': int(self.df_contents.get('comment_count', 0).sum()),
            'avg_comments': float(self.df_contents.get('comment_count', 0).mean()),
        }

        if self.df_comments is not None:
            stats['total_comments_posts'] = len(self.df_comments)

        return stats

    def extract_custom(
        self,
        filter_func: Callable,
        extract_func: Callable,
        top_n: int = 20
    ) -> List[Dict[str, Any]]:
        """
        自定义提取函数

        Args:
            filter_func: 过滤函数，接收row，返回bool
            extract_func: 提取函数，接收row，返回dict
            top_n: 返回前N条

        Returns:
            提取的结果列表
        """
        results = []

        for idx, row in self.df_contents.iterrows():
            if filter_func(row):
                extracted = extract_func(row)
                if extracted:
                    results.append(extracted)

        return results[:top_n]

    def print_results(
        self,
        results: List[Dict[str, Any]],
        title: str = "提取结果",
        max_desc_length: int = 150
    ):
        """
        美化打印结果

        Args:
            results: 结果列表
            title: 标题
            max_desc_length: 描述最大长度
        """
        print('\n' + '='*80)
        print(f'📊 {title}')
        print('='*80)
        print(f'✅ 找到 {len(results)} 条结果\n')

        for i, item in enumerate(results, 1):
            print(f"{i}. {item.get('title', 'N/A')[:70]}")

            # 动态显示所有字段
            for key, value in item.items():
                if key not in ['title', 'desc'] and value and value != 'N/A':
                    if key == 'liked':
                        print(f"   👍 点赞: {value}")
                    elif key == 'price':
                        print(f"   💰 价格: {value}")
                    elif key == 'matched_text':
                        print(f"   🔍 匹配: {value}")
                    elif key == 'matched_keyword':
                        print(f"   🔑 关键词: {value}")
                    elif key == 'collected':
                        print(f"   ⭐ 收藏: {value}")
                    elif key == 'comment_count' or key == 'comments':
                        print(f"   💬 评论: {value}")
                    else:
                        print(f"   {key}: {value}")

            if 'desc' in item and item['desc']:
                desc = item['desc']
                if len(desc) > max_desc_length:
                    desc = desc[:max_desc_length] + '...'
                print(f"   📝 {desc}")

            print('-'*80)

    def save_results(
        self,
        results: List[Dict[str, Any]],
        output_file: str,
        format: str = 'json'
    ):
        """
        保存结果到文件

        Args:
            results: 结果列表
            output_file: 输出文件路径
            format: 输出格式 ('json' 或 'csv')
        """
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"✅ 结果已保存到: {output_file}")

        elif format == 'csv':
            df = pd.DataFrame(results)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"✅ 结果已保存到: {output_file}")


# ============================================================================
# 命令行接口
# ============================================================================

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description='通用数据提取工具 - 从MediaCrawler CSV文件中提取结构化信息',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:

  # 1. 提取包含关键词的帖子
  python extractor.py contents.csv --keywords "一尺花园" "星巴克"

  # 2. 提取价格信息
  python extractor.py contents.csv --extract-prices --top 30

  # 3. 提取地理位置
  python extractor.py contents.csv --extract-locations --top 15

  # 4. 提取热门帖子
  python extractor.py contents.csv --top-posts --top 20

  # 5. 使用正则表达式提取
  python extractor.py contents.csv --pattern "(\d+)元.*天"

  # 6. 保存结果到JSON
  python extractor.py contents.csv --keywords "咖啡" --save results.json

  # 7. 同时加载帖子+评论数据
  python extractor.py contents.csv comments.csv --keywords "自习"
        """
    )

    parser.add_argument('contents_file', help='帖子内容CSV文件路径')
    parser.add_argument('comments_file', nargs='?', help='评论CSV文件路径（可选）')

    # 提取模式
    extract_group = parser.add_mutually_exclusive_group()
    extract_group.add_argument('--keywords', nargs='+', help='关键词列表')
    extract_group.add_argument('--pattern', help='正则表达式模式')
    extract_group.add_argument('--extract-prices', action='store_true', help='提取价格信息')
    extract_group.add_argument('--extract-locations', action='store_true', help='提取地理位置')
    extract_group.add_argument('--top-posts', action='store_true', help='提取热门帖子')
    extract_group.add_argument('--statistics', action='store_true', help='显示统计信息')

    # 选项参数
    parser.add_argument('--top', type=int, default=20, help='返回前N条结果（默认: 20）')
    parser.add_argument('--min-likes', type=int, default=0, help='最小点赞数过滤')
    parser.add_argument('--fields', nargs='+', default=['title', 'desc'], help='搜索字段列表')
    parser.add_argument('--sort-by', default='liked_count', help='排序字段')
    parser.add_argument('--save', help='保存结果到文件（自动识别格式: .json 或 .csv）')
    parser.add_argument('--format', choices=['json', 'csv'], help='输出格式')

    args = parser.parse_args()

    # 初始化提取器
    extractor = UniversalExtractor(args.contents_file, args.comments_file)

    results = None
    title = "提取结果"

    # 执行提取
    if args.keywords:
        results = extractor.extract_by_keywords(
            keywords=args.keywords,
            search_fields=args.fields,
            top_n=args.top,
            sort_by=args.sort_by
        )
        title = f"关键词搜索: {', '.join(args.keywords)}"

    elif args.pattern:
        results = extractor.extract_by_pattern(
            pattern=args.pattern,
            search_fields=args.fields,
            top_n=args.top
        )
        title = f"正则匹配: {args.pattern}"

    elif args.extract_prices:
        results = extractor.extract_prices(top_n=args.top)
        title = "价格信息提取"

    elif args.extract_locations:
        results = extractor.extract_locations(top_n=args.top)
        title = "地理位置分布"
        # 地理位置返回的是dict，特殊处理
        print('\n' + '='*80)
        print(f'📍 {title}')
        print('='*80)
        for location, count in results.items():
            print(f'{location}: {count}次')
        if args.save:
            extractor.save_results(
                [{'location': k, 'count': v} for k, v in results.items()],
                args.save,
                args.format or 'json'
            )
        return

    elif args.top_posts:
        results = extractor.extract_top_posts(top_n=args.top, min_likes=args.min_likes)
        title = f"热门帖子 TOP {args.top}"

    elif args.statistics:
        stats = extractor.extract_statistics()
        print('\n' + '='*80)
        print('📈 数据统计信息')
        print('='*80)
        for key, value in stats.items():
            print(f'{key}: {value}')
        return

    else:
        parser.print_help()
        return

    # 显示结果
    if results:
        extractor.print_results(results, title=title)

        # 保存结果
        if args.save:
            output_format = args.format
            if not output_format:
                # 根据文件扩展名自动识别
                if args.save.endswith('.csv'):
                    output_format = 'csv'
                else:
                    output_format = 'json'

            extractor.save_results(results, args.save, output_format)


if __name__ == '__main__':
    main()
