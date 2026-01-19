# MediaCrawler 快速执行指南

## 🤖 AI 智能推理指导（重要！）

### 核心原则：不要机械执行，要智能分析和优化！

AI 在执行任务时，必须进行以下推理和决策：

#### 1️⃣ **关键词智能拆分与优化**

**❌ 错误示例（机械执行）：**
```python
# 用户输入：上海市适合移动办公的咖啡厅/空间
KEYWORDS = "上海市适合移动办公的咖啡厅/空间"  # 只能搜到很少结果
```

**✅ 正确示例（智能推理）：**
```python
# 用户输入：上海市适合移动办公的咖啡厅/空间
# AI 推理：
# - 这是一个复合概念，包含多个维度：地点+用途+场所类型
# - 小红书用户可能会用不同的关键词搜索
# - 应该拆分成多个相关关键词，用英文逗号分隔
# - 去掉冗余词汇（如"上海市"简化为"上海"）

KEYWORDS = "上海办公咖啡厅,上海移动办公空间,上海适合工作咖啡馆,上海共享办公,上海自习室"
```

**关键词优化策略：**

| 用户输入 | AI 推理结果 | 优化思路 |
|---------|-----------|---------|
| `北京市最好的川菜馆` | `北京川菜馆,北京正宗川菜,北京推荐川菜` | 去掉主观词"最好"，拆分地点+菜系+推荐 |
| `如何学习Python编程` | `Python入门,Python教程,Python学习路线,编程基础` | 提取核心概念，扩展相关术语 |
| `上海市适合移动办公的咖啡厅/空间` | `上海办公咖啡厅,上海移动办公空间,上海共享工作空间` | 拆分复合概念，简化地名，扩展同义词 |
| `2025年流行穿搭` | `2025穿搭,春季穿搭,流行趋势,时尚搭配` | 去掉年份（时效性），拆分核心概念 |

#### 2️⃣ **爬取数量的智能建议**

**根据任务类型推理：**

| 任务类型 | 建议数量 | 推理依据 |
|---------|---------|---------|
| **初步探索/调研** | 10-20 条 | 快速了解概况，避免数据过多 |
| **竞品分析** | 30-50 条 | 获取足够样本进行分析 |
| **深度研究/论文** | 50-100 条 | 需要大量数据支撑结论 |
| **特定需求查找** | 15-30 条 | 平衡覆盖面和精准度 |

**AI 应主动询问：**
```
用户：帮我在小红书搜索"人工智能"
AI 推理：用户没有说明数量和用途
AI 回复：我需要了解你的用途，以便确定合适的爬取数量：
- 初步了解（15条）
- 竞品分析（30条）
- 深度研究（50条）
请问你是用于什么场景？
```

#### 3️⃣ **数据保存格式的智能推荐**

**根据用户需求推理：**

| 用户需求 | 推荐格式 | 推理依据 |
|---------|---------|---------|
| "我要做数据分析" | Excel 或 SQLite | Excel便于查看，SQLite便于程序处理 |
| "我要用Python处理数据" | JSON 或 CSV | 便于程序读取 |
| "我要分享给非技术人员" | Excel | 直观易读，专业格式 |
| "我要长期存储大量数据" | SQLite/MySQL/PostgreSQL | 数据库支持索引、去重、查询 |
| "我只是快速看看结果" | JSON | 默认格式，简单快捷 |

**AI 应主动推荐：**
```
用户：帮我在小红书搜索"美食教程"
AI 推理：用户没指定格式，默认用JSON，但Excel可能更合适
AI 回复：我建议保存为 Excel 格式，便于你直接打开查看和分析。
如果需要用Python处理，我可以改为 JSON 或 CSV。你希望哪种格式？
```

#### 4️⃣ **评论爬取的智能决策**

**是否爬评论的推理：**

| 用户需求 | 是否爬评论 | 推理依据 |
|---------|-----------|---------|
| "我要分析用户反馈" | ✅ 必须 | 评论包含用户真实反馈 |
| "我要了解热门话题" | ✅ 必须 | 评论反映用户关注点 |
| "我只是收集标题和图片" | ❌ 不需要 | 加快速度，减少数据量 |
| "我要做竞品分析" | ✅ 推荐 | 了解竞品内容的用户反响 |

**AI 应主动询问：**
```
用户：帮我在小红书搜索"美食教程"
AI 推理：默认开启评论爬取，但会慢一些
AI 回复：是否需要爬取评论？
- 需要（了解用户反馈和互动，但速度较慢）
- 不需要（只爬取帖子内容，速度快）
```

#### 5️⃣ **平台选择的智能建议**

**根据内容类型推理：**

| 内容类型 | 推荐平台 | 推理依据 |
|---------|---------|---------|
| "生活方式/美食/穿搭" | 小红书（xhs） | 小红书用户群体匹配 |
| "短视频/音乐/舞蹈" | 抖音（dy） | 抖音是短视频平台 |
| "教程/知识分享/长视频" | B站（bili） | B站用户喜欢学习内容 |
| "热点新闻/话题讨论" | 微博（wb） | 微博是社交讨论平台 |
| "问答/专业讨论" | 知乎（zhihu） | 知乎是问答社区 |

**AI 应主动确认：**
```
用户：帮我在搜索"人工智能教程"
AI 推理：教程类内容，B站和小红书都有，需要确认
AI 回复：教程类内容在以下平台比较丰富：
- B站（bili）：长视频教程，系统性学习
- 小红书（xhs）：图文笔记，快速入门
你希望搜索哪个平台？
```

#### 6️⃣ **执行前的预检查推理**

**AI 在修改配置前应该思考：**

```python
# ✅ AI 检查清单
检查项 1：用户输入的关键词是否需要优化？
检查项 2：爬取数量是否合理？（默认15条是否太少/太多）
检查项 3：保存格式是否适合用户需求？（默认JSON vs Excel）
检查项 4：是否需要爬评论？（默认True vs False）
检查项 5：平台选择是否正确？（用户没指定时需要询问）
检查项 6：如果使用Excel，是否已安装openpyxl？
检查项 7：如果使用抖音/知乎，是否已安装Node.js？
检查项 8：如果使用数据库，是否已初始化？
```

**AI 应主动提示：**
```
用户：帮我在抖音搜索"编程教学"
AI 推理：抖音需要Node.js，需要确认环境
AI 回复：⚠️ 提示：抖音平台需要安装 Node.js >= v16.0.0
你的环境是否已安装？如果没有安装，我可以：
1. 帮你切换到其他平台（如小红书、B站）
2. 指导你安装 Node.js 后再执行
请选择：
```

---

## 🎯 用户只需提供的参数

### 必填参数（3个）
1. **平台** (`PLATFORM`)
   - 可选值：`xhs`（小红书）| `dy`（抖音）| `bili`（B站）| `ks`（快手）| `wb`（微博）| `tieba`（贴吧）| `zhihu`（知乎）
   - 示例：`xhs`

2. **关键词** (`KEYWORDS`)
   - 多个关键词用英文逗号分隔
   - 示例：`编程副业,Python学习`

3. **爬取类型** (`CRAWLER_TYPE`)
   - `search`：关键词搜索
   - `detail`：指定帖子详情
   - `creator`：创作者主页
   - 示例：`search`

### 可选参数（常用）
4. **爬取数量** (`CRAWLER_MAX_NOTES_COUNT`)
   - 默认：15
   - 示例：`20`

5. **是否爬评论** (`ENABLE_GET_COMMENTS`)
   - 默认：`True`
   - 示例：`True` 或 `False`

6. **保存格式** (`SAVE_DATA_OPTION`)
   - 可选值：`json` | `csv` | `db` | `sqlite` | `excel` | `postgres`
   - 默认：`json`
   - 示例：`json`

## 🚀 执行步骤

### 1. 修改配置文件
编辑 `config/base_config.py`，修改以下参数：

```python
# 第21行 - 平台
PLATFORM = "xhs"  # 用户指定

# 第22行 - 关键词
KEYWORDS = "编程副业"  # 用户指定

# 第26行 - 爬取类型
CRAWLER_TYPE = "search"  # 用户指定

# 第83行 - 爬取数量（可选）
CRAWLER_MAX_NOTES_COUNT = 15  # 用户指定，默认15

# 第92行 - 是否爬评论（可选）
ENABLE_GET_COMMENTS = True  # 用户指定，默认True

# 第74行 - 保存格式（可选）
SAVE_DATA_OPTION = "json"  # 用户指定，默认json
```

### 2. 运行爬虫
```bash
uv run python main.py
```

### 3. 查看结果
数据保存在：`data/xhs/json/`（xhs会替换为对应平台名）

## 📋 完整参数参考（config/base_config.py）

| 行号 | 参数名 | 说明 | 默认值 | 常用值 |
|-----|-------|------|--------|--------|
| 21  | PLATFORM | 平台选择 | xhs | xhs/dy/bili/ks/wb/tieba/zhihu |
| 22  | KEYWORDS | 搜索关键词 | 编程副业,编程兼职 | 任意关键词，逗号分隔 |
| 23  | LOGIN_TYPE | 登录方式 | qrcode | qrcode/phone/cookie |
| 26  | CRAWLER_TYPE | 爬取类型 | search | search/detail/creator |
| 41  | HEADLESS | 是否无头浏览器 | False | True/False |
| 50  | ENABLE_CDP_MODE | CDP模式 | True | True/False |
| 74  | SAVE_DATA_OPTION | 保存格式 | json | json/csv/db/sqlite/excel/postgres |
| 83  | CRAWLER_MAX_NOTES_COUNT | 爬取数量 | 15 | 1-1000 |
| 86  | MAX_CONCURRENCY_NUM | 并发数 | 1 | 1-5 |
| 92  | ENABLE_GET_COMMENTS | 是否爬评论 | True | True/False |
| 95  | CRAWLER_MAX_COMMENTS_COUNT_SINGLENOTES | 单条评论数 | 10 | 1-100 |

## ⚠️ 注意事项

1. **登录**：首次运行需要扫码登录（会自动打开浏览器）
2. **CDP模式**：默认开启，使用你已有的Chrome浏览器，反检测能力强
3. **数据位置**：`data/{平台}/json/` 或 `data/{平台}/csv/`
4. **请求间隔**：程序自动控制，避免被封（每条间隔2秒）

## 🎯 典型使用场景

### 场景1：搜索小红书"美食教程"前20条
```python
PLATFORM = "xhs"
KEYWORDS = "美食教程"
CRAWLER_TYPE = "search"
CRAWLER_MAX_NOTES_COUNT = 20
ENABLE_GET_COMMENTS = True
```

### 场景2：搜索抖音"编程教学"前50条，保存为CSV
```python
PLATFORM = "dy"
KEYWORDS = "编程教学"
CRAWLER_TYPE = "search"
CRAWLER_MAX_NOTES_COUNT = 50
SAVE_DATA_OPTION = "csv"
```

### 场景3：爬取B站指定视频BV号详情
```python
PLATFORM = "bili"
CRAWLER_TYPE = "detail"
# 需要额外修改 config/bilibili_config.py 中的指定ID列表
```

## 🔧 故障排查

- **扫码失败**：设置 `HEADLESS = False`，手动处理验证码
- **登录过期**：删除 `browser_data/` 目录重新登录
- **爬取太慢**：可以适当增加 `MAX_CONCURRENCY_NUM`（但不要超过5）

---

## 📚 Claude 执行参考文件索引

### 核心配置文件
- [base_config.py](config/base_config.py) - 主配置文件（含所有基础参数）
- [main.py](main.py) - 程序入口文件（用于排查启动问题）

### 各平台专用配置
- [xhs_config.py](config/xhs_config.py) - 小红书专用配置
- [dy_config.py](config/dy_config.py) - 抖音专用配置
- [bili_config.py](config/bilibili_config.py) - B站专用配置
- [ks_config.py](config/ks_config.py) - 快手专用配置
- [wb_config.py](config/weibo_config.py) - 微博专用配置
- [tieba_config.py](config/tieba_config.py) - 贴吧专用配置
- [zhihu_config.py](config/zhihu_config.py) - 知乎专用配置

### 数据库配置
- [db_config.py](config/db_config.py) - 数据库连接配置（使用db/postgres时需要）

### 常见问题排查路径
1. **配置错误** → 检查 [base_config.py:21-127](config/base_config.py#L21-L127)
2. **启动失败** → 检查 [main.py:100-117](main.py#L100-L117)
3. **平台特定问题** → 检查对应平台配置文件
4. **数据库问题** → 检查 [db_config.py](config/db_config.py)

### 执行前检查清单
- ✅ 确认 `PLATFORM` 参数正确（xhs/dy/bili/ks/wb/tieba/zhihu）
- ✅ 确认 `KEYWORDS` 不为空（多个关键词用英文逗号分隔）
- ✅ 确认 `CRAWLER_TYPE` 正确（search/detail/creator）
- ✅ 如使用数据库，确认 `db_config.py` 配置正确
- ✅ 首次运行需准备好扫码登录（手机）

### 数据保存位置
- JSON格式：`data/{平台}/json/`
- CSV格式：`data/{平台}/csv/`
- Excel格式：`data/{平台}/excel/`（文件名：`{平台}_{类型}_{时间戳}.xlsx`）
- 数据库：需查看 `db_config.py` 中的配置

---

## 📖 关键文档索引

### 必读文档（AI执行前必看）
- [excel_export_guide.md](docs/excel_export_guide.md) - **Excel导出完整指南**（含依赖安装、文件结构、故障排查）
- [data_storage_guide.md](docs/data_storage_guide.md) - **数据存储完整指南**（含数据库初始化命令）
- [常见问题.md](docs/常见问题.md) - **常见错误和解决方案**
- [CDP模式使用指南.md](docs/CDP模式使用指南.md) - **反检测爬虫模式详解**

### 其他参考文档
- [项目架构文档.md](docs/项目架构文档.md) - 系统架构和数据流向（含Mermaid图表）
- [词云图使用配置.md](docs/词云图使用配置.md) - 词云功能配置
- [代理使用.md](docs/代理使用.md) - IP代理配置
- [手机号登录说明.md](docs/手机号登录说明.md) - 手机号登录方式

---

## ⚠️ 执行前必读关键信息

### 1️⃣ **Excel导出特殊要求**
```bash
# 需要安装 openpyxl 依赖
uv sync
# 或
pip install openpyxl
```

### 2️⃣ **数据库初始化（首次使用必须）**
```bash
# SQLite（推荐个人用户）
uv run main.py --init_db sqlite

# MySQL
uv run main.py --init_db mysql

# PostgreSQL
uv run main.py --init_db postgres
```

### 3️⃣ **抖音/知乎特殊要求**
- 必须安装 **Node.js** >= v16.0.0
- 否则会报错：`execjs._exceptions.ProgramError: SyntaxError`

### 4️⃣ **登录问题排查**
- **滑块验证失败**：删除 `browser_data/` 目录，设置 `HEADLESS = False`
- **更换账号**：删除 `browser_data/` 目录
- **登录过期**：删除 `browser_data/` 目录重新登录

### 5️⃣ **词云图功能**
```python
# config/base_config.py
ENABLE_GET_WORDCLOUD = True  # 开启词云
ENABLE_GET_COMMENTS = True  # 必须同时开启评论爬取
```

### 6️⃣ **CDP模式说明**
- 默认已开启（`ENABLE_CDP_MODE = True`）
- 使用你的真实Chrome浏览器，反检测能力强
- 如遇到问题，可设置为 `False` 使用标准Playwright模式

---

## 🚨 常见错误速查表

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `openpyxl not installed` | Excel导出缺少依赖 | `uv sync` 或 `pip install openpyxl` |
| `SyntaxError: 缺少 ';'` | 缺少Node.js环境 | 安装Node.js >= v16 |
| `Timeout 30000ms exceeded` | 网络超时（可能是梯子问题） | 检查VPN连接 |
| `滑块验证一直失败` | 被检测为自动化 | 删除`browser_data/`，设置`HEADLESS=False` |
| 数据库初始化失败 | 未初始化数据库 | 运行 `--init_db` 命令 |

---

## 💡 格式对比

### 推荐场景
- **个人使用、数据分析** → Excel
- **大数据量、长期存储** → SQLite/MySQL/PostgreSQL
- **程序处理、自动化** → JSON/CSV
