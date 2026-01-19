# 工作流最佳实践

管理 Fork 仓库的推荐策略和注意事项。

## 核心原则

### 1. 永不直接 push 到 upstream

```bash
# ❌ 错误
git push upstream main

# ✅ 正确
git push origin main  # 推送到你的 Fork
```

### 2. 定期同步上游

建议频率：
- **活跃项目**：每周 1-2 次
- **一般项目**：每月 1 次
- **低频项目**：每季度 1 次

### 3. 小步快跑

```bash
# ✅ 推荐：频繁提交小改动
git add .
git commit -m "小改动A"
git push origin main

# 修改代码
git add .
git commit -m "小改动B"
git push origin main

# ❌ 避免：积累大量改动才提交
# (修改了 20 个文件后才提交)
```

### 4. 同步前先备份

```bash
# 在重要操作前创建备份分支
git branch backup-$(date +%Y%m%d)

# 如果出问题，可以回退
git reset --hard backup-20250118
```

---

## 推荐工作流

### 日常开发流程

```bash
# 1. 开始工作前，先同步上游
git fetch upstream
git merge upstream/main
git push origin main

# 2. 创建功能分支（可选，用于实验性功能）
git checkout -b feature-my-experiment

# 3. 进行修改和提交
git add .
git commit -m "实现新功能"

# 4. 合并回主分支
git checkout main
git merge feature-my-experiment

# 5. 推送到 Fork
git push origin main

# 6. 删除实验分支（可选）
git branch -d feature-my-experiment
```

### 纯备份流程（无需上游同步）

```bash
# 只需推送到你的 Fork
git add .
git commit -m "我的改动"
git push origin main
```

### 上游更新流程

```bash
# 1. 获取上游更新
git fetch upstream

# 2. 查看改动（可选但推荐）
git log HEAD..upstream/main --oneline
git diff HEAD upstream/main --stat

# 3. 如果改动很大，预检冲突
git merge --no-commit --no-ff upstream/main
git status  # 查看冲突

# 如果决定暂不合并
# git merge --abort

# 4. 正式合并
git merge upstream/main

# 5. 如果有冲突，解决后：
# git add .
# git commit -m "合并上游更新，解决冲突"

# 6. 推送到 Fork
git push origin main
```

---

## 分支策略

### 策略 1: 单分支（推荐新手）

```
main（所有改动都在主分支）
```

- **优点**：简单直接
- **缺点**：实验性改动和稳定代码混在一起
- **适用**：个人项目、简单修改

### 策略 2: 功能分支（推荐）

```
main（稳定代码）
├── feature-experiment-1（实验性功能）
├── feature-experiment-2（另一个实验）
└── backup-20250118（备份分支）
```

- **优点**：清晰隔离，易于回退
- **缺点**：需要管理多个分支
- **适用**：频繁开发、实验性项目

### 策略 3: 开发分支

```
main（完全同步 upstream）
dev（你的所有改动）
└── feature-*（具体功能）
```

- **优点**：main 始终与 upstream 同步
- **缺点**：需要定期合并 dev 到 main
- **适用**：大量定制开发

---

## 冲突预防

### 1. 避免修改核心文件

如果可能，通过配置文件而不是修改代码来定制功能。

**示例：**
```python
# ✅ 推荐：添加配置项
# config/my_config.py
MY_CUSTOM_SETTING = "value"

# ❌ 避免：直接修改核心逻辑
# core/main.py
def main():
    # 大量自定义修改
```

### 2. 分离自定义代码

```bash
# 创建自己的配置文件
touch config/custom_config.py

# 在 .gitignore 中忽略敏感信息
echo "config/secrets.py" >> .gitignore
```

### 3. 定期同步

不要让本地改动落后 upstream 太多，否则冲突会更难解决。

---

## 提交信息规范

### 格式

```
<类型>: <简短描述>

<详细描述（可选）>
```

### 类型示例

```bash
# 功能添加
git commit -m "feat: 添加 Excel 导出功能"

# Bug 修复
git commit -m "fix: 修复登录超时问题"

# 配置修改
git commit -m "config: 更新关键词配置"

# 文档更新
git commit -m "docs: 添加使用说明"

# 重构
git commit -m "refactor: 优化数据结构"

# 性能优化
git commit -m "perf: 减少内存占用"
```

### 详细描述

```bash
git commit -m "feat: 添加 Excel 导出功能

- 支持 .xlsx 格式
- 自动调整列宽
- 包含数据验证"
```

---

## 安全实践

### 1. 敏感信息处理

```bash
# .gitignore
config/secrets.yml
.env
*.key
credentials.json
```

### 2. 推送前检查

```bash
# 检查将要推送的内容
git log origin/main..HEAD --oneline

# 检查敏感信息
git diff --cached | grep -i "password\|token\|secret"
```

### 3. 使用分支保护

在 GitHub 设置中：
- 保护 main 分支（需要 PR 才能合并）
- 要求状态检查通过
- 这样可以防止意外推送

---

## 故障恢复

### 场景 1: 误推送到 origin

```bash
# 回退到上一个版本
git reset --hard HEAD~1
git push origin main --force
```

⚠️ **注意**：force push 很危险，确保你了解后果！

### 场景 2: 合并后发现问题

```bash
# 查看合并历史
git log --graph --oneline

# 回退到合并前
git reset --hard HEAD~1  # 如果是合并提交
# 或
git reset --hard ORIG_HEAD  # Git 自动备份
```

### 场景 3: 本地修改丢失

```bash
# 查看所有操作历史
git reflog

# 恢复到某个状态
git reset --hard <commit-hash>
```

---

## 自动化建议

### 创建便捷别名

```bash
# ~/.gitconfig 或项目 .git/config
[alias]
    # 快速查看上游更新
    up = "!f() { git fetch upstream && git log HEAD..upstream/main --oneline; }; f"

    # 快速同步上游
    sync = "!f() { git fetch upstream && git merge upstream/main; }; f"

    # 推送到 origin
    pub = push origin main
```

使用：
```bash
git up      # 查看上游更新
git sync    # 同步上游
git pub     # 推送到 Fork
```

### 创建快捷脚本

`scripts/sync-upstream.sh`：
```bash
#!/bin/bash
echo "🔍 检查上游更新..."
git fetch upstream

echo "📝 上游新提交："
git log HEAD..upstream/main --oneline

echo "❓ 是否合并？(y/n)"
read answer

if [ "$answer" = "y" ]; then
    git merge upstream/main
    echo "✅ 合并完成，推送到 origin..."
    git push origin main
fi
```

---

## 性能优化

### 1. 浅克隆（如果不需要历史）

```bash
git clone --depth 1 https://github.com/用户名/仓库.git
```

### 2. 只克隆特定分支

```bash
git clone --branch main --single-branch https://github.com/用户名/仓库.git
```

### 3. 定期清理

```bash
# 清理不可达的对象
git gc

# 清理远程已删除的分支引用
git remote prune origin
```

---

## 总结检查清单

**日常开发：**
- [ ] 经常提交小改动
- [ ] 推送到 origin（不是 upstream）
- [ ] 使用功能分支进行实验

**定期维护：**
- [ ] 每周/月同步上游
- [ ] 查看上游改动
- [ ] 解决冲突

**安全：**
- [ ] .gitignore 包含敏感文件
- [ ] 推送前检查内容
- [ ] 重要操作前备份分支

**效率：**
- [ ] 配置 Git 别名
- [ ] 使用脚本自动化
- [ ] 定期清理仓库
