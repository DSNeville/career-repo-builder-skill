#!/usr/bin/env python3
"""Lint publish payloads for unresolved placeholders and private markers.

Usage:
  python3 scripts/publish_lint.py --path /career/public_site
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

BLOCKED_PATTERNS = [
    ("NEEDS_CLARIFICATION", re.compile(r"NEEDS_CLARIFICATION", re.IGNORECASE)),
    ("PRIVATE_UNSHARED", re.compile(r"PRIVATE_UNSHARED", re.IGNORECASE)),
    ("PRIVATE_PATH", re.compile(r"/Users/", re.IGNORECASE)),
    ("MISSING_MARKER", re.compile(r"\bMISSING\b", re.IGNORECASE)),
]


def collect_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    if not path.exists():
        return []
    return [candidate for candidate in path.rglob("*") if candidate.is_file()]


def check_string(value: str, source: str) -> list[str]:
    issues: list[str] = []
    for name, pattern in BLOCKED_PATTERNS:
        if pattern.search(value):
            issues.append(f"{source}: blocked token {name}: {value[:140]}")
    return issues


def lint_json_payload(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON ({exc})"]

    def walk(value: Any, pointer: str) -> None:
        if isinstance(value, str):
            issues.extend(check_string(value, f"{path}:{pointer}"))
            return
        if isinstance(value, list):
            for index, item in enumerate(value):
                walk(item, f"{pointer}[{index}]")
            return
        if isinstance(value, dict):
            for key, item in value.items():
                walk(item, f"{pointer}.{key}")

    walk(payload, "$")
    return issues


def lint_text_payload(path: Path) -> list[str]:
    issues: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        issues.extend(check_string(line, f"{path}:{line_number}"))
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint publish payloads for private markers.")
    parser.add_argument("--path", required=True, help="File or directory path to lint")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = Path(args.path).expanduser().resolve()

    files = collect_files(target)
    if not files:
        raise SystemExit(f"No files found at {target}")

    issues: list[str] = []
    for file_path in files:
        if file_path.suffix.lower() == ".json":
            issues.extend(lint_json_payload(file_path))
        elif file_path.suffix.lower() in {".md", ".txt", ".yml", ".yaml"}:
            issues.extend(lint_text_payload(file_path))

    if issues:
        print("Publish lint failed:\n")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)

    print(f"Publish lint passed: {target}")


if __name__ == "__main__":
    main()
