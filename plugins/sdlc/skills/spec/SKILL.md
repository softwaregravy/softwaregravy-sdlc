---
name: spec
description: Run the Spec stage for a GitHub issue whose intent.md is on the default branch. Ends with a pull request carrying its spec.md.
argument-hint: <issue number>
disable-model-invocation: true
---

Follow `${CLAUDE_PLUGIN_ROOT}/stage.md`, with:

- **S**, the stage: `spec`
- **N**, the GitHub issue number: `$ARGUMENTS`
- **The session id:** `${CLAUDE_SESSION_ID}`
