---
name: action-check
description: Establishes and preserves the actions authorized by the user, then verifies that actual changes stayed inside that boundary. Use for consultation versus implementation, requests such as 進めてください, scoped edits, completed or frozen areas, deletion, overwrite, bulk or hard-to-recover changes, installation, Git operations, publishing, out-of-scope findings, or reporting created artifacts.
---

# Action Check

Keep the work inside the boundary established by the user's request, applicable project instructions, and the latest explicit agreement. Do not reopen an agreed decision unless the user changes it or inspected evidence shows that the authorized result cannot be completed safely.

Use four internal safeguards as parts of this skill, not as separate skills:

- **Authorization Boundary:** determine what may be done.
- **Scope Diff Guard:** distinguish the starting state from this task and reconcile actual changes with the authorized scope.
- **Recovery Guard:** when failure would be costly, determine whether the affected state can actually be restored.
- **Destructive Guard:** apply stricter gates to deletion, irreversible changes, and operations with substantial loss potential.

Select only the safeguards required by the operation. Ordinary, clearly authorized, non-destructive edits should remain lightweight.

## Establish the current boundary

Before acting, identify:

- the requested outcome;
- the current phase: consultation, investigation, implementation, deletion, installation, Git operation, or publication;
- the authorized targets and operations;
- explicit exclusions, frozen areas, and the agreed stopping point;
- whether a material choice remains unresolved.

State this boundary to the user when the work is broad, risky, or easy to misread. For a simple unambiguous edit, proceed without producing a ceremonial checklist.

## Record the starting state

Before modifying files, capture enough baseline evidence to separate pre-existing work from task changes. In a Git worktree, normally inspect the relevant parts of:

- working-tree, index, and untracked status;
- changed paths and, when attribution matters, their relevant diffs or fingerprints;
- the authorized targets, explicit exclusions, and frozen areas.

Limit the baseline to the scope needed for reliable attribution. Do not read unrelated sensitive content merely to create a baseline. Treat recorded pre-existing changes as protected user work: do not edit, stage, revert, delete, or claim them as task output unless the user explicitly includes them.

A path that first appears changed during the task is not by itself proof that this agent caused it. Combine the baseline with the operations actually performed. Classify a material change as:

- `PRE_EXISTING`: present at the baseline and not changed by this task;
- `TASK_CHANGE`: produced by an authorized operation in this task;
- `OUT_OF_SCOPE_TASK_CHANGE`: attributable to this task but outside its authorization;
- `UNKNOWN`: its source cannot be established, including possible concurrent user or tool changes.

Never convert `UNKNOWN` into `TASK_CHANGE` merely because of timing.

## Preserve operation boundaries

- Treat consultation as permission to discuss, not implement.
- Treat investigation as read-only unless a change is separately requested.
- Treat permission to edit as permission only for the stated targets.
- Do not derive permission to delete, install, commit, push, publish, message, or modify external state from a different operation.
- When the user explicitly requests an unambiguous chain such as “fix, commit, and push,” complete that chain without asking for the same permission again.
- Treat “進めてください” as authorization for the immediately preceding agreed target and stopping point, not for adjacent work.

Respect higher-level safety confirmations imposed by Antigravity, the operating environment, or a tool even when the user has authorized the operation.

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

Use `evidence-audit` when an action depends on a factual conclusion, such as deletion safety, provenance, references and dependencies, downstream effects, current official behavior, or whether a generated artifact matches its source. Let that skill collect and grade the evidence; Action Check uses the result to decide whether the authorized operation may continue and does not duplicate the investigation.

For conditional deletion such as “delete it if safe,” delete only when the required safety conclusion is confirmed. Do not delete when the conclusion is partial, conflicted, or unknown.

## Apply Recovery Guard only when needed

Use Recovery Guard before deletion, destructive or complete overwrite, bulk replacement, structural change, irreversible transformation, or another operation whose recovery cost is material. For untracked or uncommitted-only data, treat Git state as a risk multiplier only when the planned operation could materially lose the original content or make it costly to reconstruct; untracked status alone is not a trigger. Do not activate Recovery Guard for a small, bounded, non-destructive edit with a clear inverse change merely because the target is untracked or uncommitted. Skip it for ordinary small edits that have a clear validation and correction path.

Determine, as relevant:

- whether each target is tracked, untracked, ignored, staged, modified, or committed;
- which exact revision, backup, or separate copy could restore it;
- whether uncommitted or untracked information would be lost;
- whether the proposed restoration procedure is actually available and sufficient.

Do not equate “inside a Git repository” with “recoverable.” A committed tracked version may be recoverable from an identified revision; untracked content and uncommitted portions are not recoverable from Git unless an inspected source contains them.

If recovery matters and no viable route is established, report that gap and stop before the risky operation. Do not create a backup, copy, commit, stash, or restore point unless that operation is already authorized or the owner approves it.

## Apply Destructive Guard to loss-capable operations

Treat file or directory deletion, `rm` or `rm -rf`, forced overwrite, `git reset --hard`, `git clean`, force push, history rewriting, bulk replacement, lossy transformation, and comparable operations more strictly than normal editing.

Before proceeding, require:

1. an exact, resolved target and complete intended scope;
2. authorization for the destructive operation itself, not merely for inspection or editing;
3. sufficient evidence about references, dependencies, downstream effects, and remaining unknowns when those facts affect safety;
4. a Recovery Guard result appropriate to the potential loss;
5. no material conflict between the requested outcome and project rules.

Do not use unresolved variables, broad roots, or ambiguous globs as destructive targets. Resolve and inspect the exact target first. If the operation is conditional on safety, stop when evidence is partial, conflicted, unknown, or when target, authorization, impact, or recovery remains materially unclear.

Detecting danger does not authorize remediation. Do not automatically delete, revert, rewrite, mask, back up, commit, or otherwise alter state. Report the issue and the bounded next action that would require permission.

## Coordinate external disclosure without merging responsibilities

For commit, push, pull request, issue, publication, or another external disclosure:

- let Action Check determine whether the operation and its change scope are authorized;
- let `secret-privacy-guard` determine whether the exact outbound information may leave the local boundary;
- use `evidence-audit` only for material factual questions requiring more evidence.

Authorization does not imply disclosure safety, and a privacy result does not authorize the operation.

## Execute and verify the authorized scope

1. Establish the Authorization Boundary and record the relevant starting-state baseline.
2. Select Recovery Guard or Destructive Guard only if the planned operation warrants it.
3. Modify only the authorized targets and keep a record of operations actually performed.
4. Run validation proportional to the risk.
5. Reinspect actual working-tree and index changes and compare them with both the baseline and authorized scope.
6. Classify material paths as `PRE_EXISTING`, `TASK_CHANGE`, `OUT_OF_SCOPE_TASK_CHANGE`, or `UNKNOWN`.
7. Do not automatically revert or delete an out-of-scope or unknown change. If an attributable out-of-scope change affects correctness or safety, do not report the work as complete; report its path and impact.
8. Do not stage unrelated files or use broad staging that would mix other work into the task.
9. Before an explicitly requested commit or push, require an unambiguous repository, branch, and change scope; successful required checks; no unresolved conflict or unrelated staged change; and the applicable `secret-privacy-guard` result. Do not ask again for the already explicit commit or push permission.

## Report in proportion to the work

For a small verified edit, report the changed target and the check that actually ran. Do not claim “no impact” unless inspected evidence supports that conclusion.

For creation, relocation, or important changes, report:

- current state;
- what was created or changed;
- exact path or external location;
- whether it is the editable canonical source, installed copy, generated output, or temporary artifact;
- what remained unchanged;
- the final scope comparison, including any protected pre-existing, out-of-scope, or `UNKNOWN` change that matters;
- validation results and remaining unknowns;
- the next action required from the owner, or that none is required.

When waiting for a decision, report the single material choice, concise options, a recommendation when useful, and what will happen after the choice. Keep reports readable and avoid forcing the owner to perform a technical diff review.
