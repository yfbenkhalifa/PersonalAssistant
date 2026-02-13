from abc import abstractmethod
from typing import List, override
import numpy as np

class TextEncoder:
    @abstractmethod
    def encode(content: str) -> np.ndarray:
        pass
    
    
class SentenceTransformerTextEncoder(TextEncoder):
    def __init__(self, model_name: str) -> None:
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        
    @override
    def encode(self, content: str) -> np.ndarray:
        return self.model.encode(content)
