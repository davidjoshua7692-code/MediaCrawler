



"""

DEPRECATED：不需要脚本自动化执行。爬虫自动接到数据分析

MediaCrawler 自动分析桥接工具
根据爬虫配置自动选择合适的分析策略
"""
import os
import re
from pathlib import Path
from datetime import datetime
import pandas as pd

def get_latest_files(platform, data_type='csv'):
    """
    获取指定平台的最新数据文件

    Args:
        platform: 平台标识符 (xhs, dy, bili等)
        data_type: 数据类型 (csv, json, excel等)

    Returns:
        tuple: (contents_file, comments_file) 文件路径
    """
    base_path = Path(f'data/{platform}/{data_type}')

    if not base_path.exists():
        print(f"❌ 目录不存在: {base_path}")
        return None, None

    # 查找内容文件
    contents_files = list(base_path.glob('search_contents_*.csv'))
    contents_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    # 查找评论文件
    comments_files = list(base_path.glob('search_comments_*.csv'))
    comments_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    contents_file = contents_files[0] if contents_files else None
    comments_file = comments_files[0] if comments_files else None

    return contents_file, comments_file

def analyze_from_config(config_file='config/base_config.py'):
    """
    读取爬虫配置并自动运行分析

    Args:
        config_file: 配置文件路径

    Returns:
        dict: 分析结果
    """
    # 读取配置
    config_globals = {
        '__name__': '__main__',
        '__builtins__': __builtins__
    }

    with open(config_file, 'r', encoding='utf-8') as f:
        config_content = f.read()

    # 简单提取关键配置（避免执行整个配置文件）
    import re

    def extract_config_var(content, var_name, default=''):
        pattern = rf'{var_name}\s*=\s*[\'"]([^\'\"]*)[\'"]'
        match = re.search(pattern, content)
        return match.group(1) if match else default

    platform = extract_config_var(config_content, 'PLATFORM', 'xhs')
    keywords = extract_config_var(config_content, 'KEYWORDS', '')
    crawler_type = extract_config_var(config_content, 'CRAWLER_TYPE', 'search')
    save_option = extract_config_var(config_content, 'SAVE_DATA_OPTION', 'csv')

    print(f"📋 从配置读取参数:")
    print(f"  平台: {platform}")
    print(f"  关键词: {keywords}")
    print(f"  爬取类型: {crawler_type}")
    print(f"  保存格式: {save_option}")

    # 检测数据类型
    if save_option not in ['csv', 'json', 'excel']:
        print(f"⚠️ 当前仅支持 CSV/JSON/Excel 格式分析")
        return None

    # 获取最新文件
    contents_file, comments_file = get_latest_files(platform, save_option)

    if not contents_file:
        print(f"❌ 未找到数据文件，请先运行爬虫: uv run python main.py")
        return None

    print(f"\n📂 检测到数据文件:")
    print(f"  内容文件: {contents_file}")
    if comments_file:
        print(f"  评论文件: {comments_file}")
    else:
        print(f"  评论文件: 未找到（可选）")

    # 自动选择分析关键词
    custom_keywords = auto_select_keywords(keywords)

    if custom_keywords:
        print(f"\n🎯 自动选择关键词配置: {custom_keywords.get('category', '通用')}")

    # 导入分析器
    import sys
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))

    from claude.skills.mediacrawler_analyzer.analyze import analyze_mediacrawler_data

    # 运行分析
    results = analyze_mediacrawler_data(
        contents_file=str(contents_file),
        comments_file=str(comments_file) if comments_file else None,
        custom_keywords=custom_keywords,
        custom_title=f"📊 {keywords} - 数据分析报告"
    )

    return results

def auto_select_keywords(keywords):
    """
    根据搜索关键词自动选择合适的分析配置

    Args:
        keywords: 搜索关键词字符串

    Returns:
        dict: 自定义关键词配置
    """
    keywords_lower = keywords.lower()

    # 咖啡厅/办公场景
    if any(word in keywords_lower for word in ['咖啡', 'cafe', '办公', '自习', '工作', '笔记本', '久坐']):
        return {
            'category': '咖啡厅/办公空间',
            'features': {
                '安静': ['安静', '清净', '不吵', 'silent', 'quiet'],
                '插座': ['插座', '电源', '充电', 'plug'],
                '网络': ['wifi', 'wi-fi', '网速', '网络'],
                '停车位': ['停车', 'parking', '停车券'],
                '有厕所': ['厕所', '卫生间', '洗手间', 'wc'],
                '营业时间': ['营业', '开门', '关门', '24小时'],
                '价格': ['价格', '便宜', '贵', '实惠', '人均'],
            },
            'sentiment': {
                'positive': ['推荐', '好', '不错', '舒服', '棒', '喜欢', '适合', '方便'],
                'negative': ['吵', '贵', '差', '不好', '失望', '慢', '挤']
            }
        }

    # 美食场景
    elif any(word in keywords_lower for word in ['美食', '好吃', '餐厅', '小吃', '菜', '吃']):
        return {
            'category': '美食推荐',
            'features': {
                '口味': ['好吃', '美味', '正宗', '口感', '味道', '香'],
                '环境': ['装修', '氛围', '环境', '装潢', '档次', '干净'],
                '服务': ['服务', '服务员', '态度', '热情', '周到'],
                '价格': ['便宜', '实惠', '性价比', '平价', '亲民'],
                '分量': ['分量', '量足', '量少', '量大', '管饱'],
                '等待时间': ['排队', '等位', '上菜快', '上菜慢', '等很久']
            },
            'sentiment': {
                'positive': ['推荐', '赞', '爱了', '满意', '惊喜', '超出预期', '必吃'],
                'negative': ['失望', '差', '不值', '坑', '不会再来', '踩雷', '后悔']
            }
        }

    # 穿搭场景
    elif any(word in keywords_lower for word in ['穿搭', '搭配', '衣服', '裙子', '裤子', '鞋子']):
        return {
            'category': '穿搭推荐',
            'features': {
                '风格': ['风格', '穿搭', '搭配', '造型'],
                '季节': ['春秋', '夏季', '冬季', '保暖', '透气'],
                '身材': ['显瘦', '显高', '宽松', '修身', '显腿长'],
                '价格': ['平价', '性价比', '贵', '便宜', '白菜价'],
                '场合': ['日常', '约会', '工作', '度假', '运动', '通勤']
            },
            'sentiment': {
                'positive': ['好看', '喜欢', '种草', '必买', '回购', '显白'],
                'negative': ['丑', '不适合', '差评', '退了', '显黑']
            }
        }

    # 旅游场景
    elif any(word in keywords_lower for word in ['旅游', '景点', '攻略', '游玩', '景点', '旅行']):
        return {
            'category': '旅游攻略',
            'features': {
                '景点': ['景点', '名胜', '古迹', '风景', '景色', '美'],
                '交通': ['交通', '方便', '地铁', '公交', '打车', '好走'],
                '住宿': ['酒店', '民宿', '住宿', '入住', '房间'],
                '美食': ['美食', '小吃', '餐厅', '特色菜', '好吃'],
                '费用': ['门票', '免费', '便宜', '贵', '性价比'],
                '季节': ['最佳季节', '什么时候去', '天气', '气温']
            },
            'sentiment': {
                'positive': ['值得', '推荐', '不虚此行', '美', '惊艳'],
                'negative': ['不值得', '失望', '商业化', '坑', '后悔']
            }
        }

    # 学习/教育场景
    elif any(word in keywords_lower for word in ['学习', '教程', '课程', 'python', '编程', '入门', '技巧']):
        return {
            'category': '学习/教程',
            'features': {
                '难度': ['简单', '容易', '入门', '基础', '进阶', '难'],
                '实用性': ['实用', '干货', '详细', '全面', '系统'],
                '时长': ['短', '长', '分钟', '小时', '天'],
                '费用': ['免费', '收费', '便宜', '贵', '性价比']
            },
            'sentiment': {
                'positive': ['有用', '学会', '推荐', '好', '清晰', '详细'],
                'negative': ['没用', '学不会', '太复杂', '差', '浪费时间']
            }
        }

    # 默认返回None（使用通用分析）
    return None

# ============================================================================
# 命令行接口
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='MediaCrawler 自动分析工具')
    parser.add_argument('--config', default='config/base_config.py',
                       help='配置文件路径 (默认: config/base_config.py)')
    parser.add_argument('--platform', type=str,
                       help='强制指定平台 (xhs/dy/bili/wb/tieba/zhihu)')
    parser.add_argument('--contents', type=str,
                       help='强制指定内容文件路径')
    parser.add_argument('--comments', type=str,
                       help='强制指定评论文件路径')

    args = parser.parse_args()

    # 如果指定了文件，直接分析
    if args.contents:
        import sys
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))

        from claude.skills.mediacrawler_analyzer.analyze import analyze_mediacrawler_data

        results = analyze_mediacrawler_data(
            contents_file=args.contents,
            comments_file=args.comments
        )

    # 否则从配置文件读取
    else:
        results = analyze_from_config(args.config)
