---
name: notify-user
description: Present a notification or result to the user without changing external state. Use when a workflow must inform the user about an outcome, warning, blocker, or required next action.
---

# Notify user

Present the supplied message to the user and return control to the calling workflow.

## Function

```text
notify-user(message)
```

- `message` is the complete user-facing message.
- This skill does not access or mutate external systems.
- The calling workflow decides whether to stop after the notification.
