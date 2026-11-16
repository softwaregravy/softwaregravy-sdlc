# softwaregravy-sdlc: overall plan

Approved by the owner on 2026-11-11. Phase 1 is in progress: the walking skeleton is built, and section 11 lists what it showed and what is still untried.

## 1. Goal

One public repo that holds a whole software process as Claude Code skills. A project opts in, names its stack, and gets 80 to 100% of its process from this repo. The process takes one piece of work from a rough idea to a reviewed pull request, with a human gate at each stage.

The model is Anthropic's AI-native SDLC playbook (https://claude.com/resources/articles/the-ai-native-sdlc-playbook): each stage commits an artifact that the next stage reads.

"The owner" in this document is the person who owns the repo the process runs in, and who merges.

## 2. Decisions already made

| Decision | Choice |
|---|---|
| Distribution | The repo is a Claude Code plugin marketplace. Projects enable plugins in their checked-in `.claude/settings.json` |
| Opt-in | Per repo. Each machine installs the plugins once and leaves them switched off; a repo's settings switch them on. Nothing is enabled at user level, so there is one copy of the rules and nothing to keep in sync |
| Dependency direction | This repo stands alone and names no other repo of the owner's. Other repos may reference it |
| Third-party skills | Vendored with attribution when we want to edit them; referenced by name from the pipeline manifest when we don't |
| Artifact names | The playbook's: `intent.md`, `spec.md`, `plan.md` |
| Stages | Intent, Spec, Build. Each has the same four steps: start, do, review, finish |
| Gates | Three pull requests per intent, against the default branch, never stacked. Every gate is the owner's merge button |
| Feature folders | `features/active/<issue#>-<slug>/` is a feature's working folder while it is in development: its named documents, and anything else a stage keeps for it. The code PR moves the folder to `features/shipped/` |
| Committed docs | Change only through a pull request. A later stage's PR may fix an earlier stage's document, and lists each edit in its body |
| The plan | An internal step of the Build stage, not a gate of its own. A checkpoint in an interactive session; written and then agent-reviewed in an unattended run |
| Review feedback | The owner comments on the PR and applies `feedback-ready` when they have finished commenting |
| Organising skills | A pipeline manifest lists the skills that run in each step. Layers and projects add, remove or replace entries |
| Step skills | Ordinary skills marked `user-invocable: false`: hidden from the `/` menu, and invoked by name by the stage commands. Each costs one line of context in every session of an opted-in repo |
| Driving runs | Interactive sessions to start with: the owner runs each stage with a slash command. Automatic triggers come later |
| End of a run | A reviewed PR. The owner merges |
| Issue labels | Calls for action only: `feedback-ready`, `needs-info` and `wontfix`. No label says where work stands |
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
| Capture | Any idea, bug, alert or support request | A GitHub issue. The bar is low | None |
| Intent (Plan) | An issue | `intent.md` | The owner merges PR 1 |
| Spec (Design) | An approved intent on the default branch | `spec.md` and any ADRs | The owner merges PR 2 |
| Build (Build, Test, Deploy) | An approved spec on the default branch | `plan.md`, code, tests, living-doc updates | The owner merges PR 3 |
| Maintain | Production | A new issue, back at Capture | Not built yet |

### 3.1 The four steps of every stage

| Step | What it does | Intent example | Build example |
|---|---|---|---|
| Start | Reads the inputs and writes a plan for the stage | Nothing in the core | Write `plan.md` and have reviewers check it against the spec |
| Do | Produces the stage's artifact | Read the issue, related issues and the repo, propose a split or merge, interview the owner, write `intent.md` | Implement the plan test-first |
| Review | Every listed reviewer checks the artifact in a fresh context | Is it clear, consistent and complete, and should it split? | Does it meet the standards, and does it match the spec? |
| Finish | Opens the PR | PR 1 | PR 3 |

Every PR body names the host and session id that wrote it, so the owner can resume that session with `claude --resume`.

Intent's start step is empty in the core. A plan would hand nothing on: the interview runs straight after it in the same session, with everything the reading found already in context, and Intent never runs unattended. If a later phase runs that reading unattended on new issues, a plan posted to the issue becomes a real handoff, and Intent gets a start skill.

For Spec the start step's plan is a few lines posted as a comment on the issue, and needs no approval. For Build it is `plan.md`, committed as the first commit on the build branch:

- **Interactive session:** the plan is a checkpoint. The session shows it and waits for the owner.
- **Unattended run:** the plan is written, then reviewed by agents, and the build continues.

### 3.2 What each stage does

**Capture.** File an issue with whatever is known. No template is required.

**Intent.** An interview turns one issue into one clear intent. Claude reads the issue, related issues and the repo before asking anything. It asks one open question about why, then asks in rounds, each question with a recommended answer. The stage may:

- split an issue into several, each linked to the original;
- merge related issues into one, closing the others with a pointer.

Claude suggests a split when an intent grows too big. A plain yes from the owner is enough for a split or a merge.

It writes `intent.md` with seven sections, each always present. A section with nothing in it says *None*.

| Section | Holds |
|---|---|
| Problem | One specific story: who hits what, why today doesn't work, and why now |
| Proposed outcome | What is true once it ships, as observable behaviour, not design |
| Resources impacted | Repos, services, systems and data that may need changes |
| Constraints | What the spec must respect or must not change |
| Acceptance criteria | Results the owner can check without knowing the implementation |
| Out of scope | Near-misses a reader might assume are included, each with a reason |
| Claude decisions | Numbered, so a reviewer can point at one: each open question with Claude's answer, and each call Claude made that the owner didn't state |

Merging the intent's PR accepts Claude's decisions along with the rest.

**Spec.** Reads the project `CLAUDE.md`, the living docs it points to, the intent, the code, and the defaults of every enabled layer. It questions the owner on the decisions that are theirs, applies layer defaults without asking, and writes `spec.md`. The spec carries two required sections:

- **Deviations from defaults:** each one becomes a project ADR in this PR.
- **Living-doc changes:** what the code PR will change in `CLAUDE.md`, the glossary and the architecture overview.

**Build.** Writes and checks `plan.md` (tasks with exact files, interfaces and tests), then executes it test-first without pausing. Every judgment call is recorded as a ruling and listed in the PR. It applies the living-doc changes the spec listed, and moves the feature's folder from `features/active/` to `features/shipped/`. Reviewers then check the branch; critical and important findings are fixed in one pass. The PR body lists the rulings, any edits to the intent or the spec, deferred findings and pasted verification output.

**Maintain.** Defined but empty. Its only rule for now: an alert or a support request becomes an issue.

### 3.3 Where things live in a project

```
<project>/
├── CLAUDE.md                     # what the product is, its invariants, its commands. No process
├── GLOSSARY.md                   # living; created when a term is first settled
├── docs/adr/                     # living; one file per decision
├── features/
│   ├── active/
│   │   └── <issue#>-<slug>/      # the feature's working folder
│   │       ├── intent.md         # PR 1
│   │       ├── spec.md           # PR 2
│   │       ├── plan.md           # PR 3, with the code
│   │       ├── research.md       # when a stage researched something, in that stage's PR
│   │       └── …                 # anything else a stage keeps for the feature
│   └── shipped/                  # PR 3 moves the feature's folder here
├── .claude/settings.json         # names the marketplace and the stack plugins
└── .sdlc/                        # optional: this project's changes to the pipeline (4.4)
```

- **`features/active/` is the work in flight.** A feature's folder sits there from its intent PR until its code PR moves it to `features/shipped/`.
- **A feature's folder is its working folder.** Beside the named files, a stage may keep anything else the feature needs there, such as notes, sketches or sample data. It all lands through a PR, like the named files.
- **`research.md` keeps what a session researched for the feature,** with its sources, so the findings outlive the session. It lands in the PR of the stage that did the research, and a later stage adds to it.
- **Shipped folders are history.** They are not read by default.
- **A committed document changes only through a pull request.** A later stage's PR may fix an earlier stage's document, such as the spec PR fixing `intent.md` or the code PR fixing `spec.md`, and lists each edit in its body.
- **Living docs describe what exists.** A spec session starts from them, not from old specs. They change only in a code PR, with one exception: an ADR lands with the spec PR, because a decision is true once it is made.
- **An architecture overview** is added the first time a project's `CLAUDE.md` outgrows a page.

### 3.4 State tracking

No separate tracker. State is read from the default branch:

| What is on the default branch | State |
|---|---|
| Issue only | Captured |
| `intent.md` in `features/active/` | Intent approved, awaiting spec |
| `intent.md` and `spec.md` in `features/active/` | Spec approved, awaiting build |
| The above plus an open PR carrying `plan.md` | In build |
| The feature's folder in `features/shipped/` | Done |

The issue stays open as the tracking issue. Every PR references it and PR 3 closes it. Each stage refuses to start unless the previous stage's file is on the default branch, which is also the check that the previous PR really landed there.

When a stage starts, it comments on the issue with the stage, its branch, and the host and session running it. The comment is news for whoever watches the issue, not state.

### 3.5 The review loop on every PR

GitHub does not let an author approve their own PR, and Claude pushes as the owner, so approval is never a GitHub review. It is always the merge.

1. The owner reads the PR and leaves comments.
2. When they have finished commenting, they apply the label `feedback-ready`.
3. `/sdlc:respond` answers every comment with a commit or a reply, then removes the label.
4. Steps 1 to 3 repeat until the owner is satisfied.
5. The owner merges.

In an interactive session the owner can also just say they are done commenting, and the skill applies the label for them.

### 3.6 Issue labels and the queue

Labels call for action. None says where work stands: that is read from the default branch and the open PRs (3.4).

| Label | Meaning |
|---|---|
| `feedback-ready` | On a PR: the owner has finished commenting (3.5) |
| `needs-info` | Waiting on an answer |
| `wontfix` | Will not be done |

Order comes from a GitHub Project per repo with a numeric **Rank** field in gaps of ten, lowest first. The board is for ordering only. `/sdlc:status` lists open work by rank and names the next item.

## 4. The repo

```
softwaregravy-sdlc/
├── .claude-plugin/marketplace.json   # lists every plugin below
├── plugins/
│   └── sdlc/                         # the core plugin
│       ├── .claude-plugin/plugin.json
│       ├── pipeline.toml             # the default manifest: which skills run in each step (4.4)
│       ├── stage.md                  # the steps every stage command shares (4.5)
│       ├── scripts/                  # the manifest resolver
│       ├── skills/                   # one folder per skill, scripts inside
│       ├── agents/                   # the reviewer agent, which runs one review skill in a fresh context
│       ├── hooks/                    # session-start context; guards later
│       ├── context.md                # the always-on rules, under a page
│       ├── standards.md              # judgment rules the reviewers enforce
│       ├── defaults/                 # reusable decisions that apply to every project
│       └── evals/                    # test cases for the skills
├── features/                         # this repo's own features: active/ and shipped/
├── docs/adr/  GLOSSARY.md
├── THIRD_PARTY.md                    # each vendored skill: source, commit, license, what changed
├── CLAUDE.md  README.md  LICENSE
```

Stack layers appear under `plugins/` as they are first needed, for example `sdlc-ruby`, `sdlc-rails`, `sdlc-render`, and `sdlc-rails-render` for a combination. Each has the same shape as the core and declares what it depends on.

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
  "enabledPlugins": {
    "sdlc@softwaregravy-sdlc": true,
    "sdlc-ruby@softwaregravy-sdlc": true,
    "sdlc-rails@softwaregravy-sdlc": true
  },
  "extraKnownMarketplaces": {
    "softwaregravy-sdlc": {
      "source": {
        "source": "github",
        "repo": "softwaregravy/softwaregravy-sdlc"
      },
      "autoUpdate": true
    }
  }
}
```

That file and a `CLAUDE.md` are the whole required footprint. The `CLAUDE.md` is product-only apart from one line saying that the project expects the `sdlc` plugin, so that a session on a machine without it says so before anything else. The README gives the line.

- **The file lists every plugin, including the ones a layer depends on.** A file that names only the layer loads nothing: Claude Code reports the dependency as not installed. `/sdlc:adopt` will write the full list.
- **A repo can switch a plugin on, but never install it.** Claude Code leaves installing to the person at the machine, because a plugin runs code. So each machine runs `claude plugin marketplace add softwaregravy/softwaregravy-sdlc` once, then installs each plugin with `--scope user` and disables it with `--scope user`. The plugin is installed for the user but switched off, and a project's `true` switches it on in that project alone.
- **Updates follow the default branch.** No `version` is set, so each commit there is a new version. `autoUpdate` makes an interactive session in an opted-in project fetch it in the background, for the next session to load. Headless sessions do not update.

Because nothing is enabled at user level, the skills exist only inside a repo that has opted in. Two consequences:

- **Repo setup happens from a session in this repo**, which opts in to itself. `/sdlc:new-repo` creates a repo, protects its default branch and writes its settings file. `/sdlc:adopt` does the same for an existing repo.
- **The owner's user-level instructions keep a one-line pointer** saying that, in place of any process rules they hold today. It is a pointer, not a copy, so there is nothing to keep in sync.

### 4.3 Editing skills as we go

A marketplace added from a local path is read in place, so an edit takes effect at the next session or on `/reload-plugins`, with no publish step. Machines without a clone get the copy on the default branch. How a machine with a clone points its projects at the clone, now that the GitHub source is registered once per machine (4.2), is still open: issue #8 settles it.

### 4.4 The pipeline manifest

The manifest is the one place that says which skills make up each stage. For each stage and step it lists the skills that run, in order:

```toml
# plugins/sdlc/pipeline.toml: an array sets a step's whole list
[build]
start  = ["sdlc:plan-write", "sdlc:review-plan"]
do     = ["sdlc:implement", "sdlc:tdd", "sdlc:verify", "sdlc:docs-update"]
review = ["sdlc:review-standards", "sdlc:review-against-spec"]
finish = ["sdlc:pr-open"]
```

```toml
# <project>/.sdlc/pipeline.toml: a table edits the inherited list
[build.review]
remove  = ["sdlc:review-standards"]
add     = ["security-review"]
replace = { "sdlc:review-against-spec" = "strict-spec-review" }
```

- **The core ships the default manifest**, `pipeline.toml` at the plugin root. Every step is empty until its skills exist.
- **An empty step stays in the manifest, and does nothing.** `add` appends to a step's list, so a skill that must run before a step's core skills goes in the step before it. That is why Intent keeps an empty `start`.
- **A layer adds entries** in its own `pipeline.toml`. A Rails layer could add a migration reviewer to `build.review`.
- **A project overrides** in `.sdlc/pipeline.toml`: it adds a skill of its own, replaces an entry, removes one, or empties a step.
- **Entries are skill names exactly as they are invoked**, so they can name skills from elsewhere: a Claude Code built-in such as `security-review`, or a skill from another installed plugin. A skill marked `disable-model-invocation` can't be an entry, since only a person can run it.
- **Removing or replacing an entry that is not there is an error.** An override cannot silently stop applying when the skill it names is renamed upstream.
- **Every reviewer gets a turn.** The review step runs each listed reviewer in a fresh context. All report findings in one common format (severity, location, claim, evidence). The findings are then merged and fixed in one pass (4.5).
- **Small shared skills** such as `pr-open` and `pr-respond` are written once and listed wherever they are used.

A small script, `scripts/resolve_pipeline.py`, resolves core, layers and project into the effective pipeline, so the result does not depend on a model reading several files correctly. It applies each plugin after the plugins it depends on, then the project. `/sdlc:pipeline` prints the effective pipeline for the current repo and says where each entry came from.

The script finds the layers through the session: each SDLC plugin's session-start hook prints its name and root, and the skill passes those roots to the script. Only enabled plugins run their hooks, so Claude Code decides which layers are active.

Still to add in phase 2: per-stage rule files under `.sdlc/`, for a project that wants to add a rule to a stage without writing a skill.

### 4.5 The stage commands

`/sdlc:intent`, `/sdlc:spec` and `/sdlc:build` each take a GitHub issue number and follow one shared file, `stage.md`:

1. **Check,** and stop at the first failure: the issue is open, the working tree is clean, the previous stage's file is on the default branch, and the stage's branch, `<stage>/<issue#>`, doesn't exist yet.
2. **Resolve** the effective pipeline with the resolver.
3. **Start** the branch from the default branch, and comment on the issue (3.4).
4. **Run** start, do, review and finish, in that order. Every skill gets the stage and the issue number as its arguments, such as `intent 12`.

Start, do and finish run in the command's session, one skill after another, because each builds on what came before. Review runs once, with each skill in its own `sdlc:reviewer` agent: a fresh context with read-only tools, which gives the skill the common findings format, so a review skill says only what it checks. The findings are merged and handed back to the session, which fixes them as the do step's skills say. If none says, it fixes critical and important findings and lists the minor ones in the PR.

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
| Setup | `/sdlc:adopt` | Opt an existing repo in: settings file, labels, the ranked Project, the `features/` folders |

Every command takes an issue or PR number and reads its state from GitHub and the default branch. What triggers a command can therefore change later without changing the command.

### 5.2 The default manifest and where each skill comes from

| Stage | Step | Skill | Built from |
|---|---|---|---|
| Intent | Start | None | |
| Intent | Do | `intent-interview` | superpowers `brainstorming`, trimmed. Split and merge are new |
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
| This repo's own CI | The resolver's tests and `claude plugin validate`. Not `--strict`, which fails on the `version` field this repo leaves out on purpose | `claude plugin eval` on the skills |

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

1. **Label names:** `feedback-ready`, `needs-info` and `wontfix` (3.6).
2. **A label, not a special comment,** for "I have finished commenting", because labels can be listed and are two taps on a phone.
3. **`.sdlc/`** as the folder for a project's pipeline overrides.
4. **Skill names** in 5.2.
5. **Stage branch names:** `<stage>/<issue#>`, such as `intent/12`.
6. **Severity grades:** critical, important and minor, as `agents/reviewer.md` defines them.

## 11. Phase 1 findings

Tried on 2026-11-11 with Claude Code 2.1.311 on Linux, in non-interactive sessions (`claude -p`), against a throwaway marketplace on local disk that held the core and a dummy layer.

| Question | Result |
|---|---|
| Does a plugin's session-start hook inject context? | Yes. Whatever the hook prints becomes context, for the core and the layer alike |
| Can a project's `.claude/settings.json` enable the plugins? | From a local-path marketplace, yes, once the machine knows the marketplace. A machine that had never seen it loaded nothing. The GitHub source needs more (below) |
| Does enabling a layer enable what it depends on? | Only through `claude plugin install`, which writes every plugin into the file. A hand-written file naming only the layer loaded nothing |
| Do a local-path registration and the project's settings coexist? | Yes. The local one wins and the tracked file is untouched |
| Do edits to a local-path marketplace take effect without a reinstall? | Yes, at the next session |
| Can the resolver find every enabled layer's manifest? | Yes, through the session-start announcements. `/sdlc:pipeline` printed the core, the dummy layer's entry and the dummy project's overrides, each with its source |

Then, the same day, against the GitHub source, from throwaway projects in headless and interactive sessions:

| Question | Result |
|---|---|
| Does a project's settings file install the plugin? | No. It can switch a plugin on, never install it. With the settings file alone, nothing loaded, headless or interactive |
| Does trusting the folder in an interactive session set it up? | For that session only. Trust registered the marketplace and loaded the plugin once; the next session reported `Plugin "sdlc" not cached` |
| Does a headless session read the marketplace a project's settings declare? | No, not in a folder that has never been trusted. `claude plugin install` failed there until the marketplace was registered |
| Is the marketplace registered per project? | No, per user. A second project installed from it without registering anything |
| Is an install per project? | With `--scope project`, per clone: a clone that had not run it loaded nothing. With `--scope user`, once for every project |
| Can a plugin be installed for the user but on only where a project says so? | Yes. Installed and then disabled at user scope, it loaded in a project whose settings set it `true`, and in no other folder |
| What version is installed with no `version` field? | The default branch's commit hash, shortened to 12 characters |
| Does `install --scope project` leave the tracked file alone? | Only if the file is already in the layout the command writes. Otherwise it reorders and reformats it, without changing what it says |
| What does `uninstall --scope project` do to the tracked file? | It empties `enabledPlugins`, which switches the plugin off for every clone |
| Does a line in the project's `CLAUDE.md` make a session notice a missing plugin? | Yes. With the plugin missing, the session opened by saying so and linking the setup steps. With it installed, the session said nothing about it |

Not yet tried:

- A session launched by a service, a cloud session, and macOS. The resolver needs Python 3.11 or later, and macOS ships an older system Python.

Settled in phase 2 (#3): a skill with `disable-model-invocation` can be run only by a person typing its name, so step skills are marked `user-invocable: false` instead (section 2).

Then, on 2026-11-16 with Claude Code 2.1.311 on Linux, headless: `/sdlc:intent` on a throwaway issue (#21) in a scratch worktree, with test skills from a second plugin at every step and the built-in `security-review` as a second reviewer:

| Question | Result |
|---|---|
| Are `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_SKILL_DIR}` and `${CLAUDE_SESSION_ID}` filled into a skill's text? | Yes, all three, but not into a file the skill reads. So each stage command passes the plugin root and the session id on to `stage.md` |
| Can a stage invoke a `user-invocable: false` skill from another plugin? | Yes, by name with the Skill tool, with `intent 21` as its arguments |
| Can a reviewer agent invoke a skill? | Yes. `sdlc:reviewer`, with the Skill tool among its tools, ran another plugin's `user-invocable: false` skill and the built-in `security-review` |
| Does the review run once? | Only once `stage.md` said so plainly. "Go on to finish when every reviewer reports no findings" read as a loop, and the review ran three times |
| Can a reviewer whose skill failed look clean? | It did: `security-review` failed to load and the reviewer replied `No findings.` It now replies `Review did not run`, and the stage lists that in the PR |
| Does `security-review` run in any repo? | Only where `origin/HEAD` is set. A clone sets it; a repo set up with `git init` and `git remote add`, like the one the trial ran from, doesn't |
| Do the checks stop a stage early enough? | A re-run with the stage's branch present, and Spec with no `intent.md` on the default branch, both stopped before changing anything |

To verify in phase 6: `claude-code-action` can load plugins from this marketplace.

## 12. Risks

- **The manifest works on one machine in one mode.** It rests on the session relaying each plugin's root to the resolver. If that proves unreliable, the fallback is a naming convention plus a project deny list.
- **Volume of vendored text.** superpowers alone is about 11,000 lines. Version 0 takes a small cluster and trims it.
- **Session-start bloat.** Every layer adds always-on text. Each `context.md` stays to a few lines; `claude plugin details` reports the token cost.
- **Upstream drift.** Vendored skills stop receiving upstream fixes. `THIRD_PARTY.md` records the commit so a later comparison is possible.
- **Ceremony.** Three PRs per intent is heavy for small work. Merging issues at the Intent stage is the only relief until gates are relaxed.
- **Session pointers go stale.** A PR names the session that wrote it, but that session can be resumed only on the same host, from the same project folder, and only until Claude Code cleans up old transcripts.
- **Live edits.** A local clone on a feature branch changes the skills every project on that machine uses.
