# 常见问题与错误处理

## 🔧 分析结果问题

### 特征分析为空

**原因**：
- 使用了不匹配的模板（如用美食模板分析穿搭内容）
- 关键词未覆盖数据中的实际用语
- 数据量太少

**解决**：
```python
# 1. 预览数据，查看推荐模板
from analyze import preview_data_structure
preview = preview_data_structure('data/xhs/csv/search_contents.csv')
print(preview['suggested_template'])

# 2. 查看帖子内容，提取高频词
import pandas as pd
df = pd.read_csv('data/xhs/csv/search_contents.csv')
print(df['title'].head(10))

# 3. 自定义关键词
custom_keywords = {
    'features': {'关注点1': ['词1', '词2'], ...}
}
```

### 地点分析为空

**原因**：数据中没有地点信息或未使用支持地点分析的模板

**解决**：检查模板是否支持地点分析
```python
from templates import get_template
template = get_template('workspace')
print('支持地点:', bool(template.get('location_patterns')))
```

---

## 🐛 运行错误

### ModuleNotFoundError: No module named 'templates'

**原因**：从错误目录运行脚本

**解决**：
```bash
# 正确方式
cd d:/MediaCrawler-main
uv run python .claude/skills/mediacrawler-analyzer/analyze.py ...
```

### 中文乱码

**原因**：字体配置问题

**解决**：
```python
# Windows 通常不会有问题，如果有：
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
```

### FileNotFoundError

**原因**：CSV 文件路径错误

**解决**：
```bash
# 检查文件是否存在
dir data\xhs\csv\

# 使用完整路径
uv run python analyze.py d:/MediaCrawler-main/data/xhs/csv/search_contents_2026-01-19.csv
```

---

## 📋 模板相关

### 添加新模板

编辑 `templates.py`：

```python
ANALYSIS_TEMPLATES['my_template'] = {
    'name': '我的模板',
    'description': '模板说明',
    'trigger_keywords': ['触发词1', '触发词2'],
    'features': {
        '维度1': ['关键词1', '关键词2'],
    },
    'sentiment': {
        'positive': ['好词'],
        'negative': ['坏词']
    },
    'location_patterns': []  # 留空表示不分析地点
}
```

### 查看所有模板

```bash
uv run python .claude/skills/mediacrawler-analyzer/templates.py
```

---

## 🔍 数据格式

### 支持的平台

| 平台 | 识别字段 | 互动指标 |
|-----|---------|---------|
| 小红书 | `note_id`, `xsec_token` | liked, collected, comment, share |
| 抖音 | `aweme_id`, `sec_uid` | liked, comment, share |
| B站 | `bvid` | liked, play, coin, collect |
| 微博 | `mid`, `mblogid` | liked, comment, repost |
| 快手 | `photo_id` | liked, view, comment |
| 贴吧 | `thread_id` | reply |
| 知乎 | `answer_id` | voteup, comment |

### 必需的 CSV 列

**内容文件**：至少包含 `title` 或 `desc` 或 `text`
**评论文件**（可选）：包含 `content` 列
