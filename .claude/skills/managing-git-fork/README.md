# Fork Workflow Manager - 使用说明

完整的 Fork 仓库管理工具，帮助安全地同步上游更新、检测和解决冲突。

## 📦 包含内容

### 1. SKILL.md
主技能文件，包含：
- 完整工作流步骤
- 冲突场景说明
- 快速命令参考

### 2. 参考资料 (references/)
- **conflict-resolution.md** - 详细的冲突解决指南
- **remote-setup.md** - Git 远程仓库配置
- **best-practices.md** - 最佳实践和工作流

### 3. 脚本工具 (scripts/)
- **check-upstream-conflicts.py** - 智能冲突检测
- **sync-fork.py** - 自动化同步流程

---

## 🚀 快速开始

### 方式 1: 使用 Claude Code Skill（推荐）

1. **打包 Skill**
   ```bash
   cd fork-workflow-manager
   python ../path/to/package_skill.py . ./dist
   ```

2. **安装 Skill**
   - 在 Claude Code 中: `Skills > Install Skill`
   - 选择生成的 `fork-workflow-manager.skill` 文件

3. **使用 Skill**
   - 直接对话: "帮我检测上游冲突"
   - "同步上游更新"
   - "解决合并冲突"

### 方式 2: 直接使用脚本

#### 检测上游冲突
```bash
python fork-workflow-manager/scripts/check-upstream-conflicts.py
```

**功能：**
- ✅ 获取上游最新更新
- ✅ 显示上游新提交
- ✅ 列出修改的文件
- ✅ 预检测合并冲突
- ✅ 生成详细报告

#### 自动化同步
```bash
python fork-workflow-manager/scripts/sync-fork.py
```

**功能：**
- ✅ 检查本地未提交修改
- ✅ 获取上游更新
- ✅ 预检测冲突
- ✅ 协助解决冲突
- ✅ 推送到你的 Fork

---

## 📖 使用场景

### 场景 1: 日常备份本地修改

```bash
# 1. 提交修改
git add .
git commit -m "我的改动"

# 2. 推送到 Fork
git push origin main
```

### 场景 2: 定期同步上游更新

```bash
# 1. 运行冲突检测
python fork-workflow-manager/scripts/check-upstream-conflicts.py

# 2. 查看报告后，决定是否合并

# 3. 如果无冲突，直接同步
git fetch upstream
git merge upstream/main
git push origin main

# 4. 如果有冲突，查看 conflict-resolution.md
```

### 场景 3: 自动化同步流程

```bash
# 一键同步（包含冲突处理）
python fork-workflow-manager/scripts/sync-fork.py
```

---

## 🔧 前置条件

### 1. Git 远程仓库配置

确保已配置：
```bash
git remote -v
```

应该显示：
```
origin    https://github.com/你的用户名/你的仓库.git
upstream  https://github.com/原作者/原仓库.git
```

如果没有 upstream，添加：
```bash
git remote add upstream https://github.com/原作者/原仓库.git
```

详见 [remote-setup.md](references/remote-setup.md)

### 2. Python 环境

脚本需要 Python 3.7+

---

## 📊 脚本输出示例

### check-upstream-conflicts.py 输出

```
🚀 开始智能冲突检测

🔍 正在获取上游更新...
✅ 上游更新已获取

📝 检查上游新提交...
发现 3 个新提交:
  • abc1234 feat: add new feature
  • def5678 fix: resolve bug
  • ghi9012 docs: update readme

📊 上游修改了 5 个文件:

配置:
  • config/base_config.py
  • config/app_config.py

代码:
  • core/main.py
  • utils/helpers.py

文档:
  • README.md

🔬 预检测合并冲突...
✅ 预检测: 未发现冲突

============================================================
📋 冲突检测报告
============================================================

📈 上游更新: 3 个提交
📁 修改文件: 5 个文件

✅ 本地无未提交修改

✅ 无冲突，可以安全合并

============================================================

📌 下一步操作:
  1. 运行: git merge upstream/main
  2. 运行: git push origin main
```

---

## 🛠️ 故障排查

### 问题 1: 脚本报编码错误

**Windows 用户：**
脚本已内置 UTF-8 编码处理，如果仍有问题：
```bash
# 设置终端编码
chcp 65001
```

### 问题 2: 找不到 upstream

```bash
# 添加 upstream
git remote add upstream https://github.com/原作者/原仓库.git
```

### 问题 3: 合并冲突

参考 [conflict-resolution.md](references/conflict-resolution.md) 的详细步骤。

---

## 💡 最佳实践

1. **定期同步**：每周或每月同步一次上游更新
2. **小步提交**：频繁提交小改动，而不是积累大量改动
3. **先检测后合并**：使用 check-upstream-conflicts.py 预检测
4. **备份分支**：重要操作前创建备份分支

详见 [best-practices.md](references/best-practices.md)

---

## 📝 工作流对比

### 传统方式 vs 使用此 Skill

| 操作 | 传统方式 | 使用 Skill |
|-----|---------|-----------|
| 检查上游更新 | 手动运行多条 Git 命令 | 一条脚本自动检测 |
| 预检冲突 | 需要实际合并才知道 | 预检测报告 |
| 解决冲突 | 查找文档，手动操作 | 详细的分步指导 |
| 推送到 Fork | 多条命令 | 一键自动化 |

---

## 🎯 快速命令参考

```bash
# 检测冲突
python fork-workflow-manager/scripts/check-upstream-conflicts.py

# 自动同步
python fork-workflow-manager/scripts/sync-fork.py

# 手动同步
git fetch upstream
git merge upstream/main
git push origin main

# 查看远程仓库
git remote -v

# 查看上游新提交
git log HEAD..upstream/main --oneline

# 预检冲突（不实际合并）
git merge --no-commit --no-ff upstream/main
git merge --abort  # 取消预检
```

---

## 📚 参考文档

- [SKILL.md](SKILL.md) - 主技能文件
- [conflict-resolution.md](references/conflict-resolution.md) - 冲突解决指南
- [remote-setup.md](references/remote-setup.md) - 远程仓库配置
- [best-practices.md](references/best-practices.md) - 最佳实践

---

## 🤝 贡献

这是一个通用工具，适用于任何 Fork 仓库的工作流管理。

如有改进建议，欢迎反馈！
