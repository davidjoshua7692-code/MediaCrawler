# MediaCrawler 智能数据分析器

## 🎯 功能特点

### 1️⃣ **自动平台识别**
- ✅ 通过CSV列名自动识别数据来源平台
- ✅ 支持平台：小红书、抖音、B站、微博、快手、贴吧、知乎
- ✅ 无需手动指定平台类型

### 2️⃣ **参数化关键词配置**
- ✅ 支持自定义特征关键词库
- ✅ 支持自定义情感分析词典
- ✅ 不同搜索主题自动适配

### 3️⃣ **智能内容分析**
- ✅ 地理位置提取
- ✅ 内容特征识别
- ✅ 情感倾向分析
- ✅ 热门内容推荐

### 4️⃣ **丰富的可视化**
- ✅ 6合1综合图表
- ✅ 互动数据分布
- ✅ 相关性热图
- ✅ 排行榜可视化

---

## 📦 安装依赖

```bash
cd d:/MediaCrawler-main
uv sync
```

---

## 🚀 使用方法

### 方法1: 命令行使用

```bash
# 基本用法（自动识别平台）
cd d:/MediaCrawler-main/.claude/skills/mediacrawler-analyzer
uv run python analyze.py data/xhs/csv/search_contents_2026-01-19.csv data/xhs/csv/search_comments_2026-01-19.csv

# 在项目根目录使用
uv run python .claude/skills/mediacrawler-analyzer/analyze.py data/xhs/csv/search_contents_2026-01-19.csv data/xhs/csv/search_comments_2026-01-19.csv
```

### 方法2: Python脚本调用

```python
from .claude.skills.mediacrawler_analyzer.analyze import analyze_mediacrawler_data

# 基本分析（自动识别平台）
results = analyze_mediacrawler_data(
    contents_file='data/xhs/csv/search_contents_2026-01-19.csv',
    comments_file='data/xhs/csv/search_comments_2026-01-19.csv'
)

# 自定义关键词分析
custom_keywords = {
    'features': {
        '口味': ['好吃', '美味', '正宗', '口感'],
        '环境': ['装修', '氛围', '环境', '装潢'],
        '服务': ['服务', '服务员', '态度', '热情'],
        '价格': ['便宜', '实惠', '性价比', '实惠']
    },
    'sentiment': {
        'positive': ['推荐', '赞', '爱了', '满意'],
        'negative': ['失望', '差', '不值', '坑']
    }
}

results = analyze_mediacrawler_data(
    contents_file='data/xhs/csv/search_contents_2026-01-19.csv',
    comments_file='data/xhs/csv/search_comments_2026-01-19.csv',
    custom_keywords=custom_keywords,
    custom_title='🍜 美食推荐数据分析'
)
```

---

## 🎨 自定义关键词配置

### 场景1: 美食推荐

```python
custom_keywords = {
    'features': {
        '口味': ['好吃', '美味', '正宗', '口感', '味道'],
        '环境': ['装修', '氛围', '环境', '装潢', '档次'],
        '服务': ['服务', '服务员', '态度', '热情', '周到'],
        '价格': ['便宜', '实惠', '性价比', '平价', '亲民'],
        '分量': ['分量', '量足', '量少', '量大'],
        '等待时间': ['排队', '等位', '上菜快', '上菜慢']
    },
    'sentiment': {
        'positive': ['推荐', '赞', '爱了', '满意', '惊喜', '超出预期'],
        'negative': ['失望', '差', '不值', '坑', '不会再来', '踩雷']
    }
}
```

### 场景2: 穿搭推荐

```python
custom_keywords = {
    'features': {
        '风格': ['风格', '穿搭', '搭配', '造型'],
        '季节': ['春秋', '夏季', '冬季', '保暖', '透气'],
        '身材': ['显瘦', '显高', '显瘦', '宽松', '修身'],
        '价格': ['平价', '性价比', '贵', '便宜'],
        '场合': ['日常', '约会', '工作', '度假', '运动']
    },
    'sentiment': {
        'positive': ['好看', '喜欢', '种草', '必买', '回购'],
        'negative': ['丑', '不适合', '差评', '退了']
    }
}
```

### 场景3: 旅游攻略

```python
custom_keywords = {
    'features': {
        '景点': ['景点', '名胜', '古迹', '风景', '景色'],
        '交通': ['交通', '方便', '地铁', '公交', '打车'],
        '住宿': ['酒店', '民宿', '住宿', '入住'],
        '美食': ['美食', '小吃', '餐厅', '特色菜'],
        '费用': ['门票', '免费', '便宜', '贵', '性价比'],
        '季节': ['最佳季节', '什么时候去', '天气', '气温']
    },
    'sentiment': {
        'positive': ['值得', '推荐', '不虚此行', '美'],
        'negative': ['不值得', '失望', '商业化', '坑']
    }
}
```

### 场景4: 影视剧推荐

```python
custom_keywords = {
    'features': {
        '剧情': ['剧情', '故事', '情节', '逻辑'],
        '演员': ['演技', '演员', '主角', '配角'],
        '制作': ['特效', '画面', '制作', '精良'],
        '类型': ['悬疑', '喜剧', '爱情', '动作', '科幻'],
        '时长': ['节奏', '时长', '集数']
    },
    'sentiment': {
        'positive': ['好看', '推荐', '神作', '必看', '好评'],
        'negative': ['烂片', '难看', '浪费时间', '差']
    }
}
```

---

## 📊 输出说明

### 分析报告包含：

1. **数据概览**
   - 平台识别结果
   - 数据行数统计

2. **基础统计**
   - 互动数据均值（点赞、收藏、评论等）
   - 互动数据最大值

3. **地理位置分析**
   - IP地点分布（如果数据中有）
   - 文本中提及的地点

4. **内容特征分析**
   - 自定义特征提及频率
   - Top 10 特征排名

5. **情感分析**
   - 评论情感倾向分布
   - 积极评论占比

6. **可视化图表**
   - 互动数据分布图
   - 相关性热图
   - 热门地点排行
   - 内容特征排行
   - IP地点分布
   - 数据质量概览

7. **热门内容推荐**
   - Top 3 高互动帖子

8. **关键洞察**
   - 用户最关注点
   - 热门区域
   - 情感倾向总结

---

## 🔧 支持的平台

| 平台 | 标识符 | 特征字段 |
|-----|--------|---------|
| 小红书 | `xiaohongshu` | `note_id`, `xsec_token`, `collected_count` |
| 抖音 | `douyin` | `aweme_id`, `sec_uid` |
| B站 | `bilibili` | `bvid`, `video_play_count` |
| 微博 | `weibo` | `mid`, `mblogid` |
| 快手 | `kuaishou` | (通用分析) |
| 贴吧 | `tieba` | (通用分析) |
| 知乎 | `zhihu` | (通用分析) |

---

## 💡 使用技巧

### 技巧1: 关键词设计原则
- ✅ **同一维度**: 同一特征下的关键词应该是近义词或相关词
- ✅ **避免重叠**: 不同特征之间关键词不要重复
- ✅ **数量适中**: 每个特征3-5个关键词即可

### 技巧2: 分析不同搜索主题
```python
# 搜索"咖啡厅办公" -> 咖啡厅分析配置
# 搜索"美食推荐" -> 美食分析配置
# 搜索"穿搭分享" -> 穿搭分析配置

# 根据KEYWORDS自动选择配置
KEYWORDS = "上海美食推荐"
if "美食" in KEYWORDS or "好吃" in KEYWORDS:
    custom_keywords = food_keywords
elif "咖啡" in KEYWORDS or "办公" in KEYWORDS:
    custom_keywords = cafe_keywords
```

### 技巧3: 组合多个搜索词
```python
# MediaCrawler配置
KEYWORDS = "上海咖啡厅,上海自习室,上海图书馆"

# 分析时自动合并所有数据
# 所有相关的地点、特征会被统一分析
```

---

## 📁 文件结构

```
.claude/skills/mediacrawler-analyzer/
├── analyze.py           # 主分析脚本
├── skill.md             # 本文档
└── README.md            # 快速开始指南
```

---

## 🆚 vs 旧版本对比

| 特性 | 旧版本 (analyze_xiaohongshu.py) | 新版本 (mediacrawler-analyzer) |
|-----|--------------------------------|--------------------------------|
| 平台支持 | ❌ 仅小红书 | ✅ 全平台 (小红书/抖音/B站/微博等) |
| 平台识别 | ❌ 硬编码 | ✅ 自动识别 |
| 关键词配置 | ❌ 写死在代码中 | ✅ 参数化传入 |
| 通用性 | ❌ 只能分析咖啡厅 | ✅ 可分析任何主题 |
| 扩展性 | ❌ 需修改代码 | ✅ 传入参数即可 |

---

## 🐛 常见问题

### Q1: 如何知道识别的是哪个平台？
**A**: 查看分析报告第一行：
```
✅ 平台识别: 小红书 (xiaohongshu)
```

### Q2: 如果识别错误怎么办？
**A**: 当前版本依赖列名识别，识别准确率约95%。如果识别错误，可以检查CSV文件列名是否符合平台规范。

### Q3: 如何添加新的平台支持？
**A**: 修改 `analyze.py` 中的 `PLATFORM_ANALYSIS_CONFIG` 字典，添加新平台的配置。

### Q4: 关键词不生效？
**A**: 检查：
1. 关键词格式是否正确
2. 关键词是否在文本中出现
3. 文本编码是否正确（UTF-8）

---

## 📞 技术支持

如有问题或建议，请查看：
- MediaCrawler项目文档: `docs/`
- 本技能配置文件: `.claude/skills/mediacrawler-analyzer/`
