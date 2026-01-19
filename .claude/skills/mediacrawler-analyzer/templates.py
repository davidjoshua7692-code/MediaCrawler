"""
MediaCrawler 分析模板库
提供预设的分析配置模板，适配不同社交媒体分析场景
"""

from typing import Dict, List, Any

# ============================================================================
# 分析模板定义
# ============================================================================

ANALYSIS_TEMPLATES: Dict[str, Dict[str, Any]] = {
    
    # 美食/餐厅分析模板
    'restaurant': {
        'name': '美食餐厅分析',
        'description': '适用于美食推荐、餐厅探店、美食教程等内容分析',
        'trigger_keywords': ['美食', '餐厅', '好吃', '推荐', '打卡', '探店', '小吃', '饭店', '菜馆', '火锅', '烧烤', '甜品'],
        'features': {
            '口味': ['好吃', '美味', '正宗', '口感', '味道', '鲜', '香', '辣', '甜', '咸'],
            '环境': ['装修', '氛围', '环境', '干净', '整洁', '装潢', '格调'],
            '服务': ['服务', '态度', '热情', '周到', '服务员', '上菜快'],
            '价格': ['便宜', '实惠', '性价比', '贵', '平价', '人均', '划算'],
            '分量': ['分量', '量足', '量大', '量少', '够吃'],
            '排队': ['排队', '等位', '人多', '需要预约', '不用排队']
        },
        'sentiment': {
            'positive': ['推荐', '好吃', '赞', '满意', '惊喜', '回头客', '必吃', '绝绝子'],
            'negative': ['失望', '踩雷', '不值', '坑', '难吃', '不会再来', '差评', '一般']
        },
        'location_patterns': [
            r'(\w+路)', r'(\w+广场)', r'(\w+商场)', r'(\w+街)',
            r'(\w+区)', r'(\w+店)'
        ]
    },

    # 咖啡厅/办公空间分析模板
    'workspace': {
        'name': '咖啡厅办公空间分析',
        'description': '适用于咖啡厅、自习室、共享办公空间等内容分析',
        'trigger_keywords': ['咖啡厅', '咖啡', '自习', '办公', '工作', '学习', '图书馆', '共享空间', '安静'],
        'features': {
            '安静程度': ['安静', '清净', '不吵', '嘈杂', '静', '吵'],
            '电源插座': ['插座', '电源', '充电', '没电', '有电'],
            '网络': ['wifi', 'wi-fi', '网速', '网络', '断网', '信号'],
            '座位': ['座位', '位置', '沙发', '桌子', '舒适', '硬'],
            '停车': ['停车', '停车位', '停车场', '好停车'],
            '营业时间': ['营业', '开门', '关门', '24小时', '晚上'],
            '价格': ['价格', '消费', '人均', '便宜', '贵', '性价比']
        },
        'sentiment': {
            'positive': ['推荐', '适合', '舒服', '棒', '喜欢', '方便', '值得'],
            'negative': ['吵', '贵', '差', '不好', '失望', '慢', '挤', '不推荐']
        },
        'location_patterns': [
            r'(\w+路)', r'(\w+广场)', r'(\w+商场)', r'地铁(\w+)站',
            r'(\w+区)', r'(\w+大学)'
        ]
    },

    # 旅游攻略分析模板
    'travel': {
        'name': '旅游攻略分析',
        'description': '适用于旅游攻略、景点推荐、行程规划等内容分析',
        'trigger_keywords': ['旅游', '攻略', '景点', '旅行', '出行', '度假', '游玩', '打卡', '游记'],
        'features': {
            '景点': ['景点', '风景', '景色', '名胜', '古迹', '网红点'],
            '交通': ['交通', '地铁', '公交', '打车', '自驾', '高铁', '飞机'],
            '住宿': ['酒店', '民宿', '住宿', '入住', '房间', '预订'],
            '美食': ['美食', '小吃', '特色菜', '餐厅', '当地美食'],
            '费用': ['门票', '免费', '价格', '费用', '预算', '性价比'],
            '季节': ['季节', '天气', '最佳时间', '淡季', '旺季', '人多']
        },
        'sentiment': {
            'positive': ['推荐', '值得', '美', '震撼', '惊艳', '不虚此行', '必去'],
            'negative': ['不值', '失望', '商业化', '坑', '人太多', '不推荐']
        },
        'location_patterns': [
            r'(\w+景区)', r'(\w+公园)', r'(\w+古镇)', r'(\w+山)',
            r'(\w+湖)', r'(\w+寺)', r'(\w+博物馆)'
        ]
    },

    # 穿搭时尚分析模板
    'fashion': {
        'name': '穿搭时尚分析',
        'description': '适用于穿搭分享、时尚推荐、服装测评等内容分析',
        'trigger_keywords': ['穿搭', '时尚', '搭配', '衣服', 'ootd', '风格', '服装', '时装', '潮流'],
        'features': {
            '风格': ['风格', '穿搭', '搭配', '造型', '复古', '简约', '甜美', '酷'],
            '季节': ['春季', '夏季', '秋季', '冬季', '保暖', '透气', '清凉'],
            '身材': ['显瘦', '显高', '遮肉', '宽松', '修身', '版型'],
            '价格': ['平价', '性价比', '贵', '便宜', '白菜价', '大牌平替'],
            '场合': ['日常', '约会', '工作', '度假', '运动', '通勤', '休闲'],
            '质量': ['质量', '面料', '做工', '舒适', '起球', '掉色']
        },
        'sentiment': {
            'positive': ['好看', '推荐', '种草', '必买', '回购', '爱了', '绝美'],
            'negative': ['丑', '不值', '差评', '退了', '踩雷', '不推荐', '翻车']
        },
        'location_patterns': []  # 穿搭内容通常不关注地点
    },

    # 学习资源分析模板
    'learning': {
        'name': '学习资源分析',
        'description': '适用于学习教程、课程评测、技能分享等内容分析',
        'trigger_keywords': ['学习', '教程', '课程', '入门', '进阶', '技能', '自学', '培训', '考试', '考证'],
        'features': {
            '难度': ['入门', '基础', '进阶', '高级', '简单', '难', '零基础'],
            '实用性': ['实用', '干货', '有用', '实战', '案例', '项目'],
            '讲解': ['讲解', '清晰', '详细', '易懂', '啰嗦', '跳跃'],
            '时长': ['时长', '课时', '多久', '几小时', '几天'],
            '价格': ['免费', '付费', '价格', '贵', '便宜', '值得'],
            '证书': ['证书', '认证', '资格', '考试', '通过率']
        },
        'sentiment': {
            'positive': ['推荐', '干货', '有用', '收藏', '学到', '进步', '值得'],
            'negative': ['水', '没用', '浪费时间', '差', '不推荐', '后悔']
        },
        'location_patterns': []
    },

    # 产品测评分析模板
    'product_review': {
        'name': '产品测评分析',
        'description': '适用于产品测评、开箱、使用体验等内容分析',
        'trigger_keywords': ['测评', '开箱', '体验', '使用', '评测', '对比', '推荐', '种草'],
        'features': {
            '质量': ['质量', '做工', '材质', '耐用', '手感', '品质'],
            '性能': ['性能', '效果', '功能', '好用', '实用'],
            '外观': ['颜值', '好看', '设计', '外观', '颜色', '款式'],
            '价格': ['价格', '性价比', '值', '便宜', '贵', '划算'],
            '服务': ['售后', '物流', '包装', '客服', '退换'],
            '对比': ['对比', '比较', 'vs', '平替', '代替', '更好']
        },
        'sentiment': {
            'positive': ['推荐', '好用', '值得', '满意', '惊喜', '回购', '必买'],
            'negative': ['失望', '踩雷', '不值', '差', '退货', '不推荐', '翻车']
        },
        'location_patterns': []
    },

    # 通用社交内容分析模板（默认）
    'generic': {
        'name': '通用社交内容分析',
        'description': '适用于各类社交媒体内容的通用分析模板',
        'trigger_keywords': [],  # 作为默认模板，不限制触发关键词
        'features': {
            '质量': ['好', '不错', '优质', '精品', '专业'],
            '体验': ['体验', '感受', '效果', '满意', '舒服'],
            '推荐': ['推荐', '值得', '必看', '收藏', '分享'],
            '价格': ['价格', '性价比', '值', '便宜', '贵']
        },
        'sentiment': {
            'positive': ['好', '推荐', '喜欢', '满意', '赞', '爱了', '绝了'],
            'negative': ['差', '失望', '不好', '不推荐', '一般', '坑']
        },
        'location_patterns': [
            r'(\w+路)', r'(\w+区)', r'(\w+市)', r'(\w+省)'
        ]
    }
}


# ============================================================================
# 模板匹配函数
# ============================================================================

def match_template(keywords: str) -> str:
    """
    根据搜索关键词匹配最佳分析模板
    
    Args:
        keywords: 用户搜索的关键词（可能包含多个，用逗号分隔）
    
    Returns:
        str: 匹配的模板ID
    """
    keywords_lower = keywords.lower()
    
    # 计算每个模板的匹配分数
    scores = {}
    for template_id, template in ANALYSIS_TEMPLATES.items():
        if template_id == 'generic':
            continue  # 通用模板作为兜底
        
        score = 0
        for trigger in template.get('trigger_keywords', []):
            if trigger in keywords_lower:
                score += 1
        
        if score > 0:
            scores[template_id] = score
    
    # 返回得分最高的模板，如果没有匹配则返回通用模板
    if scores:
        return max(scores, key=scores.get)
    return 'generic'


def get_template(template_id: str) -> Dict[str, Any]:
    """
    获取指定模板的配置
    
    Args:
        template_id: 模板ID
    
    Returns:
        dict: 模板配置
    """
    return ANALYSIS_TEMPLATES.get(template_id, ANALYSIS_TEMPLATES['generic'])


def list_templates() -> List[Dict[str, str]]:
    """
    列出所有可用模板
    
    Returns:
        list: 模板列表，每项包含 id, name, description
    """
    return [
        {
            'id': template_id,
            'name': template['name'],
            'description': template['description']
        }
        for template_id, template in ANALYSIS_TEMPLATES.items()
    ]


def get_template_keywords(template_id: str) -> Dict[str, Any]:
    """
    获取模板的关键词配置（用于传入 analyze_mediacrawler_data）
    
    Args:
        template_id: 模板ID
    
    Returns:
        dict: 包含 features 和 sentiment 的关键词配置
    """
    template = get_template(template_id)
    return {
        'features': template.get('features', {}),
        'sentiment': template.get('sentiment', {})
    }


def suggest_analysis_dimensions(keywords: str) -> Dict[str, Any]:
    """
    根据关键词推荐分析维度（供 AI 推理使用）
    
    Args:
        keywords: 搜索关键词
    
    Returns:
        dict: 推荐的分析配置和说明
    """
    template_id = match_template(keywords)
    template = get_template(template_id)
    
    return {
        'recommended_template': template_id,
        'template_name': template['name'],
        'template_description': template['description'],
        'suggested_features': list(template.get('features', {}).keys()),
        'can_analyze': {
            'location': bool(template.get('location_patterns')),
            'sentiment': bool(template.get('sentiment')),
            'features': bool(template.get('features'))
        },
        'customization_hint': '可以根据用户具体需求调整 features 和 sentiment 关键词'
    }


# ============================================================================
# 命令行测试
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        keywords = sys.argv[1]
        result = suggest_analysis_dimensions(keywords)
        print(f"\n搜索关键词: {keywords}")
        print(f"推荐模板: {result['template_name']} ({result['recommended_template']})")
        print(f"模板说明: {result['template_description']}")
        print(f"建议分析维度: {', '.join(result['suggested_features'])}")
        print(f"支持分析: 地点={result['can_analyze']['location']}, "
              f"情感={result['can_analyze']['sentiment']}, "
              f"特征={result['can_analyze']['features']}")
    else:
        print("可用分析模板:")
        for t in list_templates():
            print(f"  - {t['id']}: {t['name']}")
            print(f"    {t['description']}")
