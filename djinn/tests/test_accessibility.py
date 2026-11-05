import unittest
import os
import shutil
import tempfile
from pathlib import Path


class TestAccessibility(unittest.TestCase):
    """Test ARIA attributes and accessibility patterns in component templates."""

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

    def test_button_has_aria_label(self):
        """Button supports aria-label attribute."""
        self.installer.install("button")
        html = (self.test_dir / "templates/components/button.html").read_text()
        self.assertIn("aria-label", html)

    def test_button_has_aria_pressed(self):
        """Button supports aria-pressed for toggle state."""
        self.installer.install("button")
        html = (self.test_dir / "templates/components/button.html").read_text()
        self.assertIn("aria-pressed", html)

    def test_button_no_safe_filters(self):
        """Button template does not use |safe on user content."""
        self.installer.install("button")
        html = (self.test_dir / "templates/components/button.html").read_text()
        self.assertNotIn("|safe", html)

    def test_button_templatetag_uses_inclusion_tag(self):
        """Button uses inclusion_tag pattern, not manual Node."""
        self.installer.install("button")
        py = (self.test_dir / "templatetags/djinn_button.py").read_text()
        self.assertIn("inclusion_tag", py)
        self.assertNotIn("template.Node", py)

    def test_input_has_aria_invalid(self):
        """Input shows aria-invalid when error is present."""
        self.installer.install("input")
        html = (self.test_dir / "templates/components/input.html").read_text()
        self.assertIn("aria-invalid", html)
        self.assertIn("aria-describedby", html)
        self.assertIn("role=\"alert\"", html)

    def test_input_label_for_association(self):
        """Input label uses for attribute matching input id."""
        self.installer.install("input")
        html = (self.test_dir / "templates/components/input.html").read_text()
        self.assertIn("for=", html)

    def test_select_has_aria_invalid(self):
        """Select shows aria-invalid when error is present."""
        self.installer.install("select")
        html = (self.test_dir / "templates/components/select.html").read_text()
        self.assertIn("aria-invalid", html)
        self.assertIn("role=\"alert\"", html)

    def test_modal_has_dialog_role(self):
        """Modal uses role=dialog and aria-modal."""
        self.installer.install("modal")
        html = (self.test_dir / "templates/components/modal.html").read_text()
        self.assertIn('role="dialog"', html)
        self.assertIn("aria-modal", html)
        self.assertIn("aria-labelledby", html)

    def test_modal_close_button_aria_label(self):
        """Modal close button has aria-label."""
        self.installer.install("modal")
        html = (self.test_dir / "templates/components/modal.html").read_text()
        self.assertIn('aria-label="Close dialog"', html)

    def test_no_unsafe_safe_on_slot(self):
        """Component templates do not use |safe on slot/content."""
        for comp in ["button", "modal", "input", "select"]:
            self.installer.install(comp)
            html_path = self.test_dir / "templates/components" / f"{comp}.html"
            if html_path.exists():
                content = html_path.read_text()
                self.assertNotIn(
                    "|safe", content, f"{comp}.html should not use |safe"
                )

    def test_all_templatetags_valid_python(self):
        """All installed templatetag files are valid Python."""
        for comp in ["button", "input", "select", "modal"]:
            self.installer.install(comp)
            py_path = self.test_dir / "templatetags" / f"djinn_{comp}.py"
            if py_path.exists():
                with open(py_path) as f:
                    compile(f.read(), f"djinn_{comp}.py", "exec")


if __name__ == "__main__":
    unittest.main()
