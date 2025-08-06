from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from config import settings

class DocumentModel(BaseModel):
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    author: Optional[str] = Field(None, description="Document author")
    tags: Optional[List[str]] = Field(default_factory=list, description="Document tags")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")
    
    
class IndexConfig(BaseModel):
    index_name: str = Field(..., description="Index name")
    mappings: Optional[Dict[str, Any]] = Field(None, description="Index mappings")
    settings: Optional[Dict[str, Any]] = Field(None, description="Index settings")