"""Prompt template helper shared across the Elasticsearch services."""

from __future__ import annotations

import re
from typing import List


class PromptTemplate:
    """Minimal prompt template with ``{variable}`` placeholder extraction."""

    def __init__(self, template: str) -> None:
        self.template = template
        self.variables: List[str] = self._extract_variables(template)

    @staticmethod
    def _extract_variables(template: str) -> List[str]:
        return re.findall(r"\{(\w+)\}", template)

    def format(self, **values: object) -> str:
        return self.template.format(**values)

