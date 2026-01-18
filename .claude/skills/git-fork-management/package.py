#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 Skill 打包脚本
"""

import os
import zipfile
from pathlib import Path


def package_skill(skill_dir: str, output_dir: str = "."):
    """打包 Skill 目录为 .skill 文件"""
    skill_path = Path(skill_dir)

    if not skill_path.exists():
        print(f"❌ 目录不存在: {skill_dir}")
        return False

    if not (skill_path / "SKILL.md").exists():
        print(f"❌ 未找到 SKILL.md 文件")
        return False

    skill_name = skill_path.name
    output_file = Path(output_dir) / f"{skill_name}.skill"

    # 创建 zip 文件
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in skill_path.rglob('*'):
            if file.is_file():
                # 计算相对路径
                rel_path = file.relative_to(skill_path.parent)
                arcname = f"{skill_name}/{file.relative_to(skill_path)}"
                zipf.write(file, arcname)
                print(f"  添加: {arcname}")

    print(f"\n✅ 打包完成: {output_file}")
    print(f"📦 大小: {output_file.stat().st_size} 字节")

    return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python package.py <skill目录> [输出目录]")
        sys.exit(1)

    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    package_skill(skill_dir, output_dir)
