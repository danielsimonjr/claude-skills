"""Tests for file type detection and conversion in file_converter.py."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from file_converter import detect_file_type, extract_text, format_size, convert_to_text


class TestDetectFileType:
    def test_pdf_by_extension(self):
        assert detect_file_type("document.pdf") == "pdf"

    def test_docx_by_extension(self):
        assert detect_file_type("report.docx") == "docx"

    def test_python_is_code(self):
        assert detect_file_type("script.py") == "code"

    def test_javascript_is_code(self):
        assert detect_file_type("app.js") == "code"

    def test_json_detected(self):
        assert detect_file_type("data.json") == "json"

    def test_yaml_detected(self):
        assert detect_file_type("config.yaml") == "yaml"
        assert detect_file_type("config.yml") == "yaml"

    def test_html_detected(self):
        assert detect_file_type("page.html") == "html"
        assert detect_file_type("page.htm") == "html"

    def test_csv_detected(self):
        assert detect_file_type("data.csv") == "csv"

    def test_archive_detected(self):
        assert detect_file_type("bundle.zip") == "archive"
        assert detect_file_type("bundle.tar.gz") == "archive"

    def test_text_extensions(self):
        assert detect_file_type("readme.md") == "text"
        assert detect_file_type("notes.txt") == "text"
        assert detect_file_type("doc.rst") == "text"

    def test_legacy_doc(self):
        assert detect_file_type("old.doc") == "doc_legacy"

    def test_xml_detected(self):
        assert detect_file_type("data.xml") == "xml"


class TestExtractText:
    def test_reads_text_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Hello, world!")
            f.flush()
            path = f.name
        try:
            result = extract_text(path)
            assert result == "Hello, world!"
        finally:
            os.unlink(path)

    def test_reads_utf8(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("Caf\u00e9 \u2603")
            f.flush()
            path = f.name
        try:
            result = extract_text(path)
            assert "Caf\u00e9" in result
        finally:
            os.unlink(path)


class TestConvertToText:
    def test_text_file_roundtrip(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write("test content")
            f.flush()
            path = f.name
        try:
            result = convert_to_text(path)
            assert result == "test content"
        finally:
            os.unlink(path)

    def test_missing_file_raises(self):
        try:
            convert_to_text("/nonexistent/file.txt")
            assert False, "Should have raised FileNotFoundError"
        except FileNotFoundError:
            pass

    def test_json_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8") as f:
            f.write('{"key": "value"}')
            f.flush()
            path = f.name
        try:
            result = convert_to_text(path)
            assert '"key"' in result
            assert '"value"' in result
        finally:
            os.unlink(path)


class TestFormatSize:
    def test_bytes(self):
        assert format_size(500) == "500.0 B"

    def test_kilobytes(self):
        assert format_size(1024) == "1.0 KB"

    def test_megabytes(self):
        assert format_size(1024 * 1024) == "1.0 MB"

    def test_gigabytes(self):
        assert format_size(1024 ** 3) == "1.0 GB"
