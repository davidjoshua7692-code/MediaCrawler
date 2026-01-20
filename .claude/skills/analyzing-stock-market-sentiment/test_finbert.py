"""
FinBERT 集成测试脚本
测试 FinBERT 是否正常工作
"""
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from finbert_analyzer import FinBertAnalyzer, HybridSentimentAnalyzer


def get_project_paths():
    """获取项目路径（锚定到.claude文件夹）"""
    script_dir = Path(__file__).parent
    # .claude/skills/analyzing-stock-market-sentiment/ -> .claude/
    claude_dir = script_dir.parent.parent
    project_root = claude_dir.parent

    return {
        'project_root': project_root,
        'model_dir': project_root / "models" / "finbert_chinese"
    }


def test_finbert():
    """测试 FinBERT 分析器"""

    print("="*80)
    print("🧪 FinBERT 集成测试")
    print("="*80)

    # 测试文本
    test_cases = [
        "紫金矿业业绩超预期，净利润增长50%",
        "感觉要回调，先跑了",
        "紫金确实稳，从不套人",
        "此外宁德时代上半年实现出口约2GWh，同比增加200%+。",
        "我同学说会跌，但我看好",
        "呵呵，继续涨吧",
        "不会跌了，拿住",
        "还可以吧，一般般",
        "估值太高了，风险大"
    ]

    print("\n" + "="*80)
    print("方法1: 纯 FinBERT 分析")
    print("="*80 + "\n")

    # 初始化 FinBERT
    paths = get_project_paths()
    analyzer = FinBertAnalyzer(model_path=str(paths['model_dir']))

    if analyzer.model_loaded:
        for i, text in enumerate(test_cases, 1):
            result = analyzer.analyze(text)
            sentiment = result['sentiment']
            conf = result['confidence']
            method = result['method']

            # 中文情绪
            sentiment_cn = {
                'bullish': '看涨📈',
                'bearish': '看跌📉',
                'neutral': '中性⚪'
            }[sentiment]

            # 获取细粒度情绪
            if isinstance(result, dict) and 'fine_grained' in result:
                fine_grained = result['fine_grained']
            else:
                fine_grained = sentiment_cn.get(sentiment, '中性')

            print(f"{i}. {text}")
            print(f"   → {fine_grained} (置信度: {conf:.2%}) [{method}]")

            if result['scores']:
                scores = result['scores']
                print(f"   分数详情: 看涨={scores['bullish']:.2%}, "
                      f"看跌={scores['bearish']:.2%}, "
                      f"中性={scores['neutral']:.2%}")
            print()
    else:
        print("⚠️  FinBERT 模型未加载")
        print("   请确保:")
        print("   1. 已运行: python download_finbert_model.py")
        print("   2. 模型文件在: ../../../models/finbert_chinese/")
        return False

    print("\n" + "="*80)
    print("方法2: 混合分析（关键词 + FinBERT）")
    print("="*80 + "\n")

    # 测试混合分析器
    paths = get_project_paths()
    hybrid = HybridSentimentAnalyzer(model_path=str(paths['model_dir']))

    for i, text in enumerate(test_cases, 1):
        result = hybrid.analyze(text)
        sentiment = result['sentiment']
        conf = result['confidence']
        method = result['method']

        sentiment_cn = {
            'bullish': '看涨📈',
            'bearish': '看跌📉',
            'neutral': '中性⚪'
        }[sentiment]

        # 获取细粒度情绪
        if isinstance(result, dict) and 'fine_grained' in result:
            fine_grained = result['fine_grained']
        else:
            fine_grained = sentiment_cn.get(sentiment, '中性')

        method_label = {
            'finbert': 'FinBERT 🤖',
            'keyword': '关键词 🔑'
        }[method]

        print(f"{i}. {text}")
        print(f"   → {fine_grained} ({method_label}, 置信度: {conf:.2%})")
        print()

    print("="*80)
    print("✅ 测试完成!")
    print("="*80)

    return True


if __name__ == "__main__":
    test_finbert()
