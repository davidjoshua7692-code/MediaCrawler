# 通用数据提取工具使用指南

## 📖 目录

- [快速开始](#快速开始)
- [核心功能](#核心功能)
- [使用示例](#使用示例)
- [预设模板](#预设模板)
- [API参考](#api参考)
- [常见问题](#常见问题)

---

## 🚀 快速开始

### 安装依赖

```bash
cd d:\MediaCrawler-main\.claude\skills\analyzing-social-media-data
pip install pandas
```

### 基础用法

```bash
# 提取包含关键词的帖子
python extractor.py contents.csv --keywords "咖啡厅"

# 提取价格信息
python extractor.py contents.csv --extract-prices

# 提取热门帖子
python extractor.py contents.csv --top-posts --top 10
```

---

## 🎯 核心功能

### 1. 关键词搜索 (`--keywords`)

根据一个或多个关键词提取相关帖子。

**示例：**
```bash
# 搜索单个关键词
python extractor.py contents.csv --keywords "一尺花园"

# 搜索多个关键词
python extractor.py contents.csv --keywords "咖啡" "自习" "办公"

# 指定搜索字段
python extractor.py contents.csv --keywords "宝山" --fields title desc

# 保存结果
python extractor.py contents.csv --keywords "自习" --save results.json
```

**参数说明：**
- `--keywords`: 关键词列表（空格分隔）
- `--fields`: 搜索的字段（默认: title desc）
- `--top`: 返回前N条结果（默认: 20）
- `--sort-by`: 排序字段（默认: liked_count）

---

### 2. 正则表达式匹配 (`--pattern`)

使用正则表达式提取特定模式的数据。

**示例：**
```bash
# 提取价格（XX元/天）
python extractor.py contents.csv --pattern "(\d+)元.*天"

# 提取电话号码
python extractor.py contents.csv --pattern "1[3-9]\d{9}"

# 提取邮箱
python extractor.py contents.csv --pattern "[\w\.-]+@[\w\.-]+\.\w+"

# 提取日期
python extractor.py contents.csv --pattern "\d{4}[-/年]\d{1,2}[-/月]\d{1,2}"
```

---

### 3. 价格提取 (`--extract-prices`)

自动识别并提取价格相关信息。

**示例：**
```bash
# 提取所有价格信息
python extractor.py contents.csv --extract-prices

# 返回前50条
python extractor.py contents.csv --extract-prices --top 50

# 保存为CSV
python extractor.py contents.csv --extract-prices --save prices.csv
```

**自动识别的价格格式：**
- `30元/天` → 提取为 "30 元/天"
- `免费` → 提取为 "免费"
- `30次卡` → 提取为 "30 次卡"
- `200月卡` → 提取为 "200 月卡"

---

### 4. 地理位置提取 (`--extract-locations`)

提取文本中提到的地理位置。

**示例：**
```bash
# 提取地理位置
python extractor.py contents.csv --extract-locations

# 返回TOP 15
python extractor.py contents.csv --extract-locations --top 15

# 保存结果
python extractor.py contents.csv --extract-locations --save locations.json
```

---

### 5. 热门帖子提取 (`--top-posts`)

提取点赞数最高的帖子。

**示例：**
```bash
# 提取TOP 20热门帖子
python extractor.py contents.csv --top-posts

# 过滤点赞数>100的帖子
python extractor.py contents.csv --top-posts --min-likes 100

# 提取TOP 50
python extractor.py contents.csv --top-posts --top 50
```

---

### 6. 统计信息 (`--statistics`)

显示数据集的整体统计信息。

**示例：**
```bash
python extractor.py contents.csv --statistics
```

**输出示例：**
```
================================================================================
📈 数据统计信息
================================================================================
total_posts: 120
total_likes: 38772
avg_likes: 323.1
max_likes: 3481
total_comments: 4260
avg_comments: 35.5
```

---

## 📚 使用示例

### 示例1：提取特定品牌的帖子

```bash
# 提取所有提到"一尺花园"的帖子
python extractor.py contents.csv --keywords "一尺花园" --top 30
```

### 示例2：查找30元以内的店铺

```bash
# 提取价格信息并筛选
python extractor.py contents.csv --extract-prices --top 50
```

### 示例3：分析某区域的热门地点

```bash
# 提取宝山区的地理位置分布
python extractor.py contents.csv --keywords "宝山" --extract-locations --top 20
```

### 示例4：找到高互动的办公场所帖子

```bash
# 提取"办公"相关的高赞帖子
python extractor.py contents.csv --keywords "办公" "工作" --top 20 --sort-by liked_count
```

### 示例5：组合多个关键词

```bash
# 搜索同时包含"安静"和"咖啡厅"的帖子
python extractor.py contents.csv --keywords "安静" "咖啡厅" --fields title desc
```

---

## 🎨 预设模板

### 模板1：咖啡厅分析

```bash
# 1. 提取所有咖啡厅品牌
python extractor.py contents.csv --keywords "星巴克" "一尺花园" "Manner" "瑞幸" --top 50 --save cafes.json

# 2. 提取价格信息
python extractor.py contents.csv --extract-prices --top 30 --save prices.json

# 3. 提取地理位置
python extractor.py contents.csv --extract-locations --top 15 --save locations.json

# 4. 提取热门帖子
python extractor.py contents.csv --keywords "咖啡" --top 20 --save top_posts.json
```

### 模板2：自习室分析

```bash
# 1. 提取自习室相关帖子
python extractor.py contents.csv --keywords "自习" "学习" "图书馆" --top 30

# 2. 提取价格信息
python extractor.py contents.csv --extract-prices --top 50

# 3. 提取24小时营业的场所
python extractor.py contents.csv --pattern "24小时" --top 20
```

### 模板3：旅游景点分析

```bash
# 1. 提取景点相关帖子
python extractor.py contents.csv --keywords "景点" "旅游" "打卡" --top 50

# 2. 提取地理位置
python extractor.py contents.csv --extract-locations --top 30

# 3. 提取热门帖子
python extractor.py contents.csv --top-posts --min-likes 500 --top 30
```

---

## 🔧 API参考

### Python API 使用

```python
from extractor import UniversalExtractor

# 初始化
extractor = UniversalExtractor(
    contents_file='data.csv',
    comments_file='comments.csv'  # 可选
)

# 1. 关键词搜索
results = extractor.extract_by_keywords(
    keywords=['咖啡', '自习'],
    search_fields=['title', 'desc'],
    top_n=20,
    sort_by='liked_count'
)

# 2. 正则匹配
results = extractor.extract_by_pattern(
    pattern=r'(\d+)元.*天',
    search_fields=['title', 'desc'],
    top_n=20
)

# 3. 提取价格
results = extractor.extract_prices(top_n=20)

# 4. 提取地理位置
locations = extractor.extract_locations(top_n=10)

# 5. 提取热门帖子
top_posts = extractor.extract_top_posts(top_n=20, min_likes=100)

# 6. 获取统计信息
stats = extractor.extract_statistics()

# 7. 自定义提取
def my_filter(row):
    return '咖啡' in str(row.get('title', ''))

def my_extractor(row):
    return {
        'title': row.get('title', ''),
        'liked': row.get('liked_count', 0),
        'custom_field': '自定义值'
    }

results = extractor.extract_custom(
    filter_func=my_filter,
    extract_func=my_extractor,
    top_n=20
)

# 8. 打印结果
extractor.print_results(results, title="我的提取结果")

# 9. 保存结果
extractor.save_results(results, 'output.json', format='json')
extractor.save_results(results, 'output.csv', format='csv')
```

---

## 💡 高级技巧

### 1. 链式操作

```bash
# 先提取关键词，再从结果中提取价格
python extractor.py contents.csv --keywords "自习" --save temp.json
python extractor.py temp.json --extract-prices
```

### 2. 组合多个过滤条件

```python
# Python脚本中组合条件
extractor = UniversalExtractor('contents.csv')

# 先提取关键词
results1 = extractor.extract_by_keywords(['咖啡', '安静'])

# 再从结果中过滤
filtered = [r for r in results1 if r['liked'] > 100]

# 保存
extractor.save_results(filtered, 'filtered_results.json')
```

### 3. 自定义价格模式

```python
# 添加自定义价格模式
custom_patterns = [
    (r'(\d+)美元', '美元'),
    (r'(\d+)港币', '港币'),
    (r'折扣.*?(\d+)折', r'\1折'),
]

results = extractor.extract_prices(
    price_patterns=custom_patterns,
    top_n=50
)
```

---

## ❓ 常见问题

### Q1: 如何提取多个CSV文件的数据？

```bash
# 方法1：合并CSV后再提取
# Windows
type file1.csv file2.csv > combined.csv

# Linux/Mac
cat file1.csv file2.csv > combined.csv

# 然后提取
python extractor.py combined.csv --keywords "咖啡"
```

### Q2: 如何处理中文编码问题？

```python
# 使用encoding参数
df = pd.read_csv('file.csv', encoding='utf-8-sig')
extractor = UniversalExtractor(df)
```

### Q3: 如何提高匹配精度？

```bash
# 使用更精确的关键词
python extractor.py contents.csv --keywords "宝山区咖啡厅"  # 更精确

# 或使用正则表达式
python extractor.py contents.csv --pattern "宝山.*?咖啡厅"
```

### Q4: 结果太多怎么办？

```bash
# 限制返回数量
python extractor.py contents.csv --keywords "咖啡" --top 10

# 或设置最小点赞数
python extractor.py contents.csv --top-posts --min-likes 500 --top 20
```

### Q5: 如何批量处理多个关键词？

```bash
# 创建批处理脚本
for keyword in "星巴克" "一尺花园" "Manner" "瑞幸"
do
    python extractor.py contents.csv --keywords "$keyword" --save "${keyword}.json"
done
```

---

## 📝 输出格式说明

### JSON格式

```json
[
  {
    "title": "帖子标题",
    "desc": "帖子描述...",
    "liked": 1234,
    "collected": 567,
    "comment_count": 89,
    "note_id": "abc123",
    "matched_keyword": "咖啡"
  }
]
```

### CSV格式

| title | desc | liked | collected | comment_count | note_id |
|-------|------|-------|-----------|---------------|---------|
| 帖子标题 | 描述... | 1234 | 567 | 89 | abc123 |

---

## 🔄 更新日志

### v1.0.0 (2026-01-20)
- ✅ 初始版本
- ✅ 支持关键词搜索
- ✅ 支持正则表达式匹配
- ✅ 支持价格提取
- ✅ 支持地理位置提取
- ✅ 支持热门帖子提取
- ✅ 支持统计信息
- ✅ 支持自定义提取函数
- ✅ 支持JSON/CSV导出

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

MIT License
