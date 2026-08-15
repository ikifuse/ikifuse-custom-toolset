---
name: action-check
description: Establish and preserve the actions authorized by the user, project rules, and the latest agreement. Use for consultation versus implementation, requests such as “進めてください”, creation or naming with material ambiguity, edits limited to specific files, completed or frozen areas, deletion, installation, Git operations, publishing, out-of-scope findings, or reporting the exact location and role of created artifacts. Do not use it to invent extra approval steps when the requested scope is already clear.
---

# Action Check

Keep the work inside the boundary established by the user's request, applicable project instructions, and the latest explicit agreement. Do not reopen an agreed decision unless the user changes it or inspected evidence shows that the authorized result cannot be completed safely.

## Establish the current boundary

Before acting, identify:

- the requested outcome;
- the current phase: consultation, investigation, implementation, deletion, installation, Git operation, or publication;
- the authorized targets and operations;
- explicit exclusions, frozen areas, and the agreed stopping point;
- whether a material choice remains unresolved.

State this boundary to the user when the work is broad, risky, or easy to misread. For a simple unambiguous edit, proceed without producing a ceremonial checklist.

## Preserve operation boundaries

- Treat consultation as permission to discuss, not implement.
- Treat investigation as read-only unless a change is separately requested.
- Treat permission to edit as permission only for the stated targets.
- Do not derive permission to delete, install, commit, push, publish, message, or modify external state from a different operation.
- When the user explicitly requests an unambiguous chain such as “fix, commit, and push,” complete that chain without asking for the same permission again.
- Treat “進めてください” as authorization for the immediately preceding agreed target and stopping point, not for adjacent work.

Respect higher-level safety confirmations imposed by the environment or tool even when the user has authorized the operation.

## Ask only for material choices

Proceed without asking when the user already supplied the name or location, an established convention yields one reasonable result, or the artifact is an ordinary implementation detail inside the authorized area.

Stop and present concise options when multiple reasonable choices would materially change the delivered artifact, including:

- a new plugin, repository, or top-level directory;
- a name or durable location with no governing convention;
- a change to the canonical source or future editing location;
- a persistent artifact in a location the user may not notice;
- deletion, destructive replacement, or external publication not already authorized.

Create temporary artifacts without another question only inside the authorized workspace or a safe temporary directory, when they are non-canonical, non-persistent, and cannot affect user or external data.

## Protect completed and out-of-scope work

- Treat an area as completed or frozen only when project instructions, approved documents, or the user establish that status. Do not infer it from a name or location.
- Do not change files outside the authorized scope.
- If an out-of-scope issue affects the correctness, safety, or completion of the authorized work, stop and report the fact and impact.
- If it does not affect the authorized result, finish the requested work and report the finding briefly without fixing it.
- Do not mix optional improvements or unrelated ideas into the current implementation or completion report.

## Use evidence when the action depends on a claim

Invoke an available evidence-audit workflow when an action depends on a factual conclusion, such as deletion safety, provenance, current official behavior, or whether a generated artifact matches its source.

For conditional deletion such as “delete it if safe,” delete only when the required safety conclusion is confirmed. Do not delete when the conclusion is partial, conflicted, or unknown.

## Execute and verify the authorized scope

1. Inspect the starting state needed to distinguish existing changes from this task.
2. Modify only the authorized targets.
3. Run validation proportional to the risk.
4. Compare the final changed paths with the authorized scope.
5. Do not stage unrelated files or use broad staging that would mix other work into the task.
6. Before an explicitly requested commit or push, require an unambiguous repository, branch, and change scope; successful required checks; and no unresolved conflict or unrelated staged change.

## Report in proportion to the work

For a small verified edit, report the changed target and the check that actually ran. Do not claim “no impact” unless inspected evidence supports that conclusion.

For creation, relocation, or important changes, report:

- current state;
- what was created or changed;
- exact path or external location;
- whether it is the editable canonical source, installed copy, generated output, or temporary artifact;
- what remained unchanged;
- validation results and remaining unknowns;
- the next action required from the owner, or that none is required.

When waiting for a decision, report the single material choice, concise options, a recommendation when useful, and what will happen after the choice. Keep reports readable and avoid forcing the owner to perform a technical diff review.
