# 通用数据提取工具 (Universal Data Extractor)

> 🎯 **从MediaCrawler爬取的CSV数据中快速提取结构化信息**

## ✨ 特性

- 🔍 **关键词搜索** - 支持多关键词组合搜索
- 🎨 **正则表达式** - 灵活匹配复杂模式
- 💰 **价格提取** - 自动识别各种价格格式
- 📍 **地理位置** - 提取和统计地点信息
- 🔥 **热门内容** - 快速找到高互动帖子
- 📊 **统计分析** - 一键获取数据概览
- 🔧 **自定义提取** - 支持自定义过滤和提取逻辑
- 💾 **多格式导出** - 支持JSON和CSV格式

---

## 🚀 快速开始

### 命令行使用

```bash
# 基础用法
python extractor.py contents.csv --keywords "咖啡厅"

# 提取价格信息
python extractor.py contents.csv --extract-prices --top 30

# 提取热门帖子
python extractor.py contents.csv --top-posts --min-likes 500

# 保存结果
python extractor.py contents.csv --keywords "自习" --save results.json
```

### Python API使用

```python
from extractor import UniversalExtractor

# 初始化
extractor = UniversalExtractor('contents.csv')

# 关键词搜索
results = extractor.extract_by_keywords(['咖啡', '自习'], top_n=20)

# 提取价格
prices = extractor.extract_prices(top_n=50)

# 打印结果
extractor.print_results(results, title="搜索结果")

# 保存结果
extractor.save_results(results, 'output.json')
```

---

## 📖 文件结构

```
analyzing-social-media-data/
├── extractor.py           # 🎯 核心提取工具（主文件）
├── examples.py            # 📚 9个实用示例
├── EXTRACTOR_GUIDE.md     # 📖 详细使用指南
└── README_EXTRACTOR.md    # 📄 本文件
```

---

## 🎯 核心功能

### 1. 关键词搜索

```bash
# 单个关键词
python extractor.py contents.csv --keywords "一尺花园"

# 多个关键词
python extractor.py contents.csv --keywords "咖啡" "自习" "办公"

# 指定搜索字段和数量
python extractor.py contents.csv --keywords "宝山" --fields title desc --top 50
```

### 2. 正则表达式匹配

```bash
# 提取价格
python extractor.py contents.csv --pattern "(\d+)元.*天"

# 提取电话
python extractor.py contents.csv --pattern "1[3-9]\d{9}"

# 提取日期
python extractor.py contents.csv --pattern "\d{4}[-/年]\d{1,2}[-/月]\d{1,2}"
```

### 3. 价格提取

```bash
# 自动识别价格
python extractor.py contents.csv --extract-prices

# 支持的格式：
# - 30元/天
# - 免费
# - 30次卡
# - 200月卡
```

### 4. 地理位置提取

```bash
# 统计地点分布
python extractor.py contents.csv --extract-locations --top 20

# 输出示例：
# 宝山区: 21次
# 淞沪铁路: 6次
# 上海大学: 4次
```

### 5. 热门帖子

```bash
# TOP 20热门帖子
python extractor.py contents.csv --top-posts --top 20

# 过滤点赞数>1000
python extractor.py contents.csv --top-posts --min-likes 1000
```

### 6. 统计信息

```bash
python extractor.py contents.csv --statistics

# 输出：
# total_posts: 120
# total_likes: 38772
# avg_likes: 323.1
# max_likes: 3481
```

---

## 💡 实用示例

### 示例1：分析咖啡厅品牌

```bash
python extractor.py contents.csv --keywords "星巴克" "一尺花园" "Manner" "瑞幸" --save cafes.json
```

### 示例2：查找高性价比店铺

```bash
python extractor.py contents.csv --extract-prices --top 50 --save value_shops.csv
```

### 示例3：区域分析

```bash
# 提取宝山相关帖子
python extractor.py contents.csv --keywords "宝山" --top 50

# 提取地理位置
python extractor.py contents.csv --extract-locations --top 20
```

### 示例4：综合分析

```bash
# 运行所有示例
python examples.py

# 运行特定示例
python examples.py 1  # 示例1：咖啡厅品牌
python examples.py 2  # 示例2：价格提取
python examples.py 3  # 示例3：地理位置
```

---

## 🔧 高级用法

### 自定义提取逻辑

```python
from extractor import UniversalExtractor

extractor = UniversalExtractor('contents.csv')

# 自定义过滤函数
def my_filter(row):
    text = str(row.get('title', '')) + str(row.get('desc', ''))
    return '宝山' in text and row.get('liked_count', 0) > 100

# 自定义提取函数
def my_extractor(row):
    import re
    desc = str(row.get('desc', ''))

    # 提取地址
    address_match = re.search(r'地址[：:]\s*(.*?)(?:\n|$)', desc)
    address = address_match.group(1) if address_match else '未找到'

    return {
        'title': row.get('title', ''),
        'liked': row.get('liked_count', 0),
        'address': address[:50],
        'has_plug': '插座' in desc,
        'has_wifi': 'WiFi' in desc or 'wifi' in desc,
    }

# 执行提取
results = extractor.extract_custom(
    filter_func=my_filter,
    extract_func=my_extractor,
    top_n=20
)

# 打印和保存
extractor.print_results(results, title="自定义提取")
extractor.save_results(results, 'custom_results.json')
```

### 组合多个操作

```python
# 步骤1：提取关键词
results1 = extractor.extract_by_keywords(['宝山', '咖啡'], top_n=50)

# 步骤2：提取价格
results2 = extractor.extract_prices(top_n=100)

# 步骤3：提取地理位置
results3 = extractor.extract_locations(top_n=20)

# 综合报告
report = {
    'baoshan_cafes': len(results1),
    'price_info': len(results2),
    'locations': results3
}

extractor.save_results(report, 'combined_report.json')
```

---

## 📋 参数参考

### 命令行参数

| 参数 | 说明 | 示例 |
|-----|------|-----|
| `contents_file` | 帖子CSV文件路径（必需） | `contents.csv` |
| `comments_file` | 评论CSV文件路径（可选） | `comments.csv` |
| `--keywords` | 关键词列表 | `--keywords "咖啡" "自习"` |
| `--pattern` | 正则表达式 | `--pattern "(\d+)元"` |
| `--extract-prices` | 提取价格信息 | `--extract-prices` |
| `--extract-locations` | 提取地理位置 | `--extract-locations` |
| `--top-posts` | 提取热门帖子 | `--top-posts` |
| `--statistics` | 显示统计信息 | `--statistics` |
| `--top` | 返回前N条（默认20） | `--top 50` |
| `--min-likes` | 最小点赞数 | `--min-likes 100` |
| `--fields` | 搜索字段列表 | `--fields title desc` |
| `--sort-by` | 排序字段 | `--sort-by liked_count` |
| `--save` | 保存到文件 | `--save output.json` |
| `--format` | 输出格式（json/csv） | `--format csv` |

---

## 📁 输出格式

### JSON格式

```json
[
  {
    "title": "帖子标题",
    "desc": "帖子描述...",
    "liked": 1234,
    "collected": 567,
    "comment_count": 89,
    "note_id": "abc123"
  }
]
```

### CSV格式

可直接用Excel打开，包含所有字段。

---

## 🎓 使用场景

| 场景 | 推荐命令 |
|-----|---------|
| 找品牌店铺 | `--keywords "品牌名"` |
| 比价格 | `--extract-prices` |
| 选区域 | `--extract-locations` |
| 看热门 | `--top-posts` |
| 统计数据 | `--statistics` |

---

## 🔗 相关文档

- [详细使用指南](EXTRACTOR_GUIDE.md) - 完整API文档和更多示例
- [examples.py](examples.py) - 9个可运行的示例代码

---

## 💬 常见问题

### Q: 如何提取多个文件？

```bash
# 先合并CSV
type file1.csv file2.csv > combined.csv  # Windows
cat file1.csv file2.csv > combined.csv   # Linux/Mac

# 再提取
python extractor.py combined.csv --keywords "咖啡"
```

### Q: 结果太多怎么办？

```bash
# 限制返回数量
python extractor.py contents.csv --keywords "咖啡" --top 10

# 或设置最小点赞数
python extractor.py contents.csv --top-posts --min-likes 500
```

### Q: 如何批量处理多个关键词？

```bash
# Windows批处理
for %w in ("星巴克" "一尺花园" "Manner") do python extractor.py contents.csv --keywords %w --save "%w.json"

# Linux/Mac shell
for keyword in "星巴克" "一尺花园" "Manner"; do
    python extractor.py contents.csv --keywords "$keyword" --save "${keyword}.json"
done
```

---

## 🚧 已知限制

1. **CSV格式要求**: 必须包含 `title` 和 `desc` 字段
2. **编码**: 默认使用UTF-8，如遇乱码请指定编码
3. **性能**: 大文件（>10MB）可能需要较长加载时间

---

## 🔄 更新日志

### v1.0.0 (2026-01-20)
- ✅ 初始版本发布
- ✅ 支持6种核心提取模式
- ✅ 命令行和Python API双接口
- ✅ JSON和CSV导出
- ✅ 9个实用示例

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**💡 提示**: 查看 [examples.py](examples.py) 快速上手，或阅读 [EXTRACTOR_GUIDE.md](EXTRACTOR_GUIDE.md) 了解详细用法！
