"""
Configuration settings for the Document Indexer API
"""

import os
from typing import Optional
import json

json_file_path = "settings.json"  # Path to the JSON file for settings
file = open(json_file_path, "r")
settings_dict = json.load(file)


class GlobalSettings:
    """Global Application settings"""
    
    # API configuration
    API_TITLE: str = settings_dict.get("api_title", "Document Indexer API")
    API_DESCRIPTION: str = settings_dict.get("api_description", "API for indexing and searching documents in Elasticsearch")
    API_VERSION: str = settings_dict.get("api_version", "1.0.0")
    
    # Server configuration
    HOST: str = settings_dict.get("host", os.getenv("HOST", "0.0.0.0"))
    PORT: int = int(settings_dict.get("port", os.getenv("PORT", "8000")))
    
    # Logging configuration
    LOG_LEVEL: str = settings_dict.get("log_level", os.getenv("LOG_LEVEL", "INFO"))


# Global settings instance
global_settings = GlobalSettings()
