import unittest
import os
import shutil
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djinn.tests.settings")
import django
django.setup()

from django import forms
from django.template import Engine, Context
import importlib


class TestRendering(unittest.TestCase):
    """End-to-end rendering tests: install components, load tags, render templates."""

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

        # Install components we'll test (form auto-installs form_field as dependency)
        self.installer.install("button")
        self.installer.install("input")
        self.installer.install("select")
        self.installer.install("modal")
        self.installer.install("form")

        # Make templatetags importable
        sys.path.insert(0, str(self.test_dir / "templatetags"))

    def _render(self, template_string, context_dict=None):
        """Render a Django template string with the installed component tags."""
        context_dict = context_dict or {}
        # Create a template engine with our template dirs
        engine = Engine(
            dirs=[str(self.test_dir / "templates")],
            app_dirs=False,
            autoescape=True,
        )
        # Register each installed tag library
        tt_dir = self.test_dir / "templatetags"
        if tt_dir.exists():
            for py_file in sorted(tt_dir.glob("djinn_*.py")):
                module_name = py_file.stem
                try:
                    mod = importlib.import_module(module_name)
                    engine.template_libraries[module_name] = mod.register
                except Exception:
                    pass
        t = engine.from_string(template_string)
        return t.render(Context(context_dict))

    def test_button_renders_with_aria_label(self):
        """Button renders with aria-label attribute."""
        html = self._render(
            "{% load djinn_button %}{% djinn_button label=\"Delete\" aria_label=\"Delete item\" %}"
        )
        self.assertIn('aria-label="Delete item"', html)
        self.assertIn("Delete", html)

    def test_button_renders_with_aria_pressed(self):
        """Button renders with aria-pressed for toggle state."""
        html = self._render(
            "{% load djinn_button %}{% djinn_button label=\"Toggle\" aria_pressed=True %}"
        )
        self.assertIn('aria-pressed="true"', html)

    def test_input_renders_with_aria_invalid(self):
        """Input renders aria-invalid when error present."""
        html = self._render(
            "{% load djinn_input %}{% djinn_input label=\"Email\" error=\"Invalid\" name=\"email\" %}"
        )
        self.assertIn('aria-invalid="true"', html)
        self.assertIn('role="alert"', html)

    def test_input_label_for_matches_id(self):
        """Input label for attribute matches input id."""
        html = self._render(
            "{% load djinn_input %}{% djinn_input label=\"Email\" name=\"email\" %}"
        )
        self.assertIn('for="email"', html)
        self.assertIn('id="email"', html)

    def test_select_renders_with_aria_invalid(self):
        """Select renders aria-invalid when error present."""
        html = self._render(
            "{% load djinn_select %}{% djinn_select label=\"Country\" error=\"Required\" name=\"country\" %}"
        )
        self.assertIn('aria-invalid="true"', html)
        self.assertIn('role="alert"', html)

    def test_modal_renders_with_dialog_role(self):
        """Modal renders with role=dialog and aria-modal."""
        html = self._render(
            "{% load djinn_modal %}{% djinn_modal id=\"my-modal\" title=\"Title\" %}"
        )
        self.assertIn('role="dialog"', html)
        self.assertIn('aria-modal="true"', html)
        self.assertIn('aria-labelledby="my-modal-title"', html)

    def test_modal_close_has_aria_label(self):
        """Modal close button has aria-label."""
        html = self._render(
            "{% load djinn_modal %}{% djinn_modal id=\"my-modal\" title=\"Title\" %}"
        )
        self.assertIn('aria-label="Close dialog"', html)

    def test_modal_no_safe_on_slot(self):
        """Modal template does not use |safe on slot."""
        modal_html = (self.test_dir / "templates/components/modal.html").read_text()
        self.assertNotIn("|safe", modal_html)

    def test_form_field_renders_with_django_form(self):
        """form_field renders a Django BoundField correctly."""
        class TestForm(forms.Form):
            email = forms.EmailField(label="Email Address", required=True)

        form = TestForm()
        html = self._render(
            "{% load djinn_form_field %}{% djinn_form_field field=form.email %}",
            {"form": form},
        )
        self.assertIn("Email Address", html)
        self.assertIn("id_email", html)
        self.assertIn("aria-required", html)
        self.assertIn('for="id_email"', html)

    def test_form_field_renders_with_errors(self):
        """form_field renders field errors with role=alert."""
        class TestForm(forms.Form):
            email = forms.EmailField(label="Email", required=True)

        form = TestForm(data={"email": "not-an-email"})
        form.is_valid()
        html = self._render(
            "{% load djinn_form_field %}{% djinn_form_field field=form.email %}",
            {"form": form},
        )
        self.assertIn('role="alert"', html)
        self.assertIn("aria-invalid", html)

    def test_form_renders_with_csrf_and_fields(self):
        """form renders with CSRF token and form fields."""
        class TestForm(forms.Form):
            name = forms.CharField(label="Name", required=True)
            email = forms.EmailField(label="Email", required=True)

        form = TestForm()
        html = self._render(
            "{% load djinn_form %}{% djinn_form form=form %}{% enddjinn_form %}",
            {"form": form, "csrf_token": "test-csrf-token"},
        )
        self.assertIn("csrfmiddlewaretoken", html)
        self.assertIn("test-csrf-token", html)
        self.assertIn("Name", html)
        self.assertIn("Email", html)

    def test_all_installed_templatetags_have_register(self):
        """Every installed djinn_*.py module has a `register` attribute."""
        tt_dir = self.test_dir / "templatetags"
        for py_file in tt_dir.glob("djinn_*.py"):
            if py_file.name == "__init__.py":
                continue
            module_name = py_file.stem
            try:
                mod = importlib.import_module(module_name)
                self.assertTrue(
                    hasattr(mod, "register"),
                    f"{module_name} missing 'register' attribute",
                )
            except Exception as e:
                self.fail(f"Failed to import {module_name}: {e}")

    def test_all_installed_templates_have_no_unsafe_on_user_content(self):
        """No installed template uses |safe on slot/content."""
        for html_file in (self.test_dir / "templates/components").glob("*.html"):
            content = html_file.read_text()
            # |safe is acceptable on fields/slot in form.html (developer-controlled)
            if html_file.name == "form.html":
                continue
            self.assertNotIn(
                "|safe", content, f"{html_file.name} should not use |safe"
            )


if __name__ == "__main__":
    unittest.main()
