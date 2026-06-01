import unittest
import os
import shutil
import tempfile
from io import StringIO
from pathlib import Path
from unittest.mock import patch, MagicMock
import django
from django.conf import settings
from django.core.management import call_command

if not settings.configured:
    settings.configure(
        SECRET_KEY='fake-key',
        INSTALLED_APPS=['djinn'],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
    )
    django.setup()

class TestDjinnManagementCommand(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.addCleanup(os.chdir, self.old_cwd)
        self.addCleanup(shutil.rmtree, self.test_dir, ignore_errors=True)

    @patch("requests.get")
    def test_phase1_success(self, mock_get):
        # Mock API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "files": [
                {"filename": "test.html", "content": "<div>Test</div>"},
                {"filename": "test.py", "content": "# Test code"}
            ]
        }
        mock_get.return_value = mock_response

        # Use stdout=StringIO() doesn't work well with click directly unless we mock it or use click runner,
        # but click output goes to sys.stdout usually.
        # Actually click.echo goes to sys.stdout.
        with patch('sys.stdout', new=StringIO()) as fake_out:
            call_command("djinn", "test-component")
            output = fake_out.getvalue()

        self.assertIn("Found in Live Database", output)
        self.assertTrue((self.test_dir / "components/test-component/test.html").exists())
        self.assertTrue((self.test_dir / "components/test-component/test.py").exists())

    @patch("requests.get")
    def test_phase2_fallback_success(self, mock_get):
        mock_api_resp = MagicMock()
        mock_api_resp.status_code = 404

        mock_idx_resp = MagicMock()
        mock_idx_resp.status_code = 200

        mock_comp_resp = MagicMock()
        mock_comp_resp.status_code = 200
        mock_comp_resp.json.return_value = {
            "files": {"template": "fallback.html"}
        }

        mock_asset_resp = MagicMock()
        mock_asset_resp.status_code = 200
        mock_asset_resp.text = "Fallback Content"

        mock_get.side_effect = [mock_api_resp, mock_idx_resp, mock_comp_resp, mock_asset_resp]

        with patch('sys.stdout', new=StringIO()) as fake_out:
            call_command("djinn", "fallback-comp")
            output = fake_out.getvalue()

        self.assertIn("Looking in core package repo...", output)
        self.assertTrue((self.test_dir / "components/fallback-comp/fallback.html").exists())
        with open(self.test_dir / "components/fallback-comp/fallback.html", "r") as f:
            self.assertEqual(f.read(), "Fallback Content")

    @patch("requests.get")
    def test_not_found(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_get.return_value = mock_resp

        with patch('sys.stdout', new=StringIO()) as fake_out:
            call_command("djinn", "non-existent")
            output = fake_out.getvalue()

        self.assertIn("Error: Component 'non-existent' not found anywhere.", output)

if __name__ == "__main__":
    unittest.main()
