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

        # Register cleanups immediately
        self.addCleanup(shutil.rmtree, self.test_dir)
        self.addCleanup(os.chdir, self.old_cwd)

        os.chdir(self.test_dir)

        # Use relative path from this file to find the registry
        self.registry_url = str(Path(__file__).resolve().parent.parent / "registry")

        self.config = Config(
            registry_url=self.registry_url,
            output={"templates": "templates/", "python": "templatetags/"}
        )
        self.registry = Registry(self.registry_url)
        self.installer = Installer(self.config, self.registry)

    def test_install_button(self):
        self.installer.install("button")
        self.assertTrue(Path("templates/components/button.html").exists())
        self.assertTrue(Path("templatetags/button.py").exists())

        with open("templatetags/button.py", "r") as f:
            content = f.read()
            # We will update these names in the next steps, so keeping it generic for now
            self.assertIn("djinn_button", content)
            self.assertIn("@register.inclusion_tag", content)

    def test_install_card(self):
        self.installer.install("card")
        self.assertTrue(Path("templates/components/card.html").exists())
        self.assertTrue(Path("templatetags/card.py").exists())

        with open("templatetags/card.py", "r") as f:
            content = f.read()
            self.assertIn("djinn_card", content)

    def test_install_input(self):
        self.installer.install("input")
        self.assertTrue(Path("templates/components/input.html").exists())
        self.assertTrue(Path("templatetags/input.py").exists())

        with open("templatetags/input.py", "r") as f:
            content = f.read()
            self.assertIn("djinn_input", content)

if __name__ == "__main__":
    unittest.main()
