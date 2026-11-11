# softwaregravy-sdlc

A software development lifecycle packaged as Claude Code skills. A project opts in, names its stack, and gets its process from here: an idea becomes a GitHub issue, then an intent, a spec, and a reviewed pull request, with a human merge at each stage.

It follows Anthropic's [AI-native SDLC playbook](https://claude.com/resources/articles/the-ai-native-sdlc-playbook).

**Status: early.** The core plugin is a walking skeleton: the hooks below exist and are all empty. [`PLAN.md`](PLAN.md) holds the design, the decisions and the phases.

## How work flows

```mermaid
flowchart LR
    issue([Issue]) --> intent

    subgraph intent [Intent stage]
        direction TB
        i1[start] --> i2[do] --> i3[review] --> i4[finish]
    end

    intent --> pr1{{"PR 1<br/>intent.md"}}
    pr1 -- owner merges --> spec

    subgraph spec [Spec stage]
        direction TB
        s1[start] --> s2[do] --> s3[review] --> s4[finish]
    end

    spec --> pr2{{"PR 2<br/>spec.md"}}
    pr2 -- owner merges --> build

    subgraph build [Build stage]
        direction TB
        b1[start] --> b2[do] --> b3[review] --> b4[finish]
    end

    build --> pr3{{"PR 3<br/>plan.md + code"}}
    pr3 -- owner merges --> done([Done])
```

Every pull request targets the default branch. A stage starts only when the previous stage's file is on that branch.

## Stages

| Stage | Starts from | Produces | Ends with |
|---|---|---|---|
| Intent | A GitHub issue | `intent.md`: one clear, single-item statement of what is wanted and why | PR 1 |
| Spec | A merged intent | `spec.md`: requirements and design, plus a decision record for each decision made | PR 2 |
| Build | A merged spec | `plan.md`, then code, tests and updated docs | PR 3 |

The three files for one piece of work sit together in `intent/<issue#>-<slug>/`.

## Steps

Every stage runs the same four steps, in order.

| Step | What it does | In Intent | In Build |
|---|---|---|---|
| start | Reads the inputs and writes a plan for the stage | Read the issue, find related issues, propose a split or merge | Write `plan.md` and check it against the spec |
| do | Produces the stage's file or code | Interview the owner, write `intent.md` | Implement the plan test-first |
| review | Every listed reviewer checks the result in a fresh context | Is it clear, and is it a single item? | Does it meet the standards, and does it match the spec? |
| finish | Opens the pull request | PR 1 | PR 3 |

## Hooks

A hook is one step of one stage, named `<stage>.<step>`. There are twelve. A skill runs because a manifest lists it under a hook; a hook with nothing listed does nothing.

The skills below are the core's planned defaults. None exists yet.

| Hook | Planned core skills |
|---|---|
| `intent.start` | `intent-start` |
| `intent.do` | `intent-interview`, `intent-write` |
| `intent.review` | `review-intent` |
| `intent.finish` | `pr-open` |
| `spec.start` | `spec-start` |
| `spec.do` | `spec-grill`, `spec-write` |
| `spec.review` | `review-spec-doc` |
| `spec.finish` | `pr-open` |
| `build.start` | `plan-write`, `review-plan` |
| `build.do` | `implement`, `tdd`, `verify`, `docs-update` |
| `build.review` | `review-standards`, `review-against-spec` |
| `build.finish` | `pr-open` |

Three kinds of manifest attach skills to hooks, applied in this order:

1. **The core's** `plugins/sdlc/pipeline.toml` sets the defaults.
2. **A stack layer's** `pipeline.toml` adds to them. A Rails layer might add a migration reviewer to `build.review`.
3. **A project's** `.sdlc/pipeline.toml` has the last word: it can add a skill of its own, replace one, remove one, or empty a hook.

```toml
# <project>/.sdlc/pipeline.toml
[build.review]
add    = ["security-review"]            # any skill, by the name you would type to run it
remove = ["sdlc:review-standards"]
```

Every skill listed under a review hook gets a turn. `/sdlc:pipeline` prints the hooks for the current repo and says which manifest each skill came from.

## How it is organised

- **`plugins/sdlc`** is the core plugin: the pipeline, the pull request rules and repo setup.
- **Stack layers** are further plugins beside it, one per language, framework or hosting platform. Each is created the first time a rule needs it.
- **Always-on rules** reach a session through each plugin's session-start hook, which prints the plugin's `context.md`.

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
