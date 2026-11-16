---
name: intent-interview
description: The Intent stage's do step. Interview the owner about one issue and write its intent.md. Runs under /sdlc:intent, at intent.do.
user-invocable: false
---

Turn one issue into one clear intent: what the owner wants and why, written so that a spec can be built from it without going back to them. You build what you believe the owner wants, and that belief is usually thinner than it feels. The interview is how you find out.

`$ARGUMENTS` is the stage and the GitHub issue number, such as `intent 12`. The stage command has already created this stage's branch. If you are on the default branch, stop and say so.

## 1. Look before asking

Read until you could explain how the relevant parts of the project work today and what this change would touch, and until you know which open issues and which intents in `features/active/` overlap it. Start from the issue and its comments and the project's `CLAUDE.md`, then follow what you find.

Facts are yours to find; decisions are the owner's. Ask only what the repo and the tracker can't answer.

When the tracker is too long to skim, send a Haiku subagent through it to nominate candidates: issue numbers and a few words each, erring toward too many. Read the nominees yourself and decide.

## 2. Open

Send one message, in this order:

- The issue in your own words, so the owner can see whether you have its shape.
- What you found that bears on it: what it would touch, and anything that would change what is being asked, such as a conflict, a constraint, or something that already does part of it.
- A split or a merge, if one fits (below).
- One open question about why they want it, with no options attached: options steer. If the issue already says why, play that back instead and go straight to the rounds.

## 3. Rounds

Each round asks the frontier: every open question whose prerequisites are settled. Work roughly in the order of the template's sections, since a later section usually rests on an earlier one.

- Number the questions, and give each a recommended answer worded so that "yes" accepts it.
- Build each question on what the owner said or what you found, so it helps them think through a case they may have missed. When it isn't plain, say what the answer would change.
- When the owner describes how to build it, ask whether that is a requirement. A requirement is a constraint. Anything else goes in `notes.md` beside the intent, for the spec stage.

The interview is done when the frontier is empty, or when the owner says to write it. Whatever is still open then gets your answer, as a Claude decision.

## Split and merge

Propose a split when the issue holds outcomes that could each ship and be useful alone, either at the opening or whenever the intent grows to that size. Propose a merge when another open issue wants the same outcome, or would be changed by the same work. A plain yes from the owner is enough for either.

- **Split:** open a new issue for each other piece, carrying what is known about it and linking to this one. This issue keeps the piece being interviewed. Comment here with links to the new issues.
- **Merge:** close each other issue with a comment pointing here. Its asks become part of this interview.

## 4. Write

Write `features/active/<issue#>-<slug>/intent.md` from `${CLAUDE_SKILL_DIR}/template.md`. The slug is a few words of the issue title, lowercase and hyphenated.

- What the owner said goes in as theirs. Everything you filled in goes in Claude decisions: a default the owner never heard is one they couldn't reject.
- If the session researched anything beyond the repo and the tracker, write it to `research.md` beside the intent, with its sources, so the findings outlive the session.

Show the owner the draft and ask what is wrong or missing. Apply their corrections, and commit the folder when they have none left.

## 5. Fix review findings

The review step hands its merged findings back to this session, once. Sort them:

- **Answered already** by the interview or the project: put the answer in the intent.
- **Minor:** a spec writer could settle it without changing what gets built. Settle it yourself, as a new Claude decision.
- **The owner's:** only they can answer it, and the answer changes what gets built. Ask all of these in one message, most important first.

Commit the fixes.
