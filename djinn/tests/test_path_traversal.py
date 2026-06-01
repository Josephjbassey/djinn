import unittest
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import django
from django.conf import settings
from django.core.management import call_command, CommandError

if not settings.configured:
    settings.configure(
        SECRET_KEY='fake-key',
        INSTALLED_APPS=['djinn'],
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory:'}}
    )
    django.setup()

class TestPathTraversal(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)
        self.addCleanup(os.chdir, self.old_cwd)
        self.addCleanup(shutil.rmtree, self.test_dir, ignore_errors=True)

    @patch("requests.get")
    def test_path_traversal_rejected(self, mock_get):
        # Mock API response with malicious filename
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "files": [
                {"filename": "../../evil.py", "content": "print('evil')"}
            ]
        }
        mock_get.return_value = mock_response

        with self.assertRaises(CommandError) as cm:
            call_command("djinn", "test-component")

        self.assertIn("Path traversal detected", str(cm.exception))

    @patch("requests.get")
    def test_absolute_path_rejected(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "files": [
                {"filename": "/etc/passwd", "content": "root:x:0:0:root:/root:/bin/bash"}
            ]
        }
        mock_get.return_value = mock_response

        with self.assertRaises(CommandError) as cm:
            call_command("djinn", "test-component")

        self.assertIn("Absolute filename", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
