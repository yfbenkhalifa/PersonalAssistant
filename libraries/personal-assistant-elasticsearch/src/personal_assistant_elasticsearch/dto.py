from typing import Any

from pydantic import BaseModel, Field


class DocumentModel(BaseModel):
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    author: str | None = Field(None, description="Document author")
    tags: list[str] = Field(default_factory=list, description="Document tags")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class IndexConfig(BaseModel):
    index_name: str = Field(..., description="Index name")
    mappings: dict[str, Any] | None = Field(None, description="Index mappings")
    settings: dict[str, Any] | None = Field(None, description="Index settings")

