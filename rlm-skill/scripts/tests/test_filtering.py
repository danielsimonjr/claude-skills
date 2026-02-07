"""Tests for chunk filtering in rlm_processor.py."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from rlm_processor import filter_relevant_chunks


class TestFilterRelevantChunks:
    def test_filters_by_keywords(self):
        chunks = [
            "This chunk talks about security vulnerabilities.",
            "This chunk discusses cooking recipes.",
            "This chunk mentions security best practices.",
        ]
        result = filter_relevant_chunks(chunks, "security issues")
        indices = [idx for idx, _ in result]
        assert 0 in indices
        assert 2 in indices

    def test_returns_all_when_no_keywords(self):
        chunks = ["chunk 1", "chunk 2", "chunk 3"]
        result = filter_relevant_chunks(chunks, "hi")  # too short for keywords
        assert len(result) == 3

    def test_returns_all_when_filter_too_aggressive(self):
        chunks = [f"chunk {i} with unrelated content" for i in range(100)]
        # Query has keywords that match nothing
        result = filter_relevant_chunks(chunks, "xylophone quantum")
        # Should return all since filtering removed too much (< 10%)
        assert len(result) == 100

    def test_custom_keywords(self):
        chunks = [
            "Python is great for scripting.",
            "Java is great for enterprise.",
            "Python also works for data science.",
        ]
        result = filter_relevant_chunks(chunks, "", keywords=["python"])
        indices = [idx for idx, _ in result]
        assert 0 in indices
        assert 2 in indices
        assert 1 not in indices

    def test_preserves_original_indices(self):
        chunks = ["a", "match keyword here", "b", "another keyword match"]
        result = filter_relevant_chunks(chunks, "", keywords=["keyword"])
        assert result[0][0] == 1  # original index 1
        assert result[1][0] == 3  # original index 3
