# MediaCrawler Python 环境配置指南

> 本文档用于在新电脑上完整复刻当前项目的 Python 环境

**⚠️ 重要提示：本文档中的路径（如 `C:\Users\danie\...`、`MediaCrawler_temp`）仅为示例，实际路径会因用户名、操作系统、项目文件夹名称不同而不同。请使用相对路径或 `uv run` 命令，不要照抄路径！**

---

## 📋 环境信息总览

### 当前环境配置

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **Python 版本** | 3.11.14 | 由 uv 自动管理 |
| **包管理器** | uv 0.9.26 | 现代化 Python 包管理工具 |
| **虚拟环境** | .venv | 项目独立虚拟环境（位于项目根目录下） |
| **依赖配置文件** | pyproject.toml（主要） | 现代标准 |
| **辅助配置文件** | requirements.txt | 传统兼容 |
| **项目根目录** | `你的项目文件夹` | ⚠️ **路径会因用户名、项目名称不同而不同** |

---

## 🚀 快速复刻步骤

### 方法1：使用 uv（推荐）⚡

这是最快、最可靠的方式，完全复刻当前环境。

#### 步骤 1：安装 Node.js（必需）

**⚠️ 重要**：项目需要 Node.js（用于抖音、知乎平台）

**下载地址**：https://nodejs.org/en/download/
**版本要求**：>= 16.0.0

**验证安装**：
```bash
node --version
# 应该显示：v16.0.0 或更高版本
```

#### 步骤 2：安装 uv

**Windows（PowerShell）：**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux：**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 步骤 3：进入项目目录
```bash
# ⚠️ 路径示例（不要照抄）：
# Windows: cd C:\Users\你的用户名\你的项目文件夹
# macOS/Linux: cd ~/你的项目文件夹

# 使用 cd 进入你的项目文件夹即可
```

#### 步骤 4：创建 .python-version 文件
```bash
echo "3.11" > .python-version
```

**⚠️ 重要**：这个文件指定项目使用 Python 3.11，uv 会自动下载对应版本。

#### 步骤 5：同步依赖
```bash
uv sync
```

这会自动完成：
- 下载并安装 Python 3.11.14
- 创建虚拟环境 `.venv`
- 安装所有依赖（按照 `pyproject.toml`）

#### 步骤 6：安装 Playwright 浏览器驱动
```bash
uv run playwright install
```

#### 步骤 7：验证安装
```bash
# 验证 Python 版本
uv run python --version
# 应该显示：Python 3.11.14

# 验证 Node.js 版本
node --version
# 应该显示：v16.0.0 或更高版本

# 验证关键依赖
uv run python -c "import playwright; import PIL; import cv2; print('依赖安装成功')"
```

---

### 方法2：使用传统 pip（兼容方案）

如果不想使用 uv，可以用传统方式。

#### 步骤 1：安装 Node.js（必需）

**⚠️ 重要**：项目需要 Node.js（用于抖音、知乎平台）

**下载地址**：https://nodejs.org/en/download/
**版本要求**：>= 16.0.0

**验证安装**：
```bash
node --version
```

#### 步骤 2：安装 Python 3.11

1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载 Python 3.11.x 安装包
3. 安装时勾选 **"Add Python to PATH"**

#### 步骤 3：创建虚拟环境
```bash
python -m venv .venv
```

#### 步骤 4：激活虚拟环境

**Windows：**
```bash
.venv\Scripts\activate
```

**macOS/Linux：**
```bash
source .venv/bin/activate
```

#### 步骤 5：安装依赖
```bash
pip install -r requirements.txt
```

**⚠️ 注意**：requirements.txt 中 Pillow 版本是 12.1.0，与 pyproject.toml 的 9.5.0 不一致。

#### 步骤 6：安装 Playwright 浏览器（必需）
```bash
playwright install chromium
```

---

## 📦 依赖配置文件说明

### pyproject.toml（主要配置）

**位置**：项目根目录

**关键配置**：
```toml
[project]
name = "mediacrawler"
requires-python = ">=3.11"
dependencies = [
    "playwright==1.45.0",
    "Pillow==9.5.0",          # ⚠️ 与 requirements.txt 不一致
    "opencv-python>=4.11.0.86",
    "pandas==2.2.3",
    "openpyxl>=3.1.2",
    # ... 更多依赖
]

[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

**特点**：
- ✅ 现代标准
- ✅ uv 专用
- ✅ 包含项目元数据
- ✅ 配置了清华镜像源（国内加速）

### requirements.txt（辅助配置）

**位置**：项目根目录

**关键依赖**：
```
httpx==0.28.1
Pillow==12.1.0          # ⚠️ 与 pyproject.toml 不一致
playwright==1.45.0
opencv-python
# ... 更多依赖
```

**特点**：
- 传统格式
- pip 通用
- 版本冲突需要修复

---

## ⚠️ 已知问题与解决方案

### 问题 1：Pillow 版本冲突

**现象**：
- `pyproject.toml` 指定 `Pillow==9.5.0`
- `requirements.txt` 指定 `Pillow==12.1.0`

**影响**：
- 使用不同安装方式会得到不同版本
- 可能导致兼容性问题

**解决方案（推荐）**：

统一为 **Pillow 9.5.0**（当前实际使用版本）：

1. 编辑 `requirements.txt` 第2行：
```diff
- Pillow==12.1.0
+ Pillow==9.5.0
```

2. 重新安装依赖：
```bash
uv sync
```

---

## 🔧 验证环境配置

运行以下命令验证所有关键依赖：

```bash
uv run python -c "
import sys
print(f'Python 版本: {sys.version}')

import playwright
print(f'✅ Playwright: {playwright.__version__}')

import PIL
print(f'✅ Pillow: {PIL.__version__}')

import cv2
print(f'✅ OpenCV: {cv2.__version__}')

import pandas
print(f'✅ Pandas: {pandas.__version__}')

import openpyxl
print(f'✅ OpenPyXL: {openpyxl.__version__}')

print('\\n🎉 所有关键依赖安装成功！')
"
```

**预期输出**：
```
Python 版本: 3.11.14
✅ Playwright: 1.45.0
✅ Pillow: 9.5.0
✅ OpenCV: 4.11.0
✅ Pandas: 2.2.3
✅ OpenPyXL: 3.1.2

🎉 所有关键依赖安装成功！
```

---

## 📂 虚拟环境位置

**虚拟环境位置（相对路径，所有电脑通用）：**
```
项目根目录/.venv/
```

**关键点**：
- ✅ `.venv/` 位于项目根目录下（相对路径，通用）
- ❌ Python 绝对路径会因用户名、操作系统、项目名称不同而不同
- ✅ 使用 `uv run` 会自动找到正确的 Python，无需手动指定路径

---

## 🎯 常用命令

### 使用 uv 运行项目

```bash
# 运行主程序
uv run python main.py

# 激活虚拟环境（可选）
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 查看已安装的包
uv pip list

# 添加新依赖
uv add 包名

# 更新依赖
uv sync --upgrade
```

### 使用传统方式

```bash
# 运行主程序
python main.py

# 激活虚拟环境（必需）
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# 查看已安装的包
pip list

# 安装新包
pip install 包名
```

---

## 🔍 环境诊断清单

在新电脑上配置完成后，检查以下项目：

- [ ] **Python 版本是 3.11.14**（运行 `uv run python --version` 检查）
- [ ] **Node.js 已安装**（运行 `node --version`，版本 >= 16.0.0）
- [ ] 虚拟环境 `.venv` 存在于项目根目录下
- [ ] 可以运行 `uv run python --version`（无需手动指定 Python 路径）
- [ ] Playwright 已安装浏览器（`uv run playwright install`）
- [ ] 所有关键依赖可以导入（见验证脚本）
- [ ] 可以运行主程序 `uv run python main.py`（不报 ImportError）

**⚠️ 重要提示**：
- ❌ **不要**在命令中硬编码绝对路径（如 `C:\Users\danie\...`）
- ✅ **应该**使用相对路径或 `uv run`（自动处理路径）
- ✅ **应该**在项目根目录下运行所有命令

---

## 📚 相关文档

- [uv 官方文档](https://github.com/astral-sh/uv)
- [MediaCrawler 项目README](../README.md)
- [Excel导出指南](./excel_export_guide.md)
- [常见问题](./常见问题.md)

---

## 💡 故障排查

### 问题：uv 命令找不到
**解决**：重新安装 uv 并重启终端

### 问题：Node.js 未安装或版本过低
**解决**：
- 访问 https://nodejs.org/en/download/
- 下载并安装 Node.js >= 16.0.0
- 验证：`node --version`

### 问题：Python 3.11 下载失败
**解决**：检查网络，或手动安装 Python 3.11，然后运行 `uv sync`

### 问题：依赖安装超时
**解决**：
```bash
# 使用国内镜像
uv sync --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题：找不到 Python 路径
**解决**：
```bash
# ❌ 错误：不要使用绝对路径
C:\Users\用户名\AppData\Roaming\uv\python\...\python.exe

# ✅ 正确：使用 uv run（自动处理路径）
uv run python --version

# ✅ 正确：激活虚拟环境后使用 python
.venv\Scripts\activate  # Windows
python --version
```

### 问题：Playwright 浏览器下载失败
**解决**：
```bash
# 设置国内镜像
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/
playwright install chromium
```

---

## 🎉 完成！

按照本指南配置后，你的新电脑应该与当前环境完全一致。

如有问题，请检查：
1. Python 版本是否正确（3.11.14）
2. 是否在项目根目录操作
3. 虚拟环境是否已激活
4. 依赖是否全部安装成功

**祝使用愉快！** 🚀
