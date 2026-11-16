---
name: intent
description: Run the Intent stage for a GitHub issue. Ends with a pull request carrying the issue's intent.md.
argument-hint: <issue number>
disable-model-invocation: true
---

Follow `${CLAUDE_PLUGIN_ROOT}/stage.md`, with:

- **S**, the stage: `intent`
- **N**, the GitHub issue number: `$ARGUMENTS`
- **The session id:** `${CLAUDE_SESSION_ID}`
