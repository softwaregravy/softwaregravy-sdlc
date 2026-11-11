import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CORE = REPO / "plugins" / "sdlc"
sys.path.insert(0, str(CORE / "scripts"))

import resolve_pipeline as rp  # noqa: E402


class ResolveTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.project = self.root / "project"
        self.project.mkdir()

    def plugin(self, name, manifest=None, deps=()):
        root = self.root / name
        (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
        (root / ".claude-plugin" / "plugin.json").write_text(
            json.dumps({"name": name, "dependencies": list(deps)}))
        if manifest is not None:
            (root / "pipeline.toml").write_text(manifest)
        return root

    def override(self, manifest):
        (self.project / ".sdlc").mkdir(exist_ok=True)
        (self.project / ".sdlc" / "pipeline.toml").write_text(manifest)

    def step(self, result, stage, step):
        return [(e["skill"], e["source"]) for e in result["stages"][stage][step]]

    def core(self):
        return self.plugin("sdlc", """
            [build]
            start = ["sdlc:plan-write", "sdlc:review-plan"]
            review = ["sdlc:review-standards", "sdlc:review-against-spec"]
            finish = ["sdlc:pr-open"]
        """)

    def test_core_alone(self):
        result = rp.resolve(self.project, [self.core()])
        self.assertEqual(self.step(result, "build", "start"),
                         [("sdlc:plan-write", "sdlc"), ("sdlc:review-plan", "sdlc")])
        self.assertEqual(self.step(result, "intent", "do"), [])
        self.assertEqual(result["removed"], [])

    def test_layer_adds_after_its_dependencies_whatever_the_argument_order(self):
        core = self.core()
        ruby = self.plugin("sdlc-ruby", '[build.review]\nadd = ["sdlc-ruby:style"]', deps=["sdlc"])
        rails = self.plugin("sdlc-rails", '[build.review]\nadd = ["sdlc-rails:migrations"]',
                            deps=["sdlc-ruby@softwaregravy-sdlc"])
        result = rp.resolve(self.project, [rails, ruby, core])
        self.assertEqual([s for s, _ in self.step(result, "build", "review")],
                         ["sdlc:review-standards", "sdlc:review-against-spec",
                          "sdlc-ruby:style", "sdlc-rails:migrations"])
        self.assertEqual([s["source"] for s in result["sources"]], ["sdlc", "sdlc-ruby", "sdlc-rails"])

    def test_project_removes_replaces_and_adds(self):
        self.override("""
            [build.review]
            remove = ["sdlc:review-standards"]
            add = ["security-review"]
            replace = { "sdlc:review-against-spec" = "strict-spec-review" }
        """)
        result = rp.resolve(self.project, [self.core()])
        self.assertEqual(self.step(result, "build", "review"),
                         [("strict-spec-review", "project"), ("security-review", "project")])
        self.assertEqual([(r["skill"], r["from"], r["by"], r["replaced_by"]) for r in result["removed"]],
                         [("sdlc:review-standards", "sdlc", "project", None),
                          ("sdlc:review-against-spec", "sdlc", "project", "strict-spec-review")])

    def test_array_sets_the_whole_step_and_keeps_the_source_of_what_stays(self):
        self.override('[build]\nstart = ["house-plan", "sdlc:review-plan"]\nfinish = []')
        result = rp.resolve(self.project, [self.core()])
        self.assertEqual(self.step(result, "build", "start"),
                         [("house-plan", "project"), ("sdlc:review-plan", "sdlc")])
        self.assertEqual(self.step(result, "build", "finish"), [])
        self.assertEqual(sorted(r["skill"] for r in result["removed"]), ["sdlc:plan-write", "sdlc:pr-open"])

    def test_adding_an_entry_twice_keeps_one(self):
        layer = self.plugin("sdlc-ruby", '[build.review]\nadd = ["sdlc:review-standards"]', deps=["sdlc"])
        result = rp.resolve(self.project, [self.core(), layer])
        self.assertEqual(self.step(result, "build", "review"),
                         [("sdlc:review-standards", "sdlc"), ("sdlc:review-against-spec", "sdlc")])

    def test_plugin_without_a_manifest_contributes_nothing(self):
        result = rp.resolve(self.project, [self.core(), self.plugin("sdlc-ruby", deps=["sdlc"])])
        self.assertEqual([s["source"] for s in result["sources"]], ["sdlc"])

    def assert_error(self, text, plugins):
        with self.assertRaises(rp.ManifestError) as raised:
            rp.resolve(self.project, plugins)
        self.assertIn(text, str(raised.exception))

    def test_removing_or_replacing_a_missing_entry_fails(self):
        self.override('[build.review]\nremove = ["sdlc:renamed-upstream"]')
        self.assert_error("'sdlc:renamed-upstream' is not in this step", [self.core()])
        self.override('[build.review]\nreplace = { "sdlc:gone" = "mine" }')
        self.assert_error("'sdlc:gone' is not in this step", [self.core()])

    def test_unknown_stage_step_and_key_fail(self):
        for manifest, text in (('[deploy]\nstart = []', "unknown stage 'deploy'"),
                               ('[build]\nplan = []', "unknown step"),
                               ('[build.review]\nprepend = ["x"]', "unknown key 'prepend'"),
                               ('[build]\nreview = "x"', "expected an array or a table")):
            self.override(manifest)
            self.assert_error(text, [self.core()])

    def test_dependency_cycle_fails(self):
        a = self.plugin("a", deps=["b"])
        b = self.plugin("b", deps=["a"])
        self.assert_error("dependency cycle", [a, b])

    def test_render_shows_entries_sources_and_what_was_taken_out(self):
        self.override('[build.review]\nremove = ["sdlc:review-standards"]')
        text = rp.render(rp.resolve(self.project, [self.core()]))
        self.assertIn("sdlc:review-against-spec  (sdlc)", text)
        self.assertIn("build.review  sdlc:review-standards (from sdlc) removed by project", text)
        self.assertIn("(none)", text)


class CoreManifestTest(unittest.TestCase):
    """The manifest the core plugin ships."""

    def test_it_resolves_and_every_core_entry_is_a_skill_that_exists(self):
        with tempfile.TemporaryDirectory() as empty_project:
            result = rp.resolve(Path(empty_project), [CORE])
        for stage in rp.STAGES:
            for step in rp.STEPS:
                for entry in result["stages"][stage][step]:
                    plugin, _, skill = entry["skill"].rpartition(":")
                    if plugin == "sdlc":
                        self.assertTrue((CORE / "skills" / skill / "SKILL.md").is_file(),
                                        f"{stage}.{step} names {entry['skill']}, which has no SKILL.md")


if __name__ == "__main__":
    unittest.main()
