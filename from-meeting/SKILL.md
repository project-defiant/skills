---
name: from-meeting
description: Append a user-selected item to a project's single Obsidian meeting summary. Use when the user asks to add content to today's meeting summary or project meeting note.
---

# From meeting

Read `/Users/ss60/.agents/skills/vault/references/project-schema.md` before acting.

1. Resolve the project and date; use today's local date only when the user says today's meeting.
2. Extract only the purpose and decisions the user explicitly provides or selects.
3. Propose the appended block for `Meetings.md`:

   ```markdown
   ## YYYY-MM-DD — Purpose

   **Decisions**

   - Decision
   ```

4. Obtain approval, then append the block at the bottom of the file.

Do not update requirements, PRDs, Linear, or `log.md`. A decision can be transferred later only at the user's request.
