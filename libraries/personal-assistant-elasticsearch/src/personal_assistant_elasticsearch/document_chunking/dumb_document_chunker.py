from __future__ import annotations

from personal_assistant_elasticsearch.document_chunking.document_chunker import (
    DocumentChunker,
    DocumentContentType,
)


class DumbDocumentChunker(DocumentChunker):
    def chunk_document(
        self,
        content: str,
        content_type: DocumentContentType = DocumentContentType.GENERIC_DOCUMENT,
    ) -> list[dict[str, str | int]]:
        return [
            {"id": chunk_index, "content": content[offset : offset + self.max_chunk_length]}
            for chunk_index, offset in enumerate(range(0, len(content), self.max_chunk_length))
        ] or [{"id": 0, "content": ""}]

