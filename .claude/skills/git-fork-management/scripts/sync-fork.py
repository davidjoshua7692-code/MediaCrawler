#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化 Fork 同步脚本

完整的同步工作流：获取上游、检测冲突、合并、推送
"""

import subprocess
import sys
import time
from typing import List, Tuple

# Windows 编码兼容
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def run_command(cmd: List[str]) -> Tuple[int, str, str]:
    """运行命令并返回状态码、标准输出和标准错误"""
    print(f"▶️  {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def check_git_repo() -> bool:
    """检查是否在 Git 仓库中"""
    code, stdout, stderr = run_command(["git", "rev-parse", "--git-dir"])
    return code == 0


def check_remotes() -> bool:
    """检查远程仓库配置"""
    print("\n🔍 检查远程仓库配置...")

    code, stdout, stderr = run_command(["git", "remote", "-v"])

    if code != 0:
        print("❌ 无法获取远程仓库信息")
        return False

    has_origin = "origin" in stdout
    has_upstream = "upstream" in stdout

    if not has_origin:
        print("❌ 未找到 origin 远程仓库")
        print("💡 请先运行: git remote add origin <你的-Fork-URL>")
        return False

    if not has_upstream:
        print("⚠️  未找到 upstream 远程仓库")
        print("💡 建议添加: git remote add upstream <原仓库-URL>")
        print("⏭️  继续执行（将只同步 origin）...")

    print("✅ 远程仓库配置正常\n")
    return True


def save_local_changes() -> bool:
    """保存本地修改"""
    print("📝 检查本地修改...")

    # 检查是否有未提交的修改
    code, stdout, stderr = run_command(["git", "status", "--porcelain"])

    if code != 0:
        print("⚠️  无法检查状态")
        return False

    if not stdout:
        print("✅ 没有未提交的修改\n")
        return True

    print("⚠️  发现有未提交的修改:")
    print(stdout)

    # 提示用户
    print("\n❓ 是否要提交这些修改？(y/n)", end=" ")
    response = input().strip().lower()

    if response != 'y':
        print("❌ 取消操作")
        return False

    # 提交修改
    print("\n💬 请输入提交信息:", end=" ")
    message = input().strip() or "Update"

    code, stdout, stderr = run_command(["git", "add", "."])
    if code != 0:
        print(f"❌ git add 失败: {stderr}")
        return False

    code, stdout, stderr = run_command(["git", "commit", "-m", message])
    if code != 0:
        print(f"❌ git commit 失败: {stderr}")
        return False

    print("✅ 本地修改已提交\n")
    return True


def fetch_upstream() -> bool:
    """获取上游更新"""
    print("📥 获取上游更新...")

    # 先尝试获取 upstream
    code, stdout, stderr = run_command(["git", "remote", "-v"])
    has_upstream = "upstream" in stdout

    if has_upstream:
        code, stdout, stderr = run_command(["git", "fetch", "upstream"])
        if code != 0:
            print(f"❌ 获取 upstream 失败: {stderr}")
            return False

        print("✅ upstream 更新已获取")
        return True
    else:
        print("⚠️  没有 upstream，跳过")
        return True


def show_upstream_changes():
    """显示上游改动"""
    code, stdout, stderr = run_command([
        "git", "log", "HEAD..upstream/main", "--oneline"
    ])

    if code != 0 or not stdout:
        print("✅ 上游没有新提交")
        return True

    print(f"\n📊 上游有 {len(stdout.split(chr(10)))} 个新提交:")
    print(stdout)
    return True


def preview_merge() -> Tuple[bool, List[str]]:
    """预览合并"""
    print("\n🔬 预检测合并冲突...")

    code, stdout, stderr = run_command([
        "git", "merge", "--no-commit", "--no-ff", "upstream/main"
    ])

    if code == 0:
        print("✅ 预检测通过，无冲突")
        run_command(["git", "merge", "--abort"])
        return True, []
    else:
        # 提取冲突文件
        code, stdout, stderr = run_command(["git", "status"])
        conflict_files = []
        for line in stderr.split('\n'):
            if 'both modified' in line:
                file = line.split(':')[-1].strip()
                conflict_files.append(file)

        run_command(["git", "merge", "--abort"])

        if conflict_files:
            print(f"⚠️  发现 {len(conflict_files)} 个冲突文件:")
            for f in conflict_files:
                print(f"  • {f}")

        return False, conflict_files


def merge_with_conflict_resolution(conflict_files: List[str]) -> bool:
    """协助解决冲突"""
    if not conflict_files:
        return True

    print("\n" + "=" * 60)
    print("⚠️  需要手动解决冲突")
    print("=" * 60)

    print("\n💡 冲突解决步骤:")
    print("1. 打开冲突文件，查找标记 <<<<<<< HEAD")
    print("2. 选择保留的代码，删除冲突标记")
    print("3. 保存文件")
    print("4. 对所有冲突文件重复此操作")

    print("\n📝 冲突文件列表:")
    for i, f in enumerate(conflict_files, 1):
        print(f"  {i}. {f}")

    print("\n❓ 冲突已解决完毕？(y/n)", end=" ")
    response = input().strip().lower()

    if response != 'y':
        print("❌ 取消合并")
        run_command(["git", "merge", "--abort"])
        return False

    return True


def perform_merge() -> bool:
    """执行合并"""
    print("\n🔀 执行合并...")

    code, stdout, stderr = run_command(["git", "merge", "upstream/main"])

    if code != 0:
        print(f"❌ 合并失败: {stderr}")
        return False

    print("✅ 合并成功")
    return True


def push_to_origin() -> bool:
    """推送到 origin"""
    print("\n📤 推送到 origin...")

    code, stdout, stderr = run_command(["git", "push", "origin", "main"])

    if code != 0:
        print(f"❌ 推送失败: {stderr}")
        print("\n💡 可能需要:")
        print("  git pull origin main --allow-unrelated-histories")
        print("  git push origin main")
        return False

    print("✅ 推送成功")
    return True


def main():
    """主流程"""
    print("🚀 Fork 自动化同步流程")
    print("=" * 60)

    # 1. 检查环境
    if not check_git_repo():
        print("❌ 当前目录不是 Git 仓库")
        sys.exit(1)

    if not check_remotes():
        sys.exit(1)

    # 2. 保存本地修改
    if not save_local_changes():
        sys.exit(1)

    # 3. 获取上游更新
    if not fetch_upstream():
        sys.exit(1)

    # 4. 显示上游改动
    show_upstream_changes()

    # 5. 预览合并
    has_conflict, conflict_files = preview_merge()

    # 6. 询问是否继续
    print("\n❓ 是否继续合并？(y/n)", end=" ")
    response = input().strip().lower()

    if response != 'y':
        print("❌ 取消操作")
        sys.exit(0)

    # 7. 执行合并
    if not perform_merge():
        if has_conflict:
            # 尝试协助解决冲突
            if not merge_with_conflict_resolution(conflict_files):
                sys.exit(1)

            # 标记冲突已解决
            print("\n✅ 标记冲突已解决...")
            code, stdout, stderr = run_command(["git", "add", "."])
            if code != 0:
                print(f"❌ git add 失败: {stderr}")
                sys.exit(1)

            code, stdout, stderr = run_command(["git", "commit"])
            if code != 0:
                print(f"❌ git commit 失败: {stderr}")
                sys.exit(1)

            print("✅ 冲突已解决并提交")
        else:
            sys.exit(1)

    # 8. 推送到 origin
    if not push_to_origin():
        sys.exit(1)

    # 9. 完成
    print("\n" + "=" * 60)
    print("✅ 同步完成！")
    print("=" * 60)
    print("\n📊 当前状态:")
    run_command(["git", "status"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 用户中断操作")
        sys.exit(1)
