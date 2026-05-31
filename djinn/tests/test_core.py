import unittest
import os
import shutil
import json
from pathlib import Path
from djinn.core.config import Config, CONFIG_FILE
from djinn.core.registry import Registry, ComponentMetadata
from djinn.core.installer import Installer

class TestDjinnCore(unittest.TestCase):
    def setUp(self):
        # Create a unique test sandbox directory
        self.test_sandbox = Path("test_sandbox_run")
        self.test_sandbox.mkdir(parents=True, exist_ok=True)
        self.old_cwd = os.getcwd()
        os.chdir(self.test_sandbox)

        # Setup fake registry
        self.registry_dir = Path("test_registry")
        self.comp_dir = self.registry_dir / "components" / "test_comp"
        self.comp_dir.mkdir(parents=True)

        with open(self.comp_dir / "registry.json", "w") as f:
            json.dump({
                "name": "test_comp",
                "version": "1.0.0",
                "files": {"template": "comp.html"},
                "install": {"template_path": "tpl/"}
            }, f)

        with open(self.comp_dir / "comp.html", "w") as f:
            f.write("<div>test</div>")

    def tearDown(self):
        os.chdir(self.old_cwd)
        if Path("test_sandbox_run").exists():
            shutil.rmtree("test_sandbox_run")

    def test_config_init_load(self):
        config = Config.init()
        self.assertTrue(os.path.exists(CONFIG_FILE))
        loaded = Config.load()
        self.assertEqual(loaded.registry_url, config.registry_url)

    def test_registry_load(self):
        registry = Registry(str(self.registry_dir))
        metadata = registry.load_component("test_comp")
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata.name, "test_comp")

    def test_installer(self):
        config = Config.init()
        config.registry_url = str(self.registry_dir)
        registry = Registry(str(self.registry_dir))
        installer = Installer(config, registry)

        installed = installer.install("test_comp")
        self.assertEqual(len(installed), 1)
        self.assertTrue(Path("tpl/comp.html").exists())

if __name__ == "__main__":
    unittest.main()
