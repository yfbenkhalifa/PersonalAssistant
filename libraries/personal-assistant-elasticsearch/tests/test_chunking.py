import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from personal_assistant_elasticsearch.document_chunking import DumbDocumentChunker


def test_chunk_document_splits_into_expected_sizes():
    chunker = DumbDocumentChunker(max_chunk_length=4)

    result = chunker.chunk_document("abcdefghij")

    assert result == [
        {"id": 0, "content": "abcd"},
        {"id": 1, "content": "efgh"},
        {"id": 2, "content": "ij"},
    ]


def test_chunk_document_returns_placeholder_for_empty_content():
    chunker = DumbDocumentChunker(max_chunk_length=4)

    result = chunker.chunk_document("")

    assert result == [{"id": 0, "content": ""}]


