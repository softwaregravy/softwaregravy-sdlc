---
name: review-intent
description: The Intent stage's review step. Check an intent.md from a fresh context: is it clear, consistent and complete, and should it split? Runs under /sdlc:intent, at intent.review.
user-invocable: false
---

`$ARGUMENTS` is the stage and the GitHub issue number, such as `intent 12`. Review that issue's intent, in `features/active/<issue#>-<slug>/intent.md`. You have nothing from the session that wrote it, and that is the test: the intent has to stand on its own.

Read the intent; the template it was written from, `${CLAUDE_SKILL_DIR}/../intent-interview/template.md`; the issue and its comments; and the project's `CLAUDE.md`, glossary and ADRs where they exist.

Apply every check below. Your output is findings only: the session that wrote the intent fixes them.

## Builder check

You will write the spec from this intent, and you can't talk to the owner. Where would you have to guess, with a wrong guess changing what gets built? Skip what the intent deliberately leaves to the spec, anything you could reasonably decide yourself, and wording nitpicks.

## Clear

- Every term is defined, or is one the project already uses.
- Every adjective that needs a number or an example has one, such as "fast", "large" or "simple".

## Consistent

- Each acceptance criterion traces to the proposed outcome.
- Nothing in out of scope contradicts a criterion or a constraint.
- No constraint conflicts with `CLAUDE.md` or an ADR. Report a conflict; resolving it is the owner's call.
- Each ask in the issue is either covered or listed as out of scope.

## Complete

- All seven sections are present, in the template's order, and an empty one says *None*.
- The outcome and the criteria describe behaviour someone can observe. Any design in them is a finding.
- A choice the intent states as settled, which neither the issue nor a Claude decision accounts for, is a Claude call that went unlisted.

## Split

- The intent holds outcomes that could each ship and be useful alone, or criteria that fall into groups sharing nothing.
