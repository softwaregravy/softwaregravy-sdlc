---
name: build
description: Run the Build stage for a GitHub issue whose spec.md is on the default branch. Ends with a pull request carrying plan.md and the code.
argument-hint: <issue number>
disable-model-invocation: true
---

Follow `${CLAUDE_PLUGIN_ROOT}/stage.md`, with:

- **S**, the stage: `build`
- **N**, the GitHub issue number: `$ARGUMENTS`
- **The session id:** `${CLAUDE_SESSION_ID}`
