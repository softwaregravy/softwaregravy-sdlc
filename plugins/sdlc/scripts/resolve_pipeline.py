#!/usr/bin/env python3
"""Resolve the effective SDLC pipeline for a project.

A pipeline names the skills that run in each step of each stage. It is built
from manifests, lowest precedence first:

  1. `pipeline.toml` at the root of every active SDLC plugin, a plugin's
     dependencies before the plugin itself
  2. `.sdlc/pipeline.toml` in the project

A manifest holds one table per stage with one key per step. An array sets the
step's whole list. A table edits the inherited list:

    [build]
    start = ["sdlc:plan-write"]             # set the whole step

    [build.review]
    remove = ["sdlc:review-standards"]      # must be in the list
    add = ["security-review"]               # appended, in order
    replace = { "sdlc:a" = "house:b" }      # swapped in place

Entries are skill names exactly as they are invoked. `remove` and `replace`
fail on an entry that is not there, so an override cannot silently stop
applying when the skill it names is renamed upstream.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # Python < 3.11
    sys.exit("error: resolve_pipeline.py needs Python 3.11 or later (tomllib)")

STAGES = ("intent", "spec", "build")
STEPS = ("start", "do", "review", "finish")
EDITS = ("remove", "replace", "add")
PROJECT = "project"


class ManifestError(Exception):
    pass


def plugin_identity(root):
    """Return (name, dependency names) from a plugin's manifest."""
    path = root / ".claude-plugin" / "plugin.json"
    try:
        data = json.loads(path.read_text())
    except FileNotFoundError:
        raise ManifestError(f"{path}: not found; --plugin must be a plugin root")
    except json.JSONDecodeError as e:
        raise ManifestError(f"{path}: {e}")
    deps = []
    for dep in data.get("dependencies", []):
        name = dep["name"] if isinstance(dep, dict) else dep
        deps.append(name.split("@")[0])
    return data["name"], deps


def order_plugins(roots):
    """Sort plugins so each comes after the plugins it depends on."""
    plugins = {}
    for root in roots:
        name, deps = plugin_identity(root)
        plugins[name] = (root, deps)

    ordered, visiting = [], []

    def visit(name):
        if name in ordered:
            return
        if name in visiting:
            cycle = " -> ".join(visiting[visiting.index(name):] + [name])
            raise ManifestError(f"plugin dependency cycle: {cycle}")
        visiting.append(name)
        # a dependency that was not passed in contributes nothing
        for dep in sorted(d for d in plugins[name][1] if d in plugins):
            visit(dep)
        visiting.pop()
        ordered.append(name)

    for name in sorted(plugins):
        visit(name)
    return [(name, plugins[name][0]) for name in ordered]


def load_manifest(path):
    try:
        return tomllib.loads(path.read_text())
    except tomllib.TOMLDecodeError as e:
        raise ManifestError(f"{path}: {e}")


def skill_list(value, where):
    if not isinstance(value, list) or not all(isinstance(s, str) and s for s in value):
        raise ManifestError(f"{where}: expected an array of skill names")
    return value


def apply_manifest(pipeline, removed, source, path):
    """Apply one manifest to `pipeline`, recording what it takes out."""
    for stage, steps in load_manifest(path).items():
        if stage not in STAGES:
            raise ManifestError(f"{path}: unknown stage '{stage}'; stages are {', '.join(STAGES)}")
        if not isinstance(steps, dict):
            raise ManifestError(f"{path}: [{stage}] must be a table of steps")
        for step, value in steps.items():
            where = f"{path}: {stage}.{step}"
            if step not in STEPS:
                raise ManifestError(f"{where}: unknown step; steps are {', '.join(STEPS)}")
            current = pipeline[stage][step]

            def drop(skill, by=None):
                entry = next((e for e in current if e["skill"] == skill), None)
                if entry is None:
                    raise ManifestError(f"{where}: '{skill}' is not in this step")
                removed.append({"stage": stage, "step": step, "skill": skill,
                                "from": entry["source"], "by": source, "replaced_by": by})
                return current.index(entry)

            if isinstance(value, list):
                kept = {e["skill"]: e for e in current}
                wanted = skill_list(value, where)
                for skill in [s for s in kept if s not in wanted]:
                    drop(skill)
                current[:] = [kept.get(s, {"skill": s, "source": source}) for s in dict.fromkeys(wanted)]
            elif isinstance(value, dict):
                unknown = sorted(set(value) - set(EDITS))
                if unknown:
                    raise ManifestError(f"{where}: unknown key '{unknown[0]}'; keys are {', '.join(EDITS)}")
                for skill in skill_list(value.get("remove", []), f"{where}.remove"):
                    del current[drop(skill)]
                replace = value.get("replace", {})
                if not isinstance(replace, dict):
                    raise ManifestError(f"{where}.replace: expected a table of old = new")
                for old, new in replace.items():
                    current[drop(old, by=new)] = {"skill": new, "source": source}
                for skill in skill_list(value.get("add", []), f"{where}.add"):
                    if all(e["skill"] != skill for e in current):
                        current.append({"skill": skill, "source": source})
            else:
                raise ManifestError(f"{where}: expected an array or a table")


def resolve(project, plugin_roots):
    pipeline = {stage: {step: [] for step in STEPS} for stage in STAGES}
    removed, sources = [], []
    manifests = [(name, root / "pipeline.toml") for name, root in order_plugins(plugin_roots)]
    manifests.append((PROJECT, project / ".sdlc" / "pipeline.toml"))
    for source, path in manifests:
        if path.is_file():
            apply_manifest(pipeline, removed, source, path)
            sources.append({"source": source, "path": str(path)})
    return {"project": str(project), "sources": sources, "stages": pipeline, "removed": removed}


def render(result):
    lines = [f"Effective pipeline for {result['project']}", ""]
    entries = [e for steps in result["stages"].values() for step in steps.values() for e in step]
    width = max([len(e["skill"]) for e in entries] + [len("(none)")])
    for stage in STAGES:
        lines.append(stage)
        for step in STEPS:
            label = step
            for e in result["stages"][stage][step] or [None]:
                skill, source = (e["skill"], f"  ({e['source']})") if e else ("(none)", "")
                lines.append(f"  {label:<8}{skill:<{width}}{source}".rstrip())
                label = ""
        lines.append("")
    if result["removed"]:
        lines.append("Taken out")
        for r in result["removed"]:
            how = f"replaced with {r['replaced_by']}" if r["replaced_by"] else "removed"
            lines.append(f"  {r['stage']}.{r['step']}  {r['skill']} (from {r['from']}) {how} by {r['by']}")
        lines.append("")
    lines.append("Manifests applied, lowest precedence first")
    lines += [f"  {s['source']:<12}{s['path']}" for s in result["sources"]] or ["  (none)"]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Resolve the effective SDLC pipeline for a project.")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="project root (default: current directory)")
    parser.add_argument("--plugin", type=Path, action="append", default=[], metavar="ROOT",
                        help="root of an active SDLC plugin; repeat for each one")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)
    try:
        result = resolve(args.project.resolve(), [p.resolve() for p in args.plugin])
    except ManifestError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2) if args.json else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
