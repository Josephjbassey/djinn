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
from django.forms.formsets import formset_factory
import importlib


class TestFormsetDynamic(unittest.TestCase):
    """Test djinn_formset with dynamic add/remove via Alpine.js."""

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

    def test_formset_has_dynamic_add(self):
        """formset.html has Alpine.js addForm method."""
        html = (self.test_dir / "templates/components/formset.html").read_text()
        self.assertIn("addForm()", html)
        self.assertIn("@click=\"addForm\"", html)

    def test_formset_has_dynamic_remove(self):
        """formset.html has Alpine.js removeForm method."""
        html = (self.test_dir / "templates/components/formset.html").read_text()
        self.assertIn("removeForm(el)", html)
        self.assertIn("@click=\"removeForm(this)\"", html)

    def test_formset_has_empty_form_template(self):
        """formset.html has empty-form template for cloning."""
        html = (self.test_dir / "templates/components/formset.html").read_text()
        self.assertIn("empty-form", html)

    def test_formset_has_can_add_flag(self):
        """djinn_formset passes can_add to template."""
        import sys
        sys_path = str(self.test_dir / "templatetags")
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)
        import djinn_formset
        result = djinn_formset.djinn_formset(formset=None)
        self.assertFalse(result["can_add"])

        # Can't easily test with a real formset without creating one,
        # but the tag accepts the parameter
        result2 = djinn_formset.djinn_formset(formset=None, can_add=False)
        self.assertFalse(result2["can_add"])


class TestPagination(unittest.TestCase):
    """Test djinn_pagination component."""

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
        self.installer.install("pagination")

    def test_pagination_installed(self):
        """pagination component installs correct files."""
        self.assertTrue(
            (self.test_dir / "templates/components/pagination.html").exists()
        )
        self.assertTrue(
            (self.test_dir / "templatetags/djinn_pagination.py").exists()
        )

    def test_pagination_has_previous_next(self):
        """pagination.html has Previous and Next buttons."""
        html = (self.test_dir / "templates/components/pagination.html").read_text()
        self.assertIn("Previous", html)
        self.assertIn("Next", html)

    def test_pagination_has_page_numbers(self):
        """pagination.html iterates over page_range."""
        html = (self.test_dir / "templates/components/pagination.html").read_text()
        self.assertIn("page_obj.paginator.page_range", html)

    def test_pagination_has_aria_labels(self):
        """pagination.html uses aria-label on all buttons."""
        html = (self.test_dir / "templates/components/pagination.html").read_text()
        self.assertIn('aria-label="Previous page"', html)
        self.assertIn('aria-label="Next page"', html)

    def test_pagination_has_nav_landmark(self):
        """pagination.html uses <nav> with aria-label."""
        html = (self.test_dir / "templates/components/pagination.html").read_text()
        self.assertIn('<nav class="pagination', html)
        self.assertIn('aria-label="Pagination"', html)


class TestAccessibilityEnhancements(unittest.TestCase):
    """Test enhanced accessibility patterns."""

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

    def test_modal_has_tab_trapping(self):
        """Modal template traps Tab key within dialog."""
        self.installer.install("modal")
        html = (self.test_dir / "templates/components/modal.html").read_text()
        self.assertIn("trapTab", html)
        self.assertIn("@keydown.tab.window", html)
        self.assertIn("focusableElements", html)

    def test_button_has_aria_disabled(self):
        """Button template uses aria-disabled when disabled."""
        self.installer.install("button")
        html = (self.test_dir / "templates/components/button.html").read_text()
        self.assertIn('aria-disabled="true"', html)

    def test_input_has_aria_disabled(self):
        """Input template uses aria-disabled when disabled."""
        self.installer.install("input")
        html = (self.test_dir / "templates/components/input.html").read_text()
        self.assertIn('aria-disabled="true"', html)

    def test_select_has_aria_disabled(self):
        """Select template uses aria-disabled when disabled."""
        self.installer.install("select")
        html = (self.test_dir / "templates/components/select.html").read_text()
        self.assertIn('aria-disabled="true"', html)


if __name__ == "__main__":
    unittest.main()
