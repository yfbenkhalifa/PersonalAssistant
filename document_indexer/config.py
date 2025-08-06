"""
Configuration settings for the Document Indexer API
"""

import os
from typing import Optional

class Settings:
    """Application settings"""
    
    # Elasticsearch configuration
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "https://localhost:9200")
    
    # API configuration
    API_TITLE: str = "Document Indexer API"
    API_DESCRIPTION: str = "API for indexing and searching documents in Elasticsearch"
    API_VERSION: str = "1.0.0"
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Search configuration
    DEFAULT_SEARCH_SIZE: int = int(os.getenv("DEFAULT_SEARCH_SIZE", "10"))
    MAX_SEARCH_SIZE: int = int(os.getenv("MAX_SEARCH_SIZE", "100"))
    
    # Index configuration
    DEFAULT_SHARDS: int = int(os.getenv("DEFAULT_SHARDS", "1"))
    DEFAULT_REPLICAS: int = int(os.getenv("DEFAULT_REPLICAS", "0"))

# Global settings instance
settings = Settings()
