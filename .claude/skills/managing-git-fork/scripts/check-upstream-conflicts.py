#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能上游冲突检测器

检测上游更新并分析可能的冲突，提供详细的冲突报告。
"""

import subprocess
import sys
from typing import List, Tuple

# Windows 编码兼容
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def run_command(cmd: List[str]) -> Tuple[int, str, str]:
    """运行命令并返回状态码、标准输出和标准错误"""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def fetch_upstream() -> bool:
    """获取上游更新"""
    print("🔍 正在获取上游更新...")
    code, stdout, stderr = run_command(["git", "fetch", "upstream"])

    if code != 0:
        print(f"❌ 获取上游失败: {stderr}")
        return False

    print("✅ 上游更新已获取\n")
    return True


def get_upstream_commits() -> List[str]:
    """获取上游的新提交"""
    print("📝 检查上游新提交...")
    code, stdout, stderr = run_command([
        "git", "log", "HEAD..upstream/main", "--oneline"
    ])

    if code != 0:
        print(f"⚠️  无法获取提交历史: {stderr}")
        return []

    commits = stdout.split('\n') if stdout else []

    if not commits:
        print("✅ 没有新的上游提交\n")
        return []

    print(f"发现 {len(commits)} 个新提交:")
    for commit in commits:
        print(f"  • {commit}")
    print()

    return commits


def get_changed_files() -> List[str]:
    """获取上游修改的文件列表"""
    code, stdout, stderr = run_command([
        "git", "diff", "HEAD", "upstream/main", "--name-only"
    ])

    if code != 0:
        print(f"⚠️  无法获取文件列表: {stderr}")
        return []

    return stdout.split('\n') if stdout else []


def get_local_modified_files() -> List[str]:
    """获取本地修改的文件"""
    code, stdout, stderr = run_command([
        "git", "diff", "--name-only"
    ])

    if code != 0:
        return []

    local_files = stdout.split('\n') if stdout else []

    # 检查暂存区
    code, stdout, stderr = run_command([
        "git", "diff", "--cached", "--name-only"
    ])

    if code == 0 and stdout:
        staged_files = stdout.split('\n')
        local_files.extend(staged_files)

    return list(set(local_files))  # 去重


def detect_potential_conflicts(
    upstream_files: List[str],
    local_files: List[str]
) -> List[str]:
    """检测潜在冲突"""
    conflicts = set(upstream_files) & set(local_files)
    return sorted(list(conflicts))


def preview_merge() -> Tuple[bool, List[str]]:
    """预览合并，检测实际冲突"""
    print("🔬 预检测合并冲突...")

    # 尝试无提交合并
    code, stdout, stderr = run_command([
        "git", "merge", "--no-commit", "--no-ff", "upstream/main"
    ])

    if code == 0:
        # 无冲突
        print("✅ 预检测: 未发现冲突\n")
        run_command(["git", "merge", "--abort"])
        return True, []
    else:
        # 有冲突，提取冲突文件
        code, stdout, stderr = run_command(["git", "status"])

        conflict_files = []
        for line in stdout.split('\n'):
            if 'both modified' in line:
                # 提取文件名
                file = line.split(':')[-1].strip()
                conflict_files.append(file)

        # 取消合并
        run_command(["git", "merge", "--abort"])

        if conflict_files:
            print(f"⚠️  发现 {len(conflict_files)} 个冲突文件:")
            for f in conflict_files:
                print(f"  • {f}")
            print()

        return False, conflict_files


def show_upstream_changes(upstream_files: List[str]):
    """显示上游改动的摘要"""
    if not upstream_files:
        return

    print(f"📊 上游修改了 {len(upstream_files)} 个文件:\n")

    # 分类显示
    categories = {
        '配置': [f for f in upstream_files if 'config' in f.lower()],
        '代码': [f for f in upstream_files if f.endswith(('.py', '.js', '.ts')) and 'config' not in f.lower()],
        '文档': [f for f in upstream_files if f.endswith(('.md', '.txt', '.rst'))],
        '其他': []
    }

    for category, files in categories.items():
        if files:
            print(f"{category}:")
            for f in files:
                print(f"  • {f}")
            print()


def generate_report(
    commits: List[str],
    upstream_files: List[str],
    local_files: List[str],
    potential_conflicts: List[str],
    actual_conflicts: List[str]
):
    """生成完整报告"""

    print("=" * 60)
    print("📋 冲突检测报告")
    print("=" * 60)
    print()

    # 1. 上游更新情况
    if commits:
        print(f"📈 上游更新: {len(commits)} 个提交")
        print(f"📁 修改文件: {len(upstream_files)} 个")
    else:
        print("✅ 上游无更新")

    print()

    # 2. 本地修改情况
    if local_files:
        print(f"✏️  本地修改: {len(local_files)} 个文件")
        for f in local_files:
            print(f"  • {f}")
    else:
        print("✅ 本地无未提交修改")

    print()

    # 3. 冲突分析
    if actual_conflicts:
        print("⚠️  实际冲突（需要手动解决）:")
        for f in actual_conflicts:
            print(f"  • {f}")
        print()
        print("💡 建议:")
        print("  1. 查看 conflict-resolution.md 了解解决步骤")
        print("  2. 运行 'git merge upstream/main' 开始合并")
        print("  3. 解决冲突后运行 'git add <file>' 和 'git commit'")
    elif potential_conflicts:
        print("⚠️  潜在冲突（文件重叠，但可能自动合并）:")
        for f in potential_conflicts:
            print(f"  • {f}")
        print()
        print("💡 建议: 运行 'git merge upstream/main' 安全合并")
    else:
        print("✅ 无冲突，可以安全合并")

    print()
    print("=" * 60)


def main():
    """主流程"""
    print("🚀 开始智能冲突检测\n")

    # 1. 获取上游更新
    if not fetch_upstream():
        sys.exit(1)

    # 2. 获取上游新提交
    commits = get_upstream_commits()

    if not commits:
        print("✅ 上游没有新更新，无需继续")
        return

    # 3. 获取修改的文件
    upstream_files = get_changed_files()
    local_files = get_local_modified_files()

    # 4. 显示上游改动
    show_upstream_changes(upstream_files)

    # 5. 检测潜在冲突
    potential_conflicts = detect_potential_conflicts(upstream_files, local_files)

    # 6. 预览实际冲突
    has_conflict, actual_conflicts = preview_merge()

    # 7. 生成报告
    generate_report(
        commits,
        upstream_files,
        local_files,
        potential_conflicts,
        actual_conflicts
    )

    # 8. 给出下一步建议
    print("📌 下一步操作:")
    if actual_conflicts:
        print("  1. 查看 conflict-resolution.md")
        print("  2. 运行: git merge upstream/main")
        print("  3. 手动解决冲突")
        print("  4. 运行: git add . && git commit")
        print("  5. 运行: git push origin main")
    else:
        print("  1. 运行: git merge upstream/main")
        print("  2. 运行: git push origin main")


if __name__ == "__main__":
    main()
