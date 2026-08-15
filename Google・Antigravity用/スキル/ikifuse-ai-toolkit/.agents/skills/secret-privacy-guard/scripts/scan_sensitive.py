#!/usr/bin/env python3
"""秘密情報・個人情報・ローカル専用情報の候補を検出する読み取り専用スキャナー。"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Finding:
    classification: str
    kind: str
    source: str
    line: int | None
    reason: str


KNOWN_SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN(?: [A-Z0-9]+)? PRIVATE KEY-----"), "秘密鍵の開始マーカーに一致しました。"),
    ("openai-style-api-key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "APIキー形式の文字列に一致しました。"),
    ("github-token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"), "GitHubトークン形式の文字列に一致しました。"),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"), "AWSアクセスキー形式の文字列に一致しました。"),
    ("google-api-key", re.compile(r"\bAIza[A-Za-z0-9_-]{30,}\b"), "Google APIキー形式の文字列に一致しました。"),
)

ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|(?:[a-z0-9]+[_-])?(?:access[_-]?)?token|client[_-]?secret|password|passwd|secret|private[_-]?key|cookie|session(?:[_-]?id|[_-]?token)?)\b\s*[:=]\s*['\"]?([^'\"\s,;#]+)"
)
EMAIL_PATTERN = re.compile(r"(?<![\w.+-])[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}(?![\w.-])", re.IGNORECASE)
PHONE_PATTERN = re.compile(r"(?<!\d)(?:\+?81[-\s]?)?0\d{1,4}[-\s]\d{1,4}[-\s]\d{3,4}(?!\d)")
LOCAL_PATH_PATTERN = re.compile(
    r"(?:/" + r"Users/[^/\s]+/|/" + r"home/[^/\s]+/|[A-Za-z]:\\" + r"Users\\[^\\\s]+\\)"
)
LABELED_PERSON_PATTERN = re.compile(
    r"(?i)(?:\b(?:full[_-]?name|personal[_-]?name|home[_-]?address|postal[_-]?address)\b|氏名|個人名|住所|名前)\s*[:=]\s*['\"]?([^'\"\n,;#]{2,})"
)
ENV_NAMES = {".env", ".env.local", ".env.production", ".env.development", ".env.test"}
LOCAL_CONFIG_PARTS = {".agent", ".agents", ".codex", ".gemini", ".ssh", ".aws", ".kube"}
PLACEHOLDERS = {
    "",
    "changeme",
    "example",
    "placeholder",
    "redacted",
    "replace_me",
    "replace-with-value",
    "test",
    "todo",
    "your_key_here",
    "your_token_here",
}


def _looks_real(value: str) -> bool:
    normalized = value.strip().strip("'\"").lower()
    if normalized in PLACEHOLDERS:
        return False
    if normalized.startswith(("${", "{{", "<")):
        return False
    return len(normalized) >= 8


def scan_text(text: str, source: str) -> list[Finding]:
    findings: list[Finding] = []
    source_path = Path(source)

    if source_path.name in ENV_NAMES:
        findings.append(
            Finding("REVIEW_REQUIRED", "environment-file", source, None, ".env系ファイルが外部公開対象に含まれています。")
        )
    if any(part in LOCAL_CONFIG_PARTS for part in source_path.parts):
        findings.append(
            Finding("REVIEW_REQUIRED", "local-configuration", source, None, "ユーザー固有になりやすいローカル設定パスです。")
        )

    for line_number, line in enumerate(text.splitlines(), start=1):
        for kind, pattern, reason in KNOWN_SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(Finding("SENSITIVE", kind, source, line_number, reason))

        for match in ASSIGNMENT_PATTERN.finditer(line):
            if _looks_real(match.group(2)):
                findings.append(
                    Finding("SENSITIVE", "credential-assignment", source, line_number, "認証情報を示す名前へ実値らしい文字列が設定されています。")
                )

        if EMAIL_PATTERN.search(line):
            findings.append(Finding("SENSITIVE", "email-address", source, line_number, "メールアドレス形式の個人情報候補です。"))
        if PHONE_PATTERN.search(line):
            findings.append(Finding("SENSITIVE", "phone-number", source, line_number, "電話番号形式の個人情報候補です。"))
        if LOCAL_PATH_PATTERN.search(line):
            findings.append(
                Finding("REVIEW_REQUIRED", "user-local-path", source, line_number, "ユーザー名を含む可能性がある絶対ローカルパスです。")
            )
        if LABELED_PERSON_PATTERN.search(line):
            findings.append(
                Finding("REVIEW_REQUIRED", "labeled-personal-data", source, line_number, "氏名または住所として記載された情報の候補です。")
            )

    return _deduplicate(findings)


def _deduplicate(findings: Iterable[Finding]) -> list[Finding]:
    return list(dict.fromkeys(findings))


def _decode(data: bytes, source: str, max_bytes: int) -> tuple[str | None, str | None]:
    if len(data) > max_bytes:
        return None, f"{source}: サイズ上限{max_bytes}バイトを超えたため未確認です。"
    if b"\x00" in data:
        return None, f"{source}: バイナリファイルのため未確認です。"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, f"{source}: UTF-8で読み取れないため未確認です。"


def _expand_paths(paths: Iterable[str]) -> Iterable[Path]:
    for raw_path in paths:
        path = Path(raw_path)
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file() and ".git" not in child.parts:
                    yield child
        else:
            yield path


def scan_paths(paths: Iterable[str], max_bytes: int = 1_000_000) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    unknowns: list[str] = []
    for path in _expand_paths(paths):
        source = str(path)
        try:
            data = path.read_bytes()
        except OSError as exc:
            unknowns.append(f"{source}: 読み取り失敗（{exc.__class__.__name__}）")
            continue
        text, unknown = _decode(data, source, max_bytes)
        if unknown:
            unknowns.append(unknown)
            continue
        findings.extend(scan_text(text or "", source))
    return _deduplicate(findings), unknowns


def _staged_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
        check=True,
        stdout=subprocess.PIPE,
    )
    return [item.decode("utf-8") for item in result.stdout.split(b"\x00") if item]


def scan_staged(max_bytes: int = 1_000_000) -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    unknowns: list[str] = []
    for source in _staged_files():
        result = subprocess.run(["git", "show", f":{source}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            unknowns.append(f"{source}: Git indexから読み取れませんでした。")
            continue
        text, unknown = _decode(result.stdout, source, max_bytes)
        if unknown:
            unknowns.append(unknown)
            continue
        findings.extend(scan_text(text or "", source))
    return _deduplicate(findings), unknowns


def classify(findings: Iterable[Finding], unknowns: Iterable[str]) -> str:
    classifications = {finding.classification for finding in findings}
    if "SENSITIVE" in classifications:
        return "SENSITIVE"
    if "REVIEW_REQUIRED" in classifications:
        return "REVIEW_REQUIRED"
    if list(unknowns):
        return "UNKNOWN"
    return "SAFE"


def build_report(findings: list[Finding], unknowns: list[str]) -> dict[str, object]:
    return {
        "status": classify(findings, unknowns),
        "findings": [asdict(finding) for finding in findings],
        "unknowns": unknowns,
        "note": "検出値そのものは出力していません。SAFEは今回読み取れた範囲の判定です。",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="外部公開前の機密・個人・ローカル専用情報候補を読み取り専用で検査します。")
    parser.add_argument("paths", nargs="*", help="検査するファイルまたはディレクトリ")
    parser.add_argument("--staged", action="store_true", help="Git indexへステージされた内容を検査する")
    parser.add_argument("--json", action="store_true", help="JSONで結果を出力する")
    parser.add_argument("--max-bytes", type=int, default=1_000_000, help="1ファイルの読み取り上限")
    args = parser.parse_args()

    if not args.staged and not args.paths:
        parser.error("pathsまたは--stagedのどちらかが必要です。")

    findings: list[Finding] = []
    unknowns: list[str] = []
    if args.paths:
        path_findings, path_unknowns = scan_paths(args.paths, args.max_bytes)
        findings.extend(path_findings)
        unknowns.extend(path_unknowns)
    if args.staged:
        staged_findings, staged_unknowns = scan_staged(args.max_bytes)
        findings.extend(staged_findings)
        unknowns.extend(staged_unknowns)

    report = build_report(_deduplicate(findings), list(dict.fromkeys(unknowns)))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"STATUS: {report['status']}")
        for finding in report["findings"]:
            line = f":{finding['line']}" if finding["line"] else ""
            print(f"- {finding['classification']} {finding['kind']} {finding['source']}{line}: {finding['reason']}")
        for unknown in report["unknowns"]:
            print(f"- UNKNOWN {unknown}")
        print(report["note"])
    return 0 if report["status"] == "SAFE" else 2


if __name__ == "__main__":
    sys.exit(main())
