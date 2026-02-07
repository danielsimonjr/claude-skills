"""Security tests for archive extraction path traversal protection."""

import os
import sys
import tempfile
import zipfile
import tarfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from file_converter import _is_safe_tar_member, _is_safe_zip_member, extract_archive


class TestIsSafeZipMember:
    def test_normal_path_is_safe(self):
        with tempfile.TemporaryDirectory() as d:
            assert _is_safe_zip_member("readme.txt", d) is True

    def test_nested_path_is_safe(self):
        with tempfile.TemporaryDirectory() as d:
            assert _is_safe_zip_member("src/main.py", d) is True

    def test_parent_traversal_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            assert _is_safe_zip_member("../../../etc/passwd", d) is False

    def test_dot_dot_in_middle_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            assert _is_safe_zip_member("foo/../../etc/passwd", d) is False

    def test_absolute_path_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            assert _is_safe_zip_member("/etc/passwd", d) is False


class TestIsSafeTarMember:
    def _make_member(self, name, is_symlink=False, is_hardlink=False, linkname=""):
        """Create a mock TarInfo-like object."""
        member = tarfile.TarInfo(name=name)
        if is_symlink:
            member.type = tarfile.SYMTYPE
            member.linkname = linkname
        elif is_hardlink:
            member.type = tarfile.LNKTYPE
            member.linkname = linkname
        return member

    def test_normal_file_is_safe(self):
        with tempfile.TemporaryDirectory() as d:
            member = self._make_member("readme.txt")
            assert _is_safe_tar_member(member, d) is True

    def test_nested_file_is_safe(self):
        with tempfile.TemporaryDirectory() as d:
            member = self._make_member("src/main.py")
            assert _is_safe_tar_member(member, d) is True

    def test_parent_traversal_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            member = self._make_member("../../../etc/passwd")
            assert _is_safe_tar_member(member, d) is False

    def test_dot_dot_in_middle_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            member = self._make_member("foo/../../etc/passwd")
            assert _is_safe_tar_member(member, d) is False

    def test_symlink_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            member = self._make_member("link", is_symlink=True, linkname="/etc/passwd")
            assert _is_safe_tar_member(member, d) is False

    def test_hardlink_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            member = self._make_member("link", is_hardlink=True, linkname="/etc/passwd")
            assert _is_safe_tar_member(member, d) is False

    def test_absolute_path_blocked(self):
        with tempfile.TemporaryDirectory() as d:
            member = self._make_member("/etc/passwd")
            assert _is_safe_tar_member(member, d) is False


class TestExtractArchiveSecurity:
    def test_zip_traversal_skipped(self):
        """Malicious zip with path traversal entries should be safely skipped."""
        with tempfile.TemporaryDirectory() as d:
            zip_path = os.path.join(d, "malicious.zip")
            safe_content = "safe file content"

            with zipfile.ZipFile(zip_path, "w") as zf:
                # Add a safe file
                zf.writestr("safe.txt", safe_content)
                # Add a malicious path traversal entry
                zf.writestr("../../../tmp/evil.txt", "evil content")

            result = extract_archive(zip_path)
            assert "safe file content" in result
            assert "evil content" not in result

    def test_tar_symlink_skipped(self):
        """Tar with symlink members should skip them."""
        with tempfile.TemporaryDirectory() as d:
            tar_path = os.path.join(d, "malicious.tar")
            safe_file = os.path.join(d, "safe.txt")
            with open(safe_file, "w") as f:
                f.write("safe file content")

            with tarfile.open(tar_path, "w") as tf:
                tf.add(safe_file, arcname="safe.txt")
                # Add a symlink member
                info = tarfile.TarInfo(name="evil_link")
                info.type = tarfile.SYMTYPE
                info.linkname = "/etc/passwd"
                tf.addfile(info)

            result = extract_archive(tar_path)
            assert "safe file content" in result
