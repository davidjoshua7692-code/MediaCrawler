"""
MediaCrawler 智能数据分析器
自动识别平台类型并加载相应的分析配置
支持模板化分析和自定义关键词配置
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re
from collections import Counter
from typing import Dict, List, Any, Optional
import warnings
warnings.filterwarnings('ignore')

# 导入模板库
try:
    from templates import (
        ANALYSIS_TEMPLATES, 
        match_template, 
        get_template, 
        get_template_keywords,
        suggest_analysis_dimensions
    )
except ImportError:
    # 如果直接运行脚本，使用相对导入
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from templates import (
        ANALYSIS_TEMPLATES, 
        match_template, 
        get_template, 
        get_template_keywords,
        suggest_analysis_dimensions
    )

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
    },
    'douyin': {
        'name': '抖音',
        'platform_keywords': ['aweme_id', 'sec_uid'],
        'content_fields': ['title', 'desc'],
        'metrics': ['liked_count', 'comment_count', 'share_count'],
        'text_fields': ['title', 'desc'],
        'location_field': 'ip_location',
    },
    'bilibili': {
        'name': 'B站',
        'platform_keywords': ['bvid', 'video_play_count'],
        'content_fields': ['title', 'desc'],
        'metrics': ['liked_count', 'video_play_count', 'video_coin_count', 'video_collect_count'],
        'text_fields': ['title', 'desc'],
        'location_field': None,
    },
    'weibo': {
        'name': '微博',
        'platform_keywords': ['mid', 'mblogid'],
        'content_fields': ['text', 'topic_list'],
        'metrics': ['liked_count', 'comments_count', 'reposts_count'],
        'text_fields': ['text'],
        'location_field': None,
    },
    'kuaishou': {
        'name': '快手',
        'platform_keywords': ['photo_id'],
        'content_fields': ['caption'],
        'metrics': ['liked_count', 'view_count', 'comment_count'],
        'text_fields': ['caption'],
        'location_field': None,
    },
    'tieba': {
        'name': '贴吧',
        'platform_keywords': ['tieba_id', 'thread_id'],
        'content_fields': ['title', 'content'],
        'metrics': ['reply_count'],
        'text_fields': ['title', 'content'],
        'location_field': None,
    },
    'zhihu': {
        'name': '知乎',
        'platform_keywords': ['answer_id', 'question_id'],
        'content_fields': ['title', 'content'],
        'metrics': ['voteup_count', 'comment_count'],
        'text_fields': ['title', 'content'],
        'location_field': None,
    }
}

# ============================================================================
# 平台检测器
# ============================================================================

def detect_platform(contents_df: pd.DataFrame, comments_df: pd.DataFrame = None) -> str:
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

    return 'generic'


def extract_locations(
    text: str, 
    custom_patterns: List[str] = None
) -> List[str]:
    """
    提取地理位置信息

    Args:
        text: 文本内容
        custom_patterns: 自定义地点匹配模式列表

    Returns:
        list: 提取到的地点列表
    """
    locations = []

    if pd.isna(text):
        return locations

    text_str = str(text)

    # 默认通用地点模式
    default_patterns = [
        r'(\w{2,}路)',      # XX路
        r'(\w{2,}广场)',    # XX广场
        r'(\w{2,}商场)',    # XX商场
        r'(\w{2,}购物中心)', # XX购物中心
        r'(\w{2,}大学)',    # XX大学
        r'(\w{2,}公园)',    # XX公园
        r'(\w{2,}图书馆)',  # XX图书馆
        r'地铁(\w+)站',     # 地铁XX站
        r'(\w{2,}区)',      # XX区（城市行政区）
    ]

    # 使用自定义模式或默认模式
    patterns = custom_patterns if custom_patterns else default_patterns

    for pattern in patterns:
        matches = re.findall(pattern, text_str)
        locations.extend(matches)

    return locations


def analyze_features(
    text: str, 
    feature_keywords: Dict[str, List[str]] = None
) -> List[str]:
    """
    分析文本特征

    Args:
        text: 文本内容
        feature_keywords: 特征关键词字典 {特征名: [关键词列表]}

    Returns:
        list: 提取到的特征列表
    """
    features = []

    if pd.isna(text):
        return features

    if not feature_keywords:
        return features

    text_lower = str(text).lower()

    for feature, keywords in feature_keywords.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                features.append(feature)
                break

    return features


def analyze_sentiment(
    text: str, 
    sentiment_keywords: Dict[str, List[str]] = None
) -> str:
    """
    分析情感倾向

    Args:
        text: 文本内容
        sentiment_keywords: 情感关键词字典 {'positive': [...], 'negative': [...]}

    Returns:
        str: 'positive', 'negative', 或 'neutral'
    """
    if pd.isna(text):
        return 'neutral'

    if not sentiment_keywords:
        return 'neutral'

    text_lower = str(text).lower()

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
    contents_file: str,
    comments_file: str = None,
    custom_keywords: Dict[str, Any] = None,
    template_id: str = None,
    custom_title: str = None,
    custom_location_patterns: List[str] = None,
    output_dir: str = None
) -> Dict[str, Any]:
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
        template_id: 使用的分析模板ID（如 'restaurant', 'travel' 等）
        custom_title: 自定义分析报告标题
        custom_location_patterns: 自定义地点匹配正则表达式列表
        output_dir: 输出目录（默认为项目根目录）

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

    # 确定分析关键词配置
    if custom_keywords:
        # 使用用户自定义关键词
        analysis_keywords = custom_keywords
    elif template_id:
        # 使用指定模板
        analysis_keywords = get_template_keywords(template_id)
    else:
        # 尝试从数据中推断模板
        # 检查是否有 source_keyword 字段
        if 'source_keyword' in df_contents.columns:
            sample_keywords = df_contents['source_keyword'].dropna().head(5).tolist()
            keywords_str = ' '.join(sample_keywords)
            template_id = match_template(keywords_str)
        else:
            template_id = 'generic'
        analysis_keywords = get_template_keywords(template_id)

    feature_keywords = analysis_keywords.get('features', {})
    sentiment_keywords = analysis_keywords.get('sentiment', {})

    # 获取地点匹配模式
    if custom_location_patterns:
        location_patterns = custom_location_patterns
    elif template_id:
        template = get_template(template_id)
        location_patterns = template.get('location_patterns', [])
    else:
        location_patterns = None

    # 自定义标题
    if not custom_title:
        template_name = get_template(template_id or 'generic').get('name', '')
        custom_title = f"📊 {platform_name}数据分析报告 - {template_name}"

    print("=" * 80)
    print(custom_title)
    print("=" * 80)

    # 数据概览
    print(f"\n✅ 平台识别: {platform_name} ({platform})")
    if template_id:
        print(f"✅ 分析模板: {get_template(template_id).get('name', template_id)}")
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
    location_counter = Counter()

    if location_field and location_field in df_contents.columns:
        # 从专用字段提取
        locations_data = df_contents[location_field].value_counts().head(10)
        print(f"\n{location_field} 分布 Top 10:")
        for loc, count in locations_data.items():
            if pd.notna(loc):
                print(f"  {loc}: {count} 次")
                location_counter[loc] = count
    
    # 从文本中提取地点
    text_fields = platform_config.get('text_fields', [])
    for idx, row in df_contents.iterrows():
        text = ' '.join([str(row.get(field, '')) for field in text_fields])
        locations = extract_locations(text, location_patterns)
        all_locations.extend(locations)

    if all_locations:
        location_counter = Counter(all_locations)
        print(f"\n文本中提及的地点 Top 10:")
        for location, count in location_counter.most_common(10):
            print(f"  {location}: {count} 次")

    # 3. 特征分析
    print("\n" + "=" * 80)
    print("🎯 三、内容特征分析")
    print("=" * 80)

    all_features = []

    for idx, row in df_contents.iterrows():
        text = ' '.join([str(row.get(field, '')) for field in text_fields])
        features = analyze_features(text, feature_keywords)
        all_features.extend(features)

    feature_counter = Counter(all_features)

    if feature_counter:
        print(f"\n特征提及次数 Top 10:")
        for feature, count in feature_counter.most_common(10):
            print(f"  {feature}: {count} 次")
    else:
        print("\n未检测到显著特征（可使用custom_keywords参数或template_id指定分析模板）")

    # 4. 情感分析
    sentiment_results = {'positive': 0, 'negative': 0, 'neutral': 0}
    positive_pct = 0.0

    if df_comments is not None:
        print("\n" + "=" * 80)
        print("💬 四、评论情感分析")
        print("=" * 80)

        for idx, row in df_comments.head(200).iterrows():
            comment = row.get('content', '')
            sentiment = analyze_sentiment(comment, sentiment_keywords)
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
        location_counter if (all_locations or location_counter) else None,
        feature_counter,
        output_dir
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
            title = row.get('title', row.get('text', row.get('caption', 'N/A')))
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

    if location_counter:
        top_location = location_counter.most_common(1)[0]
        insights.append(f"最热门区域: {top_location[0]} (提及{top_location[1]}次)")

    if df_comments is not None and total > 0:
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
        'template_id': template_id,
        'contents_count': len(df_contents),
        'comments_count': len(df_comments) if df_comments is not None else 0,
        'top_features': feature_counter.most_common(5),
        'top_locations': location_counter.most_common(5) if location_counter else [],
        'sentiment': sentiment_results,
        'visualization': output_file,
        'insights': insights
    }


def create_visualizations(
    df_contents: pd.DataFrame,
    df_comments: pd.DataFrame,
    platform: str,
    platform_config: Dict[str, Any],
    location_counter: Counter,
    feature_counter: Counter,
    output_dir: str = None
) -> str:
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
        if top_locations:
            plt.barh(range(len(top_locations)), list(top_locations.values()))
            plt.yticks(range(len(top_locations)), list(top_locations.keys()))
            plt.xlabel('提及次数')
            plt.title('热门地点 Top 10')
            plt.grid(True, alpha=0.3, axis='x')

    # 图4: 内容特征排名
    ax4 = plt.subplot(2, 3, 4)
    if feature_counter:
        top_features = dict(feature_counter.most_common(10))
        if top_features:
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

    # 确定输出路径
    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = Path('d:/MediaCrawler-main')
    
    output_file = str(output_path / f'{platform}_analysis.png')
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()

    return output_file


# ============================================================================
# 辅助函数（供 AI 推理使用）
# ============================================================================

def preview_data_structure(contents_file: str) -> Dict[str, Any]:
    """
    预览数据结构，用于 AI 推理分析方向
    
    Args:
        contents_file: 内容CSV文件路径
    
    Returns:
        dict: 数据结构预览信息
    """
    df = pd.read_csv(contents_file)
    platform = detect_platform(df)
    
    # 获取搜索关键词
    keywords = []
    if 'source_keyword' in df.columns:
        keywords = df['source_keyword'].dropna().unique().tolist()
    
    # 推荐分析模板
    keywords_str = ' '.join(keywords) if keywords else ''
    suggested = suggest_analysis_dimensions(keywords_str)
    
    return {
        'platform': platform,
        'platform_name': PLATFORM_ANALYSIS_CONFIG.get(platform, {}).get('name', platform),
        'row_count': len(df),
        'columns': list(df.columns),
        'search_keywords': keywords,
        'suggested_template': suggested['recommended_template'],
        'suggested_template_name': suggested['template_name'],
        'suggested_features': suggested['suggested_features'],
        'sample_titles': df['title'].head(5).tolist() if 'title' in df.columns else []
    }


# ============================================================================
# 命令行接口
# ============================================================================

if __name__ == "__main__":
    import sys

    # 简单的命令行接口
    if len(sys.argv) < 2:
        print("用法: python analyze.py <contents.csv> [comments.csv] [--template=<template_id>]")
        print("\n可用模板:")
        from templates import list_templates
        for t in list_templates():
            print(f"  {t['id']}: {t['name']}")
        sys.exit(1)

    contents_file = sys.argv[1]
    comments_file = None
    template_id = None

    # 解析参数
    for arg in sys.argv[2:]:
        if arg.startswith('--template='):
            template_id = arg.split('=')[1]
        elif not arg.startswith('--'):
            comments_file = arg

    results = analyze_mediacrawler_data(
        contents_file, 
        comments_file,
        template_id=template_id
    )
