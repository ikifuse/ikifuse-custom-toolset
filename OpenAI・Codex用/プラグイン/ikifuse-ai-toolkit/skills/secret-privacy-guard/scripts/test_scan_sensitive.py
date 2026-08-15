#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from scan_sensitive import build_report, scan_paths, scan_staged


SKILL_PATH = Path(__file__).resolve().parents[1] / "SKILL.md"


def _scan(path: Path) -> dict[str, object]:
    findings, unknowns = scan_paths([str(path)])
    return build_report(findings, unknowns)


class SecretPrivacyGuardCases(unittest.TestCase):
    def test_01_api_key_before_push(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repository, check=True)
            target = repository / "config.py"
            target.write_text('API_KEY = "' + "sk-" + "A" * 32 + '"\n', encoding="utf-8")
            subprocess.run(["git", "add", "config.py"], cwd=repository, check=True)
            previous = Path.cwd()
            try:
                os.chdir(repository)
                findings, unknowns = scan_staged()
            finally:
                os.chdir(previous)
            self.assertEqual(build_report(findings, unknowns)["status"], "SENSITIVE")

    def test_02_env_in_publication_scope(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / ".env"
            target.write_text("SERVICE_TOKEN=" + "T" * 32 + "\n", encoding="utf-8")
            self.assertEqual(_scan(target)["status"], "SENSITIVE")

    def test_03_log_with_email_and_phone(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "app.log"
            email = "user" + "@" + "example.test"
            phone = "090-" + "1234-" + "5678"
            target.write_text(f"contact={email} phone={phone}\n", encoding="utf-8")
            report = _scan(target)
            kinds = {item["kind"] for item in report["findings"]}
            self.assertEqual(report["status"], "SENSITIVE")
            self.assertTrue({"email-address", "phone-number"}.issubset(kinds))

    def test_04_relative_local_path_is_safe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "settings.toml"
            target.write_text('output_dir = "./build"\n', encoding="utf-8")
            self.assertEqual(_scan(target)["status"], "SAFE")

    def test_05_normal_file_is_safe(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "README.md"
            target.write_text("# Sample\nPublic documentation only.\n", encoding="utf-8")
            self.assertEqual(_scan(target)["status"], "SAFE")

    def test_06_detection_does_not_modify_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "secrets.txt"
            target.write_text("password=" + "P" * 24 + "\n", encoding="utf-8")
            before = hashlib.sha256(target.read_bytes()).hexdigest()
            _scan(target)
            after = hashlib.sha256(target.read_bytes()).hexdigest()
            self.assertEqual(before, after)

    def test_07_masking_requires_explicit_permission(self) -> None:
        text = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("explicitly authorizes that exact operation", text)
        self.assertIn("Do not delete, rewrite, redact, mask", text)

    def test_08_routine_local_edit_does_not_trigger(self) -> None:
        frontmatter = SKILL_PATH.read_text(encoding="utf-8").split("---", 2)[1]
        self.assertIn("Do not use for routine local editing", frontmatter)

    def test_user_specific_absolute_path_requires_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "settings.toml"
            local_path = "/Users/" + "sample-user/private/output"
            target.write_text(f'output_dir = "{local_path}"\n', encoding="utf-8")
            self.assertEqual(_scan(target)["status"], "REVIEW_REQUIRED")


if __name__ == "__main__":
    unittest.main()
