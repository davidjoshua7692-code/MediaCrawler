# Git 远程仓库配置

配置 `origin`（你的 Fork）和 `upstream`（原项目）的完整指南。

## 验证当前配置

```bash
git remote -v
```

**期望输出：**
```
origin    https://github.com/你的用户名/仓库名.git (fetch)
origin    https://github.com/你的用户名/仓库名.git (push)
upstream  https://github.com/原作者/原仓库.git (fetch)
upstream  https://github.com/原作者/原仓库.git (push)
```

## 配置场景

### 场景 A: 已 Fork，但 origin 指向原项目

**当前状态：**
```
origin    https://github.com/NanmiCoder/MediaCrawler.git
```

**解决：**
```bash
# 修改 origin 指向你的 Fork
git remote set-url origin https://github.com/你的用户名/MediaCrawler.git

# 添加 upstream 指向原项目
git remote add upstream https://github.com/NanmiCoder/MediaCrawler.git

# 验证
git remote -v
```

### 场景 B: 从零开始配置

1. **在 GitHub Fork 原仓库**
   - 访问 https://github.com/NanmiCoder/MediaCrawler
   - 点击 Fork 按钮

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/你的用户名/MediaCrawler.git
   cd MediaCrawler
   ```

3. **添加 upstream**
   ```bash
   git remote add upstream https://github.com/NanmiCoder/MediaCrawler.git
   ```

### 场景 C: origin 指向本地或其他地方

**修改为你的 Fork：**
```bash
git remote set-url origin https://github.com/你的用户名/你的仓库.git
```

## 常用操作

### 查看远程仓库信息

```bash
# 显示所有远程仓库
git remote -v

# 显示某个远程仓库的详细信息
git remote show origin

# 显示远程分支
git branch -r
```

### 添加远程仓库

```bash
# 添加 upstream
git remote add upstream https://github.com/原作者/仓库.git

# 添加其他远程仓库（可选）
git remote add backup https://github.com/你的其他账号/仓库.git
```

### 删除远程仓库

```bash
# 删除 upstream（不推荐）
git remote remove upstream
```

### 重命名远程仓库

```bash
# 将 origin 重命名为 myfork
git remote rename origin myfork
```

### 修改远程仓库 URL

```bash
# 修改 origin 的 URL
git remote set-url origin https://github.com/新用户名/新仓库.git

# 只修改 push URL
git remote set-url --push origin git@github.com:用户名/仓库.git
```

## 验证配置

### 测试连接

```bash
# 测试 origin 连接
git remote show origin

# 测试 upstream 连接
git remote show upstream
```

### 测试拉取

```bash
# 拉取但不合并（测试 upstream 是否正常）
git fetch upstream

# 查看 upstream 的分支
git branch -r | grep upstream
```

## SSH vs HTTPS

### HTTPS（推荐新手）
```bash
origin	https://github.com/用户名/仓库.git
```

- **优点**：简单，无需配置
- **缺点**：每次推送需要输入密码（除非配置了 credential helper）

### SSH（推荐频繁使用）
```bash
origin	git@github.com:用户名/仓库.git
```

- **优点**：一次配置，无需密码
- **缺点**：需要生成 SSH 密钥

**切换到 SSH：**
```bash
git remote set-url origin git@github.com:用户名/仓库.git
```

## 故障排查

### 问题 1: upstream 已存在

```bash
fatal: remote upstream already exists.
```

**解决：**
```bash
# 先删除旧的
git remote remove upstream

# 再添加新的
git remote add upstream https://github.com/正确的URL.git
```

### 问题 2: 权限拒绝

```
ERROR: Permission to 用户名/仓库.git denied to 用户名
```

**检查：**
1. 确认 URL 中的用户名是你的账号
2. 检查仓库访问权限
3. 如果是 SSH，确认密钥已配置

### 问题 3: 找不到远程仓库

```
fatal: 'origin' does not appear to be a git repository
```

**解决：**
```bash
# 添加 origin
git remote add origin https://github.com/你的用户名/仓库.git
```

## 完整示例

从零开始的完整配置流程：

```bash
# 1. Fork 原仓库（在 GitHub 网页操作）

# 2. 克隆你的 Fork
git clone https://github.com/davidjoshua7692-code/MediaCrawler.git
cd MediaCrawler

# 3. 添加 upstream
git remote add upstream https://github.com/NanmiCoder/MediaCrawler.git

# 4. 验证配置
git remote -v
# 应该看到：
# origin    https://github.com/davidjoshua7692-code/MediaCrawler.git (fetch)
# origin    https://github.com/davidjoshua7692-code/MediaCrawler.git (push)
# upstream  https://github.com/NanmiCoder/MediaCrawler.git (fetch)
# upstream  https://github.com/NanmiCoder/MediaCrawler.git (push)

# 5. 测试拉取
git fetch upstream
git branch -r | grep upstream
# 应该看到：upstream/main
```

## 快速参考

```bash
# 查看配置
git remote -v

# 添加 upstream
git remote add upstream <URL>

# 修改 URL
git remote set-url <name> <URL>

# 删除远程
git remote remove <name>

# 重命名远程
git remote rename <old> <new>
```
