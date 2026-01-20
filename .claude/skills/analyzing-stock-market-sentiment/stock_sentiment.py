"""
股市情绪分析器
专门针对股票讨论进行多空情绪分析
支持小红书、微博、股吧等平台数据

支持两种分析方法：
1. 关键词匹配（快速，默认）
2. FinBERT（精准，需下载模型）
"""
import pandas as pd
import re
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys
import argparse


# ============================================================================
# 股市专属关键词配置
# ============================================================================

# 多空关键词
BULLISH_KEYWORDS = [
    '涨', '加仓', '买入', '看多', '起飞', '突破', '牛市', '向上',
    '持有', '不卖', '继续涨', '还能涨', '目标', '好', '牛', '强',
    '稳', '值', '低吸', '补仓', '机会', '买', '持仓', '拿住',
    '看好', '值得', '价值', '优秀', '龙头', '上涨', '攀升'
]

BEARISH_KEYWORDS = [
    '跌', '减仓', '卖出', '看空', '回调', '熊市', '向下',
    '出货', '高估', '贵', '弱', '风险', '怕', '跌了', '清仓',
    '割肉', '亏损', '套', '怕跌', '还会跌', '洗盘', '危险',
    '担心', '怕被套', '止损', '离场', '逃顶', '泡沫'
]

NEUTRAL_KEYWORDS = [
    '观望', '等待', '再看看', '不确定', '震荡', '横盘',
    '整理', '犹豫', '暂时不动'
]

# 投资行为关键词
BEHAVIOR_KEYWORDS = {
    '加仓/买入': ['加仓', '买入', '买了', '补仓', '抄底', '建仓', '上车'],
    '减仓/卖出': ['减仓', '卖出', '卖了', '清仓', '止盈', '割肉', '跑了', '下车'],
    '持有/观望': ['持有', '拿住', '不动', '观望', '等待', '躺平', '锁仓']
}

# 关注主题关键词
THEME_KEYWORDS = {
    '黄金': ['黄金', '金', '贵金属', '金价'],
    '铜价': ['铜', '铜价', 'lme', '有色', '工业金属'],
    '业绩/财报': ['业绩', '财报', '利润', '营收', '年报', '中报', '季报', 'roe'],
    '估值': ['估值', '市盈率', 'pe', '贵了', '便宜', '高估', '低估', '泡沫'],
    '分红': ['分红', '股息', '派息', '股息率'],
    '锂矿': ['锂', '锂矿', '碳酸锂', '锂资源'],
    '宏观经济': ['美联储', '降息', '利率', '美元', '宏观', '经济', '通胀'],
    '技术面': ['支撑', '压力', '阻力', '突破', '趋势', '震荡', '均线', 'macd', 'k线']
}

# 风险信号关键词
RISK_SIGNALS = {
    '情绪过热': ['从不套人', '只会涨', '闭眼买', '稳赚', '肯定涨', '无脑买'],
    '高位震荡': ['不是舒服的上车点', '等回调', '观望一下', '再看看'],
    '获利回吐': ['获利了结', '落袋为安', '先出来', '短线资金'],
    'FOMO情绪': ['卖飞', '买少', '后悔', '错过', '没买']
}


# ============================================================================
# FinBERT 集成
# ============================================================================

# 尝试导入 FinBERT 分析器
try:
    from finbert_analyzer import HybridSentimentAnalyzer
    FINBERT_AVAILABLE = True
except ImportError:
    FINBERT_AVAILABLE = False

# 全局 FinBERT 分析器
_finbert_analyzer = None


def get_project_paths():
    """
    获取项目路径（锚定到.claude文件夹）

    Returns:
        dict: {
            'project_root': 项目根目录,
            'data_dir': 数据目录,
            'model_dir': 模型目录,
            'report_dir': 报告目录（项目根目录/REPORT）
        }
    """
    script_dir = Path(__file__).parent
    # .claude/skills/analyzing-stock-market-sentiment/ -> .claude/
    claude_dir = script_dir.parent.parent
    # .claude/ -> 项目根目录
    project_root = claude_dir.parent

    return {
        'project_root': project_root,
        'data_dir': project_root / "data" / "xhs" / "csv",
        'model_dir': project_root / "models" / "finbert_chinese",
        'report_dir': project_root / "REPORT"  # 改为项目根目录/REPORT
    }


def get_finbert_analyzer():
    """获取 FinBERT 分析器（单例模式）"""
    global _finbert_analyzer

    if not FINBERT_AVAILABLE:
        return None

    if _finbert_analyzer is None:
        try:
            paths = get_project_paths()
            _finbert_analyzer = HybridSentimentAnalyzer(
                model_path=str(paths['model_dir'])
            )
            if _finbert_analyzer.finbert.model_loaded:
                print("✅ FinBERT 模型已启用（混合模式）")
        except Exception as e:
            print(f"⚠️  FinBERT 初始化失败: {e}")
            print("   将使用纯关键词匹配模式")
            _finbert_analyzer = None

    return _finbert_analyzer


# ============================================================================
# 核心分析函数
# ============================================================================

def analyze_sentiment(text: str, use_finbert: bool = True) -> Tuple[str, int]:
    """
    分析单条文本的情绪

    Args:
        text: 文本内容
        use_finbert: 是否尝试使用 FinBERT（默认True）

    Returns:
        (情绪类型, 得分) - 情绪类型为 'bullish', 'bearish', 'neutral', 'uncertain'
    """
    if pd.isna(text):
        return 'uncertain', 0

    # 优先使用 FinBERT（如果启用且可用）
    if use_finbert and FINBERT_AVAILABLE:
        finbert = get_finbert_analyzer()
        if finbert and finbert.finbert.model_loaded:
            try:
                result = finbert.analyze(str(text))
                # 返回完整结果，包含细粒度情绪
                return result
            except Exception as e:
                # FinBERT 失败，回退到关键词
                pass

    # 关键词匹配（回退方案或默认方案）
    text_lower = str(text).lower()

    bullish_score = sum(1 for kw in BULLISH_KEYWORDS if kw in text_lower)
    bearish_score = sum(1 for kw in BEARISH_KEYWORDS if kw in text_lower)
    neutral_score = sum(1 for kw in NEUTRAL_KEYWORDS if kw in text_lower)

    if bullish_score > bearish_score and bullish_score > neutral_score:
        return 'bullish', bullish_score
    elif bearish_score > bullish_score and bearish_score > neutral_score:
        return 'bearish', bearish_score
    elif neutral_score > 0:
        return 'neutral', neutral_score
    else:
        return 'uncertain', 0


def extract_price_targets(text: str) -> List[float]:
    """
    提取文本中的价格目标

    Args:
        text: 文本内容

    Returns:
        价格目标列表
    """
    if pd.isna(text):
        return []

    # 匹配数字，合理股价范围 5-200元
    price_pattern = r'(\d{1,3}\.?\d*)\s*[元块]?'
    prices = []

    for match in re.finditer(price_pattern, str(text)):
        try:
            price = float(match.group(1))
            # 过滤合理股价范围
            if 5 <= price <= 200:
                # 排除明显不是股价的数字（如100股、10年等）
                if not any(exclude in str(text) for exclude in ['股', '年', '倍', '%', '次']):
                    prices.append(price)
        except (ValueError, IndexError):
            continue

    return prices


def analyze_investment_behavior(text: str) -> Optional[str]:
    """
    识别投资行为

    Args:
        text: 文本内容

    Returns:
        行为类型或None
    """
    if pd.isna(text):
        return None

    text_lower = str(text).lower()

    for behavior, keywords in BEHAVIOR_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return behavior

    return None


def detect_themes(text: str) -> List[str]:
    """
    检测文本中的投资主题

    Args:
        text: 文本内容

    Returns:
        主题列表
    """
    if pd.isna(text):
        return []

    text_lower = str(text).lower()
    detected_themes = []

    for theme, keywords in THEME_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            detected_themes.append(theme)

    return detected_themes


def detect_risk_signals(text: str) -> List[str]:
    """
    检测风险信号

    Args:
        text: 文本内容

    Returns:
        风险信号列表
    """
    if pd.isna(text):
        return []

    text_lower = str(text).lower()
    signals = []

    for signal_type, keywords in RISK_SIGNALS.items():
        if any(kw in text_lower for kw in keywords):
            signals.append(signal_type)

    return signals


# ============================================================================
# 主分析函数
# ============================================================================

def analyze_stock_sentiment(
    comments_file: str,
    contents_file: str = None,
    stock_name: str = '目标股票',
    output_dir: str = None,
    use_finbert: bool = True
) -> Dict:
    """
    综合分析股票讨论情绪

    Args:
        comments_file: 评论CSV文件路径
        contents_file: 内容CSV文件路径（可选）
        stock_name: 股票名称
        output_dir: 输出目录
        use_finbert: 是否使用 FinBERT（默认True，自动回退到关键词）

    Returns:
        分析结果字典
    """
    print(f"\n{'='*80}")
    print(f"📊 {stock_name} - 股市情绪分析报告")
    print(f"{'='*80}\n")

    # 读取数据
    df_comments = pd.read_csv(comments_file)
    df_contents = pd.read_csv(contents_file) if contents_file else None

    print(f"✅ 数据加载成功!")
    print(f"   评论数据: {len(df_comments)} 条")
    if df_contents is not None:
        print(f"   内容数据: {len(df_contents)} 条")

    # 1. 多空情绪分析
    print(f"\n{'='*80}")
    print(f"📈 一、多空情绪分布")
    print(f"{'='*80}\n")

    bullish_comments = []
    bearish_comments = []
    neutral_comments = []
    uncertain_comments = []
    fine_grained_stats = Counter()  # 细粒度情绪统计
    layer_stats = Counter({'第1层(关键词明确)': 0, '第2层(FinBERT)': 0})  # 分层统计

    for idx, row in df_comments.iterrows():
        content = row.get('content', '')
        result = analyze_sentiment(content, use_finbert)

        # 兼容返回值：可能是 (sentiment, score) 或 dict
        if isinstance(result, dict):
            sentiment = result['sentiment']
            score = result['confidence'] * 10  # 转换为得分
            fine_grained = result.get('fine_grained', None)
            method = result.get('method', 'unknown')

            # 统计分层
            if method == 'keyword':
                layer_stats['第1层(关键词明确)'] += 1
            elif method == 'finbert':
                layer_stats['第2层(FinBERT)'] += 1

            # FinBERT 结果直接纳入细粒度统计
            if fine_grained:
                fine_grained_stats[fine_grained] += 1

            # 将 FinBERT 结果加入分类列表
            if sentiment == 'bullish':
                bullish_comments.append((content, score, row.get('like_count', 0), row.get('ip_location', '')))
            elif sentiment == 'bearish':
                bearish_comments.append((content, score, row.get('like_count', 0), row.get('ip_location', '')))
            elif sentiment == 'neutral':
                neutral_comments.append((content, score, row.get('like_count', 0), row.get('ip_location', '')))
            else:
                uncertain_comments.append(content)

        else:
            # 关键词模式：需要重新计算得分差并映射到细粒度情绪
            sentiment, score = result

            # 重新计算关键词得分
            text_lower = str(content).lower()
            bullish_score = sum(1 for kw in BULLISH_KEYWORDS if kw in text_lower)
            bearish_score = sum(1 for kw in BEARISH_KEYWORDS if kw in text_lower)
            score_diff = abs(bullish_score - bearish_score)

            # 只统计得分差 ≥ 2 的明确评论
            if score_diff >= 2:
                layer_stats['第1层(关键词明确)'] += 1

                # 映射到细粒度情绪
                if sentiment == 'bullish':
                    if score_diff >= 4:
                        fine_grained = '强烈看涨📈📈'
                    else:  # score_diff = 2-3
                        fine_grained = '看涨📈'
                elif sentiment == 'bearish':
                    if score_diff >= 4:
                        fine_grained = '强烈看跌📉📉'
                    else:  # score_diff = 2-3
                        fine_grained = '看跌📉'
                else:  # neutral
                    fine_grained = '纯中性⚪'

                if fine_grained:
                    fine_grained_stats[fine_grained] += 1

                # 只将明确评论(score_diff >= 2)加入分类列表
                if sentiment == 'bullish':
                    bullish_comments.append((content, score, row.get('like_count', 0), row.get('ip_location', '')))
                elif sentiment == 'bearish':
                    bearish_comments.append((content, score, row.get('like_count', 0), row.get('ip_location', '')))
                elif sentiment == 'neutral':
                    neutral_comments.append((content, score, row.get('like_count', 0), row.get('ip_location', '')))
            # score_diff < 2 的模糊评论：在关键词模式下跳过，不加入任何统计
            # (这些评论应该由FinBERT第2层处理，但use_finbert=False时没有第2层)

    total_classified = len(bullish_comments) + len(bearish_comments) + len(neutral_comments)

    if total_classified > 0:
        bullish_pct = len(bullish_comments) / total_classified * 100
        bearish_pct = len(bearish_comments) / total_classified * 100
        neutral_pct = len(neutral_comments) / total_classified * 100
        net_sentiment = bullish_pct - bearish_pct

        print(f"  看涨（多头）: {len(bullish_comments)} 条 ({bullish_pct:.1f}%)")
        print(f"  看跌（空头）: {len(bearish_comments)} 条 ({bearish_pct:.1f}%)")
        print(f"  观望（中性）: {len(neutral_comments)} 条 ({neutral_pct:.1f}%)")
        print(f"  未明确: {len(uncertain_comments)} 条")
        print(f"\n  🎯 净多头情绪: {net_sentiment:+.1f}%")

        # 显示分层统计
        total_processed = sum(layer_stats.values())
        if total_processed > 0:
            print(f"\n  📊 分析分层统计:")
            for layer, count in layer_stats.most_common():
                pct = count / total_processed * 100
                print(f"    {layer}: {count} 条 ({pct:.1f}%)")

        # 显示细粒度情绪分布
        if fine_grained_stats:
            print(f"\n  📊 细粒度情绪分布 (9类):")
            total_fine_grained = sum(fine_grained_stats.values())
            for emotion, count in fine_grained_stats.most_common():
                pct = count / total_fine_grained * 100
                print(f"    {emotion}: {count} 条 ({pct:.1f}%)")

        # 判断情绪区间
        if net_sentiment > 50:
            sentiment_level = "🔴 极度贪婪（风险警告）"
        elif net_sentiment > 30:
            sentiment_level = "🟠 贪婪（需谨慎）"
        elif net_sentiment > 10:
            sentiment_level = "🟢 适度看多（健康）"
        elif net_sentiment > -10:
            sentiment_level = "⚪ 中性（观望）"
        elif net_sentiment > -30:
            sentiment_level = "🔵 适度看空（谨慎）"
        else:
            sentiment_level = "⚫ 极度恐惧（机会区间）"

        print(f"\n  情绪区间: {sentiment_level}")

    # 2. 价格目标分析
    print(f"\n{'='*80}")
    print(f"💰 二、价格预期分析")
    print(f"{'='*80}\n")

    all_price_targets = []
    for idx, row in df_comments.iterrows():
        content = row.get('content', '')
        prices = extract_price_targets(content)
        for price in prices:
            all_price_targets.append((content, price, row.get('like_count', 0)))

    if all_price_targets:
        prices_only = [p[1] for p in all_price_targets]
        print(f"  提及价格目标: {len(all_price_targets)} 次")
        print(f"  价格区间: {min(prices_only):.2f} - {max(prices_only):.2f} 元")
        print(f"  平均预期: {sum(prices_only)/len(prices_only):.2f} 元")

        # 价格频次统计
        price_counter = Counter(prices_only)
        top_prices = price_counter.most_common(10)

        print(f"\n  热门目标价位 Top 10:")
        for price, count in top_prices:
            # 计算支持度（点赞数）
            related_comments = [c for c in all_price_targets if abs(c[1] - price) < 0.01]
            total_likes = sum(c[2] for c in related_comments)
            print(f"    {price:6.2f} 元: {count:2d}次提及 | 👍{total_likes} 支持")

    # 3. 投资行为分析
    print(f"\n{'='*80}")
    print(f"🎯 三、投资者行为分析")
    print(f"{'='*80}\n")

    behavior_stats = {behavior: 0 for behavior in BEHAVIOR_KEYWORDS.keys()}
    for idx, row in df_comments.iterrows():
        content = row.get('content', '')
        behavior = analyze_investment_behavior(content)
        if behavior:
            behavior_stats[behavior] += 1

    for behavior, count in behavior_stats.items():
        if count > 0:
            print(f"  {behavior}: {count} 条评论")

    # 4. 核心关注主题
    print(f"\n{'='*80}")
    print(f"🔍 四、核心关注主题")
    print(f"{'='*80}\n")

    theme_counter = Counter()
    for idx, row in df_comments.iterrows():
        content = row.get('content', '')
        themes = detect_themes(content)
        theme_counter.update(themes)

    if theme_counter:
        print(f"  主题提及排名:")
        for theme, count in theme_counter.most_common():
            print(f"    {theme}: {count} 条提及")

    # 5. 看涨理由 Top 10
    print(f"\n{'='*80}")
    print(f"✅ 五、看涨理由 Top 10（按点赞排序）")
    print(f"{'='*80}\n")

    bullish_comments_sorted = sorted(bullish_comments, key=lambda x: x[2], reverse=True)
    for i, (content, score, likes, location) in enumerate(bullish_comments_sorted[:10], 1):
        display_content = content[:80] + '...' if len(content) > 80 else content
        print(f"{i:2d}. [{location}] 👍{likes}: {display_content}")

    # 6. 看跌/担忧理由 Top 10
    print(f"\n{'='*80}")
    print(f"⚠️  六、看跌/担忧理由 Top 10")
    print(f"{'='*80}\n")

    bearish_comments_sorted = sorted(bearish_comments, key=lambda x: x[2], reverse=True)
    for i, (content, score, likes, location) in enumerate(bearish_comments_sorted[:10], 1):
        display_content = content[:80] + '...' if len(content) > 80 else content
        print(f"{i:2d}. [{location}] 👍{likes}: {display_content}")

    # 7. 投资者故事
    print(f"\n{'='*80}")
    print(f"📖 七、投资者故事与操作")
    print(f"{'='*80}\n")

    stories = []
    for idx, row in df_comments.iterrows():
        content = str(row.get('content', ''))
        if pd.notna(content) and any(kw in content for kw in ['买了', '卖了', '卖飞', '后悔', '可惜', '庆幸', '持有', '年']):
            likes = row.get('like_count', 0)
            if likes and likes > 5:  # 只取高互动故事
                stories.append((content, likes, row.get('ip_location', '')))

    stories_sorted = sorted(stories, key=lambda x: x[1], reverse=True)
    for i, (content, likes, location) in enumerate(stories_sorted[:8], 1):
        display_content = content[:100] + '...' if len(content) > 100 else content
        print(f"{i}. [{location}] 👍{likes}: {display_content}")

    # 8. 风险信号识别
    print(f"\n{'='*80}")
    print(f"🚨 八、风险信号识别")
    print(f"{'='*80}\n")

    risk_signals_found = Counter()
    risk_examples = {signal: [] for signal in RISK_SIGNALS.keys()}

    for idx, row in df_comments.iterrows():
        content = row.get('content', '')
        signals = detect_risk_signals(content)
        for signal in signals:
            risk_signals_found[signal] += 1
            if len(risk_examples[signal]) < 3:  # 每类信号保留3个例子
                risk_examples[signal].append(content[:60])

    if risk_signals_found:
        print(f"  检测到风险信号:")
        for signal, count in risk_signals_found.most_common():
            print(f"\n  ⚠️  {signal}: {count} 条提及")
            for example in risk_examples[signal]:
                print(f"     - {example}...")
    else:
        print("  未检测到明显风险信号")

    # 9. 综合投资建议
    print(f"\n{'='*80}")
    print(f"💡 九、综合投资洞察")
    print(f"{'='*80}\n")

    insights = []

    # 情绪面
    if total_classified > 0:
        if net_sentiment > 50:
            insights.append("⚠️  情绪过热：净多头超过50%，需警惕短期回调风险")
        elif net_sentiment > 30:
            insights.append("⚠️  情绪偏热：建议关注获利回吐压力")
        elif net_sentiment > 10:
            insights.append("✅ 情绪健康：多头占优，市场信心较强")
        elif net_sentiment > -10:
            insights.append("⚪ 情绪中性：多空分歧，等待方向选择")
        else:
            insights.append("💡 情绪偏空：可能存在机会区间")

    # 价格面
    if all_price_targets:
        avg_price = sum(p[1] for p in all_price_targets) / len(all_price_targets)
        insights.append(f"💰 价格共识：市场平均目标价 {avg_price:.2f} 元")

    # 行为面
    total_behavior = sum(behavior_stats.values())
    if total_behavior > 0:
        buy_ratio = behavior_stats.get('加仓/买入', 0) / total_behavior * 100
        if buy_ratio > 60:
            insights.append(f"📈 买入意愿强：{buy_ratio:.1f}% 投资者计划加仓")
        elif buy_ratio < 40:
            insights.append(f"📉 卖出压力增：{buy_ratio:.1f}% 投资者计划买入")

    # 风险面
    if risk_signals_found:
        top_risk = risk_signals_found.most_common(1)[0]
        insights.append(f"🚨 风险提示：检测到'{top_risk[0]}'信号 {top_risk[1]} 次")

    for i, insight in enumerate(insights, 1):
        print(f"  {i}. {insight}")

    print(f"\n{'='*80}")
    print(f"✅ 分析完成!")
    print(f"{'='*80}\n")

    # 返回结果
    return {
        'total_comments': len(df_comments),
        'bullish_count': len(bullish_comments),
        'bearish_count': len(bearish_comments),
        'neutral_count': len(neutral_comments),
        'bullish_pct': bullish_pct if total_classified > 0 else 0,
        'bearish_pct': bearish_pct if total_classified > 0 else 0,
        'net_sentiment': net_sentiment if total_classified > 0 else 0,
        'price_targets': all_price_targets,
        'behavior_stats': behavior_stats,
        'theme_stats': dict(theme_counter),
        'risk_signals': dict(risk_signals_found)
    }


# ============================================================================
# 命令行接口
# ============================================================================

def find_latest_dedup_files(data_dir: str = None) -> Tuple[Optional[str], Optional[str]]:
    """
    自动查找最新的去重CSV文件

    Args:
        data_dir: 数据目录路径（默认自动查找）

    Returns:
        (comments_dedup_file, contents_dedup_file) 找到的文件路径，未找到返回None
    """
    if data_dir is None:
        paths = get_project_paths()
        data_dir = paths['data_dir']
    else:
        data_dir = Path(data_dir)

    if not data_dir.exists():
        return None, None

    # 查找 -dedup 后缀的文件（支持 search_comments_2026-01-20-dedup.csv 格式）
    comments_dedup_files = list(data_dir.glob("*comments*dedup.csv"))
    contents_dedup_files = list(data_dir.glob("*contents*dedup.csv"))

    # 按修改时间排序，取最新的
    comments_dedup = max(comments_dedup_files, key=lambda f: f.stat().st_mtime) if comments_dedup_files else None
    contents_dedup = max(contents_dedup_files, key=lambda f: f.stat().st_mtime) if contents_dedup_files else None

    return comments_dedup, contents_dedup


def save_report_to_file(report_content: str, stock_name: str, output_dir: str = None, suffix: str = ""):
    """
    保存报告到文件（输出到项目根目录/REPORT/）

    Args:
        report_content: 报告内容
        stock_name: 股票名称
        output_dir: 输出目录（默认项目根目录/REPORT/）
        suffix: 文件名后缀（用于区分不同报告）
    """
    from datetime import datetime

    if output_dir is None:
        paths = get_project_paths()
        output_path = paths['report_dir']
    else:
        output_path = Path(output_dir)

    output_path.mkdir(parents=True, exist_ok=True)

    # 生成文件名：股票名_日期时间_后缀.txt
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{stock_name}_情绪分析_{timestamp}{suffix}.txt"
    file_path = output_path / filename

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"\n📄 报告已保存到: {file_path}")
    return str(file_path)


if __name__ == "__main__":
    import sys
    import argparse
    from io import StringIO

    parser = argparse.ArgumentParser(
        description='股市情绪分析器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 自动模式：查找最新去重文件，输出到 REPORT/
  python stock_sentiment.py --auto

  # 手动指定文件
  python stock_sentiment.py data/comments-dedup.csv data/contents-dedup.csv "紫金矿业"

  # 禁用 FinBERT
  python stock_sentiment.py --auto --no-finbert
        """
    )

    parser.add_argument('--auto', action='store_true',
                        help='自动模式：查找最新去重文件')
    parser.add_argument('--data-dir', type=str, default=None,
                        help='数据目录（默认: 自动从项目根目录查找）')
    parser.add_argument('--output-dir', type=str, default=None,
                        help='报告输出目录（默认: 项目根目录/REPORT/）')
    parser.add_argument('comments_file', nargs='?', help='评论CSV文件路径')
    parser.add_argument('contents_file', nargs='?', help='内容CSV文件路径（可选）')
    parser.add_argument('stock_name', nargs='?', default='目标股票', help='股票名称')
    parser.add_argument('--no-finbert', action='store_true', help='禁用 FinBERT，仅使用关键词匹配')

    args = parser.parse_args()

    # 解析股票名
    stock_name = args.stock_name if args.stock_name != '目标股票' else '股票分析'

    # 确定是否生成两份报告（关键词 + FinBERT）
    if args.no_finbert:
        # 用户指定 --no-finbert，只生成关键词报告
        generate_both = False
    else:
        # 自动模式或手动模式都生成两份报告
        generate_both = True

    # 捕获控制台输出
    old_stdout = sys.stdout

    try:
        # 自动模式或手动模式都需要先获取文件路径
        if args.auto:
            sys.stdout = old_stdout  # 临时恢复，打印查找信息
            print(f"\n🔍 自动模式：查找最新去重文件...")
            print(f"   数据目录: {args.data_dir}")

            comments_file, contents_file = find_latest_dedup_files(args.data_dir)

            # 如果找不到去重文件，自动运行去重脚本
            if not comments_file:
                print("\n⚠️  未找到去重文件，自动运行去重脚本...")
                print("="*80)
                import subprocess
                import locale
                script_dir = Path(__file__).parent
                dedup_script = script_dir / "stock_sentiment_dedup.py"
                # 使用系统默认编码，避免 Windows GBK 编码问题
                result = subprocess.run(
                    ["uv", "run", "python", str(dedup_script), "--auto"],
                    encoding=locale.getpreferredencoding(),
                    errors='replace'
                )
                print("="*80)
                if result.returncode == 0:
                    print("✅ 去重完成！")
                    # 重新查找去重文件
                    comments_file, contents_file = find_latest_dedup_files(args.data_dir)
                    if not comments_file:
                        print("\n❌ 去重失败，无法继续分析")
                        sys.exit(1)
                else:
                    print(f"\n❌ 去重脚本执行失败，返回码: {result.returncode}")
                    sys.exit(1)

            print(f"   ✓ 评论文件: {comments_file.name}")
            if contents_file:
                print(f"   ✓ 内容文件: {contents_file.name}")

            comments_path = str(comments_file)
            contents_path = str(contents_file) if contents_file else None
        else:
            # 手动模式
            if not args.comments_file:
                parser.error("请指定 --auto 自动模式，或提供 comments_file 路径")

            comments_path = args.comments_file
            contents_path = args.contents_file

        # ========================================================================
        # 第一份报告：关键词分析（不使用 FinBERT）
        # ========================================================================
        print("\n" + "="*80)
        print("📊 生成第 1/2 份报告：关键词分析")
        print("="*80)

        sys.stdout = mystdout_keyword = StringIO()

        analyze_stock_sentiment(
            comments_file=comments_path,
            contents_file=contents_path,
            stock_name=stock_name,
            use_finbert=False  # 纯关键词
        )

        keyword_report = mystdout_keyword.getvalue()
        sys.stdout = old_stdout
        print(keyword_report)  # 打印到控制台

        save_report_to_file(keyword_report, stock_name, args.output_dir, suffix="_关键词")

        # ========================================================================
        # 第二份报告：FinBERT 分析
        # ========================================================================
        if generate_both:
            print("\n" + "="*80)
            print("🤖 生成第 2/2 份报告：FinBERT 分析")
            print("="*80)

            sys.stdout = mystdout_finbert = StringIO()

            analyze_stock_sentiment(
                comments_file=comments_path,
                contents_file=contents_path,
                stock_name=stock_name,
                use_finbert=True  # FinBERT
            )

            finbert_report = mystdout_finbert.getvalue()
            sys.stdout = old_stdout
            print(finbert_report)  # 打印到控制台

            save_report_to_file(finbert_report, stock_name, args.output_dir, suffix="_FinBERT")

    except Exception as e:
        sys.stdout = old_stdout
        print(f"\n❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
