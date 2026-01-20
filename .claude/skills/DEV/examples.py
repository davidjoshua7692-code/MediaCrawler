#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用提取工具 - 快速开始示例

这个文件包含了常见的使用场景，可以直接复制修改
"""

from extractor import UniversalExtractor


# ============================================================================
# 示例1：提取咖啡厅品牌
# ============================================================================

def example_1_cafe_brands():
    """提取咖啡厅品牌"""
    print("\n" + "="*80)
    print("示例1：提取咖啡厅品牌")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 提取品牌
    brands = ['一尺花园', '星巴克', 'Manner', '瑞幸', 'Costa']
    results = extractor.extract_by_keywords(
        keywords=brands,
        top_n=30
    )

    extractor.print_results(results, title="咖啡厅品牌提取")

    # 保存结果
    extractor.save_results(results, 'output/brands.json')


# ============================================================================
# 示例2：提取价格信息
# ============================================================================

def example_2_extract_prices():
    """提取价格信息"""
    print("\n" + "="*80)
    print("示例2：提取价格信息")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 提取价格
    prices = extractor.extract_prices(top_n=50)

    extractor.print_results(prices, title="价格信息提取")

    # 保存为CSV（方便Excel打开）
    extractor.save_results(prices, 'output/prices.csv', format='csv')


# ============================================================================
# 示例3：分析地理位置分布
# ============================================================================

def example_3_location_analysis():
    """分析地理位置分布"""
    print("\n" + "="*80)
    print("示例3：地理位置分析")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 自定义地点关键词
    locations = extractor.extract_locations(
        location_keywords=[
            '宝山区', '淞沪铁路', '智慧湾', '顾村', '杨行',
            '吴淞', '大场', '上海大学', '宝杨路', '友谊路'
        ],
        top_n=20
    )

    print("\n📍 地理位置分布:")
    print("-"*80)
    for location, count in locations.items():
        print(f"{location}: {count}次")


# ============================================================================
# 示例4：查找高性价比店铺
# ============================================================================

def example_4_value_for_money():
    """查找高性价比店铺"""
    print("\n" + "="*80)
    print("示例4：查找高性价比店铺")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 先提取价格信息
    prices = extractor.extract_prices(top_n=100)

    # 过滤出低价位（<50元或免费）
    value_shops = []
    for item in prices:
        price_text = item.get('price', '')

        if '免费' in price_text:
            value_shops.append(item)
        elif any(num in price_text for num in ['11', '20', '30']):
            value_shops.append(item)

    extractor.print_results(value_shops[:20], title="高性价比店铺")

    extractor.save_results(value_shops, 'output/value_shops.json')


# ============================================================================
# 示例5：提取热门帖子
# ============================================================================

def example_5_top_posts():
    """提取热门帖子"""
    print("\n" + "="*80)
    print("示例5：提取热门帖子")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 提取点赞>1000的帖子
    top_posts = extractor.extract_top_posts(
        top_n=20,
        min_likes=1000
    )

    extractor.print_results(top_posts, title="热门帖子 TOP 20")

    extractor.save_results(top_posts, 'output/top_posts.json')


# ============================================================================
# 示例6：使用正则表达式提取特定信息
# ============================================================================

def example_6_regex_pattern():
    """使用正则表达式提取"""
    print("\n" + "="*80)
    print("示例6：正则表达式提取")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 提取营业时间信息
    results = extractor.extract_by_pattern(
        pattern=r'(\d+:\d+\s*[-至]\s*\d+:\d+)',  # 匹配 10:00-20:00
        search_fields=['desc'],
        top_n=20
    )

    extractor.print_results(results, title="营业时间信息")


# ============================================================================
# 示例7：自定义提取逻辑
# ============================================================================

def example_7_custom_extraction():
    """自定义提取逻辑"""
    print("\n" + "="*80)
    print("示例7：自定义提取")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 自定义过滤和提取函数
    def filter_function(row):
        """只保留包含'宝山'且点赞>100的帖子"""
        text = str(row.get('title', '')) + str(row.get('desc', ''))
        return '宝山' in text and row.get('liked_count', 0) > 100

    def extract_function(row):
        """提取自定义字段"""
        title = row.get('title', '')
        desc = str(row.get('desc', ''))

        # 提取地址
        import re
        address_match = re.search(r'地址[：:]\s*(.*?)(?:\n|$)', desc)
        address = address_match.group(1) if address_match else '未找到'

        return {
            'title': title,
            'liked': row.get('liked_count', 0),
            'address': address[:50],
            'has_plug': '插座' in desc or '电源' in desc,
            'has_wifi': 'WiFi' in desc or 'wifi' in desc or '无线' in desc,
        }

    results = extractor.extract_custom(
        filter_func=filter_function,
        extract_func=extract_function,
        top_n=20
    )

    extractor.print_results(results, title="宝山区店铺详情")

    extractor.save_results(results, 'output/custom_extraction.json')


# ============================================================================
# 示例8：统计分析
# ============================================================================

def example_8_statistics():
    """统计分析"""
    print("\n" + "="*80)
    print("示例8：统计分析")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 获取统计信息
    stats = extractor.extract_statistics()

    print("\n📈 数据统计:")
    print("-"*80)
    for key, value in stats.items():
        print(f"{key}: {value:,}")


# ============================================================================
# 示例9：组合多个操作
# ============================================================================

def example_9_combined_analysis():
    """组合分析流程"""
    print("\n" + "="*80)
    print("示例9：组合分析")
    print("="*80)

    extractor = UniversalExtractor(
        contents_file=r'd:\MediaCrawler-main\data\xhs\csv\search_contents_2026-01-20.csv'
    )

    # 步骤1：提取宝山相关帖子
    baoshan_posts = extractor.extract_by_keywords(
        keywords=['宝山'],
        top_n=50
    )

    # 步骤2：提取价格信息
    all_prices = extractor.extract_prices(top_n=100)

    # 步骤3：提取地理位置
    locations = extractor.extract_locations(top_n=15)

    # 步骤4：提取热门帖子
    top_posts = extractor.extract_top_posts(top_n=10)

    # 打印综合报告
    print("\n" + "="*80)
    print("📊 宝山区域综合分析报告")
    print("="*80)

    print(f"\n1️⃣ 宝山相关帖子: {len(baoshan_posts)} 条")
    print(f"2️⃣ 价格信息: {len(all_prices)} 条")
    print(f"3️⃣ 涉及地点: {len(locations)} 个")
    print(f"4️⃣ 热门帖子: {len(top_posts)} 条")

    print("\n📍 TOP 5 地点:")
    for i, (loc, count) in enumerate(list(locations.items())[:5], 1):
        print(f"   {i}. {loc}: {count}次")

    print("\n💰 TOP 5 价格信息:")
    for i, price in enumerate(all_prices[:5], 1):
        print(f"   {i}. {price['title'][:40]}... | {price['price']}")

    # 保存综合报告
    report = {
        'summary': {
            'baoshan_posts': len(baoshan_posts),
            'price_info': len(all_prices),
            'locations': len(locations),
            'top_posts': len(top_posts)
        },
        'details': {
            'locations': locations,
            'top_prices': all_prices[:10],
            'top_posts': top_posts[:10]
        }
    }

    extractor.save_results(report, 'output/combined_report.json')


# ============================================================================
# 主程序
# ============================================================================

if __name__ == '__main__':
    import sys

    # 可通过命令行参数选择运行哪个示例
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        examples = {
            '1': example_1_cafe_brands,
            '2': example_2_extract_prices,
            '3': example_3_location_analysis,
            '4': example_4_value_for_money,
            '5': example_5_top_posts,
            '6': example_6_regex_pattern,
            '7': example_7_custom_extraction,
            '8': example_8_statistics,
            '9': example_9_combined_analysis,
        }

        if example_num in examples:
            examples[example_num]()
        else:
            print(f"❌ 未找到示例 {example_num}")
            print("可用示例: 1-9")
    else:
        # 运行所有示例
        print("\n" + "="*80)
        print("🚀 运行所有示例")
        print("="*80)

        # 创建输出目录
        import os
        os.makedirs('output', exist_ok=True)

        # 运行示例
        example_1_cafe_brands()
        example_2_extract_prices()
        example_3_location_analysis()
        example_4_value_for_money()
        example_5_top_posts()
        example_8_statistics()
        example_9_combined_analysis()

        print("\n" + "="*80)
        print("✅ 所有示例运行完成！")
        print("📁 结果已保存到 output/ 目录")
        print("="*80)
