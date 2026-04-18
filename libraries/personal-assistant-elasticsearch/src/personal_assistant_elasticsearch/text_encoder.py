from __future__ import annotations

from abc import ABC, abstractmethod
import importlib

import numpy as np


class TextEncoder(ABC):
    @abstractmethod
    def encode(self, content: str) -> np.ndarray:
        raise NotImplementedError


class SentenceTransformerTextEncoder(TextEncoder):
    def __init__(self, model_name: str) -> None:
        sentence_transformers = importlib.import_module("sentence_transformers")
        self.model = sentence_transformers.SentenceTransformer(model_name)

    def encode(self, content: str) -> np.ndarray:
        return self.model.encode(content)


