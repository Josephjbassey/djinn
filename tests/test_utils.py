"""Tests for djinn.core.utils"""

from djinn.core.utils import calculate_hash
from pathlib import Path
import tempfile
import os


class TestCalculateHash:
    def test_hash_bytes(self):
        h1 = calculate_hash(b"hello world")
        h2 = calculate_hash(b"hello world")
        assert h1 == h2
        assert len(h1) == 64  # SHA256 hex length

    def test_hash_different_inputs(self):
        assert calculate_hash(b"a") != calculate_hash(b"b")

    def test_hash_empty(self):
        h = calculate_hash(b"")
        assert h == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    def test_hash_file(self, tmp_path):
        file_path = tmp_path / "test.txt"
        file_path.write_bytes(b"file content")
        h = calculate_hash(file_path)
        assert h == calculate_hash(b"file content")

    def test_hash_file_not_found(self):
        try:
            calculate_hash(Path("/nonexistent/file.txt"))
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass
