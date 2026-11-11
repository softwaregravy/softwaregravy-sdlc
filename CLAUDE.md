# CLAUDE.md

A software development lifecycle packaged as Claude Code plugins. This repo is a plugin marketplace: `plugins/sdlc` is the core, and each stack layer (a language, framework or hosting platform) is a further plugin beside it. `PLAN.md` is the roadmap, the decisions behind it, and the current phase.

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

A marketplace added from a local path is read in place, so an edit takes effect at the next session or on `/reload-plugins`. To load one plugin into a single session without registering anything, run `claude --plugin-dir plugins/sdlc`.

`claude plugin marketplace remove`, run inside a project, also empties `enabledPlugins` and `extraKnownMarketplaces` in that project's tracked `.claude/settings.json`. Check `git diff` afterwards.
