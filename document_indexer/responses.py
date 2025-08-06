from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from config import settings
from dto import DocumentModel

class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    author: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}