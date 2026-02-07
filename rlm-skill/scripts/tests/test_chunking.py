"""Tests for chunking strategies in rlm_processor.py."""

import sys
from pathlib import Path

# Add parent dir to path so we can import the scripts
sys.path.insert(0, str(Path(__file__).parent.parent))

from rlm_processor import (
    chunk_by_chars,
    chunk_by_lines,
    chunk_by_separator,
    chunk_by_regex,
    auto_chunk,
)


class TestChunkByChars:
    def test_single_chunk_when_content_fits(self):
        content = "Hello world"
        chunks = chunk_by_chars(content, chunk_size=100)
        assert len(chunks) == 1
        assert chunks[0] == content

    def test_splits_large_content(self):
        content = "a" * 200
        chunks = chunk_by_chars(content, chunk_size=100, overlap=0)
        assert len(chunks) == 2
        assert chunks[0] == "a" * 100
        assert chunks[1] == "a" * 100

    def test_overlap_creates_shared_regions(self):
        content = "a" * 200
        chunks = chunk_by_chars(content, chunk_size=100, overlap=20)
        # With overlap=20, chunks start at 0, 80, 160 => 3 chunks
        assert len(chunks) == 3
        assert len(chunks[0]) == 100
        assert len(chunks[2]) == 40  # 200 - 160

    def test_empty_content(self):
        chunks = chunk_by_chars("", chunk_size=100)
        assert chunks == []

    def test_exact_chunk_size(self):
        content = "a" * 100
        chunks = chunk_by_chars(content, chunk_size=100, overlap=0)
        assert len(chunks) == 1


class TestChunkByLines:
    def test_single_chunk(self):
        content = "line1\nline2\nline3"
        chunks = chunk_by_lines(content, lines_per_chunk=10)
        assert len(chunks) == 1

    def test_splits_at_line_boundary(self):
        lines = [f"line{i}" for i in range(10)]
        content = "\n".join(lines)
        chunks = chunk_by_lines(content, lines_per_chunk=5)
        assert len(chunks) == 2
        assert chunks[0] == "\n".join(lines[:5])
        assert chunks[1] == "\n".join(lines[5:])

    def test_empty_content(self):
        chunks = chunk_by_lines("", lines_per_chunk=5)
        assert len(chunks) == 1  # split produces ['']


class TestChunkBySeparator:
    def test_default_separator(self):
        content = "part1\n---\npart2\n---\npart3"
        chunks = chunk_by_separator(content, separator="\n---\n")
        assert len(chunks) == 3
        assert chunks[0] == "part1"
        assert chunks[1] == "part2"
        assert chunks[2] == "part3"

    def test_empty_parts_filtered(self):
        content = "part1\n---\n\n---\npart2"
        chunks = chunk_by_separator(content, separator="\n---\n")
        assert len(chunks) == 2

    def test_custom_separator(self):
        content = "a|||b|||c"
        chunks = chunk_by_separator(content, separator="|||")
        assert len(chunks) == 3


class TestChunkByRegex:
    def test_markdown_header_split(self):
        content = "# Header 1\ncontent1\n# Header 2\ncontent2"
        chunks = chunk_by_regex(content, r"\n(?=# )")
        assert len(chunks) == 2

    def test_no_match_returns_whole(self):
        content = "no regex match here"
        chunks = chunk_by_regex(content, r"ZZZZZ")
        assert len(chunks) == 1
        assert chunks[0] == content


class TestAutoChunk:
    def test_returns_tuple(self):
        content = "some content here"
        result = auto_chunk(content)
        assert isinstance(result, tuple)
        assert len(result) == 2
        chunks, strategy = result
        assert isinstance(chunks, list)
        assert isinstance(strategy, str)

    def test_markdown_detection(self):
        headers = "\n".join(f"## Section {i}\nContent for section {i}" for i in range(15))
        chunks, strategy = auto_chunk(headers, target_chunk_size=100)
        assert strategy == "markdown_headers"

    def test_separator_detection(self):
        parts = "\n---\n".join(f"Document {i}\nLong content here." for i in range(10))
        chunks, strategy = auto_chunk(parts, target_chunk_size=100000)
        assert strategy == "document_separator"

    def test_character_fallback(self):
        content = "a" * 100000
        chunks, strategy = auto_chunk(content, target_chunk_size=40000)
        assert strategy == "character_count"
        assert len(chunks) >= 2
