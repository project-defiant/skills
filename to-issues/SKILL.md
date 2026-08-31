---
name: to-issues
description: Break a plan, spec, or PRD into independently-grabbable Linear issues using tracer-bullet vertical slices. Use when user wants to convert a plan into Linear implementation tickets or break down work into Linear issues.
---

# To Issues

Break a plan into independently-grabbable Linear issues using vertical slices (tracer bullets).

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a GitHub issue number or URL as an argument, fetch it with `gh issue view <number>` (with comments).
If the user passes a WIKI project, explore it first using vault skill. Require an
explicit `vault=<name|id>`, project name, and selected PRD.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code.

### 3. Draft vertical slices

Break the plan into **tracer bullet** issues. Each issue is a thin vertical slice that cuts through ALL integration layers end-to-end, NOT a horizontal slice of one layer.

Slices may be 'HITL' or 'AFK'. HITL slices require human interaction, such as an architectural decision or a design review. AFK slices can be implemented and merged without human interaction. Prefer AFK over HITL where possible.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 4. Quiz the user

Present the proposed breakdown as a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Type**: HITL / AFK
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices marked as HITL and AFK?

Iterate until the user approves the breakdown.


### 5. Create Linear issues

Read the selected PRD and the project's `linear_project` link through the Vault
workflows. Treat the Wiki as read-only. For each approved slice, invoke the existing
Linear `create-issue` workflow with the slice title and description. Do not call
Linear atomic connector operations directly from this skill.

Create all approved issues first without dependency relations and collect their real
Linear identifiers. Then, in a second pass, invoke the existing Linear `update-issue`
workflow to add `blockedBy` and `blocks` relations between issues created in this run.
If a relation update fails, continue with the remaining updates and report all
failures. Never roll back successfully created issues.

<issue-template>
## What to build

A concise description of this vertical slice. Describe the end-to-end behavior, not layer-by-layer implementation.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

</issue-template>

Return the created Linear issue links and identifiers. If issue creation fails,
stop the workflow without rolling back issues already created and report the failure
plainly. Do not create GitHub issues, milestones, or modify Wiki files.
