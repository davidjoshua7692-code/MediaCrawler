"""
MediaCrawler 智能数据分析器
自动识别平台类型并加载相应的分析配置
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# ============================================================================
# 平台分析配置库
# ============================================================================

PLATFORM_ANALYSIS_CONFIG = {
    'xiaohongshu': {
        'name': '小红书',
        'platform_keywords': ['note_id', 'xsec_token', 'collected_count'],
        'content_fields': ['title', 'desc', 'tag_list'],
        'metrics': ['liked_count', 'collected_count', 'comment_count', 'share_count'],
        'text_fields': ['title', 'desc'],
        'location_field': 'ip_location',
        'special_keywords': {
            'features': {
                '安静': ['安静', '清净', '不吵', 'silent', 'quiet'],
                '插座': ['插座', '电源', '充电', 'plug'],
                '网络': ['wifi', 'wi-fi', '网速', '网络'],
                '停车位': ['停车', 'parking', '停车券'],
                '有厕所': ['厕所', '卫生间', '洗手间', 'wc'],
                '价格': ['价格', '便宜', '贵', '实惠', '人均'],
            },
            'sentiment': {
                'positive': ['推荐', '好', '不错', '舒服', '棒', '喜欢', '适合', '方便'],
                'negative': ['吵', '贵', '差', '不好', '失望', '慢', '挤']
            }
        }
    },
    'douyin': {
        'name': '抖音',
        'platform_keywords': ['aweme_id', 'sec_uid'],
        'content_fields': ['title', 'desc'],
        'metrics': ['liked_count', 'comment_count', 'share_count'],
        'text_fields': ['title', 'desc'],
        'location_field': 'ip_location',
        'special_keywords': {
            'features': {},
            'sentiment': {
                'positive': ['好看', '不错', '推荐', '喜欢', '爱了'],
                'negative': ['不好看', '无聊', '差']
            }
        }
    },
    'bilibili': {
        'name': 'B站',
        'platform_keywords': ['bvid', 'video_play_count'],
        'content_fields': ['title', 'desc'],
        'metrics': ['liked_count', 'video_play_count', 'video_coin_count', 'video_collect_count'],
        'text_fields': ['title', 'desc'],
        'location_field': None,
        'special_keywords': {
            'features': {},
            'sentiment': {
                'positive': ['好看', '不错', '推荐', '干货', '实用'],
                'negative': ['水', '不好看', '差']
            }
        }
    },
    'weibo': {
        'name': '微博',
        'platform_keywords': ['mid', 'mblogid'],
        'content_fields': ['text', 'topic_list'],
        'metrics': ['liked_count', 'comments_count', 'reposts_count'],
        'text_fields': ['text'],
        'location_field': None,
        'special_keywords': {
            'features': {},
            'sentiment': {
                'positive': ['赞', '支持', '推荐'],
                'negative': ['吐槽', '差']
            }
        }
    }
}

# ============================================================================
# 平台检测器
# ============================================================================

def detect_platform(contents_df, comments_df=None):
    """
    智能检测平台类型

    Args:
        contents_df: 内容DataFrame
        comments_df: 评论DataFrame（可选）

    Returns:
        str: 平台标识符
    """
    columns = set(contents_df.columns.tolist())

    # 通过特征列名识别平台
    for platform_id, config in PLATFORM_ANALYSIS_CONFIG.items():
        if any(keyword in columns for keyword in config['platform_keywords']):
            return platform_id

    # 如果无法识别，尝试从文件路径推断
    # （调用方需要传入文件路径参数）

    return 'generic'

def extract_locations(text, platform='xiaohongshu'):
    """
    提取地理位置信息

    Args:
        text: 文本内容
        platform: 平台类型

    Returns:
        list: 提取到的地点列表
    """
    locations = []

    if pd.isna(text):
        return locations

    text_str = str(text)

    # 通用地点模式
    location_patterns = [
        r'(\w+路)', r'(\w+广场)', r'(\w+商场)', r'(\w+购物中心)',
        r'(\w+大学)', r'(\w+公园)', r'图书馆', r'地铁站'
    ]

    # 平台特定地点
    if platform == 'xiaohongshu':
        shanghai_districts = [
            '徐汇', '静安', '黄浦', '长宁', '普陀', '虹口',
            '杨浦', '浦东', '闵行', '宝山', '嘉定', '松江',
            '青浦', '奉贤', '金山', '崇明'
        ]
        location_patterns.insert(0, r'(' + '|'.join(shanghai_districts) + r')')

    for pattern in location_patterns:
        matches = re.findall(pattern, text_str)
        locations.extend(matches)

    return locations

def analyze_features(text, platform='xiaohongshu', custom_keywords=None):
    """
    分析文本特征

    Args:
        text: 文本内容
        platform: 平台类型
        custom_keywords: 自定义关键词字典（可选）

    Returns:
        list: 提取到的特征列表
    """
    features = []

    if pd.isna(text):
        return features

    text_lower = str(text).lower()

    # 使用自定义关键词或平台默认关键词
    if custom_keywords and 'features' in custom_keywords:
        feature_keywords = custom_keywords['features']
    else:
        feature_keywords = PLATFORM_ANALYSIS_CONFIG.get(
            platform, {}
        ).get('special_keywords', {}).get('features', {})

    for feature, keywords in feature_keywords.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                features.append(feature)
                break

    return features

def analyze_sentiment(text, platform='xiaohongshu', custom_keywords=None):
    """
    分析情感倾向

    Args:
        text: 文本内容
        platform: 平台类型
        custom_keywords: 自定义关键词字典（可选）

    Returns:
        str: 'positive', 'negative', 或 'neutral'
    """
    if pd.isna(text):
        return 'neutral'

    text_lower = str(text).lower()

    # 使用自定义关键词或平台默认关键词
    if custom_keywords and 'sentiment' in custom_keywords:
        sentiment_keywords = custom_keywords['sentiment']
    else:
        sentiment_keywords = PLATFORM_ANALYSIS_CONFIG.get(
            platform, {}
        ).get('special_keywords', {}).get('sentiment', {})

    positive_words = sentiment_keywords.get('positive', [])
    negative_words = sentiment_keywords.get('negative', [])

    for word in positive_words:
        if word.lower() in text_lower:
            return 'positive'

    for word in negative_words:
        if word.lower() in text_lower:
            return 'negative'

    return 'neutral'

# ============================================================================
# 主分析函数
# ============================================================================

def analyze_mediacrawler_data(
    contents_file,
    comments_file=None,
    custom_keywords=None,
    custom_title=None
):
    """
    综合分析MediaCrawler爬取的数据

    Args:
        contents_file: 内容CSV文件路径
        comments_file: 评论CSV文件路径（可选）
        custom_keywords: 自定义关键词字典，格式：
            {
                'features': {
                    '特征名': ['关键词1', '关键词2'],
                    ...
                },
                'sentiment': {
                    'positive': ['好词1', '好词2'],
                    'negative': ['坏词1', '坏词2']
                }
            }
        custom_title: 自定义分析报告标题

    Returns:
        dict: 分析结果和可视化文件路径
    """
    # 读取数据
    df_contents = pd.read_csv(contents_file)
    df_comments = pd.read_csv(comments_file) if comments_file else None

    # 智能检测平台
    platform = detect_platform(df_contents, df_comments)
    platform_config = PLATFORM_ANALYSIS_CONFIG.get(platform, {})
    platform_name = platform_config.get('name', platform.title())

    # 自定义标题
    if not custom_title:
        custom_title = f"📊 {platform_name}数据分析报告"

    print("=" * 80)
    print(custom_title)
    print("=" * 80)

    # 数据概览
    print(f"\n✅ 平台识别: {platform_name} ({platform})")
    print(f"✅ 数据加载成功!")
    print(f"   帖子数据: {len(df_contents)} 条")
    if df_comments is not None:
        print(f"   评论数据: {len(df_comments)} 条")

    # 1. 基础统计
    print("\n" + "=" * 80)
    print("📈 一、基础数据统计")
    print("=" * 80)

    metrics = platform_config.get('metrics', [])
    metric_names = [m for m in metrics if m in df_contents.columns]

    if metric_names:
        print(f"\n互动数据统计:")
        for metric in metric_names:
            mean_val = df_contents[metric].mean()
            max_val = df_contents[metric].max()
            metric_label = metric.replace('_', ' ').title()
            print(f"  平均{metric_label}: {mean_val:.1f}")
            print(f"  最高{metric_label}: {max_val}")

    # 2. 地理位置分析
    print("\n" + "=" * 80)
    print("📍 二、地理位置分析")
    print("=" * 80)

    location_field = platform_config.get('location_field')
    all_locations = []

    if location_field and location_field in df_contents.columns:
        # 从专用字段提取
        locations_data = df_contents[location_field].value_counts().head(10)
        print(f"\n{location_field} 分布 Top 10:")
        for loc, count in locations_data.items():
            if pd.notna(loc):
                print(f"  {loc}: {count} 次")
    else:
        # 从文本中提取
        text_fields = platform_config.get('text_fields', [])
        for idx, row in df_contents.iterrows():
            text = ' '.join([str(row.get(field, '')) for field in text_fields])
            locations = extract_locations(text, platform)
            all_locations.extend(locations)

        location_counter = Counter(all_locations)
        if location_counter:
            print(f"\n文本中提及的地点 Top 10:")
            for location, count in location_counter.most_common(10):
                print(f"  {location}: {count} 次")

    # 3. 特征分析
    print("\n" + "=" * 80)
    print("🎯 三、内容特征分析")
    print("=" * 80)

    all_features = []
    text_fields = platform_config.get('text_fields', [])

    for idx, row in df_contents.iterrows():
        text = ' '.join([str(row.get(field, '')) for field in text_fields])
        features = analyze_features(text, platform, custom_keywords)
        all_features.extend(features)

    feature_counter = Counter(all_features)

    if feature_counter:
        print(f"\n特征提及次数 Top 10:")
        for feature, count in feature_counter.most_common(10):
            print(f"  {feature}: {count} 次")
    else:
        print("\n未检测到显著特征（可使用custom_keywords参数自定义特征库）")

    # 4. 情感分析
    if df_comments is not None:
        print("\n" + "=" * 80)
        print("💬 四、评论情感分析")
        print("=" * 80)

        sentiment_results = {'positive': 0, 'negative': 0, 'neutral': 0}

        for idx, row in df_comments.head(200).iterrows():
            comment = row.get('content', '')
            sentiment = analyze_sentiment(comment, platform, custom_keywords)
            sentiment_results[sentiment] += 1

        total = sentiment_results['positive'] + sentiment_results['negative']
        positive_pct = (sentiment_results['positive'] / total * 100) if total > 0 else 0

        print(f"\n评论情感分布 (基于前200条评论):")
        print(f"  积极: {sentiment_results['positive']} 条")
        print(f"  消极: {sentiment_results['negative']} 条")
        print(f"  中性: {sentiment_results['neutral']} 条")
        if total > 0:
            print(f"  积极占比: {positive_pct:.1f}%")

    # 5. 创建可视化
    print("\n" + "=" * 80)
    print("📊 五、生成可视化图表")
    print("=" * 80)

    output_file = create_visualizations(
        df_contents,
        df_comments,
        platform,
        platform_config,
        location_counter if all_locations else None,
        feature_counter
    )

    print(f"\n✅ 图表已保存: {output_file}")

    # 6. 热门内容
    print("\n" + "=" * 80)
    print("🔥 六、热门内容 Top 3")
    print("=" * 80)

    if metric_names:
        primary_metric = metric_names[0]
        top_contents = df_contents.nlargest(3, primary_metric)

        for idx, row in top_contents.iterrows():
            title = row.get('title', row.get('text', 'N/A'))
            print(f"\n  {str(title)[:60]}...")
            print(f"  👍 {row[primary_metric]} {primary_metric}")

    # 7. 关键洞察
    print("\n" + "=" * 80)
    print("💡 七、关键洞察")
    print("=" * 80)

    insights = []

    if feature_counter:
        top_feature = feature_counter.most_common(1)[0]
        insights.append(f"用户最关注: {top_feature[0]} (提及{top_feature[1]}次)")

    if all_locations:
        top_location = location_counter.most_common(1)[0]
        insights.append(f"最热门区域: {top_location[0]} (提及{top_location[1]}次)")

    if df_comments is not None:
        insights.append(f"评论情感倾向: 积极{positive_pct:.1f}%")

    if metric_names and len(metric_names) >= 2:
        metric1_mean = df_contents[metric_names[0]].mean()
        metric2_mean = df_contents[metric_names[1]].mean()
        ratio = metric2_mean / metric1_mean if metric1_mean > 0 else 0
        insights.append(f"{metric_names[1]}是{metric_names[0]}的{ratio:.2f}倍")

    for insight in insights:
        print(f"  • {insight}")

    print("\n" + "=" * 80)
    print("✅ 分析完成!")
    print("=" * 80)

    return {
        'platform': platform,
        'contents_count': len(df_contents),
        'comments_count': len(df_comments) if df_comments is not None else 0,
        'top_features': feature_counter.most_common(5),
        'top_locations': location_counter.most_common(5) if all_locations else [],
        'visualization': output_file
    }

def create_visualizations(
    df_contents,
    df_comments,
    platform,
    platform_config,
    location_counter,
    feature_counter
):
    """创建综合可视化图表"""

    fig = plt.figure(figsize=(16, 12))
    metrics = platform_config.get('metrics', [])
    available_metrics = [m for m in metrics if m in df_contents.columns]

    # 图1: 互动数据分布
    ax1 = plt.subplot(2, 3, 1)
    if available_metrics:
        for metric in available_metrics[:3]:
            data = df_contents[metric].dropna()
            if len(data) > 0:
                plt.hist(data, bins=20, alpha=0.5, label=metric.replace('_', ' ').title())
        plt.xlabel('数量')
        plt.ylabel('帖子数')
        plt.title('互动数据分布')
        plt.legend()
        plt.grid(True, alpha=0.3)

    # 图2: 互动数据相关性
    ax2 = plt.subplot(2, 3, 2)
    if len(available_metrics) > 1:
        corr_data = df_contents[available_metrics].dropna()
        if len(corr_data) > 0:
            corr = corr_data.corr()
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                       square=True, linewidths=1, ax=ax2, cbar_kws={'shrink': 0.8})
            ax2.set_title('互动数据相关性')

    # 图3: 热门区域/地点
    ax3 = plt.subplot(2, 3, 3)
    if location_counter:
        top_locations = dict(location_counter.most_common(10))
        plt.barh(range(len(top_locations)), list(top_locations.values()))
        plt.yticks(range(len(top_locations)), list(top_locations.keys()))
        plt.xlabel('提及次数')
        plt.title('热门地点 Top 10')
        plt.grid(True, alpha=0.3, axis='x')

    # 图4: 内容特征排名
    ax4 = plt.subplot(2, 3, 4)
    if feature_counter:
        top_features = dict(feature_counter.most_common(10))
        plt.barh(range(len(top_features)), list(top_features.values()))
        plt.yticks(range(len(top_features)), list(top_features.keys()))
        plt.xlabel('提及次数')
        plt.title('内容特征 Top 10')
        plt.grid(True, alpha=0.3, axis='x')

    # 图5: IP地点分布（如果有）
    ax5 = plt.subplot(2, 3, 5)
    location_field = platform_config.get('location_field')
    if location_field and location_field in df_contents.columns:
        ip_locations = df_contents[location_field].value_counts().head(10)
        if len(ip_locations) > 0:
            plt.barh(range(len(ip_locations)), ip_locations.values)
            plt.yticks(range(len(ip_locations)), ip_locations.index)
            plt.xlabel('帖子数')
            plt.title(f'{location_field} 分布')
            plt.grid(True, alpha=0.3, axis='x')

    # 图6: 数据质量
    ax6 = plt.subplot(2, 3, 6)
    missing_data = df_contents.isnull().sum()
    missing_data = missing_data[missing_data > 0].sort_values(ascending=True)
    if len(missing_data) > 0:
        plt.barh(range(len(missing_data)), missing_data.values)
        plt.yticks(range(len(missing_data)), missing_data.index)
        plt.xlabel('缺失数量')
        plt.title('数据缺失情况')
        plt.grid(True, alpha=0.3, axis='x')
    else:
        ax6.text(0.5, 0.5, '数据完整\n无缺失', ha='center', va='center',
                fontsize=14, transform=ax6.transAxes)
        ax6.set_title('数据质量')

    plt.tight_layout()

    output_file = f'd:/MediaCrawler-main/{platform}_analysis.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()

    return output_file

# ============================================================================
# 命令行接口
# ============================================================================

if __name__ == "__main__":
    import sys

    # 简单的命令行接口
    if len(sys.argv) < 2:
        print("用法: python analyze.py <contents.csv> [comments.csv]")
        sys.exit(1)

    contents_file = sys.argv[1]
    comments_file = sys.argv[2] if len(sys.argv) > 2 else None

    results = analyze_mediacrawler_data(contents_file, comments_file)
