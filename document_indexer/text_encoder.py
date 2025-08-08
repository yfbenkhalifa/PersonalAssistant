from typing import List
import numpy as np

def chunk_document(content: str) -> List[str]:
    """
    Splits the document content into smaller chunks for processing.
    
    Args:
        content (str): The full content of the document.
        
    Returns:
        List[str]: A list of content chunks.
    """
    from llm_client import encode_text



def encode_text(input: str) -> np.ndarray:
    from sentence_transformers import SentenceTransformer
    import torch
    # Load pre-trained model and tokenizer
    model_name = "Qwen/Qwen3-Embedding-8B"
    model = SentenceTransformer("Qwen/Qwen3-Embedding-8B")

    # Tokenize and encode
    embeddings = model.encode(input, prompt_name="query")
        
    return embeddings.flatten()