# softwaregravy-sdlc

A software development lifecycle packaged as Claude Code skills. A project opts in, names its stack, and gets its process from here: an idea becomes a GitHub issue, then an intent, a spec, and a reviewed pull request, with a human merge at each stage.

It follows Anthropic's [AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook).

**Status: early.** The core plugin is a walking skeleton. [`PLAN.md`](PLAN.md) holds the design, the decisions and the phases.

## How it is organised

- **`plugins/sdlc`** is the core plugin: the pipeline, the pull request rules and repo setup.
- **Stack layers** are further plugins beside it, one per language, framework or hosting platform. Each is created the first time a rule needs it.
- **A pipeline manifest** in each plugin lists the skills that run in each step of each stage. A project can add, remove or replace entries in `.sdlc/pipeline.toml`.

## Opting a project in

Add this to the project's `.claude/settings.json`, listing every plugin you want, including the ones a layer depends on:

```json
{
  "extraKnownMarketplaces": {
    "softwaregravy-sdlc": {
      "source": { "source": "github", "repo": "softwaregravy/softwaregravy-sdlc" }
    }
  },
  "enabledPlugins": {
    "sdlc@softwaregravy-sdlc": true
  }
}
```

Then, once per machine, register the marketplace from inside the project:

```bash
claude plugin marketplace add softwaregravy/softwaregravy-sdlc --scope local
```

To work on the skills themselves, give that command the path of a local clone instead. Claude Code then reads the plugins in place, and an edit takes effect at the next session.

## License

MIT. See [`LICENSE`](LICENSE).
