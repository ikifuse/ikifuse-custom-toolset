#!/usr/bin/env python3
"""Regression checks for the Action Check policy contract."""

from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"


def require(case: str, *phrases: str) -> None:
    text = SKILL.read_text(encoding="utf-8")
    missing = [phrase for phrase in phrases if phrase not in text]
    if missing:
        raise AssertionError(f"{case}: missing {missing}")
    print(f"PASS: {case}")


def main() -> None:
    require(
        "1 small untracked edit stays lightweight",
        "For a simple unambiguous edit, proceed without producing a ceremonial checklist.",
        "Ordinary, clearly authorized, non-destructive edits should remain lightweight.",
        "untracked status alone is not a trigger",
        "Do not activate Recovery Guard for a small, bounded, non-destructive edit",
    )
    require(
        "2 out-of-scope task change is detected",
        "`OUT_OF_SCOPE_TASK_CHANGE`",
        "do not report the work as complete",
    )
    require(
        "3 pre-existing changes are separated and protected",
        "`PRE_EXISTING`",
        "Treat recorded pre-existing changes as protected user work",
    )
    require(
        "4 tracked deletion requires a real recovery source",
        "which exact revision, backup, or separate copy could restore it",
        "A committed tracked version may be recoverable from an identified revision",
    )
    require(
        "5 untracked deletion is not called Git-recoverable",
        "untracked content and uncommitted portions are not recoverable from Git",
    )
    require(
        "6 rm-rf activates destructive safeguards",
        "`rm` or `rm -rf`",
        "an exact, resolved target and complete intended scope",
    )
    require(
        "7 conditional deletion stops without confirmed evidence",
        "delete only when the required safety conclusion is confirmed",
        "Do not delete when the conclusion is partial, conflicted, or unknown.",
    )
    require(
        "8 ordinary edits skip recovery and destructive overhead",
        "Skip it for ordinary small edits",
        "Select only the safeguards required by the operation.",
    )
    require(
        "9 explicit commit-push permission is not requested twice",
        "complete that chain without asking for the same permission again",
        "the applicable `secret-privacy-guard` result",
    )
    require(
        "10 final actual scope is reconciled with baseline and authorization",
        "compare them with both the baseline and authorized scope",
        "`UNKNOWN`",
        "Never convert `UNKNOWN` into `TASK_CHANGE` merely because of timing.",
    )


if __name__ == "__main__":
    main()
