import unittest
import os
import shutil
import tempfile
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djinn.tests.settings")
import django
django.setup()

from django import forms
from django.template import Engine, Context
import importlib


class TestModalFocusTrap(unittest.TestCase):
    """Test modal focus management and trigger patterns."""

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

        self.config = Config(
            registry_url=registry_url,
            aliases={"components": "templates/components", "utils": "templatetags"},
        )
        self.registry = Registry(self.config)
        self.installer = Installer(self.config, self.registry)
        self.installer.install("modal")
        self.installer.install("button")

    def test_modal_has_focus_trap(self):
        """Modal template uses x-ref dialog with tabindex for focus management."""
        html = (self.test_dir / "templates/components/modal.html").read_text()
        self.assertIn('x-ref="dialog"', html)
        self.assertIn('tabindex="-1"', html)
        self.assertIn("previousFocus", html)
        self.assertIn("$watch('show'", html)

    def test_modal_has_return_focus(self):
        """Modal restores focus to previous element on close."""
        html = (self.test_dir / "templates/components/modal.html").read_text()
        self.assertIn("previousFocus.focus()", html)

    def test_modal_trigger_renders(self):
        """djinn_modal_trigger renders a button with @click handler."""
        sys_path = str(self.test_dir / "templatetags")
        import sys
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)
        import djinn_modal
        result = djinn_modal.djinn_modal_trigger("my-modal", label="Open Modal")
        self.assertIn("@click=", result)
        self.assertIn("open-modal", result)
        self.assertIn("my-modal", result)
        self.assertIn("Open Modal", result)
        self.assertIn("type=\"button\"", result)

    def test_modal_trigger_escapes_label(self):
        """djinn_modal_trigger escapes user-provided label."""
        import sys
        sys_path = str(self.test_dir / "templatetags")
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)
        import djinn_modal
        result = djinn_modal.djinn_modal_trigger("my-modal", label="<script>alert(1)</script>")
        self.assertIn("&lt;script&gt;", result)
        self.assertNotIn("<script>", result)


class TestFormsetComponent(unittest.TestCase):
    """Test djinn_formset component for Django formset rendering."""

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

        self.config = Config(
            registry_url=registry_url,
            aliases={"components": "templates/components", "utils": "templatetags"},
        )
        self.registry = Registry(self.config)
        self.installer = Installer(self.config, self.registry)
        self.installer.install("formset")

    def test_formset_installed(self):
        """formset component installs correct files."""
        self.assertTrue(
            (self.test_dir / "templates/components/formset.html").exists()
        )
        self.assertTrue(
            (self.test_dir / "templatetags/djinn_formset.py").exists()
        )

    def test_formset_template_has_management_form(self):
        """formset.html renders the management form."""
        html = (self.test_dir / "templates/components/formset.html").read_text()
        self.assertIn("management_form", html)

    def test_formset_template_iterates_forms(self):
        """formset.html iterates over formset.forms."""
        html = (self.test_dir / "templates/components/formset.html").read_text()
        self.assertIn("formset.forms", html)

    def test_formset_templatetag_valid_python(self):
        """djinn_formset.py is valid Python."""
        py_path = self.test_dir / "templatetags/djinn_formset.py"
        with open(py_path) as f:
            compile(f.read(), "djinn_formset.py", "exec")


class TestFormAttrsFix(unittest.TestCase):
    """Test that form {{ attrs }} is inside the form tag, not after."""

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

        self.config = Config(
            registry_url=registry_url,
            aliases={"components": "templates/components", "utils": "templatetags"},
        )
        self.registry = Registry(self.config)
        self.installer = Installer(self.config, self.registry)
        self.installer.install("form")

    def test_attrs_inside_form_tag(self):
        """{{ attrs }} appears before the closing > of the form tag."""
        html = (self.test_dir / "templates/components/form.html").read_text()
        # Find the form opening tag
        import re
        match = re.search(r"<form[^>]*>", html)
        self.assertIsNotNone(match, "No form opening tag found")
        form_tag = match.group(0)
        self.assertIn("{{ attrs }}", form_tag, "{{ attrs }} should be inside the form tag")


if __name__ == "__main__":
    unittest.main()
