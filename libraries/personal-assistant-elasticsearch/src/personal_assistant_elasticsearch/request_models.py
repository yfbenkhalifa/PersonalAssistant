from pydantic import BaseModel, Field

from .dto import DocumentModel
from .settings import SearchServiceSettings

_DEFAULTS = SearchServiceSettings()


class SearchQuery(BaseModel):
    query: str = Field(..., description="Search query text")
    fields: list[str] | None = Field(None, description="Fields to search in")
    size: int = Field(
        _DEFAULTS.default_search_size,
        description="Number of results to return",
        ge=1,
        le=_DEFAULTS.max_search_size,
    )
    from_: int = Field(0, description="Starting offset for pagination", ge=0, alias="from")


class BulkIndexRequest(BaseModel):
    documents: list[DocumentModel] = Field(..., description="List of documents to index")
    index_name: str = Field(..., description="Elasticsearch index name")


