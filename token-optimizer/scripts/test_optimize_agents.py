import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("optimize_agents.py")
SPEC = importlib.util.spec_from_file_location("optimize_agents", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class OptimizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_claude_settings_are_updated_and_backed_up(self):
        path = self.root / "settings.json"
        path.write_text('{"alwaysThinkingEnabled": true, "env": {}}')
        message = MODULE.edit_json(path, "Claude Code", False)
        result = json.loads(path.read_text())
        self.assertFalse(result["alwaysThinkingEnabled"])
        self.assertEqual(result["env"]["MAX_THINKING_TOKENS"], "0")
        self.assertTrue(path.with_name("settings.json.BAK").exists())
        self.assertIn("UPDATED", message)

    def test_dry_run_does_not_write(self):
        path = self.root / "settings.json"
        original = '{"reasoning_effort": "high"}'
        path.write_text(original)
        MODULE.edit_json(path, "Muse Code", True)
        self.assertEqual(path.read_text(), original)
        self.assertFalse(path.with_name("settings.json.BAK").exists())

    def test_codex_o_series_uses_low_floor(self):
        path = self.root / "config.toml"
        path.write_text('model = "o3"\n')
        MODULE.edit_codex(path, False)
        self.assertIn('model_reasoning_effort = "low"', path.read_text())

    def test_codex_general_model_uses_none(self):
        path = self.root / "config.toml"
        path.write_text('model = "gpt-5-codex"\n')
        MODULE.edit_codex(path, False)
        self.assertIn('model_reasoning_effort = "none"', path.read_text())

    def test_aider_sets_both_controls(self):
        path = self.root / ".aider.conf.yml"
        path.write_text("model: test\n")
        MODULE.edit_aider(path, False)
        self.assertIn("thinking-tokens: 0", path.read_text())
        self.assertIn("reasoning-effort: none", path.read_text())

    def test_opencode_only_changes_existing_provider_keys(self):
        path = self.root / "opencode.json"
        path.write_text('{"provider":{"x":{"options":{"enable_thinking":true,"reasoning":{"enabled":true}}}}}')
        MODULE.edit_json(path, "OpenCode", False)
        options = json.loads(path.read_text())["provider"]["x"]["options"]
        self.assertFalse(options["enable_thinking"])
        self.assertFalse(options["reasoning"]["enabled"])
        self.assertNotIn("thinking", options)


if __name__ == "__main__":
    unittest.main()
