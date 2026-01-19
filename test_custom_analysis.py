"""
测试自定义关键词功能 - 模拟美食推荐场景
"""
from .claude.skills.mediacrawler_analyzer.analyze import analyze_mediacrawler_data

# 美食推荐关键词配置
food_keywords = {
    'features': {
        '口味': ['好吃', '美味', '正宗', '口感', '味道', '香'],
        '环境': ['装修', '氛围', '环境', '装潢', '档次', '干净'],
        '服务': ['服务', '服务员', '态度', '热情', '周到'],
        '价格': ['便宜', '实惠', '性价比', '平价', '亲民', '实惠'],
        '分量': ['分量', '量足', '量少', '量大', '管饱'],
        '等待时间': ['排队', '等位', '上菜快', '上菜慢', '等很久']
    },
    'sentiment': {
        'positive': ['推荐', '赞', '爱了', '满意', '惊喜', '超出预期', '必吃'],
        'negative': ['失望', '差', '不值', '坑', '不会再来', '踩雷', '后悔']
    }
}

print("测试自定义关键词功能（模拟美食场景）")
print("=" * 80)

results = analyze_mediacrawler_data(
    contents_file='data/xhs/csv/search_contents_2026-01-19.csv',
    comments_file='data/xhs/csv/search_comments_2026-01-19.csv',
    custom_keywords=food_keywords,
    custom_title='🍜 美食推荐数据分析（模拟测试）'
)

print(f"\n分析结果:")
print(f"  平台: {results['platform']}")
print(f"  帖子数: {results['contents_count']}")
print(f"  评论数: {results['comments_count']}")
print(f"  Top特征: {results['top_features'][:3]}")
