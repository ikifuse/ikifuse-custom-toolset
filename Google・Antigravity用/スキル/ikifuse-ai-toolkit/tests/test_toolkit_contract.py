#!/usr/bin/env python3

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents" / "skills"


def read_skill(name: str) -> str:
    return (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")


class ToolkitContractCases(unittest.TestCase):
    def test_01_all_skills_have_antigravity_frontmatter(self) -> None:
        for name in ("evidence-audit", "action-check", "secret-privacy-guard"):
            text = read_skill(name)
            match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
            self.assertIsNotNone(match, name)
            frontmatter = match.group(1)
            self.assertIn(f"name: {name}", frontmatter)
            self.assertRegex(frontmatter, r"(?m)^description: .+")

    def test_02_evidence_shortage_is_not_confirmed(self) -> None:
        text = read_skill("evidence-audit")
        self.assertIn("Never convert `SYNTHESIS`, `UNKNOWN`, or `NOT_CHECKED` into “confirmed.”", text)
        self.assertIn("`PARTIAL`: useful evidence exists", text)

    def test_03_small_normal_edits_stay_lightweight(self) -> None:
        text = read_skill("action-check")
        self.assertIn("Ordinary, clearly authorized, non-destructive edits should remain lightweight.", text)
        self.assertIn("Skip it for ordinary small edits", text)

    def test_04_out_of_scope_changes_are_detected(self) -> None:
        text = read_skill("action-check")
        self.assertIn("`OUT_OF_SCOPE_TASK_CHANGE`", text)
        self.assertIn("do not report the work as complete", text)

    def test_05_untracked_deletion_is_not_git_recoverable(self) -> None:
        text = read_skill("action-check")
        self.assertIn("untracked content and uncommitted portions are not recoverable from Git", text)

    def test_06_rm_rf_is_destructive(self) -> None:
        text = read_skill("action-check")
        self.assertIn("`rm` or `rm -rf`", text)
        self.assertIn("Apply Destructive Guard", text)

    def test_07_conditional_deletion_stops_without_evidence(self) -> None:
        text = read_skill("action-check")
        self.assertIn("delete only when the required safety conclusion is confirmed", text)
        self.assertIn("Do not delete when the conclusion is partial, conflicted, or unknown.", text)

    def test_08_external_disclosure_uses_privacy_guard(self) -> None:
        action = read_skill("action-check")
        privacy = read_skill("secret-privacy-guard")
        self.assertIn("let `secret-privacy-guard` determine whether the exact outbound information", action)
        self.assertIn("Trigger only at a disclosure boundary", privacy)

    def test_09_api_key_patterns_and_no_automatic_rewrite(self) -> None:
        scanner = (SKILLS / "secret-privacy-guard" / "scripts" / "scan_sensitive.py").read_text(encoding="utf-8")
        privacy = read_skill("secret-privacy-guard")
        self.assertIn("google-api-key", scanner)
        self.assertIn("openai-style-api-key", scanner)
        self.assertIn("Do not delete, rewrite, redact, mask", privacy)

    def test_10_responsibilities_remain_separate(self) -> None:
        evidence = read_skill("evidence-audit")
        action = read_skill("action-check")
        privacy = read_skill("secret-privacy-guard")
        self.assertIn("evidence-sufficiency", evidence)
        self.assertIn("Authorization Boundary", action)
        self.assertIn("whether the scoped information may leave", privacy)
        self.assertIn("Authorization does not imply disclosure safety", action)
        self.assertIn("Never let a `SAFE` result authorize an action", privacy)

    def test_no_codex_specific_metadata_was_ported(self) -> None:
        self.assertFalse((ROOT / ".codex-plugin").exists())
        self.assertEqual(list(ROOT.rglob("openai.yaml")), [])


if __name__ == "__main__":
    unittest.main()
