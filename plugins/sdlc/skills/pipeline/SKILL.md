---
name: pipeline
description: Print the skills that run in each stage of this repo, and where each one came from.
disable-model-invocation: true
---

Print this repo's effective pipeline: the skills in each step of each stage, after every active SDLC plugin's manifest and the project's `.sdlc/pipeline.toml` are applied.

1. Collect the root of every active SDLC plugin. Each one announced itself at session start with a pair of lines: `SDLC plugin active: <name>` then `Plugin root: <path>`.

2. Run the resolver from the project root, with one `--plugin` for every root collected:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/scripts/resolve_pipeline.py" --project . --plugin "<root>" --plugin "<root>"
   ```

3. Show the resolver's output verbatim in a code block. When it exits with an error, show the error instead: it names the manifest file to fix.
