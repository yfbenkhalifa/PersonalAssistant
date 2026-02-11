from abc import abstractmethod
from enum import Enum
from typing import List


class DocumentContentType(Enum):
    CHAT = "chat"
    GENERIC_DOCUMENT = "document"

class DocumentChunker:
    def __init__(self, max_chunk_lenght: int = 4096):
        self.max_chunk_length = max_chunk_lenght
        
    @abstractmethod
    def chunk_document(self, content: str, content_type: DocumentContentType = DocumentContentType.GENERIC_DOCUMENT) -> List[str]:
        """
        Splits the document content into smaller chunks for processing.
        
        Args:
            content (str): The full content of the document.
            
        Returns:
            List[str]: A list of content chunks.
        """
        pass