from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from dto import DocumentModel
from appSettings import AppSettings as settings

class SearchQuery(BaseModel):
    query: str = Field(..., description="Search query text")
    fields: Optional[List[str]] = Field(None, description="Fields to search in")
    size: int = Field(settings.DEFAULT_SEARCH_SIZE, description="Number of results to return", ge=1, le=settings.MAX_SEARCH_SIZE)
    from_: int = Field(0, description="Starting offset for pagination", ge=0, alias="from")
    
    
    
class BulkIndexRequest(BaseModel):
    documents: List[DocumentModel] = Field(..., description="List of documents to index")
    index_name: str = Field(..., description="Elasticsearch index name")