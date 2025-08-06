import numpy as np



def encode_text(input: str) -> np.ndarray:
    from sentence_transformers import SentenceTransformer
    import torch
    # Load pre-trained model and tokenizer
    model_name = "Qwen/Qwen3-Embedding-8B"
    model = SentenceTransformer("Qwen/Qwen3-Embedding-8B")

    # Tokenize and encode
    embeddings = model.encode(input, prompt_name="query")
        
    return embeddings.flatten()