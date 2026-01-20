# 通用提取工具 - 快速参考卡片

## 🚀 常用命令速查

| 需求 | 命令 |
|-----|------|
| 🔍 搜索关键词 | `python extractor.py data.csv --keywords "咖啡"` |
| 💰 提取价格 | `python extractor.py data.csv --extract-prices` |
| 📍 提取地点 | `python extractor.py data.csv --extract-locations` |
| 🔥 热门帖子 | `python extractor.py data.csv --top-posts` |
| 📊 统计信息 | `python extractor.py data.csv --statistics` |
| 💾 保存结果 | `添加 --save output.json 或 output.csv` |

---

## 📝 参数速查

| 参数 | 说明 | 默认值 |
|-----|------|-------|
| `--keywords` | 关键词列表 | - |
| `--top` | 返回前N条 | 20 |
| `--min-likes` | 最小点赞数 | 0 |
| `--fields` | 搜索字段 | title desc |
| `--sort-by` | 排序字段 | liked_count |
| `--save` | 保存文件 | - |
| `--format` | 输出格式 | 自动识别 |

---

## 🎯 典型使用场景

### 场景1: 找品牌店铺

```bash
python extractor.py data.csv --keywords "星巴克" "一尺花园" --save brands.json
```

### 场景2: 比价格选店

```bash
python extractor.py data.csv --extract-prices --top 50 --save prices.csv
```

### 场景3: 看热门推荐

```bash
python extractor.py data.csv --top-posts --min-likes 1000 --top 30
```

### 场景4: 区域分析

```bash
python extractor.py data.csv --keywords "宝山" --extract-locations --top 20
```

---

## 💻 Python API 速查

```python
from extractor import UniversalExtractor

# 初始化
extractor = UniversalExtractor('data.csv')

# 1. 关键词搜索
results = extractor.extract_by_keywords(['咖啡'], top_n=20)

# 2. 提取价格
prices = extractor.extract_prices(top_n=50)

# 3. 提取地点
locations = extractor.extract_locations(top_n=20)

# 4. 热门帖子
top_posts = extractor.extract_top_posts(top_n=20)

# 5. 打印结果
extractor.print_results(results, title="结果")

# 6. 保存结果
extractor.save_results(results, 'output.json', format='json')
```

---

## 🔥 常用正则表达式

| 需求 | 正则表达式 |
|-----|-----------|
| 价格（元/天） | `(\d+)元.*天` |
| 手机号 | `1[3-9]\d{9}` |
| 邮箱 | `[\w\.-]+@[\w\.-]+\.\w+` |
| 日期 | `\d{4}[-/年]\d{1,2}[-/月]\d{1,2}` |
| 营业时间 | `(\d+:\d+\s*[-至]\s*\d+:\d+)` |

---

## 📊 输出格式

### JSON格式
```json
[
  {
    "title": "标题",
    "liked": 1234,
    "desc": "描述..."
  }
]
```

### CSV格式
直接用Excel打开，包含所有字段

---

## 🎓 学习路径

1. **5分钟入门** → 运行 `examples.py`
2. **15分钟上手** → 阅读 `EXTRACTOR_GUIDE.md`
3. **30分钟精通** → 查看 `extractor.py` 源码

---

## 🔗 相关文件

- `extractor.py` - 核心工具
- `examples.py` - 9个示例
- `EXTRACTOR_GUIDE.md` - 详细指南
- `README_EXTRACTOR.md` - 完整说明

---

## 💡 小技巧

1. **组合使用**: 多个关键词用空格分隔
2. **限制结果**: 使用 `--top` 控制数量
3. **过滤质量**: 使用 `--min-likes` 筛选
4. **批量处理**: 写脚本循环调用
5. **保存格式**: `.json` 或 `.csv` 自动识别

---

**📞 遇到问题？**
- 查看 `EXTRACTOR_GUIDE.md` 常见问题章节
- 运行 `python extractor.py --help`
- 查看 `examples.py` 中的示例代码
