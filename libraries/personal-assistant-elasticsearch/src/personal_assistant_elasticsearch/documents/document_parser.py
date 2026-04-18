"""Optional OCR-based document parser.

Requires the ``ocr`` extra: ``pip install personal-assistant-elasticsearch[ocr]``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from loguru import logger


@dataclass
class DocumentProcessingInput:
    image: Any
    message: str


class DocumentParser:
    """Thin wrapper around PaddleOCR for document image parsing."""

    def __init__(self, model_name: str | None = None) -> None:
        try:
            from paddleocr import PaddleOCR  # local import so the extra is optional
        except ImportError as exc:  # pragma: no cover - optional dependency
            raise ImportError(
                "DocumentParser requires the 'ocr' extra. "
                "Install with: pip install personal-assistant-elasticsearch[ocr]"
            ) from exc

        try:
            self.ocr_model = PaddleOCR(
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
            )
        except Exception as exc:  # pragma: no cover - runtime boundary
            logger.error(f"Failed to initialize OCR model: {exc}")
            raise

    def process_document(self, payload: DocumentProcessingInput) -> Any:
        return self.ocr_model.predict(payload.image)

