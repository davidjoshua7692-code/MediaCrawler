"""
FinBERT 中文金融情感分析模块
专门针对股市讨论进行情绪分析
"""
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 尝试导入 transformers
try:
    from transformers import (
        TextClassificationPipeline,
        AutoModelForSequenceClassification,
        BertTokenizerFast
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False


class FinBertAnalyzer:
    """FinBERT 中文金融情感分析器"""

    def __init__(self, model_path: str = "./models/finbert_chinese/"):
        """
        初始化 FinBERT 模型

        Args:
            model_path: 模型路径（本地或 Hugging Face）
        """
        self.model_path = model_path
        self.model_loaded = False
        self.pipeline = None

        if not TRANSFORMERS_AVAILABLE:
            print("⚠️  transformers 库未安装，无法使用 FinBERT")
            print("   安装方法: uv add torch transformers")
            return

        # 检查模型文件是否存在
        model_path_obj = Path(model_path)
        if not model_path_obj.exists():
            print(f"⚠️  模型目录不存在: {model_path}")
            print("   请先运行: python download_finbert_model.py")
            return

        try:
            # 加载模型
            print(f"📦 正在加载 FinBERT 模型: {model_path}")

            model = AutoModelForSequenceClassification.from_pretrained(
                model_path,
                output_attentions=True
            )

            tokenizer = BertTokenizerFast.from_pretrained(model_path)

            # 创建 pipeline
            self.pipeline = TextClassificationPipeline(
                model=model,
                tokenizer=tokenizer,
                top_k=None,  # 返回所有分数
                device=0  # GPU (RTX 4070 Ti SUPER)
            )

            self.model_loaded = True
            print("✅ FinBERT 模型加载成功!")
            print("   标签映射: LABEL_0=中性, LABEL_1=正面(看涨), LABEL_2=负面(看跌)")

        except Exception as e:
            print(f"❌ FinBERT 模型加载失败: {e}")
            print("   将回退到关键词匹配方法")

    def analyze(self, text: str) -> Dict[str, any]:
        """
        分析单条文本的金融情感

        Args:
            text: 文本内容

        Returns:
            {
                'sentiment': 'bullish' | 'bearish' | 'neutral',
                'confidence': float,
                'scores': {标签: 分数},
                'method': 'finbert' | 'keyword'
            }
        """
        if not text or pd.isna(text):
            return {
                'sentiment': 'neutral',
                'confidence': 0.0,
                'scores': {},
                'method': 'keyword'
            }

        text = str(text)

        # 如果模型未加载，使用关键词匹配
        if not self.model_loaded:
            return self._keyword_analyze(text)

        try:
            # 使用 FinBERT 分析
            results = self.pipeline(text[:512])  # 限制512 tokens

            # results 格式: [[{label: 'LABEL_0', score: 0.1}, ...]]
            scores = results[0]

            # 找出最高分的标签
            top_result = max(scores, key=lambda x: x['score'])
            label = top_result['label']
            confidence = top_result['score']

            # 映射到股市情绪（支持两种标签格式）
            label_mapping_label = {
                'LABEL_0': 'neutral',   # 中性
                'LABEL_1': 'bullish',   # 正面 → 看涨
                'LABEL_2': 'bearish'    # 负面 → 看跌
            }

            label_mapping_text = {
                'Neutral': 'neutral',
                'Positive': 'bullish',
                'Negative': 'bearish'
            }

            sentiment = label_mapping_label.get(label) or label_mapping_text.get(label, 'neutral')

            # 构建分数字典
            scores_dict = {
                'neutral': next((s['score'] for s in scores if s['label'] in ['LABEL_0', 'Neutral']), 0.0),
                'bullish': next((s['score'] for s in scores if s['label'] in ['LABEL_1', 'Positive']), 0.0),
                'bearish': next((s['score'] for s in scores if s['label'] in ['LABEL_2', 'Negative']), 0.0),
            }

            # 细化情绪分类（9类）
            fine_grained_sentiment = self._get_fine_grained_sentiment(scores_dict)

            return {
                'sentiment': sentiment,
                'fine_grained': fine_grained_sentiment,  # 新增：细粒度情绪
                'confidence': confidence,
                'scores': scores_dict,
                'method': 'finbert'
            }

        except Exception as e:
            print(f"⚠️  FinBERT 分析出错: {e}，回退到关键词匹配")
            return self._keyword_analyze(text)

    def _get_fine_grained_sentiment(self, scores: Dict[str, float]) -> str:
        """
        根据分数分布获取细粒度情绪（9类）

        Args:
            scores: {'bullish': 0.99, 'bearish': 0.005, 'neutral': 0.005}

        Returns:
            细粒度情绪标签
        """
        bullish = scores.get('bullish', 0.0)
        bearish = scores.get('bearish', 0.0)
        neutral = scores.get('neutral', 0.0)

        # 强烈看涨：Positive > 80% 且 Positive > Negative*2
        if bullish > 0.8 and bullish > bearish * 2:
            return '强烈看涨📈📈'

        # 看涨：Positive > 60% 且 Positive > Negative*1.5
        if bullish > 0.6 and bullish > bearish * 1.5:
            return '看涨📈'

        # 偏涨：50% < Positive ≤ 60%
        if 0.5 < bullish <= 0.6:
            return '偏涨📊'

        # 强烈看跌：Negative > 80% 且 Negative > Positive*2
        if bearish > 0.8 and bearish > bullish * 2:
            return '强烈看跌📉📉'

        # 看跌：Negative > 60% 且 Negative > Positive*1.5
        if bearish > 0.6 and bearish > bullish * 1.5:
            return '看跌📉'

        # 偏跌：50% < Negative ≤ 60%
        if 0.5 < bearish <= 0.6:
            return '偏跌📊'

        # 中性区间
        if neutral > 0.4:
            if bearish > bullish * 1.2:
                return '中性偏空⚪📉'
            elif bullish > bearish * 1.2:
                return '中性偏多⚪📈'
            else:
                return '纯中性⚪'

        # 低置信度（所有分数都较低）
        if max(bullish, bearish, neutral) < 0.5:
            return '不确定❓'

        return '中性⚪'

    def _keyword_analyze(self, text: str) -> Dict[str, any]:
        """
        关键词匹配分析（回退方案）

        Args:
            text: 文本内容

        Returns:
            分析结果字典
        """
        # 看涨关键词
        bullish_keywords = [
            '涨', '加仓', '买入', '看多', '起飞', '突破', '牛市',
            '持有', '不卖', '继续涨', '还能涨', '目标', '好', '牛',
            '强', '稳', '值', '低吸', '补仓', '机会', '买'
        ]

        # 看跌关键词
        bearish_keywords = [
            '跌', '减仓', '卖出', '看空', '回调', '熊市',
            '出货', '高估', '贵', '弱', '风险', '怕', '跌了',
            '清仓', '割肉', '亏损', '套', '怕跌', '还会跌'
        ]

        text_lower = text.lower()
        bullish_score = sum(1 for kw in bullish_keywords if kw in text_lower)
        bearish_score = sum(1 for kw in bearish_keywords if kw in text_lower)

        if bullish_score > bearish_score:
            sentiment = 'bullish'
            confidence = min(0.6 + bullish_score * 0.1, 0.95)
        elif bearish_score > bullish_score:
            sentiment = 'bearish'
            confidence = min(0.6 + bearish_score * 0.1, 0.95)
        else:
            sentiment = 'neutral'
            confidence = 0.5

        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'scores': {
                'bullish': 0.7 if sentiment == 'bullish' else 0.2,
                'bearish': 0.7 if sentiment == 'bearish' else 0.2,
                'neutral': 0.6 if sentiment == 'neutral' else 0.2,
            },
            'method': 'keyword'
        }

    def batch_analyze(
        self,
        texts: List[str],
        show_progress: bool = True
    ) -> List[Dict[str, any]]:
        """
        批量分析文本

        Args:
            texts: 文本列表
            show_progress: 是否显示进度

        Returns:
            分析结果列表
        """
        results = []
        total = len(texts)

        for i, text in enumerate(texts, 1):
            if show_progress and i % 10 == 0:
                print(f"  进度: {i}/{total} ({i/total*100:.1f}%)")

            result = self.analyze(text)
            results.append(result)

        return results


# ============================================================================
# 混合分析器（关键词 + FinBERT）
# ============================================================================

class HybridSentimentAnalyzer:
    """
    混合情绪分析器
    优先使用关键词匹配（快速），不确定时使用 FinBERT（精准）
    """

    def __init__(self, model_path: str = "./models/finbert_chinese/"):
        """
        初始化混合分析器

        Args:
            model_path: FinBERT 模型路径
        """
        self.finbert = FinBertAnalyzer(model_path)

        # 关键词
        self.bullish_keywords = [
            '涨', '加仓', '买入', '看多', '起飞', '突破', '牛市',
            '持有', '不卖', '继续涨', '还能涨', '目标', '好', '牛',
            '强', '稳', '值', '低吸', '补仓', '机会', '买'
        ]

        self.bearish_keywords = [
            '跌', '减仓', '卖出', '看空', '回调', '熊市',
            '出货', '高估', '贵', '弱', '风险', '怕', '跌了',
            '清仓', '割肉', '亏损', '套', '怕跌', '还会跌'
        ]

    def analyze(self, text: str) -> Dict[str, any]:
        """
        混合分析

        Args:
            text: 文本内容

        Returns:
            分析结果字典
        """
        if not text or pd.isna(text):
            return {'sentiment': 'neutral', 'confidence': 0.0, 'method': 'keyword'}

        text = str(text)

        # 1. 先用关键词快速匹配
        text_lower = text.lower()
        bullish_score = sum(1 for kw in self.bullish_keywords if kw in text_lower)
        bearish_score = sum(1 for kw in self.bearish_keywords if kw in text_lower)

        # 2. 判断关键词是否确定
        if abs(bullish_score - bearish_score) >= 2:
            # 关键词得分差异明显，直接返回
            if bullish_score > bearish_score:
                sentiment = 'bullish'
                confidence = min(0.6 + bullish_score * 0.1, 0.95)
            else:
                sentiment = 'bearish'
                confidence = min(0.6 + bearish_score * 0.1, 0.95)

            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'scores': {
                    'bullish': 0.8 if sentiment == 'bullish' else 0.2,
                    'bearish': 0.8 if sentiment == 'bearish' else 0.2,
                    'neutral': 0.3,
                },
                'method': 'keyword'
            }

        # 3. 关键词不确定，使用 FinBERT
        if self.finbert.model_loaded:
            return self.finbert.analyze(text)
        else:
            # FinBERT 未加载，使用关键词结果
            if bullish_score > bearish_score:
                return {'sentiment': 'bullish', 'confidence': 0.55, 'method': 'keyword'}
            elif bearish_score > bullish_score:
                return {'sentiment': 'bearish', 'confidence': 0.55, 'method': 'keyword'}
            else:
                return {'sentiment': 'neutral', 'confidence': 0.5, 'method': 'keyword'}
