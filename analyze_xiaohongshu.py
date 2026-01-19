import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import re
from collections import Counter
import jieba
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def extract_locations(text):
    """提取上海区域信息"""
    shanghai_districts = ['徐汇', '静安', '黄浦', '长宁', '普陀', '虹口', '杨浦', '浦东', '闵行', '宝山', '嘉定', '松江', '青浦', '奉贤', '金山', '崇明']
    locations = []

    if pd.isna(text):
        return locations

    for district in shanghai_districts:
        if district in str(text):
            locations.append(district)

    # 提取具体地点关键词
    location_patterns = [
        r'(\w+路)', r'(\w+广场)', r'(\w+商场)', r'(\w+购物中心)',
        r'(\w+大学)', r'(\w+公园)', r'图书馆', r'地铁站'
    ]

    for pattern in location_patterns:
        matches = re.findall(pattern, str(text))
        locations.extend(matches)

    return locations

def analyze_cafe_features(text):
    """分析咖啡厅特征"""
    features = {
        '插座': ['插座', '电源', '充电', 'plug'],
        '安静': ['安静', '清净', '不吵', 'silent', 'quiet'],
        '网络': ['wifi', 'wi-fi', '网速', '网络'],
        '停车位': ['停车', 'parking', '停车券'],
        '宠物友好': ['宠物', '狗', '猫', 'pet', '宠物友好'],
        '有厕所': ['厕所', '卫生间', '洗手间', 'wc'],
        '营业时间': ['营业', '开门', '关门', '24小时'],
        '价格': ['价格', '便宜', '贵', '实惠', '人均'],
    }

    found_features = []
    if pd.isna(text):
        return found_features

    text_lower = str(text).lower()

    for feature, keywords in features.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_features.append(feature)
                break

    return found_features

def analyze_xiaohongshu_data(contents_file, comments_file):
    """综合分析小红书数据"""

    print("=" * 80)
    print("📊 小红书上海适合办公的咖啡厅数据分析报告")
    print("=" * 80)

    # 读取数据
    df_contents = pd.read_csv(contents_file)
    df_comments = pd.read_csv(comments_file)

    print(f"\n✅ 数据加载成功!")
    print(f"   帖子数据: {len(df_contents)} 条")
    print(f"   评论数据: {len(df_comments)} 条")

    # 1. 基础统计
    print("\n" + "=" * 80)
    print("📈 一、基础数据统计")
    print("=" * 80)

    print(f"\n帖子互动数据:")
    print(f"  平均点赞数: {df_contents['liked_count'].mean():.1f}")
    print(f"  平均收藏数: {df_contents['collected_count'].mean():.1f}")
    print(f"  平均评论数: {df_contents['comment_count'].mean():.1f}")
    print(f"  最高点赞: {df_contents['liked_count'].max()}")
    print(f"  最高收藏: {df_contents['collected_count'].max()}")

    # 2. 提取地理位置信息
    print("\n" + "=" * 80)
    print("📍 二、地理位置分析")
    print("=" * 80)

    all_locations = []
    for idx, row in df_contents.iterrows():
        text = f"{row.get('title', '')} {row.get('desc', '')} {row.get('ip_location', '')}"
        locations = extract_locations(text)
        all_locations.extend(locations)

    location_counter = Counter(all_locations)

    if location_counter:
        print(f"\n提及最多的上海区域 (Top 10):")
        for location, count in location_counter.most_common(10):
            print(f"  {location}: {count} 次")

    # 3. 咖啡厅特征分析
    print("\n" + "=" * 80)
    print("☕ 三、咖啡厅特征分析")
    print("=" * 80)

    all_features = []
    for idx, row in df_contents.iterrows():
        text = f"{row.get('title', '')} {row.get('desc', '')}"
        features = analyze_cafe_features(text)
        all_features.extend(features)

    feature_counter = Counter(all_features)

    if feature_counter:
        print(f"\n用户最关心的特征 (Top 10):")
        for feature, count in feature_counter.most_common(10):
            print(f"  {feature}: {count} 次提及")

    # 4. 评论情感分析（简单关键词）
    print("\n" + "=" * 80)
    print("💬 四、评论热点分析")
    print("=" * 80)

    positive_words = ['推荐', '好', '不错', '舒服', '安静', '棒', '喜欢', '适合', '方便']
    negative_words = ['吵', '贵', '差', '不好', '失望', '慢', '挤']

    positive_count = 0
    negative_count = 0

    for idx, row in df_comments.head(100).iterrows():
        comment = str(row.get('content', ''))
        for word in positive_words:
            if word in comment:
                positive_count += 1
                break
        for word in negative_words:
            if word in comment:
                negative_count += 1
                break

    print(f"\n评论情感倾向 (基于前100条评论):")
    print(f"  积极评价: {positive_count} 条")
    print(f"  消极评价: {negative_count} 条")
    print(f"  积极占比: {positive_count/(positive_count+negative_count)*100:.1f}%")

    # 5. 创建可视化
    print("\n" + "=" * 80)
    print("📊 正在生成可视化图表...")
    print("=" * 80)

    fig = plt.figure(figsize=(16, 12))

    # 图1: 互动数据分布
    ax1 = plt.subplot(2, 3, 1)
    engagement_metrics = ['liked_count', 'collected_count', 'comment_count']
    for i, metric in enumerate(engagement_metrics):
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
    corr_data = df_contents[engagement_metrics].dropna()
    if len(corr_data) > 0:
        corr = corr_data.corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=1, ax=ax2, cbar_kws={'shrink': 0.8})
        ax2.set_title('互动数据相关性热图')

    # 图3: 热门区域Top 10
    ax3 = plt.subplot(2, 3, 3)
    if location_counter:
        top_locations = dict(location_counter.most_common(10))
        plt.barh(range(len(top_locations)), list(top_locations.values()))
        plt.yticks(range(len(top_locations)), list(top_locations.keys()))
        plt.xlabel('提及次数')
        plt.title('热门上海区域 Top 10')
        plt.grid(True, alpha=0.3, axis='x')

    # 图4: 咖啡厅特征排名
    ax4 = plt.subplot(2, 3, 4)
    if feature_counter:
        top_features = dict(feature_counter.most_common(10))
        plt.barh(range(len(top_features)), list(top_features.values()))
        plt.yticks(range(len(top_features)), list(top_features.keys()))
        plt.xlabel('提及次数')
        plt.title('用户最关心的咖啡厅特征')
        plt.grid(True, alpha=0.3, axis='x')

    # 图5: IP地点分布
    ax5 = plt.subplot(2, 3, 5)
    ip_locations = df_contents['ip_location'].dropna().value_counts().head(10)
    if len(ip_locations) > 0:
        plt.barh(range(len(ip_locations)), ip_locations.values)
        plt.yticks(range(len(ip_locations)), ip_locations.index)
        plt.xlabel('帖子数')
        plt.title('IP地点分布 Top 10')
        plt.grid(True, alpha=0.3, axis='x')

    # 图6: 数据质量概览
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
    plt.savefig('d:/MediaCrawler-main/xiaohongshu_analysis.png', dpi=150, bbox_inches='tight')
    print(f"\n✅ 图表已保存: d:/MediaCrawler-main/xiaohongshu_analysis.png")
    plt.close()

    # 6. 关键洞察
    print("\n" + "=" * 80)
    print("💡 五、关键洞察总结")
    print("=" * 80)

    insights = []

    # 洞察1: 最受欢迎的内容
    if len(df_contents) > 0:
        top_liked = df_contents.nlargest(3, 'liked_count')[['title', 'liked_count']]
        print("\n🔥 最受欢迎的帖子 Top 3:")
        for idx, row in top_liked.iterrows():
            print(f"\n  {row['title'][:50]}...")
            print(f"  👍 {row['liked_count']} 个赞")

    # 洞察2: 用户最关心的特征
    if feature_counter:
        print(f"\n🎯 用户最在意的3个特征:")
        for feature, count in feature_counter.most_common(3):
            print(f"  • {feature}: {count} 次提及")

    # 洞察3: 热门区域推荐
    if location_counter:
        print(f"\n🏙️ 最热门的3个区域:")
        for location, count in location_counter.most_common(3):
            print(f"  • {location}: {count} 次提及")

    # 洞察4: 互动模式
    if len(df_contents) > 0:
        avg_likes = df_contents['liked_count'].mean()
        avg_collects = df_contents['collected_count'].mean()
        print(f"\n📊 互动模式:")
        print(f"  • 平均收藏数是点赞数的 {avg_collects/avg_likes:.2f} 倍")
        print(f"  • 说明用户更倾向收藏实用信息")

    print("\n" + "=" * 80)
    print("✅ 分析完成!")
    print("=" * 80)

    return {
        'contents': len(df_contents),
        'comments': len(df_comments),
        'top_locations': location_counter.most_common(5),
        'top_features': feature_counter.most_common(5),
        'avg_likes': df_contents['liked_count'].mean(),
        'avg_collects': df_contents['collected_count'].mean()
    }

if __name__ == "__main__":
    results = analyze_xiaohongshu_data(
        'd:/MediaCrawler-main/data/xhs/csv/search_contents_2026-01-19.csv',
        'd:/MediaCrawler-main/data/xhs/csv/search_comments_2026-01-19.csv'
    )
