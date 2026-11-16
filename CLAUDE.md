# CLAUDE.md

A software development lifecycle packaged as Claude Code plugins. This repo is a plugin marketplace: `plugins/sdlc` is the core, and each stack layer (a language, framework or hosting platform) is a further plugin beside it. `PLAN.md` is the roadmap, the decisions behind it, and the current phase.

This repo opts in to itself: its development process comes from its own `sdlc` plugin, installed from the GitHub source like any other project's. A session here opens with the line `SDLC plugin active: sdlc`. If that line is missing, the plugin isn't set up on this machine: say so before anything else, and point to "Setting up a machine" in `README.md`.

## Rules

- **This repo stands alone.** It names no other repo of the owner's: no paths, links or calls into them. Other repos reference this one.
- **Layers start empty.** A rule, standard or default reaches a layer only through an issue on this repo. Add a layer when its first approved rule needs one.
- **`version` stays out of every `plugin.json`.** Setting it pins installed copies to that version until it is bumped; left out, a merge to the default branch reaches projects on their next marketplace update.
- **Plugin text is public and reusable.** Write "the owner" for the person who merges, and keep machine names and personal tooling out of anything under `plugins/`.
- **Until phase 3 of `PLAN.md`,** changes land as ordinary single-concern pull requests. From phase 3 on, every change goes through this repo's own pipeline.

## Checks

```bash
python3 -m unittest discover -s tests   # needs Python 3.11+
claude plugin validate .                # the marketplace and every plugin it lists
```

`claude plugin validate --strict` fails here by design: it treats the missing `version` as an error.

## Trying a change

A session here runs the copy installed from the default branch, not this checkout's. To run the checkout's copy, start the session with `claude --plugin-dir plugins/sdlc`. It replaces the installed copy for that session only and reads the files in place, so an edit takes effect at the next session. A stage run in such a session uses the branch's skills.

`claude plugin marketplace remove`, run inside a project, also empties `enabledPlugins` and `extraKnownMarketplaces` in that project's tracked `.claude/settings.json`. Check `git diff` afterwards.
