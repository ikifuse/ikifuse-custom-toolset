---
name: evidence-audit
description: Investigate claims and decisions with evidence before reporting them as confirmed. Use for requests containing verify, confirm, investigate, audit, fact-check, evidence, no speculation, unknowns, deletion safety, root-cause analysis, historical context, or high-confidence conclusions, including Japanese requests such as 確認, 実質調査, 嘘・憶測禁止, 事実のみ, 中身も調べる, or 削除してよいか; especially when local files, Git history, prior agent sessions, official documentation, or external sources may need cross-checking.
---

# Evidence Audit

Investigate to the depth required by the requested conclusion. Treat “確認” as an evidence-sufficiency claim, not as merely looking at one source.

## Establish the claim boundary

1. Restate the exact claim or decision to establish.
2. List the subclaims that must be true for that conclusion.
3. Identify the evidence lanes capable of proving or disproving each subclaim.
4. Do not expand a narrow request into unrelated research.

Typical evidence lanes include:

- current artifacts and their complete relevant contents;
- references, imports, links, callers, and downstream consumers;
- Git status, log, blame, introduction commit, deletions, and renames;
- prior agent history through an available history-search skill or tool;
- official primary documentation for current product behavior;
- runtime output, tests, logs, metadata, or external authoritative sources.

History is one evidence lane, never proof of current state by itself. Official documentation is one evidence lane, never proof of the user's local state by itself.

## Select sources deliberately

For every evidence lane, record one of:

- `examined`: inspected sufficiently for the subclaim;
- `partial`: inspected, but known gaps remain;
- `unavailable`: access or tooling is unavailable;
- `not needed`: irrelevant to the conclusion, with a short reason.

If prior agent sessions may contain relevant intent, decisions, attempts, or provenance, use an available history-search capability such as `ctx-agent-history-search`. Confirm its readiness first. Inspect focused events or sessions before relying on search snippets. Report index failures, stale records, unavailable raw sources, and excluded sources.

For current or changeable OpenAI product behavior, use the official OpenAI documentation capability and cite the fetched page. Do not substitute history or memory for current specifications.

Use read-only investigation unless the user separately authorizes changes. A request to investigate, verify, audit, or report does not authorize deletion or repair.

## Collect and challenge evidence

1. Inspect the strongest direct source first.
2. Cross-check important conclusions with an independent evidence lane when practical.
3. Search for disconfirming evidence, not only supporting evidence.
4. Distinguish absence of evidence from evidence of absence.
5. Do not infer intent from timestamps, paths, names, similarity, or proximity alone.
6. Do not infer that duplicate-looking artifacts are interchangeable; compare their relevant contents and consumers.
7. For deletion safety, establish all of the following before recommending deletion:
   - exact target and complete contents;
   - tracked or untracked state;
   - origin and history, including introduction when Git records it;
   - references and runtime discovery paths;
   - overlap with canonical artifacts;
   - consequences of removal and recovery route;
   - remaining unknowns.

When tools fail or outputs are truncated, retry with a narrower query or alternate source. If the gap remains, preserve it as an unknown; never silently fill it.

## Classify every material statement

Use these labels internally and expose them when the distinction matters:

- `VERIFIED`: directly supported by inspected evidence;
- `SYNTHESIS`: reasoned conclusion from identified verified facts;
- `CONFLICTED`: credible evidence disagrees;
- `UNKNOWN`: required evidence was not obtained;
- `NOT_CHECKED`: outside the examined scope.

Never convert `SYNTHESIS`, `UNKNOWN`, or `NOT_CHECKED` into “confirmed.” Never say a tool decided something unless its source text explicitly states that decision.

## Calculate conclusion coverage

Before reporting, assign the overall conclusion one status:

- `CONFIRMED`: every required material subclaim has sufficient evidence and no unresolved contradiction changes the conclusion;
- `PARTIAL`: useful evidence exists, but one or more material gaps remain;
- `CONFLICTED`: evidence supports incompatible conclusions;
- `UNKNOWN`: evidence is insufficient to choose responsibly.

Source count does not determine coverage. Coverage depends on whether the required subclaims were established.

## Report evidence before confidence

Lead with the conclusion status and answer. Then provide:

1. verified facts and their sources;
2. synthesis, explicitly labeled;
3. conflicts and unknowns;
4. evidence-lane coverage;
5. recommended action and its safety boundary;
6. what was not done, especially destructive or external actions.

For history-derived findings, include provider, session ID, event ID when available, and source status without exposing unnecessary private transcript content. For web findings, cite the supporting primary page near the claim.

Use precise language:

- Say “I examined X and found Y,” not “I checked everything,” unless the defined evidence set was actually exhausted.
- Say “no reference was found in the searched scope,” not “there are no references,” unless the search scope is demonstrably complete.
- Say “Git does not record the origin” when appropriate, rather than inventing an origin.

Stop and request direction only when a missing choice would materially change the authorized outcome. Otherwise complete all safe, relevant, read-only investigation first.
