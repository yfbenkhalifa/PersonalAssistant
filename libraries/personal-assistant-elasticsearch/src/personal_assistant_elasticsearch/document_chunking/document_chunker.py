from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum


class DocumentContentType(str, Enum):
    CHAT = "chat"
    GENERIC_DOCUMENT = "document"


class DocumentChunker(ABC):
    def __init__(self, max_chunk_length: int = 4096):
        self.max_chunk_length = max_chunk_length

    @abstractmethod
    def chunk_document(
        self,
        content: str,
        content_type: DocumentContentType = DocumentContentType.GENERIC_DOCUMENT,
    ) -> list[dict[str, str | int]]:
        raise NotImplementedError

