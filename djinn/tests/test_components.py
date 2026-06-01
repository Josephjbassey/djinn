import unittest
import os
import shutil
import tempfile
from pathlib import Path
from djinn.core.config import Config
from djinn.core.registry import Registry
from djinn.core.installer import Installer

class TestComponents(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

        # Use the real bundled registry
        self.registry_url = str(Path(self.old_cwd) / "djinn/registry")
        self.config = Config(
            registry_url=self.registry_url,
            output={"templates": "templates/", "python": "components/"}
        )
        self.registry = Registry(self.registry_url)
        self.installer = Installer(self.config, self.registry)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_install_button(self):
        self.installer.install("button")
        self.assertTrue(Path("templates/components/button.html").exists())
        self.assertTrue(Path("components/button.py").exists())

        with open("components/button.py", "r") as f:
            content = f.read()
            self.assertIn("def djinn_button", content)
            self.assertIn("@register.inclusion_tag", content)

    def test_install_card(self):
        self.installer.install("card")
        self.assertTrue(Path("templates/components/card.html").exists())
        self.assertTrue(Path("components/card.py").exists())

        with open("components/card.py", "r") as f:
            content = f.read()
            self.assertIn("def djinn_card", content)

    def test_install_input(self):
        self.installer.install("input")
        self.assertTrue(Path("templates/components/input.html").exists())
        self.assertTrue(Path("components/input.py").exists())

        with open("components/input.py", "r") as f:
            content = f.read()
            self.assertIn("def djinn_input", content)

if __name__ == "__main__":
    unittest.main()
