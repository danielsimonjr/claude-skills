"""Tests for directory discovery and classification in directory_processor.py."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from directory_processor import _classify_priority, discover_files, generate_manifest, FileEntry


class TestClassifyPriority:
    def test_readme_detection(self):
        assert _classify_priority("README.md", "text") == "readme"
        assert _classify_priority("CHANGELOG.md", "text") == "readme"
        assert _classify_priority("LICENSE", "text") == "readme"

    def test_doc_detection(self):
        assert _classify_priority("docs/guide.md", "text") == "doc"
        assert _classify_priority("doc/api.rst", "text") == "doc"

    def test_test_detection(self):
        assert _classify_priority("tests/test_main.py", "code") == "test"
        assert _classify_priority("test_main.py", "code") == "test"
        assert _classify_priority("src/app.test.js", "code") == "test"
        assert _classify_priority("spec/helper.spec.ts", "code") == "test"

    def test_source_detection(self):
        assert _classify_priority("src/main.py", "code") == "source"
        assert _classify_priority("app.js", "code") == "source"

    def test_config_detection(self):
        assert _classify_priority("package.json", "json") == "config"
        assert _classify_priority("settings.ini", "text") == "config"

    def test_data_detection(self):
        assert _classify_priority("data/records.csv", "csv") == "data"
        assert _classify_priority("output.json", "json") == "data"


class TestDiscoverFiles:
    def test_discovers_text_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            Path(tmpdir, "hello.txt").write_text("hello", encoding="utf-8")
            Path(tmpdir, "world.py").write_text("print('world')", encoding="utf-8")

            files, skip_counts = discover_files(tmpdir)
            assert len(files) == 2
            names = {f.rel_path for f in files}
            assert "hello.txt" in names
            assert "world.py" in names

    def test_skips_hidden_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, ".hidden").write_text("secret", encoding="utf-8")
            Path(tmpdir, "visible.txt").write_text("public", encoding="utf-8")

            files, _ = discover_files(tmpdir)
            names = {f.rel_path for f in files}
            assert ".hidden" not in names
            assert "visible.txt" in names

    def test_skips_excluded_dirs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            nm = Path(tmpdir, "node_modules")
            nm.mkdir()
            Path(nm, "pkg.js").write_text("module", encoding="utf-8")
            Path(tmpdir, "app.js").write_text("app", encoding="utf-8")

            files, _ = discover_files(tmpdir)
            assert len(files) == 1
            assert files[0].rel_path == "app.js"

    def test_include_patterns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "main.py").write_text("python", encoding="utf-8")
            Path(tmpdir, "style.css").write_text("css", encoding="utf-8")

            files, _ = discover_files(tmpdir, include_patterns=["*.py"])
            assert len(files) == 1
            assert files[0].rel_path == "main.py"

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            files, skip_counts = discover_files(tmpdir)
            assert len(files) == 0

    def test_skips_empty_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "empty.txt").write_text("", encoding="utf-8")
            Path(tmpdir, "notempty.txt").write_text("content", encoding="utf-8")

            files, _ = discover_files(tmpdir)
            assert len(files) == 1
            assert files[0].rel_path == "notempty.txt"


class TestGenerateManifest:
    def test_manifest_contains_file_info(self):
        files = [
            FileEntry(
                abs_path="/tmp/test.py",
                rel_path="test.py",
                size_bytes=100,
                file_type="code",
                priority_group="source",
            )
        ]
        manifest = generate_manifest("/tmp", files, 100)
        assert "test.py" in manifest
        assert "DIRECTORY MANIFEST" in manifest
        assert "code" in manifest
