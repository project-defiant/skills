---
name: create-topic-note
description: Create a user-selected Obsidian topic note from reviewed research. Use when the user explicitly asks to record a novel concept, method, or phrase introduced by a source note.
---

# Create topic note

Read `/Users/ss60/.agents/skills/vault/references/project-schema.md` before acting.

1. Require the user to identify the concept, method, or phrase to capture.
2. Locate the relevant source note and annotation links.
3. Draft a concise topic note under `$SZYMON_WIKI/../Topic-notes/`, named after the selected topic.
4. Include frontmatter for title, `kind: topic-note`, tags, projects, source notes, and source papers.
5. Use a compact structure:

   ```markdown
   > [!definition]
   > …

   ## Core statements

   > [!claim]
   > …

   ## Notes
   ```

6. Preserve supporting PDF annotation links and links to source notes.
7. Show the path and full proposed content for approval before creating or updating the note.

Do not update project requirements, PRDs, Linear, or `log.md`.
