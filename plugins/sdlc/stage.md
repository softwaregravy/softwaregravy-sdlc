# Running a stage

The steps every stage command shares. The command that sent you here gave you three values:

- **S**, the stage: `intent`, `spec` or `build`.
- **N**, the number of a GitHub issue in this repo, such as `12`. It is never a pull request number.
- **The session id** of this session.

The plugin root is the folder this file is in. Run every command from the project root.

## 1. Check

Stop and say why at the first check that fails. Change nothing until they all pass.

- **N names an open issue.** `gh issue view N --json state,title` shows it as `OPEN`. If N is missing, ask the owner for it.
- **The working tree is clean.** `git status --porcelain` prints nothing.
- **The previous stage's file is on the default branch.** Find the default branch with `gh repo view --json defaultBranchRef --jq .defaultBranchRef.name`, run `git fetch origin <default>`, and look for the feature's folder, `features/active/N-<slug>/`, in `git ls-tree -r --name-only origin/<default> features/active/`:

  | S | Needs in the feature's folder |
  |---|---|
  | `intent` | Nothing |
  | `spec` | `intent.md` |
  | `build` | `spec.md` |

- **The stage hasn't started already.** No branch `S/N` exists: `git rev-parse --verify --quiet refs/heads/S/N` and `git ls-remote --heads origin S/N` both print nothing. If one exists, say where, and leave it to the owner.

## 2. Resolve the pipeline

Collect the root of every active SDLC plugin. Each one announced itself at session start with a pair of lines: `SDLC plugin active: <name>` then `Plugin root: <path>`. Run the resolver with one `--plugin` for every root collected:

```bash
python3 "<plugin root>/scripts/resolve_pipeline.py" --project . --json --plugin "<root>" --plugin "<root>"
```

Keep `stages.S` from its output: the skill names listed for `start`, `do`, `review` and `finish`. When it exits with an error, show the error and stop: it names the manifest file to fix.

## 3. Start the branch

```bash
git switch --no-track -c S/N origin/<default>
```

Then comment on issue N, so anyone watching it knows the stage has started:

```markdown
Starting S on branch `S/N`, on `<host>` in session `<session id>`: `claude --resume <session id>` from this repo there.
```

`<host>` is the output of `hostname`. The comment is news, not state: where work stands is read from the default branch and the open pull requests.

## 4. Run the steps

Run `start`, `do`, `review` and `finish`, in that order. A step with no skills listed does nothing. Every skill gets the arguments `S N`, such as `intent 12`.

- **start, do and finish** run in this session. Invoke each skill with the Skill tool, in the order listed, and follow it through, an interview included, before invoking the next.
- **review** runs once, each skill in a fresh context. Launch one `sdlc:reviewer` agent per skill, all in one message, each with the prompt `Run <skill> with the arguments S N.` When all have reported:
  1. **Merge.** Findings from two reviewers that make the same claim about the same place become one, at the higher severity. Number what is left.
  2. **Hand them back.** Fix them as the do step's skills say to fix review findings. If none of them says, fix every critical and important finding, commit, and keep the minor ones for the pull request body, under "Deferred findings".
  3. **Go on to finish** without reviewing again. A reviewer that replied `Review did not run` is not fixed or retried: name it to the owner, and list it in the pull request body with the deferred findings.

If a skill stops on a problem it can't resolve, stop the stage there and report it. The branch stays for the owner.
