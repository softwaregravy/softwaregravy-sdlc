---
name: pr-open
description: Open a pull request in this repo, with its title and body. Use for every pull request here; each stage's finish step runs it.
user-invocable: false
---

Open a pull request for the current branch, with a body a reviewer can follow without opening anything else, then stop for the owner to merge.

`$ARGUMENTS` may name a stage and the issue the work is for, such as `intent 12`. Outside a stage, use the issue the work is for, if there is one.

## 1. Check

You are on a branch other than the default branch, everything the pull request should carry is committed, and the branch has commits beyond the default branch. Otherwise, stop and say what is missing.

## 2. Write the body

Write the body to a file, from this template. Skip preambles, keep the prose brief, and use the project's terms from `GLOSSARY.md` where it exists.

```markdown
## Description

<The problem, recapped. Then how this pull request solves it.>

## Summary

<The smallest view that makes the change clear.>

## Edits to earlier documents

- `<path>`: <what changed, and why>

<Anything the stage's skills said this pull request must list.>

Refs #<issue>

Written on `<host>` in session `${CLAUDE_SESSION_ID}`: `claude --resume ${CLAUDE_SESSION_ID}` from this repo there.
```

- **Description:** the reviewer won't reread the issue. Recap its problem in a few sentences: who hits what, and why it matters. Then say how this change solves it, in a few sentences or bullets.
- **Summary:** pick the smallest view that makes the key point clear: pseudocode for logic, a call tree for control flow, a file tree for layout, a Mermaid diagram for interaction, or a `diff` sketch when the point is what changed in a shape that already exists. For a document, a short outline of what it says. Put each view beside the text it supports. One is usually enough.
- **Edits to earlier documents:** each change the branch makes to an `intent.md` or `spec.md` that is already on the default branch. Include the section only when there are some.
- **Refs:** `Closes #<issue>` for a Build pull request, which finishes the issue; `Refs #<issue>` for any other. Include the line only when the work has an issue.
- **Written on:** `<host>` is the output of `hostname`.

## 3. Open it

Push the branch, then run `gh pr create --body-file <file>` with no `--base`. The title is `<stage>: <issue title>`, with the stage in lowercase. Outside a stage, write a short title in the style of the repo's recent pull requests.

Stop and report the pull request's URL. The owner merges.
