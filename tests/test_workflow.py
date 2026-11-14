import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_pr import validate


ROOT = Path(__file__).resolve().parents[1]
PR_TEMPLATE = ROOT / ".github" / "pull_request_template.md"
COMPLETE_PR = """## 关联 Issue
#12

## 风险
中
调整普通功能。

## 变更
实现 Issue 所需的修改。

## 验证
运行测试通过。
"""


class WorkflowTests(unittest.TestCase):
    def test_required_files_exist(self):
        for relative_path in (
            "AGENTS.md",
            "CLAUDE.md",
            "PROJECT.md",
            "docs/workflow.md",
            "docs/task-briefs.md",
            "docs/orchestrator-instructions.md",
            ".agents/skills/dev-orchestrator/SKILL.md",
            ".claude/skills/dev-orchestrator/SKILL.md",
            ".github/ISSUE_TEMPLATE/task.yml",
        ):
            with self.subTest(relative_path=relative_path):
                self.assertTrue((ROOT / relative_path).is_file())

    def test_complete_pr_passes(self):
        self.assertEqual(validate(COMPLETE_PR), [])

    def test_template_comments_are_not_evidence(self):
        self.assertEqual(len(validate(PR_TEMPLATE.read_text(encoding="utf-8"))), 5)

    def test_issue_and_risk_must_match_expected_format(self):
        body = COMPLETE_PR.replace("#12", "#0").replace("中\n", "未知\n")
        self.assertEqual(len(validate(body)), 2)

    def test_code_block_headings_do_not_create_sections(self):
        body = COMPLETE_PR.replace("## 验证\n运行测试通过。", "```text\n## 验证\n运行测试通过。\n```")
        self.assertEqual(validate(body), ["填写「验证」章节。"])

    def test_github_event_entrypoint(self):
        with tempfile.TemporaryDirectory() as folder:
            event_path = Path(folder) / "event.json"
            for body, expected_exit in ((COMPLETE_PR, 0), (None, 1)):
                with self.subTest(expected_exit=expected_exit):
                    event_path.write_text(json.dumps({"pull_request": {"body": body}}), encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(ROOT / "scripts" / "check_pr.py")],
                        env={**os.environ, "GITHUB_EVENT_PATH": str(event_path), "PYTHONIOENCODING": "utf-8"},
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        check=False,
                    )
                    self.assertEqual(result.returncode, expected_exit, result.stderr or result.stdout)


if __name__ == "__main__":
    unittest.main()
