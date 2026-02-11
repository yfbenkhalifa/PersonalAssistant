from typing import List
from .document_chunker import (
    DocumentChunker,
    DocumentContentType,
)


class DumbDocumentChunker(DocumentChunker):
    def __init__(self, max_chunk_length: int = 4096):
        super().__init__(max_chunk_length)

    def chunk_document(
        self,
        content: str,
        content_type: DocumentContentType = DocumentContentType.GENERIC_DOCUMENT,
    ) -> List[str]:
        
        return [
            {"id": i/self.max_chunk_length, "content": content[i : i + self.max_chunk_length]}
            for i in range(0, len(content), self.max_chunk_length)
        ]
