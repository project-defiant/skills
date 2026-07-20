---
name: to-prd
description: Turn the current conversation context into a PRD and submit it to Wiki. Use when user wants to create a PRD from the current context.
---

Turn the current conversation context and your codebase understanding into a PRD,
then submit that PRD as a document to the Szymon WIKI.

Do not interview the user. Synthesize from what is already known in the conversation
and from the repository. Only ask the user something if issue creation is blocked by
missing access or missing repository information.

## Process

1. Explore the repo to understand the current state of the codebase if you have not
   already done so.
2. Sketch the major modules that would need to be built or modified to implement the
   feature. Prefer deep modules: simple, stable interfaces that hide meaningful
   complexity and can be tested in isolation.
3. Decide which modules should have tests written for them. Base this on risk,
   surface area, and whether the behavior can be validated externally.
4. Write the PRD using the template below.
5. Find the WIKI, use vault skills to explore how to add a document to the WIKI
6. Add document to WIKI.

When you write the PRD:

- Write from the user's perspective.
- Be concrete and exhaustive.
- Make the user stories extremely extensive and cover the full feature surface,
  edge cases, failure cases, and operational flows.
- Include implementation and testing decisions that follow from the current
  conversation and codebase state.
- Do not include specific file paths or code snippets.
- Do not invent decisions that conflict with the current conversation.

When you write to the WIKI:

- Use a clear title that describes the feature or PRD topic.
- Use the PRD body as the issue body.
- If issue creation fails, surface the failure plainly instead of pretending it worked.

Use this template exactly:

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.
