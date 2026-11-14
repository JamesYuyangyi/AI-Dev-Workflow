"""Validate the pull request template fields using GitHub's event payload."""

import json
import os
from pathlib import Path
import re


SECTION_NAMES = ("关联 Issue", "风险", "变更", "验证")
ISSUE_REFERENCE = re.compile(r"#[1-9][0-9]*")
HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.*?)[ \t]*#*[ \t]*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HTML_COMMENT = re.compile(r"<!--.*?(?:-->|\Z)", re.DOTALL)


def read_sections(body: str) -> dict[str, list[str]]:
    sections = {name: [] for name in SECTION_NAMES}
    current = None
    fence = ""
    for line in HTML_COMMENT.sub("", body).splitlines():
        marker = FENCE.match(line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = ""
        elif marker:
            fence = marker[1]
        else:
            heading = HEADING.fullmatch(line)
            if heading:
                current = heading[1] if heading[1] in sections else None
                continue
        if current and line.strip():
            sections[current].append(line.strip())
    return sections


def validate(body: str) -> list[str]:
    sections = read_sections(body)
    errors = []
    issue_lines = sections["关联 Issue"]
    if not any(ISSUE_REFERENCE.fullmatch(line) for line in issue_lines):
        errors.append("在「关联 Issue」中单独一行填写本仓库的 Issue 编号，例如 #12。")
    risk_lines = sections["风险"]
    if not risk_lines or risk_lines[0] not in {"低", "中", "高"}:
        errors.append("在「风险」第一行填写 低、中 或 高。")
    if len(risk_lines) < 2:
        errors.append("在「风险」第二行填写分级原因。")
    for name in ("变更", "验证"):
        if not sections[name]:
            errors.append(f"填写「{name}」章节。")
    return errors


def main() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        print("缺少 GITHUB_EVENT_PATH。请使用 pull_request 事件运行此检查。")
        return 1
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    errors = validate(event["pull_request"]["body"] or "")
    for error in errors:
        print(f"::error::{error}")
    if errors:
        return 1
    print("PR 信息检查通过。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
