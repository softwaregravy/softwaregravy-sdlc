# softwaregravy-sdlc: overall plan

Approved by the owner on 2026-11-11. Phase 1 is in progress.

## 1. Goal

One public repo that holds a whole software process as Claude Code skills. A project opts in, names its stack, and gets 80 to 100% of its process from this repo. The process takes one piece of work from a rough idea to a reviewed pull request, with a human gate at each stage.

The model is Anthropic's AI-native SDLC playbook (https://claude.com/resources/articles/the-ai-native-sdlc-playbook): each stage commits an artifact that the next stage reads.

"The owner" in this document is the person who owns the repo the process runs in, and who merges.

## 2. Decisions already made

| Decision | Choice |
|---|---|
| Distribution | The repo is a Claude Code plugin marketplace. Projects enable plugins in their checked-in `.claude/settings.json` |
| Opt-in | Per repo only. Nothing is enabled at user level, so there is one copy of the rules and nothing to keep in sync |
| Dependency direction | This repo stands alone and names no other repo of the owner's. Other repos may reference it |
| Third-party skills | Vendored with attribution when we want to edit them; referenced by name from the pipeline manifest when we don't |
| Artifact names | The playbook's: `intent.md`, `spec.md`, `plan.md` |
| Stages | Intent, Spec, Build. Each has the same four steps: start, do, review, finish |
| Gates | Three pull requests per intent, against the default branch, never stacked. Every gate is the owner's merge button |
| The plan | An internal step of the Build stage, not a gate of its own. A checkpoint in an interactive session; written and then agent-reviewed in an unattended run |
| Review feedback | The owner comments on the PR and applies `feedback-ready` when they have finished commenting |
| Organising skills | A pipeline manifest lists the skills that run in each step. Layers and projects add, remove or replace entries |
| Driving runs | Interactive sessions to start with: the owner runs each stage with a slash command. Automatic triggers come later |
| End of a run | A reviewed PR. The owner merges |
| Issue labels | One stage label per issue, plus `needs-info` and `wontfix` |
| Queue order | A GitHub Project per repo with a numeric Rank field |
| Stack layers | One per language, framework and hosting platform, plus combinations when needed. All start empty; nothing is seeded |
| Self-improvement | A change to the SDLC starts as an issue on this repo and goes through the SDLC's own pipeline |
| Repo setup | New repos are created, and existing ones adopted, from a session in this repo |
| Pilot | One existing Rails project, alongside this repo running on itself |
| The pilot's existing docs | Frozen as history. Its reusable decisions are harvested into this repo through issues |
| License | MIT, keeping the Apache 2.0 notice for anything taken from an Apache-licensed source |
| Small changes | They go through the full pipeline for now. A lighter path for low-risk fixes is a later problem |

## 3. The lifecycle

| Stage (playbook name) | Starts from | Produces | Gate |
|---|---|---|---|
| Capture | Any idea, bug, alert or support request | A GitHub issue labelled `stage:inbox`. The bar is low | None |
| Intent (Plan) | An issue | `intent.md` | The owner merges PR 1 |
| Spec (Design) | An approved intent on the default branch | `spec.md` and any ADRs | The owner merges PR 2 |
| Build (Build, Test, Deploy) | An approved spec on the default branch | `plan.md`, code, tests, living-doc updates | The owner merges PR 3 |
| Maintain | Production | A new issue, back at Capture | Not built yet |

### 3.1 The four steps of every stage

| Step | What it does | Intent example | Build example |
|---|---|---|---|
| Start | Reads the inputs and writes a plan for the stage | Read the issue, find related issues, propose a split or merge, list what to ask | Write `plan.md` and have reviewers check it against the spec |
| Do | Produces the stage's artifact | Interview the owner, write `intent.md` | Implement the plan test-first |
| Review | Every listed reviewer checks the artifact in a fresh context | Is it clear, and is it a single item? | Does it meet the standards, and does it match the spec? |
| Finish | Opens the PR | PR 1 | PR 3 |

For Intent and Spec the start step's plan is a few lines posted as a comment on the issue, and needs no approval. For Build it is `plan.md`, committed as the first commit on the build branch:

- **Interactive session:** the plan is a checkpoint. The session shows it and waits for the owner.
- **Unattended run:** the plan is written, then reviewed by agents, and the build continues.

### 3.2 What each stage does

**Capture.** File an issue with whatever is known. No template is required.

**Intent.** An interview turns one issue into one clear, single-item intent. "Single item" means it can ship as one code PR that the owner can review in one sitting. The stage may:

- split an issue into several, each linked to the original;
- merge related issues into one, closing the others with a pointer.

It writes `intent.md` (author, status, problem, proposed outcome, affected users and systems, constraints, open questions).

**Spec.** Reads the project `CLAUDE.md`, the living docs it points to, the intent, the code, and the defaults of every enabled layer. It questions the owner on the decisions that are theirs, applies layer defaults without asking, and writes `spec.md`. The spec carries two required sections:

- **Deviations from defaults:** each one becomes a project ADR in this PR.
- **Living-doc changes:** what the code PR will change in `CLAUDE.md`, the glossary and the architecture overview.

**Build.** Writes and checks `plan.md` (tasks with exact files, interfaces and tests), then executes it test-first without pausing. Every judgment call is recorded as a ruling and listed in the PR. It applies the living-doc changes the spec listed and sets the intent's status to implemented. Reviewers then check the branch; critical and important findings are fixed in one pass. The PR body lists the rulings, deferred findings and pasted verification output.

**Maintain.** Defined but empty. Its only rule for now: an alert or a support request becomes an issue.

### 3.3 Where things live in a project

```
<project>/
├── CLAUDE.md                     # what the product is, its invariants, its commands. No process
├── GLOSSARY.md                   # living; created when a term is first settled
├── docs/adr/                     # living; one file per decision
├── intent/
│   └── <issue#>-<slug>/
│       ├── intent.md             # PR 1
│       ├── spec.md               # PR 2
│       └── plan.md               # PR 3, with the code
├── .claude/settings.json         # names the marketplace and the stack plugins
└── .sdlc/                        # optional: this project's changes to the pipeline (4.4)
```

- **Per-intent folders are history.** They are frozen once merged and are not read by default.
- **Living docs describe what exists.** A spec session starts from them, not from old specs. They change only in a code PR, with one exception: an ADR lands with the spec PR, because a decision is true once it is made.
- **An architecture overview** is added the first time a project's `CLAUDE.md` outgrows a page.

### 3.4 State tracking

No separate tracker. State is read from the default branch:

| What is on the default branch | State |
|---|---|
| Issue only | Captured |
| `intent.md` | Intent approved, awaiting spec |
| `intent.md` and `spec.md` | Spec approved, awaiting build |
| The above plus an open PR carrying `plan.md` | In build |
| `intent.md` with `status: implemented` | Done |

The issue stays open as the tracking issue. Every PR references it and PR 3 closes it. Each stage refuses to start unless the previous stage's file is on the default branch, which is also the check that the previous PR really landed there.

### 3.5 The review loop on every PR

GitHub does not let an author approve their own PR, and Claude pushes as the owner, so approval is never a GitHub review. It is always the merge.

1. The owner reads the PR and leaves comments.
2. When they have finished commenting, they apply the label `feedback-ready`.
3. `/sdlc:respond` answers every comment with a commit or a reply, then removes the label.
4. Steps 1 to 3 repeat until the owner is satisfied.
5. The owner merges.

In an interactive session the owner can also just say they are done commenting, and the skill applies the label for them.

### 3.6 Issue labels and the queue

| Label | Meaning |
|---|---|
| `stage:inbox` | Captured, not yet clarified |
| `stage:intent` | Intent being written or in PR 1 |
| `stage:spec` | Intent approved; spec being written or in PR 2 |
| `stage:build` | Spec approved; build in progress or in PR 3 |
| `needs-info` | Waiting on an answer |
| `wontfix` | Will not be done |

Labels are a view that each stage keeps current. The default branch remains the truth (3.4).

Order comes from a GitHub Project per repo with a numeric **Rank** field in gaps of ten, lowest first. The board is for ordering only. `/sdlc:status` lists open work by rank and names the next item.

## 4. The repo

```
softwaregravy-sdlc/
├── .claude-plugin/marketplace.json   # lists every plugin below
├── plugins/
│   └── sdlc/                         # the core plugin
│       ├── .claude-plugin/plugin.json
│       ├── pipeline                  # the default manifest: which skills run in each step (4.4)
│       ├── skills/                   # one folder per skill, scripts inside
│       ├── agents/                   # reviewer agents
│       ├── hooks/                    # session-start context; guards later
│       ├── context.md                # the always-on rules, under a page
│       ├── standards.md              # judgment rules the reviewers enforce
│       ├── defaults/                 # reusable decisions that apply to every project
│       └── evals/                    # test cases for the skills
├── intent/                           # this repo's own intents
├── docs/adr/  GLOSSARY.md
├── THIRD_PARTY.md                    # each vendored skill: source, commit, license, what changed
├── CLAUDE.md  README.md  LICENSE
```

Stack layers appear under `plugins/` as they are first needed, for example `sdlc-ruby`, `sdlc-rails`, `sdlc-render`, and `sdlc-rails-render` for a combination. Each has the same shape as the core and declares what it depends on, so enabling `sdlc-rails` also enables `sdlc-ruby` and `sdlc`.

### 4.1 What a layer holds, and where a rule goes

| Kind of rule | Where it goes | Who applies it |
|---|---|---|
| Mechanical (a pattern a tool can check) | A linter config, hook or CI job the layer installs | The tool |
| Judgment (style, consistency) | The layer's `standards.md` | The reviewers |
| A decision not worth repeating (preferred host, test framework) | The layer's `defaults/`, one short record each | The spec stage |
| A procedure | A skill in the layer, listed in the layer's manifest | The step it is listed under |
| Needed in every session | The layer's `context.md`, a few lines | Injected at session start |

Precedence: the project, then the most specific layer, then the core.

### 4.2 How a project opts in

```json
{
  "extraKnownMarketplaces": {
    "softwaregravy-sdlc": {
      "source": { "source": "github", "repo": "softwaregravy/softwaregravy-sdlc" }
    }
  },
  "enabledPlugins": {
    "sdlc-rails@softwaregravy-sdlc": true
  }
}
```

That file and a product-only `CLAUDE.md` are the whole required footprint.

Because nothing is enabled at user level, the skills exist only inside a repo that has opted in. Two consequences:

- **Repo setup happens from a session in this repo**, which opts in to itself. `/sdlc:new-repo` creates a repo, protects its default branch and writes its settings file. `/sdlc:adopt` does the same for an existing repo.
- **The owner's user-level instructions keep a one-line pointer** saying that, in place of any process rules they hold today. It is a pointer, not a copy, so there is nothing to keep in sync.

### 4.3 Editing skills as we go

On a machine with a clone, the marketplace is added from the local path. Claude Code then reads the plugin files in place, so an edit takes effect at the next session or on `/reload-plugins`, with no publish step. Machines without a clone get the copy on GitHub's default branch.

### 4.4 The pipeline manifest

The manifest is the one place that says which skills make up each stage. For each stage and step it lists the skills that run, in order:

```
build:
  start:   [plan-write, review-plan]
  do:      [implement, tdd, verify, docs-update]
  review:  [review-standards, review-against-spec]
  finish:  [pr-open]
```

- **The core ships the default manifest.**
- **A layer adds entries.** A Rails layer could add a migration reviewer to `build.review`.
- **A project overrides.** Files under `.sdlc/` in the project add a rule to a stage, add a skill of the project's own, replace an entry, or drop a step.
- **Entries can name skills from elsewhere:** a Claude Code built-in such as `security-review`, or a skill from another installed plugin.
- **Every reviewer gets a turn.** The review step runs each listed reviewer in a fresh context. All report findings in one common format (severity, location, claim, evidence). The findings are then merged, re-graded and fixed in one pass.
- **Small shared skills** such as `pr-open` and `pr-respond` are written once and listed wherever they are used.

A small script resolves core, layers and project into the effective pipeline, so the result does not depend on a model reading several files correctly. `/sdlc:pipeline` prints the effective pipeline for the current repo and says where each entry came from.

The file format, and how the script finds each enabled layer's manifest, are settled in phase 1.

## 5. Commands and skills, version 0

### 5.1 Commands

| Kind | Command | Purpose |
|---|---|---|
| Stage | `/sdlc:intent <issue>` | Run the Intent stage; ends with PR 1 open |
| Stage | `/sdlc:spec <issue>` | Run the Spec stage; ends with PR 2 open |
| Stage | `/sdlc:build <issue>` | Run the Build stage; ends with PR 3 open |
| Any time | `/sdlc:capture` | File a low-bar issue on this project |
| Any time | `/sdlc:respond <PR>` | Answer every comment on a PR labelled `feedback-ready` |
| Any time | `/sdlc:status` | Show where every intent stands, in rank order, and name the next item |
| Any time | `/sdlc:pipeline` | Print the effective pipeline for this repo |
| Any time | `/sdlc:feedback` | File an issue on the SDLC repo from any project |
| Setup | `/sdlc:new-repo` | Create a repo, push, protect the default branch, opt it in |
| Setup | `/sdlc:adopt` | Opt an existing repo in: settings file, labels, the ranked Project, the `intent/` folder |

Every command takes an issue or PR number and reads its state from GitHub and the default branch. What triggers a command can therefore change later without changing the command.

### 5.2 The default manifest and where each skill comes from

| Stage | Step | Skill | Built from |
|---|---|---|---|
| Intent | Start | `intent-start` | New. Includes split and merge |
| Intent | Do | `intent-interview`, `intent-write` | superpowers `brainstorming`, trimmed |
| Intent | Review | `review-intent` | superpowers' builder check |
| Spec | Start | `spec-start` | New |
| Spec | Do | `spec-grill`, `spec-write` | mattpocock `grilling`, `to-spec` template, `domain-modeling` |
| Spec | Review | `review-spec-doc` | New, adversarial |
| Build | Start | `plan-write`, `review-plan` | superpowers `writing-plans` |
| Build | Do | `implement`, `tdd`, `verify`, `docs-update` | superpowers `executing-plans` and `verification-before-completion`; both TDD skills merged |
| Build | Review | `review-standards`, `review-against-spec` | mattpocock `code-review`, split into its two axes, with superpowers' severity grades and "declined to judge" list |
| Shared | Finish | `pr-open` | mattpocock `pr`, plus the owner's existing pull request rules |
| Shared | Any | `pr-respond`, `findings-triage` | superpowers `receiving-code-review`; new |

Deferred until an issue asks for them: the subagent executor, git worktree handling, a debugging skill, `retro`, the skill-authoring skill, the `egm` review swarm, and the browser mockup server.

### 5.3 Vendoring rules

- Every vendored skill is recorded in `THIRD_PARTY.md` with its source repo, commit and license, and a note of what changed.
- Licenses checked so far: `mattpocock/skills` MIT, `obra/superpowers` MIT, `google/elephant-goldfish-model` Apache 2.0.
- Not vendored: superpowers' `using-superpowers` skill and its session-start text, which force a skill check before every reply.

## 6. Enforcement and triggers

| Layer | Now | Later |
|---|---|---|
| GitHub ruleset on the default branch (pull requests only, no bypass) | Yes, applied by `/sdlc:new-repo` and `/sdlc:adopt` | |
| Always-on instructions | Yes, the core's `context.md` | |
| Hooks that block a PR with a non-default base, a push to the default branch, or a merge | No | Yes |
| Commands triggered automatically | No; the owner types them | Yes |
| This repo's own CI | `claude plugin validate --strict` | `claude plugin eval` on the skills |

Two ways to trigger commands automatically, to be chosen in phase 6:

| | GitHub Actions | A poller on the owner's server |
|---|---|---|
| Trigger | GitHub events: a label applied, a PR merged. No polling | A timer lists PRs labelled `feedback-ready` |
| Runs on | GitHub's runners, using Anthropic's `claude-code-action` | The owner's machine |
| Hooked in by | A workflow file that `/sdlc:adopt` adds to the repo | A service that lives outside this repo and references it |
| Cost | A Claude credential stored as a repo secret; Actions minutes on private repos | The existing login; a few minutes' delay |

## 7. Self-improvement

1. Any session that settles a standard runs `/sdlc:feedback`, which files an issue here.
2. Intent clarifies the rule.
3. Spec generalises it: which layer it belongs to, and which form from the table in 4.1.
4. Build changes the skill, standard, default or manifest, and adds an eval case.
5. A layer is created by the first approved rule that needs it.

Related small issues can be merged into one intent, so a batch of defaults for one layer does not cost three PRs each.

## 8. Migration

Process rules that live in the owner's other repos today move here. Each of those repos tracks its own part of the move in its own issues, since this repo names none of them.

Order matters: a repo opts in before the rule it relied on is deleted from wherever it lives today.

## 9. Phases

| Phase | Work | Done when |
|---|---|---|
| 0 | Approve this plan | Done, 2026-11-11 |
| 1 | Walking skeleton: create the repo, marketplace file, core plugin with one trivial skill, the session-start hook, and the manifest resolver with a dummy layer and a dummy project override; protect the default branch; settle section 11 | A session in the pilot project lists an `/sdlc:` skill, shows the injected rules, and `/sdlc:pipeline` prints a pipeline that includes the dummy entries |
| 2 | Core pipeline, version 0: the commands and skills in section 5, the templates, `THIRD_PARTY.md` | The plugin validates, and each stage has been run once on a throwaway issue |
| 3 | Pilot: the pilot project opts in and one real issue goes through all three PRs. Everything that chafes is filed with `/sdlc:feedback` | One intent is implemented in the pilot, and one SDLC issue has gone through the SDLC's own pipeline |
| 4 | Harvest: sort the pilot's decisions into reusable and bespoke; reusable ones become issues here and create the first layers | The pilot's `CLAUDE.md` holds product content only |
| 5 | Migrate the owner's other repos; remove the third-party plugins enabled at user level | Each repo's migration issue is closed |
| 6 | Hardening: hooks, automatic triggers, skill evals, stronger reviews, the subagent executor | Each arrives as its own issue |
| 7 | Maintain stage, then risk-based relaxation of gates | The pilot is in production |

Phases 1 and 2 are built with ordinary single-concern PRs, because the pipeline does not exist yet. From phase 3 on, every change to this repo goes through its own pipeline.

## 10. Details chosen while drafting

These are easy to change:

1. **Label names:** `feedback-ready`, and the `stage:` set in 3.6.
2. **A label, not a special comment,** for "I have finished commenting", because labels can be listed and are two taps on a phone.
3. **`.sdlc/`** as the folder for a project's pipeline overrides.
4. **Skill names** in 5.2.

## 11. To verify in phase 1

These come from the Claude Code docs or from other plugins and have not been tried.

- A project's `.claude/settings.json` can register the marketplace and enable plugins for anyone who opens the repo, and what prompt that shows.
- Enabling a layer plugin enables the plugins it depends on.
- A marketplace added from a local path and the same marketplace named in project settings coexist, and which one wins.
- With no `version` set, a merge to the default branch reaches projects on the next marketplace update.
- A plugin's session-start hook injects context in a session launched by a service, with no terminal.
- Cloud sessions can install from the public marketplace.
- The resolver script can find the manifest of every enabled layer.
- A manifest entry can name a built-in skill or another plugin's skill, and the stage can invoke it.

To verify in phase 6: `claude-code-action` can load plugins from this marketplace.

## 12. Risks

- **The manifest is the least proven part.** If resolving it across plugins turns out to be awkward, the fallback is a naming convention plus a project deny list.
- **Volume of vendored text.** superpowers alone is about 11,000 lines. Version 0 takes a small cluster and trims it.
- **Session-start bloat.** Every layer adds always-on text. Each `context.md` stays to a few lines; `claude plugin details` reports the token cost.
- **Upstream drift.** Vendored skills stop receiving upstream fixes. `THIRD_PARTY.md` records the commit so a later comparison is possible.
- **Ceremony.** Three PRs per intent is heavy for small work. Merging issues at the Intent stage is the only relief until gates are relaxed.
- **Live edits.** A local clone on a feature branch changes the skills every project on that machine uses.
