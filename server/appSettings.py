import os
from typing import Optional
import json

json_file_path = "appSettings.json"  # Path to the JSON file for settings
file = open(json_file_path, "r")
settings_dict = json.load(file)


class AppSettings:
    """Application settings"""

    # Elasticsearch configuration
    ELASTICSEARCH_HOST: str = settings_dict["elasticsearch"]["host"]
    ELASTICSEARCH_PORT: int = int(settings_dict["elasticsearch"]["port"])
    ELASTICSEARCH_USERNAME: str = settings_dict["elasticsearch"]["username"]
    ELASTICSEARCH_PASSWORD: Optional[str] = os.getenv("ELASTICSEARCH_PASSWORD",
                                                      settings_dict["elasticsearch"].get("password", ""))
    ELASTICSEARCH_API_KEY: Optional[str] = os.getenv("ELASTICSEARCH_API_KEY",
                                                     settings_dict["elasticsearch"].get("api_key", None))
    # API configuration
    API_TITLE: str = settings_dict.get("api_title", "Document Indexer API")
    API_DESCRIPTION: str = settings_dict.get("api_description",
                                             "API for indexing and searching documents in Elasticsearch")
    API_VERSION: str = settings_dict.get("api_version", "1.0.0")

    # Server configuration
    HOST: str = settings_dict.get("host", os.getenv("HOST", "0.0.0.0"))
    PORT: int = int(settings_dict.get("port", os.getenv("PORT", "8000")))

    # Logging configuration
    LOG_LEVEL: str = settings_dict.get("log_level", os.getenv("LOG_LEVEL", "INFO"))

    # Search configuration
    DEFAULT_SEARCH_SIZE: int = int(settings_dict.get("default_search_size", os.getenv("DEFAULT_SEARCH_SIZE", "10")))
    MAX_SEARCH_SIZE: int = int(settings_dict.get("max_search_size", os.getenv("MAX_SEARCH_SIZE", "100")))

    # Index configuration
    DEFAULT_SHARDS: int = int(settings_dict.get("default_shards", os.getenv("DEFAULT_SHARDS", "1")))
    DEFAULT_REPLICAS: int = int(settings_dict.get("default_replicas", os.getenv("DEFAULT_REPLICAS", "0")))

    # Chunk Agent configuration
    AGENTIC_DOCUMENT_CHUNKER_HOST: str = settings_dict["chunk_agent_model"]["host"]
    AGENTIC_DOCUMENT_CHUNKER_PORT: int = int(settings_dict["chunk_agent_model"]["port"])
    AGENTIC_DOCUMENT_CHUNKER_API_KEY: Optional[str] = os.getenv("AGENTIC_DOCUMENT_CHUNKER_API_KEY",
                                                                settings_dict["chunk_agent_model"].get("api_key", None))

    MAX_DOCUMENT_LENGTH: int = int(settings_dict.get("max_document_length", os.getenv("MAX_DOCUMENT_LENGTH", "4096")))
