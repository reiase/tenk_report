#!/usr/bin/env python3
"""Dependency-free checks for Markdown files in this repository."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {".git", "build", "site"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
REMOTE_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:")


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts)
    )


def clean_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = target.split(maxsplit=1)[0]
    return unquote(target).split("#", maxsplit=1)[0]


def check_file(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    relative = path.relative_to(ROOT)

    if text and not text.endswith("\n"):
        errors.append(f"{relative}: 文件末尾缺少换行")

    fence_count = 0
    for line_number, line in enumerate(lines, start=1):
        if line.rstrip() != line:
            errors.append(f"{relative}:{line_number}: 行尾有空白字符")
        if line.startswith("```"):
            fence_count += 1
    if fence_count % 2:
        errors.append(f"{relative}: Markdown 代码围栏未成对")

    for match in IMAGE_RE.finditer(text):
        if not match.group(1).strip():
            line_number = text.count("\n", 0, match.start()) + 1
            errors.append(f"{relative}:{line_number}: 图片缺少替代文本")

    for match in LINK_RE.finditer(text):
        raw_target = match.group(1)
        target = clean_target(raw_target)
        if not target or target.startswith("#") or target.startswith(REMOTE_SCHEMES):
            continue
        if target.startswith("/"):
            line_number = text.count("\n", 0, match.start()) + 1
            errors.append(f"{relative}:{line_number}: 仓库文档请使用相对链接: {target}")
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            line_number = text.count("\n", 0, match.start()) + 1
            errors.append(f"{relative}:{line_number}: 链接指向仓库外: {target}")
            continue
        if not resolved.exists():
            line_number = text.count("\n", 0, match.start()) + 1
            errors.append(f"{relative}:{line_number}: 链接目标不存在: {target}")

    return errors


def main() -> int:
    files = markdown_files()
    errors = [error for path in files for error in check_file(path)]
    if errors:
        print("Markdown 检查失败：")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Markdown 检查通过：共检查 {len(files)} 个文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
