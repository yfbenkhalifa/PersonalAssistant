"""API response models."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    title: str
    content: str
    author: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}

