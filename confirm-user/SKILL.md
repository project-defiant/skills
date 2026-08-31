---
name: confirm-user
description: Ask the user for explicit confirmation before a consequential action. Use when a workflow is ready to create, modify, link, or otherwise change user data or external state.
---

# Confirm user

Present the action summary to the user and wait for an explicit response before the calling workflow continues.

## Function

```text
confirm-user(prompt)
```

- `prompt` is the complete action summary requiring confirmation.
- Return `confirmed: true` only for an explicit affirmative response.
- Return `confirmed: false` for a negative response, cancellation, or no response.
- This skill does not access or mutate external systems.

## Output

```json
{
  "confirmed": true
}
```
