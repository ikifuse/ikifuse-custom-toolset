---
name: secret-privacy-guard
description: Inspect information immediately before external disclosure and classify whether it is safe to send. Use before git commit or push, pull requests, GitHub issues, external-service submissions, public artifact generation, or sharing logs and configuration files; especially for API keys, tokens, passwords, private keys, .env secrets, credentials, personal information, cookies, sessions, user-specific paths, and local-only settings. Do not use for routine local editing or simple read-only checks that have no external disclosure path.
---

# Secret & Privacy Guard

Determine whether the exact information about to leave the local boundary can be disclosed. Keep this responsibility separate from whether an action is authorized and whether a factual conclusion has enough evidence.

## Preserve the three responsibilities

- Let `action-check` decide whether the external operation is authorized and what its scope is.
- Use this skill to inspect whether the scoped information may leave the local environment.
- Invoke `evidence-audit` only when classification requires additional evidence, such as whether a value is already public, synthetic, canonical, revoked, or still in use.
- Do not replace or duplicate either skill's decision.

## Trigger only at a disclosure boundary

Run immediately before content crosses into Git history, a remote repository, a pull request, an issue, a message, an external API or service, a public artifact, or a shared log or configuration file.

Do not burden routine local editing, local-only generation, or simple read-only investigation when no external disclosure is planned. If an external action becomes planned later, inspect the final outbound scope at that point.

## Establish the exact outbound scope

Identify the material that will actually leave the local boundary:

- for commit, inspect the staged snapshot rather than only the working tree;
- for push, inspect commits and files not yet present on the destination remote;
- for a pull request, inspect its complete diff, generated files, and relevant metadata;
- for an issue or external message, inspect the final title, body, attachments, pasted logs, and links;
- for public artifacts, inspect the generated output as well as embedded metadata and source-derived content;
- for shared logs or configuration, inspect the exact copy being sent.

Record any unreadable, excluded, binary, oversized, generated, or externally stored part as unexamined. Do not classify the whole scope as safe when a material part was not inspected.

## Inspect candidate information

Check at least:

- API keys, access tokens, passwords, private keys, and credential assignments;
- `.env` files and environment-specific secret values;
- session identifiers, cookies, authentication headers, and saved login material;
- email addresses, phone numbers, addresses, names, account identifiers, and personal data in logs;
- user-specific absolute paths and usernames;
- local-only settings, machine configuration, internal endpoints, and files that should not enter GitHub;
- encoded, generated, historical, or indirect copies of the same data.

Treat automated pattern matches as candidates, not proof of complete coverage. Names and addresses often require contextual inspection. Search for disconfirming context such as placeholders, synthetic fixtures, already-public contact information, or revoked credentials, and use `evidence-audit` when that distinction matters.

## Use the read-only scanner

Run the bundled scanner when the target consists of local text files:

```bash
python3 scripts/scan_sensitive.py --staged
python3 scripts/scan_sensitive.py path/to/file path/to/directory
```

The scanner reports candidate type, path, line, and reason without printing the detected value. It does not modify files. It cannot prove absence, reliably identify every personal name or address, inspect inaccessible external content, or replace contextual review.

## Classify the result

- `SAFE`: No disclosure problem was found in the scope that was actually inspected. State the inspected scope and any exclusions; never translate this into universal absence.
- `SENSITIVE`: A secret, credential, private key, personal datum, or other information requiring protection was found.
- `REVIEW_REQUIRED`: A candidate such as a user-specific path, local setting, ambiguous personal datum, or uncertain disclosure policy needs an owner decision or more evidence.
- `UNKNOWN`: A material part of the outbound scope could not be inspected.

If sensitive information is found while other material remains unknown, report both the sensitive finding and the unknown coverage instead of hiding either.

## Stop safely on findings

Do not delete, rewrite, redact, mask, rotate, revoke, unstage, commit, push, publish, or send anything merely because a problem was detected.

Before changing a finding, require that the user explicitly authorizes that exact operation. Permission to inspect is not permission to repair. Permission to mask one copy is not permission to rotate credentials, alter source data, rewrite Git history, or publish the result.

When a finding blocks an authorized external action, report:

- what category was detected without exposing the value;
- which file or outbound item contains it;
- why it is risky;
- whether it appears capable of reaching the external destination;
- the recommended response;
- whether a bounded automatic fix appears possible;
- any unexamined scope or unresolved classification.

Resume the external action only after the finding is resolved or the owner makes an informed disclosure decision within applicable policy. Re-scan the final outbound material after any authorized correction.

## Coordinate the external action

Use this order when all three skills are relevant:

1. Use `action-check` to establish that the external action and its scope are authorized.
2. Use `secret-privacy-guard` to inspect the exact outbound information.
3. Use `evidence-audit` only for material classification questions that need additional evidence.
4. Continue only when the external action remains authorized and the privacy result permits disclosure.

Never let a `SAFE` result authorize an action. Never let action authorization imply that the information is safe to disclose.
