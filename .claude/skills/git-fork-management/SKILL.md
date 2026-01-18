---
name: git-fork-management
description: Comprehensive Git Fork repository management with intelligent upstream synchronization, conflict detection, and resolution guidance. Use when working with forked repositories, syncing upstream updates, handling merge conflicts, or managing git remotes (origin/upstream). Includes automated scripts for conflict analysis and step-by-step workflows for safe upstream merging.
---

# Git Fork Management

管理 Fork 仓库的完整工作流，包括智能同步上游更新、冲突检测和解决协助。

## 核心功能

### 1. 自动检测上游更新
检查 `upstream` 仓库是否有新提交，并显示改动摘要。

### 2. 智能冲突预检
在合并前预分析可能的冲突，标记高风险文件。

### 3. 冲突解决协助
提供分步指导，帮助用户安全解决合并冲突。

### 4. 完整工作流执行
从本地修改到推送备份的自动化流程。

---

## 前置条件

确保已配置 `origin`（你的 Fork）和 `upstream`（原项目）：

```bash
git remote -v
# 应显示：
# origin    https://github.com/你的用户名/仓库名.git
# upstream  https://github.com/原作者/原仓库.git
```

如果未配置，参见 [Git 远程仓库配置](references/remote-setup.md)。

---

## 工作流步骤

### 阶段 1: 保存本地修改

```bash
# 1. 查看当前修改
git status

# 2. 提交修改
git add .
git commit -m "描述修改内容"
```

### 阶段 2: 获取上游更新

```bash
# 获取上游最新代码（不合并）
git fetch upstream
```

### 阶段 3: 智能冲突检测

```bash
# 查看上游有哪些新提交
git log HEAD..upstream/main --oneline

# 查看具体改动内容
git diff HEAD upstream/main

# 预检测潜在冲突
git merge --no-commit --no-ff upstream/main
```

**检测后处理：**

- **无冲突**：继续阶段 4
- **有冲突**：查看 `git status`，参见 [冲突解决指南](references/conflict-resolution.md)

如果预检测后不想继续合并：

```bash
git merge --abort
```

### 阶段 4: 执行合并

```bash
# 正式合并上游更新
git merge upstream/main
```

### 阶段 5: 推送到 Fork

```bash
git push origin main
```

---

## 常见场景

### 场景 A: 纯推送备份（无上游同步）

```bash
git add .
git commit -m "我的修改"
git push origin main
```

### 场景 B: 同步上游但无冲突

```bash
git fetch upstream
git merge upstream/main
git push origin main
```

### 场景 C: 同步上游且有冲突

1. 运行冲突检测（阶段 3）
2. 查看 [冲突解决指南](references/conflict-resolution.md)
3. 手动解决冲突
4. 推送更新

详见 [完整冲突处理流程](references/conflict-resolution.md#完整流程)。

---

## 冲突类型说明

| 场景 | 结果 | 说明 |
|-----|------|------|
| 不同文件 | ✅ 自动合并 | 两个修改都保留 |
| 不同行 | ✅ 自动合并 | 同一文件的不同位置 |
| 同一行不同内容 | ❌ 冲突 | 需手动选择 |
| 你改了，上游删除 | ❌ 冲突 | 需决定是否保留 |

Git 不会静默覆盖修改！有冲突时会明确标记。

---

## 故障排查

### 推送被拒绝
```
error: failed to push some refs to 'origin'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
```

**解决：**
```bash
git pull origin main --allow-unrelated-histories
git push origin main
```

### 合并冲突
```
Automatic merge failed; fix conflicts and then commit
```

**解决：** 参见 [冲突解决指南](references/conflict-resolution.md)。

### 找不到 upstream
```
fatal: 'upstream' does not appear to be a git repository
```

**解决：** 参见 [Git 远程仓库配置](references/remote-setup.md) 添加 upstream。

---

## 快速参考

### 基本命令
- `git remote -v` - 查看远程仓库
- `git fetch upstream` - 获取上游更新
- `git log HEAD..upstream/main --oneline` - 查看上游新提交
- `git diff HEAD upstream/main` - 查看上游改动
- `git merge upstream/main` - 合并上游更新
- `git push origin main` - 推送到 Fork

### 冲突相关
- `git status` - 查看冲突文件
- `git merge --abort` - 取消合并
- `git add .` - 标记冲突已解决
- `git commit` - 完成合并提交

---

## 参考资料

- [Git 远程仓库配置](references/remote-setup.md) - 配置 origin 和 upstream
- [冲突解决指南](references/conflict-resolution.md) - 详细的冲突处理步骤
- [工作流最佳实践](references/best-practices.md) - 推荐的工作流和注意事项
