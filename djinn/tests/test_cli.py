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
        self.assertIn("Initialized djinn.json with defaults.", result.output)
        self.assertTrue((self.test_dir / CONFIG_FILE).exists())

    def test_list_fallback(self):
        result = self.runner.invoke(cli, ["list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Djinn not initialized. Showing components from bundled registry.", result.output)
        self.assertIn("button", result.output)

    def test_add_fallback(self):
        result = self.runner.invoke(cli, ["add", "button"])
        if result.exit_code != 0:
            print("OUTPUT:", result.output)
            print("EXCEPTION:", result.exception)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Djinn not initialized. Using bundled registry defaults.", result.output)
        self.assertTrue((self.test_dir / "templates/components/button.html").exists())
        self.assertTrue((self.test_dir / "templatetags/djinn_button.py").exists())

    def test_init_interactive(self):
        # Simulate interactive input:
        # style: custom_style
        # color: custom_color
        # css_variables: y
        # css_path: custom_css.css
        # tailwind_config: custom_tailwind.config.js
        # components alias: custom_tpl
        # utils alias: custom_py
        input_data = "custom_style\ncustom_color\ny\ncustom_css.css\ncustom_tailwind.config.js\ncustom_tpl\ncustom_py\n"
        result = self.runner.invoke(cli, ["init"], input=input_data)
        if result.exit_code != 0:
            print("OUTPUT:", result.output)
            print("EXCEPTION:", result.exception)
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Djinn initialized successfully!", result.output)

        import json
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            self.assertEqual(config["style"], "custom_style")
            self.assertEqual(config["aliases"]["components"], "custom_tpl")
            self.assertEqual(config["aliases"]["utils"], "custom_py")
            self.assertEqual(config["tailwind"]["css"], "custom_css.css")
            self.assertEqual(config["tailwind"]["config"], "custom_tailwind.config.js")

if __name__ == "__main__":
    unittest.main()
