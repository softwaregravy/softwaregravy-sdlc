This repo follows softwaregravy-sdlc. Work moves from a GitHub issue through three stages (intent, spec, build), each ending in a pull request that the repo owner merges.

Pull requests:

- Target the default branch with every pull request: run `gh pr create` with no `--base`.
- Keep one concern per pull request. When two changes touch the same file, land the first, then rebase the second onto the default branch.
- After opening a pull request, stop and report its URL. The owner merges.
- After a merge, confirm the commit reached the default branch with `git merge-base --is-ancestor <sha> origin/<default-branch>`. GitHub shows "Merged" for a pull request that landed in some other branch.

`/sdlc:pipeline` prints the skills that run in each stage of this repo.
