# 冲突解决指南

详细的 Git 合并冲突处理步骤和示例。

## 冲突标记示例

当 Git 检测到冲突时，会在文件中插入标记：

```
<<<<<<< HEAD
你的代码（当前分支）
=======
上游的代码（upstream/main）
>>>>>>> upstream/main
```

## 完整流程

### 步骤 1: 识别冲突文件

```bash
git status
```

输出示例：
```
Unmerged paths:
  (use "git restore --staged <file>..." to unstage)
  (use "git add <file>..." to mark resolution)

	both modified:   config/base_config.py
```

### 步骤 2: 打开冲突文件

使用编辑器打开标记为 "both modified" 的文件。

### 步骤 3: 理解冲突内容

#### 示例 1: 同一行不同修改

```python
<<<<<<< HEAD
KEYWORDS = "美食教程"  # 你的版本
=======
KEYWORDS = "人工智能"  # 上游版本
>>>>>>> upstream/main
```

**选择方式：**
- 保留你的：删除 `<<<<<<< HEAD` 到 `=======` 和 `>>>>>>> upstream/main`
- 用上游的：删除 `<<<<<<< HEAD` 到 `=======` 和 `>>>>>>> upstream/main`
- 合并两者：手动编辑，如 `KEYWORDS = "美食教程,人工智能"`

#### 示例 2: 你修改了，上游删除了

```python
<<<<<<< HEAD
ENABLE_CDP = False  # 你改了这个
PLATFORM = "xhs"
=======
PLATFORM = "xhs"
>>>>>>> upstream/main
```

**决定：**
- 如果需要保留：删除标记，保留这一行
- 如果不需要：删除这一行和标记

#### 示例 3: 复杂冲突（多行）

```python
<<<<<<< HEAD
# 你的修改：新增配置
ENABLE_NEW_FEATURE = True
FEATURE_CONFIG = {
    "mode": "advanced",
    "timeout": 30
}
=======
# 上游的修改：重构了配置
FEATURE_SETTINGS = {
    "enabled": False,
    "mode": "basic"
}
>>>>>>> upstream/main
```

**处理：**
需要理解两边的逻辑，手动合并为：
```python
# 合并后的配置
FEATURE_SETTINGS = {
    "enabled": True,  # 保留你的启用状态
    "mode": "advanced",  # 保留你的高级模式
    "timeout": 30  # 保留你的超时设置
}
```

### 步骤 4: 解决冲突

删除所有 Git 冲突标记（`<<<<<<<`、`=======`、`>>>>>>>`），保留你想要的代码。

### 步骤 5: 标记冲突已解决

```bash
git add <file>
```

例如：
```bash
git add config/base_config.py
```

### 步骤 6: 完成合并

```bash
git commit
```

Git 会自动生成合并提交信息，或你可以自定义：
```bash
git commit -m "合并上游更新，解决配置冲突"
```

### 步骤 7: 推送到 Fork

```bash
git push origin main
```

---

## 高级场景

### 场景 1: 多个文件冲突

```bash
# 查看所有冲突文件
git status

# 逐个解决，或者使用工具
git mergetool  # 如果配置了可视化合并工具

# 解决完所有冲突后
git add .
git commit
```

### 场景 2: 想放弃合并

如果冲突太复杂，想重新开始：

```bash
# 取消当前合并
git merge --abort

# 重新尝试
git merge upstream/main
```

### 场景 3: 先查看上游改动再决定合并

```bash
# 预览上游改动
git diff HEAD upstream/main

# 预检测冲突（不实际合并）
git merge --no-commit --no-ff upstream/main

# 查看冲突后，取消合并
git merge --abort

# 决定策略后再真正合并
git merge upstream/main
```

### 场景 4: 使用特定策略合并

```bash
# 策略 1: 优先上游（放弃你的冲突修改）
git merge -X theirs upstream/main

# 策略 2: 优先你自己的（放弃上游的冲突修改）
git merge -X ours upstream/main

# 策略 3: 手动逐个文件解决（推荐）
git merge upstream/main  # 然后手动编辑
```

---

## 常见错误处理

### 错误 1: 提交前忘记解决某个文件

```bash
git status
# 显示还有 "both modified" 文件
```

**解决：** 继续解决剩余冲突文件，然后 `git add` 它们。

### 错误 2: 删除了代码但没删除标记

文件中还包含 `<<<<<<<` 或 `>>>>>>>`。

```bash
# 搜索残留标记
grep -r "<<<<<<< HEAD" .
```

**解决：** 打开文件，删除所有标记。

### 错误 3: 解决冲突后想回退

```bash
# 回退到合并前
git reset --hard HEAD~1
```

---

## 最佳实践

1. **先预览，再合并**
   ```bash
   git fetch upstream
   git log HEAD..upstream/main --oneline  # 看改了什么
   git diff HEAD upstream/main  # 看具体改动
   ```

2. **小步快跑**
   - 定期同步，不要让改动积累太多
   - 频繁推送本地修改到你的 Fork

3. **备份关键分支**
   ```bash
   git branch backup-before-merge
   git merge upstream/main
   # 如果出问题
   git reset --hard backup-before-merge
   ```

4. **使用可视化工具**（可选）
   - VS Code 的 Git 扩展
   - GitKraken
   - SourceTree

---

## 快速命令参考

```bash
# 查看冲突
git status

# 搜索冲突标记
grep -r "<<<<<<< HEAD" .

# 取消合并
git merge --abort

# 标记已解决
git add <file>

# 完成合并
git commit

# 回退合并
git reset --hard HEAD~1
```
