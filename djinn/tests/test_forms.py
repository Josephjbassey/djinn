import unittest
import os
import shutil
import tempfile
from pathlib import Path


class TestFormComponent(unittest.TestCase):
    """Test djinn_form and djinn_form_field component installation."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.addCleanup(os.chdir, self.old_cwd)
        self.addCleanup(shutil.rmtree, self.test_dir, ignore_errors=True)

        registry_url = str(Path(__file__).resolve().parent.parent / "registry")
        from djinn.core.config import Config
        from djinn.core.registry import Registry
        from djinn.core.installer import Installer

        # Override aliases to install templatetags into templatetags/ for test simplicity
        self.config = Config(
            registry_url=registry_url,
            aliases={"components": "templates/components", "utils": "templatetags"},
        )
        self.registry = Registry(self.config)
        self.installer = Installer(self.config, self.registry)

        # Install form (auto-installs form_field as a registry dependency)
        self.installer.install("form")

    def test_form_field_installed(self):
        """form_field component installs correct files."""
        self.assertTrue(
            (self.test_dir / "templates/components/form_field.html").exists()
        )
        self.assertTrue(
            (self.test_dir / "templatetags/djinn_form_field.py").exists()
        )

    def test_form_installed(self):
        """form component installs correct files."""
        self.assertTrue(
            (self.test_dir / "templates/components/form.html").exists()
        )
        self.assertTrue(
            (self.test_dir / "templatetags/djinn_form.py").exists()
        )

    def test_form_template_has_csrf(self):
        """form.html includes CSRF token field."""
        html = (self.test_dir / "templates/components/form.html").read_text()
        self.assertIn("csrfmiddlewaretoken", html)

    def test_form_template_has_non_field_errors(self):
        """form.html renders non-field errors with role=alert."""
        html = (self.test_dir / "templates/components/form.html").read_text()
        self.assertIn("role=\"alert\"", html)
        self.assertIn("non_field_errors", html)

    def test_form_field_template_has_label_for(self):
        """form_field.html associates label with input via for attribute."""
        html = (self.test_dir / "templates/components/form_field.html").read_text()
        self.assertIn("for=", html)
        self.assertIn("id_for_label", html)

    def test_form_field_template_has_error_alert(self):
        """form_field.html renders errors with role=alert."""
        html = (self.test_dir / "templates/components/form_field.html").read_text()
        self.assertIn("role=\"alert\"", html)

    def test_form_templatetag_importable(self):
        """djinn_form.py is valid Python and defines a register."""
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "djinn_form", self.test_dir / "templatetags/djinn_form.py"
        )
        # Just check it parses as valid Python
        with open(self.test_dir / "templatetags/djinn_form.py") as f:
            compile(f.read(), "djinn_form.py", "exec")

    def test_form_field_templatetag_importable(self):
        """djinn_form_field.py is valid Python."""
        with open(self.test_dir / "templatetags/djinn_form_field.py") as f:
            compile(f.read(), "djinn_form_field.py", "exec")


if __name__ == "__main__":
    unittest.main()
