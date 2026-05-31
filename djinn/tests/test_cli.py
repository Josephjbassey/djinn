import unittest
import os
import shutil
import tempfile
from pathlib import Path
from click.testing import CliRunner
from djinn.cli.main import cli
from djinn.core.config import CONFIG_FILE

class TestDjinnCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.test_dir = Path(tempfile.mkdtemp())
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

        self.addCleanup(os.chdir, self.old_cwd)
        self.addCleanup(shutil.rmtree, self.test_dir, ignore_errors=True)

    def test_init_yes(self):
        result = self.runner.invoke(cli, ["init", "--yes"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Initialized djinn.config.json with defaults.", result.output)
        self.assertTrue((self.test_dir / CONFIG_FILE).exists())

    def test_list_fallback(self):
        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Djinn not initialized. Showing components from bundled registry.", result.output)
        self.assertIn("button", result.output)

    def test_add_fallback(self):
        result = self.runner.invoke(cli, ["add", "button"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Djinn not initialized. Using bundled registry defaults.", result.output)
        self.assertTrue((self.test_dir / "templates/components/button.html").exists())
        self.assertTrue((self.test_dir / "components/button.py").exists())

    def test_init_interactive(self):
        # Simulate interactive input: Registry URL, template path, python path
        result = self.runner.invoke(cli, ["init"], input="custom_registry\ncustom_tpl\ncustom_py\n")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Djinn initialized successfully!", result.output)

        import json
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            self.assertEqual(config["registry_url"], "custom_registry")
            self.assertEqual(config["output"]["templates"], "custom_tpl")
            self.assertEqual(config["output"]["python"], "custom_py")

if __name__ == "__main__":
    unittest.main()
